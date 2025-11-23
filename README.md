# n8n Docker Setup with PostgreSQL and Worker

This project provides a complete Docker setup for running n8n locally with PostgreSQL database and worker mode for scalable workflow execution.

## Prerequisites

- Docker Desktop installed on Windows
- Docker Compose (included with Docker Desktop)

## Project Structure

```
n8n/
├── docker-compose.yml    # Docker Compose configuration
├── .env                  # Environment variables (configure before running)
├── init-data.sh         # PostgreSQL initialization script
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## Quick Start

### 1. Configure Environment Variables

Edit the `.env` file and change the default passwords and encryption key:

```bash
# IMPORTANT: Generate a secure encryption key
# On Windows PowerShell, run:
# [Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))
```

**⚠️ Security Note**: Never commit the `.env` file with real credentials to version control!

### 2. Start the Services

Open PowerShell in the project directory and run:

```powershell
docker-compose up -d
```

This will start:

- **PostgreSQL**: Database server (port 5432)
- **Redis**: Queue management for workers
- **n8n**: Main n8n instance (accessible at http://localhost:5678)
- **n8n-worker**: Worker instance for executing workflows

### 3. Access n8n

Open your browser and navigate to:

```
http://localhost:5678
```

On first access, you'll be prompted to create an admin account.

## Managing the Services

### View logs

```powershell
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f n8n
docker-compose logs -f n8n-worker
docker-compose logs -f postgres
```

### Stop services

```powershell
docker-compose stop
```

### Stop and remove containers (keeps data)

```powershell
docker-compose down
```

### Stop and remove everything including volumes (⚠️ deletes all data)

```powershell
docker-compose down -v
```

### Restart services

```powershell
docker-compose restart
```

### Update to latest n8n version

```powershell
docker-compose pull
docker-compose up -d
```

## Configuration Details

### Services

- **n8n Main**: Handles the UI and API requests
- **n8n Worker**: Executes workflows in queue mode (scalable)
- **PostgreSQL 16**: Persistent database for n8n data
- **Redis 6**: Message queue for distributing work to workers

### Volumes

Data is persisted in Docker volumes:

- `db_storage`: PostgreSQL database files
- `n8n_storage`: n8n workflows, credentials, and settings
- `redis_storage`: Redis data

### Environment Variables

Key variables in `.env`:

| Variable                     | Description                                       |
| ---------------------------- | ------------------------------------------------- |
| `POSTGRES_USER`              | PostgreSQL admin user                             |
| `POSTGRES_PASSWORD`          | PostgreSQL admin password                         |
| `POSTGRES_NON_ROOT_USER`     | n8n database user                                 |
| `POSTGRES_NON_ROOT_PASSWORD` | n8n database password                             |
| `ENCRYPTION_KEY`             | n8n encryption key for credentials (must be set!) |

## Troubleshooting

### Containers won't start

1. Check if ports 5678 and 5432 are already in use
2. View logs: `docker-compose logs`

### Database connection issues

1. Wait for PostgreSQL health check to pass: `docker-compose ps`
2. Check PostgreSQL logs: `docker-compose logs postgres`

### Reset everything

```powershell
docker-compose down -v
docker-compose up -d
```

## Production Considerations

For production deployment:

1. Use strong, unique passwords
2. Generate a secure `ENCRYPTION_KEY` (32+ random characters)
3. Configure proper backup for volumes
4. Use environment-specific `.env` files
5. Consider using Docker secrets instead of `.env` files
6. Set up SSL/TLS with a reverse proxy (nginx/traefik)
7. Configure proper logging and monitoring

## Additional Resources

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Docker Setup Guide](https://docs.n8n.io/hosting/installation/docker/)
- [n8n Hosting Repository](https://github.com/n8n-io/n8n-hosting)

## License

This setup is based on the official n8n hosting repository. Please refer to n8n's license for usage terms.
