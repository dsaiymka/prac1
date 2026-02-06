list={"Aiym":90, "Meier":69, "Saule":95}
for key, value in list.items():
    if value >= 95:
        gpa = 4.0
    elif value >= 90:
        gpa = 3.67
    elif value >= 85:
        gpa = 3.0
    elif value >= 80:
        gpa = 2.67
    elif value >= 75:
        gpa = 2.0
    elif value >= 70:
        gpa = 1.67
    elif value >= 65:
        gpa = 1.0
    else:
        gpa = 0.0

    print(key, gpa)