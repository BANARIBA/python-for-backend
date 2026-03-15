numbers: list[int] = [1,2,3,4,5]
addition: int = 0

for number in numbers:
  print(number)
  addition += number
  
print(f'Total addition: {addition}')

for index, number in enumerate(list(range(10))):
  print(index, number * number)