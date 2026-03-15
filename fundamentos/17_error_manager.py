def divide_numbers() -> float:
  try:
    a: float = float(input('Ingrese el numerador: '))
    b: float = float(input('Ingrese el denominador: '))
    return a / b
  except ZeroDivisionError:
    print('No se puede dividir por cero')
    return 0
  except ValueError:
    print('Por favor ingresa solo numeros')
    return 0
  except Exception as error:
    print(type(error))
    return 0
  else:
    pass
  finally:
    print('Gracias por usar nuestra calculadora')
    
print(divide_numbers())