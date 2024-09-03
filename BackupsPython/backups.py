import os
import shutil
import requests
import configparser

# Determine path to config.ini
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config.ini')

# Load config file
config = configparser.ConfigParser()
config.read(config_path)

def send_slack_notification(message):
    webhook_url = config['Slack']['webhook_url']
    payload = {
        "text": message
    }
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        print("Slack notification sent successfully!")
    else:
        print(f"Failed to send Slack notification. Status Code: {response.status_code}")

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
send_slack_notification("Backup Completed: Your backup was successfully completed.")