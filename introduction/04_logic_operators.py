age: int = 25
licensed: bool = True

if age >= 18 and licensed:
    print("Puedes manejar")

is_student: bool = False
has_membership: bool = True

if is_student or has_membership:
    print("Obtiene precio de descuento")

is_admin: bool = False

if not is_admin:
    print("Acceso denegado")

name: str = "Juan Orlando Hernandez Alvarado"

print(name.upper())