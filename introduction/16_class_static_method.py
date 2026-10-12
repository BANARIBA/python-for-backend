class Person:
    species: str = "Human"
    name: str = ""
    age: int = 0

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    @classmethod
    def change_specie(cls, new_specie: str) -> None:
        cls.species = new_specie

    @staticmethod
    def is_older(age: int) -> bool:
        return age >= 18

Person.change_specie("Cyborg")

person_one: Person = Person("Orlando", 59)
person_two: Person = Person("Juan", 59)

print(person_one.species)
print(person_two.species)
print(person_two.is_older(20))