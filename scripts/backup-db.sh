#!/bin/sh
set -e

# PostgreSQL backup script for PyStarter
# Usage: ./scripts/backup-db.sh
# Optional: BACKUP_DIR=./my-backups PRUNE_DAYS=30 ./scripts/backup-db.sh

BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="pystarter_${TIMESTAMP}.sql.gz"

mkdir -p "$BACKUP_DIR"

echo "Backing up database to ${BACKUP_DIR}/${FILENAME}..."
docker compose exec -T db pg_dump -U pystarter pystarter | gzip > "${BACKUP_DIR}/${FILENAME}"

SIZE=$(ls -lh "${BACKUP_DIR}/${FILENAME}" | awk '{print $5}')
echo "Backup complete: ${BACKUP_DIR}/${FILENAME} (${SIZE})"

# Optional: prune old backups
if [ -n "$PRUNE_DAYS" ]; then
    echo "Pruning backups older than ${PRUNE_DAYS} days..."
    find "$BACKUP_DIR" -name "pystarter_*.sql.gz" -mtime +"$PRUNE_DAYS" -delete
    echo "Pruning complete."
fi
