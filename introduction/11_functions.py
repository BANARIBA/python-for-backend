def get_user_greet(greet: str, full_name: str) -> str:
    return f"{greet} {full_name}"

print(get_user_greet("Hi and welcome", "Juan Orlando Hernandez Alvarado"))

# recibir varios valores
def big_function(*args, **kwargs) -> None:
    print("Valores normales:", args)
    print("Valores nombrados:", kwargs)

big_function(1,2,3,4,5,5,6,7,first_name="Juan Orlando", last_name="Hernandez Alvarado")