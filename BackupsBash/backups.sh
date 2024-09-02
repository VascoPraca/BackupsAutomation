#!/bin/bash

SOURCE="$HOME/Documents"
DESTINATION="$HOME/Backups/Documents_$(date +%Y-%m-%d_%H-%M-%S)"

mkdir -p "$DESTINATION" || { echo "Error: Failed to create directory $DESTINATION"; exit 1; }

rsync -avh --delete "$SOURCE/" "$DESTINATION/" || { echo "Error: rsync failed"; exit 1; }

echo "Backup completed on $(date)" >> "$HOME/Backup/backup.log" || { echo "Error: Failed to write to log file"; exit 1; }