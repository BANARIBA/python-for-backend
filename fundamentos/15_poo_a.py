class BankAccount:
  def __init__(self, owner: str, initial_balance: float) -> None:
    self.owner = owner
    self.__balance = initial_balance
    
  def deposit(self, amount: float) -> None:
    if amount > 0:
      self.__balance +=amount
      
  def withdraw(self, amount) -> None:
    if 0 < amount <= self.__balance:
      self.__balance -= amount
    else:
      print('Saldo insuficiente o monto no permitido')

  def check_balance(self) -> str:
    return f'Saldo actual: {self.__balance}'
  
account: BankAccount = BankAccount('BSANCHEZ', 1000.00)
account.deposit(500)
account.withdraw(700)

print(account.check_balance())