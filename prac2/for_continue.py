#1
for i in range(1, 6):
    if i == 3:
        continue
    print(i)

#2
for num in range(1, 11):
    if num % 2 == 0:
        continue
    print(num)

#3
fruits = ["apple", "banana", "cherry", "date"]
for fruit in fruits:
    if fruit.startswith("b"):
        continue
    print(fruit)

#4
for i in range(1, 10):
    if i % 3 == 0:
        continue
    print(i)

#5
names = ["Alice", "Bob", "Charlie", "David"]
for name in names:
    if len(name) <= 3:
        continue
    print(name)