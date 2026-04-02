import shutil
import os

# Ensure destination exists
os.makedirs("destination", exist_ok=True)

# Move file
shutil.move("sample.txt", "destination/sample.txt")
print("File moved.")

# Copy back
shutil.copy("destination/sample.txt", "sample.txt")
print("File copied back.")