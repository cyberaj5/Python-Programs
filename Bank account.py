class Bankaccount:
    def __init__(self, acccount_holder, balance):
        self.account_holder = acccount_holder
        self.__balance = balance
    def    deposit(self,amount ):
        """allows sepositing money into the bank account"""
        if amount > 0:
            self.__balance +=amount
            print(f"Deposited $ {amount} New balnce:$ {self. __balance}")
        else:
            print("Deposited amount must be positive")

    def withdraw(self,amount):
        """method to withdraw money from acount"""
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"Withdraw ${amount}.remaining balance:$ {self.__balance}")
        else:
            print("Insuffcient funds or invalid account")
account =Bankaccount ("JOHN SIN",500)
account.deposit(200)
account.withdraw(100)
print("Current Balance:*****" )
   