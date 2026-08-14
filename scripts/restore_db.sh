#!/bin/bash
# scripts/restore_db.sh
set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <path_to_backup.sql>"
  exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
  echo "Error: File $BACKUP_FILE not found!"
  exit 1
fi

echo "Restoring database from $BACKUP_FILE..."
cat "$BACKUP_FILE" | docker exec -i mahanaayak_db psql -U postgres -d mahanaayak_db
echo "Restore complete!"
