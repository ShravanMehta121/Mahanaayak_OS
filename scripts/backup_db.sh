#!/bin/bash
# scripts/backup_db.sh
set -e

BACKUP_DIR="./backups"
mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/mahanaayak_db_$TIMESTAMP.sql"

echo "Creating database backup..."
docker exec -t mahanaayak_db pg_dump -U postgres mahanaayak_db > "$BACKUP_FILE"
echo "Backup complete: $BACKUP_FILE"
