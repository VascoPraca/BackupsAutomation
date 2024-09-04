import os
import shutil
import requests
import configparser
from datetime import datetime, timedelta

# Determine path to config.ini
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config.ini')

# Load config file
config = configparser.ConfigParser()
config.read(config_path)

def send_slack_notification(message):
    try:
        # Load webhook from config file
        webhook_url = config['Slack']['webhook_url']
        payload = {
            "text": message
        }
        # Send request to Slack
        response = requests.post(webhook_url, json=payload)

        # Check if request was successful
        if response.status_code == 200:
            print("Slack notification sent successfully!")
        else:
            print(f"Failed to send Slack notification. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending notification. An HTTP error occurred: {e}")
    except KeyError:
        print("Error: Webhook URL not found in configuration file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

source_directory = os.path.expanduser('~/Documents')
backup_directory = os.path.expanduser('~/backups')

# Get current date in YYYY-MM-DD format
date_str = datetime.now().strftime('%Y-%m-%d')


# Check if backup directory exists
try:
    if not os.path.exists(backup_directory):
        os.makedirs(backup_directory)
except OSError as e:
    print(f"Error creating backup directory: {e}")
    exit(1)

# Copy each file, appending the date to the filename
for filename in os.listdir(source_directory):
    source_file = os.path.join(source_directory, filename)
    
    # Append date before file extension
    base, extension = os.path.splitext(filename)
    backup_filename = f"{base}_{date_str}{extension}"
    backup_file = os.path.join(backup_directory, backup_filename)

    try:
        shutil.copy2(source_file, backup_file)
        print(f"Copied: {filename} -> {backup_filename}")
    except FileNotFoundError as e:
        print(f"Error: {e}. File not found: {source_file}")
    except PermissionError as e:
        print(f"Error: {e}. Permission denied for: {source_file}")
    except OSError as e:
        print(f"OS error occured: {e} when copying {source_file}")

# Define retention policy
retention_days = 7
current_date = datetime.now()

# List all backups in directory
backup_files = os.listdir(backup_directory)

for filename in backup_files:
    # Ensure filename follows expected format
    if len(filename.split('_')) > 1:
        try:
            # Extract date from filename
            backup_date_str = filename.split('_')[1].split('.')[0]
            backup_date = datetime.strptime(backup_date_str, '%Y-%m-%d')

            # Calculate difference between current date and backup date
            if (current_date - backup_date).days > retention_days:
                # If backup is older than retention period, delete
                file_path = os.path.join(backup_directory, filename)
                os.remove(file_path)
                print(f"Deleted old backup: {filename}")

        except ValueError as e:
            print(f"Error parsing date from filename: {filename}. Error: {e}")

print("Files copied successfully")
send_slack_notification("Backup Completed: Your backup was successfully completed.")