# Append new data
with open("sample.txt", "a") as f:
    f.write("This is an appended line\n")

print("Data appended successfully.")

# Verify content
with open("sample.txt", "r") as f:
    print(f.read())