import os
import shutil

source_directory = os.path.expanduser('~/Documents')
backup_directory = os.path.expanduser('~/backups')

try:
    if not os.path.exists(backup_directory):
        os.makedirs(backup_directory)
except OSError as e:
    print(f"Error creating backup directory: {e}")
    exit(1)

for filename in os.listdir(source_directory):
    source_file = os.path.join(source_directory, filename)
    backup_file = os.path.join(backup_directory, filename)
    try:
        shutil.copy2(source_file, backup_file)
        print(f"Copied: {filename}")
    except FileNotFoundError as e:
        print(f"Error: {e}. File not found: {source_file}")
    except PermissionError as e:
        print(f"Error: {e}. Permission denied for: {source_file}")
    except OSError as e:
        print(f"OS error occured: {e} when copying {source_file}")


print("Files copied successfully")