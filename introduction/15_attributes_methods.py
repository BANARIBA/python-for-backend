class Person:
    name: str = ""
    age: int = 0
    _energy: float = 0

    def __init__(self, name: str, age: int, energy: float) -> None:
        self.name: str = name
        self.age: int = age
        self._energy: float = energy
        self.__password: str = "1234"

    def work(self) -> str:
        return f"{self.name} is working really hard, energy: {self._energy}!"

    def _waste_energy(self, quantity: float) -> None:
        self._energy -= quantity

    def __generate_password(self) -> str:
        return f"{self.name}***{self.age}"

person_one: Person = Person("Juan Hernandez", 59, 100)
person_two: Person = Person("Orlando Alvarado", 29, 100)

print(person_one.work())
person_two._waste_energy(10)
print(person_two.work())
