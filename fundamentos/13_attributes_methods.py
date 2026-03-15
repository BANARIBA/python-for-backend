class Person:
  species: str = 'Human'
  
  def __init__(self, name: str, age: int) -> None:
    self.name: str = name
    self.age: int = age
    self._energy: float = 100 # Atributo protegido _
    self.__password: str = '1234' # Atributo privado __
  
  def work(self):
    return f'{self.name} is working hard with {self._energy}% of capacity!'
  
  def _waste_energy(self, quantity: float) -> None:
    self._energy -= quantity
  
  def __generate_password(self) -> str:
    return f'$${self.name}{self.age}$$'
  
person_one: Person = Person('Goku', 40)
person_two: Person = Person('Vegeta', 45)

print(person_one.work())
print(person_two.work())
person_two._waste_energy(10)
print(person_two.work())
# No se puede acceder print(person_one.__password)