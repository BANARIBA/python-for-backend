def hello(greet: str = "Hi", name: str = "Guest!") -> None:
  print(f'{greet} {name}')
  
def big_function(*args, **kwargs) -> None:
  print(args)
  print(kwargs)

hello()
big_function(1,2,3,4,5,6,7, num1=77, num2=100)