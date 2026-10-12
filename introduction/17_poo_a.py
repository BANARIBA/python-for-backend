class BankAccount:
    owner: str = ""
    __initial_balance: float = 0

    def __init__(self, owner: str, initial_balance: float) -> None:
        self.owner = owner
        self.__initial_balance = initial_balance

    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.__initial_balance += amount

    def withdraw(self, amount: float) -> None:
        if 0 < amount <= self.__initial_balance:
            self.__initial_balance -= amount
        else:
            print("Saldo insuficiente o monto invalido")

    def check_balance(self) -> str:
        return f"Saldo actual ${self.__initial_balance}"

account: BankAccount = BankAccount("Juan Orlando", 1000)
account.deposit(500)
account.withdraw(700)
print(account.check_balance())
        