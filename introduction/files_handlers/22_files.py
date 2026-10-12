try:
    with open("test.txt", mode="w") as my_file:
        text = my_file.write(":D,")
    with open("test.txt", mode="r") as my_file:
        print(my_file.readlines())
    with open("test.txt", mode="r+") as my_file:
        print(my_file.readlines())
        text = my_file.write("Hola Mundo,")
    with open("test.txt", mode="a") as my_file:
        text = my_file.write("Fin seccion")
        print(text)
except FileNotFoundError as err:
    print("El archivo no existe")
except Exception as err:
    print(f"Ha ocurrido un error: {err}")