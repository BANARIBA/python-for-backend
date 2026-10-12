class Person:
    name: str = ""
    age: int = 0

    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age

    def work(self) -> str:
        return f"{self.name} is working really hard!"

person_one: Person = Person("Juan Hernandez", 59)
person_two: Person = Person("Orlando Alvarado", 29)

print(person_one.work())
print(person_two.work())
