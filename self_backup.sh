#!/bin/bash
# NEXUS Self-Backup Script
# Runs automatically before major changes

BACKUP_DIR="$HOME/Backups/nexus"
SOURCE_DIR="$HOME/clawd"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Create backup
tar -czf "$BACKUP_DIR/nexus_backup_$DATE.tar.gz" -C "$SOURCE_DIR" . 2>/dev/null

# Keep only last 7 days
find "$BACKUP_DIR" -name "nexus_backup_*.tar.gz" -mtime +7 -delete 2>/dev/null

# Mark latest
touch "$BACKUP_DIR/latest"

echo "Backup created: $DATE" >> "$HOME/clawd/logs/backup.log"
