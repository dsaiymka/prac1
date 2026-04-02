import shutil
import os

# Copy file
shutil.copy("sample.txt", "sample_copy.txt")
print("File copied.")

# Backup file
shutil.copy("sample.txt", "backup_sample.txt")
print("Backup created.")

# Delete file safely
file_to_delete = "sample_copy.txt"

if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print("File deleted.")
else:
    print("File does not exist.")