import os
import logging
import sqlite3
from datetime import datetime, timedelta
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import ConflictingIdError
from telegram import Update

#!/usr/bin/env python3
"""
Telegram Assignment Reminder Bot

Save as: assignment_bot.py
Requirements:
    pip install python-telegram-bot==20.5 apscheduler

Usage:
    export BOT_TOKEN="your-telegram-bot-token"
    python assignment_bot.py

Notes:
    - /add starts a short dialog: assignment name -> deadline
    - Deadline format: "YYYY-MM-DD" or "YYYY-MM-DD HH:MM" (24-hour)
    - By default a pre-deadline reminder is sent 24 hours before deadline.
    - Assignments are stored in a local SQLite file assignments.db
"""



from telegram.ext import (
        ApplicationBuilder,
        ContextTypes,
        CommandHandler,
        ConversationHandler,
        MessageHandler,
        filters,
)

# --- Configuration ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_PATH = "assignments.db"
PRE_REMINDER_DELTA = timedelta(days=1)  # time before deadline to send pre-reminder
# ----------------------

if not BOT_TOKEN:
        raise SystemExit("Please set BOT_TOKEN environment variable.")

logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
NAME, DEADLINE = range(2)

# --- Database helpers ---


def init_db():
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        cur = conn.cursor()
        cur.execute(
                """
                CREATE TABLE IF NOT EXISTS assignments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        chat_id INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        deadline TEXT NOT NULL,
                        reminder_sent INTEGER DEFAULT 0,
                        deadline_sent INTEGER DEFAULT 0
                )
        """
        )
        conn.commit()
        return conn


DB = init_db()

# --- Scheduler ---
SCHED = AsyncIOScheduler()


async def send_message(context: ContextTypes.DEFAULT_TYPE, chat_id: int, text: str):
        try:
                await context.bot.send_message(chat_id=chat_id, text=text)
        except Exception as e:
                logger.exception("Failed to send message: %s", e)


async def send_reminder(context: ContextTypes.DEFAULT_TYPE, assignment_id: int, kind: str):
        """
        kind: 'pre' or 'deadline'
        """
        conn = DB
        cur = conn.cursor()
        cur.execute("SELECT id, user_id, chat_id, name, deadline, reminder_sent, deadline_sent FROM assignments WHERE id = ?", (assignment_id,))
        row = cur.fetchone()
        if not row:
                logger.info("Assignment %s not found (maybe removed).", assignment_id)
                return

        _id, user_id, chat_id, name, deadline_str, reminder_sent, deadline_sent = row
        try:
                deadline = datetime.fromisoformat(deadline_str)
        except Exception:
                deadline = datetime.fromisoformat(deadline_str)

        if kind == "pre":
                if reminder_sent:
                        logger.info("Pre-reminder already sent for assignment %s", assignment_id)
                        return
                text = f"Reminder: assignment \"{name}\" is due on {deadline_str} (in ~{(deadline - datetime.now())})."
                await send_message(context, chat_id, text)
                cur.execute("UPDATE assignments SET reminder_sent = 1 WHERE id = ?", (assignment_id,))
                conn.commit()
        elif kind == "deadline":
                if deadline_sent:
                        logger.info("Deadline notification already sent for assignment %s", assignment_id)
                        return
                text = f"Deadline reached: assignment \"{name}\" is due now ({deadline_str})."
                await send_message(context, chat_id, text)
                cur.execute("UPDATE assignments SET deadline_sent = 1 WHERE id = ?", (assignment_id,))
                conn.commit()


def schedule_jobs_for_assignment(application, assignment):
        """
        assignment: dict-like or tuple (id, user_id, chat_id, name, deadline_iso, reminder_sent, deadline_sent)
        """
        assignment_id = assignment[0]
        chat_id = assignment[2]
        name = assignment[3]
        deadline_iso = assignment[4]
        reminder_sent = assignment[5]
        deadline_sent = assignment[6]

        try:
                deadline = datetime.fromisoformat(deadline_iso)
        except Exception:
                deadline = datetime.fromisoformat(deadline_iso)

        now = datetime.now()

        # Schedule pre-reminder
        pre_time = deadline - PRE_REMINDER_DELTA
        pre_job_id = f"pre_{assignment_id}"
        if pre_time <= now and not reminder_sent and deadline > now:
                # If pre_time already passed but deadline not, send immediately via task
                logger.info("Pre-reminder time passed for %s, sending immediately.", assignment_id)
                # schedule an immediate coroutine
                application.create_task(send_reminder(application.bot, assignment_id, "pre")) if hasattr(application, "create_task") else None
                # Alternatively use asyncio
                try:
                        asyncio.get_event_loop().create_task(send_reminder(application, assignment_id, "pre"))
                except Exception:
                        pass
        elif pre_time > now and not reminder_sent:
                # schedule a job
                try:
                        SCHED.add_job(
                                send_reminder,
                                "date",
                                run_date=pre_time,
                                args=(application, assignment_id, "pre"),
                                id=pre_job_id,
                                replace_existing=True,
                        )
                        logger.info("Scheduled pre-reminder for assignment %s at %s", assignment_id, pre_time)
                except ConflictingIdError:
                        logger.info("Pre-job already exists for %s", assignment_id)

        # Schedule deadline notification
        deadline_job_id = f"deadline_{assignment_id}"
        if deadline <= now and not deadline_sent:
                logger.info("Deadline already passed for %s, sending immediate deadline notification.", assignment_id)
                try:
                        asyncio.get_event_loop().create_task(send_reminder(application, assignment_id, "deadline"))
                except Exception:
                        pass
        elif deadline > now and not deadline_sent:
                try:
                        SCHED.add_job(
                                send_reminder,
                                "date",
                                run_date=deadline,
                                args=(application, assignment_id, "deadline"),
                                id=deadline_job_id,
                                replace_existing=True,
                        )
                        logger.info("Scheduled deadline notification for assignment %s at %s", assignment_id, deadline)
                except ConflictingIdError:
                        logger.info("Deadline job already exists for %s", assignment_id)


async def schedule_all_on_start(application):
        cur = DB.cursor()
        cur.execute("SELECT id, user_id, chat_id, name, deadline, reminder_sent, deadline_sent FROM assignments")
        rows = cur.fetchall()
        for r in rows:
                schedule_jobs_for_assignment(application, r)


# --- Bot command handlers ---


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
                "Hello! I will help you track assignments and remind you before deadlines.\n\n"
                "Commands:\n"
                "/add - add new assignment\n"
                "/list - list your assignments\n"
                "/remove <id> - remove assignment by id\n"
                "/help - show help"
        )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await start(update, context)


async def add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Please send the assignment name.")
        return NAME


async def add_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["new_assignment_name"] = update.message.text.strip()
        await update.message.reply_text(
                "Now send the deadline in format YYYY-MM-DD or YYYY-MM-DD HH:MM (24h). Example: 2025-11-10 23:59"
        )
        return DEADLINE


def try_parse_deadline(text: str):
        text = text.strip()
        formats = ["%Y-%m-%d %H:%M", "%Y-%m-%d"]
        last_exc = None
        for fmt in formats:
                try:
                        dt = datetime.strptime(text, fmt)
                        # If date-only, set time to 23:59:59 to indicate end of day
                        if fmt == "%Y-%m-%d":
                                dt = dt.replace(hour=23, minute=59, second=59)
                        return dt
                except Exception as e:
                        last_exc = e
        return None


async def add_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text.strip()
        dt = try_parse_deadline(text)
        if not dt:
                await update.message.reply_text("Couldn't parse that date/time. Please use YYYY-MM-DD or YYYY-MM-DD HH:MM")
                return DEADLINE

        name = context.user_data.get("new_assignment_name")
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        deadline_iso = dt.isoformat()

        cur = DB.cursor()
        cur.execute(
                "INSERT INTO assignments (user_id, chat_id, name, deadline) VALUES (?, ?, ?, ?)",
                (user_id, chat_id, name, deadline_iso),
        )
        DB.commit()
        assignment_id = cur.lastrowid

        await update.message.reply_text(f"Saved assignment #{assignment_id}: \"{name}\" due {deadline_iso}")

        # schedule jobs
        schedule_jobs_for_assignment(context.application, (assignment_id, user_id, chat_id, name, deadline_iso, 0, 0))

        return ConversationHandler.END


async def add_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Add canceled.")
        return ConversationHandler.END


async def list_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        cur = DB.cursor()
        cur.execute(
                "SELECT id, name, deadline, reminder_sent, deadline_sent FROM assignments WHERE user_id = ? ORDER BY deadline",
                (user_id,),
        )
        rows = cur.fetchall()
        if not rows:
                await update.message.reply_text("You have no assignments saved.")
                return
        lines = []
        now = datetime.now()
        for r in rows:
                aid, name, deadline_str, reminder_sent, deadline_sent = r
                try:
                        deadline = datetime.fromisoformat(deadline_str)
                except Exception:
                        deadline = datetime.fromisoformat(deadline_str)
                delta = deadline - now
                status = []
                if reminder_sent:
                        status.append("pre-reminder sent")
                if deadline_sent:
                        status.append("deadline notified")
                if delta.total_seconds() < 0:
                        status.append("past due")
                s = ", ".join(status) if status else "upcoming"
                lines.append(f"#{aid}: {name} — due {deadline_str} ({s})")
        await update.message.reply_text("\n".join(lines))


async def remove_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        args = context.args
        if not args:
                await update.message.reply_text("Usage: /remove <assignment_id>")
                return
        try:
                aid = int(args[0])
        except ValueError:
                await update.message.reply_text("Invalid id.")
                return
        cur = DB.cursor()
        cur.execute("SELECT id, user_id FROM assignments WHERE id = ?", (aid,))
        row = cur.fetchone()
        if not row:
                await update.message.reply_text("Assignment not found.")
                return
        if row[1] != update.effective_user.id:
                await update.message.reply_text("You can only remove your own assignments.")
                return
        cur.execute("DELETE FROM assignments WHERE id = ?", (aid,))
        DB.commit()
        # remove scheduled jobs if exist
        pre_job_id = f"pre_{aid}"
        deadline_job_id = f"deadline_{aid}"
        for jid in (pre_job_id, deadline_job_id):
                try:
                        SCHED.remove_job(jid)
                except Exception:
                        pass
        await update.message.reply_text(f"Removed assignment #{aid}.")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("I didn't understand that command. Use /help.")


# --- Main setup ---


def main():
        application = ApplicationBuilder().token(BOT_TOKEN).build()

        # Conversation for /add
        conv = ConversationHandler(
                entry_points=[CommandHandler("add", add_start)],
                states={
                        NAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), add_name)],
                        DEADLINE: [MessageHandler(filters.TEXT & (~filters.COMMAND), add_deadline)],
                },
                fallbacks=[CommandHandler("cancel", add_cancel)],
        )

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_cmd))
        application.add_handler(conv)
        application.add_handler(CommandHandler("list", list_cmd))
        application.add_handler(CommandHandler("remove", remove_cmd))
        application.add_handler(MessageHandler(filters.COMMAND, unknown))

        # Start scheduler
        SCHED.start()

        # On startup schedule existing assignments
        async def on_startup(_app):
                await schedule_all_on_start(_app)

        application.post_init.append(on_startup)

        # Run the bot
        logger.info("Starting bot...")
        application.run_polling()


if __name__ == "__main__":
        main()