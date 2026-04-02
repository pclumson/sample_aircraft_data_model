#!/bin/bash

set -e

echo "🚀 Starting deployment..."

# Configuration
APP_NAME="aircraft-data-model"
DOCKER_COMPOSE_FILE="docker-compose.yml"
BACKUP_DIR="/backups/aircraft-data"
LOG_FILE="/var/log/deployment.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "$${GREEN}[INFO]$${NC} $(date '+%Y-%m-%d %H:%M:%S') - $$1" | tee -a "$$LOG_FILE"
}

warn() {
    echo -e "$${YELLOW}[WARN]$${NC} $(date '+%Y-%m-%d %H:%M:%S') - $$1" | tee -a "$$LOG_FILE"
}

error() {
    echo -e "$${RED}[ERROR]$${NC} $(date '+%Y-%m-%d %H:%M:%S') - $$1" | tee -a "$$LOG_FILE"
    exit 1
}

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup database
log "Creating database backup..."
docker exec aircraft-data-db pg_dump -U aircraft aircraft_data > "$$BACKUP_DIR/db_backup_$$(date +%Y%m%d_%H%M%S).sql"

# Stop services
log "Stopping services..."
docker-compose -f "$DOCKER_COMPOSE_FILE" down

# Pull latest images
log "Pulling latest images..."
docker-compose -f "$DOCKER_COMPOSE_FILE" pull

# Run migrations
log "Running database migrations..."
docker-compose -f "$DOCKER_COMPOSE_FILE" run --rm api python -m alembic upgrade head

# Start services
log "Starting services..."
docker-compose -f "$DOCKER_COMPOSE_FILE" up -d

# Health check
log "Waiting for services to be healthy..."
sleep 30

# Check health
if docker-compose -f "$DOCKER_COMPOSE_FILE" ps | grep -q "healthy"; then
    log "$${GREEN}✅ Deployment successful!$${NC}"
else
    error "$${RED}❌ Deployment failed - services not healthy$${NC}"
fi

# Cleanup old backups (keep last 7 days)
log "Cleaning up old backups..."
find "$BACKUP_DIR" -name "*.sql" -mtime +7 -delete

log "Deployment completed!"
