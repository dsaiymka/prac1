# Read entire file
with open("sample.txt", "r") as f:
    content = f.read()
    print("Full content:\n", content)

# Read line by line
with open("sample.txt", "r") as f:
    print("Line by line:")
    for line in f:
        print(line.strip())