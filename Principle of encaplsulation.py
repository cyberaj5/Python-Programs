class BankAccount:
    def __init__(self, owner, balance):
        self.__owner = owner
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
        else:
            print("Insufficient funds!")

    def get_balance(self):
        return self.__balance

# Main program
aj_account = BankAccount("AJ", 5000)
aj_account.deposit(2000)
aj_account.withdraw(1000)
print(aj_account.get_balance())  # Output: 6000

# aj_account.__balance = 999999  ❌ Not allowed (safeguarded)
