numbers: list[float] = [1,2,33,4,5,22]
letters: list[str] = ["A", "b", "C", "d"]
shopping_cart: str = ["Laptop", "Silla Gamer", "Mouse"]

print(numbers)
print(letters)
print(shopping_cart)

print(type(shopping_cart))

# Metodos
# Agregar
numbers.append(100)
print(numbers)

# Eliminar
numbers.remove(2)
print(numbers)

# Conteo
print(numbers.count(100))

# Ordenar
numbers.sort(reverse=True)
print(numbers)