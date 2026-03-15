try:
  # Escritura
  with open('test.txt', mode="w") as my_file:
    text = my_file.write(":) ")
  
  # Lectura
  with open('test.txt', mode="r") as my_file:
    print(my_file.readlines())
    
  # Lectura y escritura
  with open('test.txt', mode="r+") as my_file:
    print(my_file.readlines())
    text = my_file.write("Hola mundo ")
    
  # append: escribir, agrega al final de lo que hay
  with open('test.txt', mode="a") as my_file:
    text = my_file.write("123 ")
    print(text)
    
except FileNotFoundError:
  print('El archivo no existe')
except Exception as err:
  print(f'Ha ocurrido un error: {err}')