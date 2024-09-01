import os
import shutil

source_directory = os.path.expanduser('~/Documents')
backup_directory = os.path.expanduser('~/backups')

files = os.listdir(source_directory)

print(files)

if not os.path.exists(backup_directory):
    os.makedirs(backup_directory)


for filename in os.listdir(source_directory):
    source_file = os.path.join(source_directory, filename)
    backup_file = os.path.join(backup_directory, filename)
    shutil.copy2(source_file, backup_file)

print("Files copied successfully")