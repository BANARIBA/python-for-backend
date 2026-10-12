def divide_numbers() -> float:
    try:
        number_one: float = float(input("Ingrese el numerador: "))
        number_two: float = float(input("Ingrese el denominador: "))
        result: float = number_one / number_two
        return result
    except ZeroDivisionError as error:
        print("No se puede dividir por cero")
        return 0
    except ValueError as error:
        print("Solo se pueden ingresar numeros")
        return 0
    except Exception as error:
        print(type(error))
        return 0
    finally:
        pass

print(divide_numbers())