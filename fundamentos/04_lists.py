numbers: list[float] = [100,200,300,400,500,1000]
names: list[str] = ['gohan', 'vegetta', 'trunks']
mix: list[list[str] | list[float]] = [numbers, names]

print(f'Values: {numbers}')
print(f'First Value: {numbers[0]}')
print(f'Last value: {numbers[-1]}')
print(f'Mix values: ', mix)


# Agregar valoe a la lista
numbers.append(1001)

# Conteo de valores cuantos de 200 hay
print(numbers.count(200))

# Remover valores
numbers.remove(1000)

print(f'Numbers list: {numbers}')

# Eliminar el ultimo elemento 1001
numbers.pop()

print(f'Numbers list: {numbers}')

numbers.reverse()
print(f'Revertir lista: ', numbers)

numbers.sort()
print(f'Ordenamiento de lista: ', numbers)

min_value: float = min(numbers)
max_value: float = max(numbers)
total_values: float = sum(numbers)

print(f'Min: {min_value}, Max: {max_value}, Total values: {total_values}')

list_numbers: list[float] = [1,2,3,4,5]
list_names: list[str] = ['Goku', 'Vegetta']
list_mix: list[list[str] | list[float]] = [list_numbers, list_names]
print(f'''
  Numbers: {list_numbers},
  Names: {list_names},
  Mix: {list_numbers, list_names}
''')

