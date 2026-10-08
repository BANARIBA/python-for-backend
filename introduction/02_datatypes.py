first_name: str = "Juan Orlando"
last_name: str = "Hernandez Alvarado"
age: int = 59
salary: float = 19000.99
is_active: bool = True

print(f'''
    Nombre: {first_name} {last_name}
    Edad: {age}
    Salario: LPS.{salary}
    Activo: {'Activo' if is_active else 'Inactivo'}
''')