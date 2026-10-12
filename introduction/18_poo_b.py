from abc import ABC, abstractmethod

class BankAccount(ABC):
    owner: str = ""
    __initial_balance: float = 0

    def __init__(self, owner: str, initial_balance: float) -> None:
        self.owner = owner
        self.__initial_balance = initial_balance

    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.__initial_balance += amount

    @abstractmethod
    def withdraw(self, amount: float) -> None:
        pass

    def _get_balance(self) -> float:
        return self.__initial_balance;

    def _set_balance(self, balance: float) -> None:
        self.__initial_balance = balance

    def check_balance(self) -> str:
        return f"Saldo actual ${self.__initial_balance}"

# Herencia para cuenta personal se cobra el retiro
class SavingAccount(BankAccount):

    def withdraw(self, amount: float) -> None:
        penalty: float = amount * 0.05
        total: float = amount + penalty
        substract: float = self._get_balance() - total
        if total <= self._get_balance():
            self._set_balance(substract)
        else:
            print("Fondos Insuficientes.")

# Herencia para cuenta de planilla no se cobra retiro
class PayroallAccount(BankAccount):

    def withdraw(self, amount: float) -> None:
        if amount <= self._get_balance():
            substract: float = self._get_balance() - amount
            self._set_balance(substract)
        else:
            print("Fondos Insuficientes en cuenta de planilla.")

saving_acc: SavingAccount = SavingAccount("Juan", 1000)
payroall_acc: PayroallAccount = PayroallAccount("Orlando", 1000)

saving_acc.withdraw(100)
payroall_acc.withdraw(100)

print(f"Cuenta de ahorro: {saving_acc.check_balance()}")
print(f"Cuenta de planilla: {payroall_acc.check_balance()}")

