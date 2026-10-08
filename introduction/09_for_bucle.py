numbers: list[int] = [1,2,3,4,5]

addition: int = 0

for counter in numbers:
    print(f"Counter value: {counter}")
    addition+=counter

print(f"Total={addition}")

for index, number in enumerate(list(range(10))):
    print(index, number * 2)