import os

folder = "."

for file in os.listdir(folder):
    if file.endswith(".txt"):
        print("Text file found:", file)