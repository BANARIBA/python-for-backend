class Person:
  specie: str = 'Saiyan'
  
  def __init__(self, name: str, age: int) -> None:
    self.name: str = name
    self.age: int = age
  
  # Esto cambia el valor inicial de specie en la clase, las demas instancias tendran el nuevo valor
  @classmethod
  def change_species(cls, specie: str) -> None:
    cls.specie = specie
  
  @staticmethod
  def is_older(age: int) -> bool:
    return age >= 18

person_one: Person = Person('Goku', 40)
person_two: Person = Person('Gohan', 13)
print(person_one.specie)
print(person_two.specie)
person_two.change_species('Hybrid')
print(person_one.specie)
print(person_two.specie)

print(person_one.is_older(40))
print(person_two.is_older(13))