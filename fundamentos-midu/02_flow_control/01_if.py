import os

os.system('cls' if os.name == 'nt' else 'clear')

age: int = 18
if age >= 18:
    print("Eres mayor de edad")
else:
    print("Eres menor de edad")
    
nota: int = 7
if nota >= 9:
    print("Excelente")
elif nota >= 7:
    print("Aprobado")
elif nota >= 5:
    print("Suficiente")
else:
    print("Insuficiente")

edad: int = 25
carnet: bool = True
if edad >= 18 and carnet:
    print("Puedes conducir")
else:
    print("No puedes conducir")
