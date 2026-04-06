from os import system
if system("clear") != 0:
    system("cls")

print("\nEjercicio 1: Imprimir mensajes")
print("Escribe un programa que imprima tu nombre y tu ciudad en líneas separadas.")
print("Bryan Ariel")
print("San pedro sula")

print("\nEjercicio 2: Muestra los tipos de datos de las siguientes variables:")
print("Usa el comando 'type()' para determinar el tipo de datos de cada variable.")
a = 15
b = 3.14159
c = "Hola mundo"
d = True
e = None
print(f"""
    Variable a: {a} - Tipo: {type(a)}
    Variable b: {b} - Tipo: {type(b)}
    Variable c: {c} - Tipo: {type(c)}
    Variable d: {d} - Tipo: {type(d)}
    Variable e: {e} - Tipo: {type(e)}
""")

print("\nEjercicio 3: Casting de tipos")
print("Convierte la cadena \"12345\" a un entero y luego a un float.")
print("Convierte el float 3.99 a un entero. ¿Qué ocurre?")
cadena: str = "12345"
cadena_a_entero: int = int(cadena)
cadena_a_float: float = float(cadena)
print(f"Int: {cadena_a_entero}, Float: {cadena_a_float}")

print("\nEjercicio 4: Variables")
print("Crea variables para tu nombre, edad y altura.")
print("Usa f-strings para imprimir una presentación.")
name: str = "Bryan Ariel"
age: int = 30
height: float = 1.5
print(f"Hola, mi nombre es {name}, tengo {age} años y mido {height} metros.")

print("\nEjercicio 5: Números")
print("1. Crea una variable con el número PI (sin asignar una variable)")
print("2. Redondea el número con round()")
print("3. Haz la división entera entre el número que te salió y el número 2")
print("4. El resultado debería ser 1")
import math
pi: int = int(math.pi) 
result = pi//2
print("Resultado de dividir PI entre 2:", result)