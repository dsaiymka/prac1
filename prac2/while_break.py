#1
i = 1
while True:
    print(i)
    if i == 5:
        break
    i += 1

#2
while True:
    num = int(input("Введите число (0 чтобы выйти): "))
    if num == 0:
        break
    print("Вы ввели:", num)

#3
n = 1
while n <= 10:
    if n == 7:
        break
    print(n)
    n += 1

#4
text = ""
while True:
    text = input("Введите 'exit' для выхода: ")
    if text == "exit":
        break
    print("Вы написали:", text)

#5
i = 0
while True:
    i += 2
    if i > 10:
        break
    print(i)