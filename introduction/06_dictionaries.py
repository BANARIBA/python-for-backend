user_info: dict[str, str | float | int | bool] = {
    "full_name": "Juan Orlando Hernandez Alvarado",
    "age": 59,
    "role": "Lawyer",
    "email": "jhernandez@honduras.hn",
    "is_active": True
}

print(user_info["full_name"])
user_info["is_active"] = False
print(user_info)

# Imprimir valores del diccionario
print(user_info.items())
print(user_info.keys()) # dict_keys(['full_name', 'age', 'role', 'email', 'is_active'])
print(user_info.values()) # dict_values(['Juan Orlando Hernandez Alvarado', 59, 'Lawyer', 'jhernandez@honduras.hn', False])

print("country" in user_info)
print("is_active" in user_info)