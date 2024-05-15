#!/bin/bash


# Source the .env file
source .env

# Current date in yyyy-mm-dd format
DATE=$(date +"%F")

# Backup directory on the mounted USB drive
BACKUP_DIR="/media/armando/A8A6-E34B/mysql_backups"

# Ensure backup directory exists
mkdir -p $BACKUP_DIR

# Create a database backup
mysqldump -u $MARIADB_USER -p$MARIADB_PASSWORD -h $MARIADB_HOST -P $MARIADB_PORT $MARIADB_DATABASE > $BACKUP_DIR/$MARIADB_DATABASE-$DATE.sql

# Optional: Remove backups older than 30 days
find $BACKUP_DIR/* -mtime +2 -exec rm {} \;
