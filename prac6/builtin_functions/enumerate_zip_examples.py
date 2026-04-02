names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 95]

# enumerate()
for index, name in enumerate(names):
    print(index, name)

# zip()
for name, score in zip(names, scores):
    print(f"{name} scored {score}")

# sorted()
nums = [5, 2, 9, 1]
print("Sorted:", sorted(nums))

# type conversion
x = "123"
y = int(x)
print("Converted to int:", y)

# type checking
print("Type of y:", type(y))