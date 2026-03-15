from abc import ABC, abstractmethod

class BankAccount(ABC):
  def __init__(self, owner: str, initial_balance: float) -> None:
    self.owner = owner
    self.__balance = initial_balance
    
  def deposit(self, amount: float) -> None:
    if amount > 0:
      self.__balance +=amount
  
  @abstractmethod # Aplicando polimorfismo, depende el tipo de cuenta
  def withdraw(self, amount: float) -> None:
    pass
  
  def _get_balance(self) -> float:
    return self.__balance

  def _set_balance(self, new_balance: float) -> None:
    self.__balance = new_balance

  def check_balance(self) -> str:
    return f'Saldo actual: {self.__balance}'
  
class SavingAccount(BankAccount): # Herencia
  def withdraw(self, amount: float) -> None:
    penalty = amount * 0.05
    total = amount + penalty
    if total <= self._get_balance():
      self._set_balance(self._get_balance() - total)
    else:
      print('Fondos insuficientes en la cuenta de ahorro')
      
class PayrollAccount(BankAccount):
  def withdraw(self, amount: float):
    if amount <= self._get_balance():
      self._set_balance(self._get_balance() - amount)
    else:
      print('Fondos insuficientes en la cuenta de nomina')
      
savings: SavingAccount = SavingAccount('Goku', 1000)
payroll: PayrollAccount = PayrollAccount('Goku', 1000)
savings.withdraw(100)
payroll.withdraw(100)

print(f'Cuenta de ahorro: ${savings._get_balance()}')
print(f'Cuenta planilla: ${payroll._get_balance()}')