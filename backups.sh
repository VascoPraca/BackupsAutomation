#!/bin/bash

SOURCE="$HOME/Documents"
DESTINATION="$HOME/Backups/Documents_$(date)"

mkdir -p "$DESTINATION"

rsync -avh --delete "$SOURCE/" "$DESTINATION/"

echo "Backup completed on $(date)" >> "$HOME/Backup/backup.log"