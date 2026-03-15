class Person:
  def __init__(self, name: str, age: int) -> None:
    self.name = name
    self.age = age
  
  def work(self):
    return f'{self.name} is working hard!'
  
person_one: Person = Person('Goku', 40)
person_two: Person = Person('Vegeta', 45)

print(person_one.work())
print(person_two.work())