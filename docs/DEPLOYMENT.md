# Deployment Guide

This guide details the production deployment process for Mahanaayak OS.

## Architecture
- **Nginx**: Reverse Proxy and Static File Server
- **Gunicorn**: WSGI HTTP Server
- **Flask**: Application backend
- **PostgreSQL**: Primary Database
- **Redis**: Caching and Message Broker

## Production Docker Strategy
The system uses a `docker-compose.yml` to spin up the entire production stack.

### Steps
1. Clone the repository to the production server.
2. Copy `.env.production` to `.env`.
3. Generate secure keys for `SECRET_KEY` and `JWT_SECRET_KEY` in `.env`.
4. Add your `GEMINI_API_KEY`.
5. Run the startup sequence:
```bash
docker-compose up -d --build
```
6. The entrypoint script (`gunicorn_starter.sh`) will automatically run `flask db upgrade` before booting Gunicorn on port 8000, which is proxied by Nginx on port 80.

## Backups
Run `bash scripts/backup_db.sh` via a cron job for automated daily database snapshots.
