# 🤖 Jarvis Agent Dashboard

A web-based dashboard for tracking Jarvis's work as Kevin's AI assistant.

## Features

- 📊 **Dashboard** - Overview of current tasks, completed work, and statistics
- 📝 **Daily Log** - Task management with priority queue
- 📁 **Projects** - Long-term project tracking with progress bars
- ✅ **Completed Archive** - History of finished work
- 💰 **API Usage** - Track API costs and token usage

## Quick Start

### Option 1: Local Development

```bash
cd web-app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:5051

### Option 2: Docker (Recommended)

```bash
cd web-app

# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

Open http://localhost:5051

## Docker Commands

```bash
# Build image
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f dashboard

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild after code changes
docker-compose up -d --build
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_SECRET_KEY` | Session encryption key | Random (dev) |
| `FLASK_ENV` | Environment mode | production |

**Important:** Set a strong `FLASK_SECRET_KEY` in production:

```bash
# Generate secure key
export FLASK_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
```

## Data Persistence

Data is stored in `data/` directory:
- `daily_logs.json` - Task tracking
- `projects.json` - Project data
- `usage.json` - API usage tracking

When using Docker, these files are persisted via volume mounts.

## Security Notes

- Change default secret key in production
- Data files are excluded from git (see .gitignore)
- Keep personal-dashboard data local only

## Version

v1.2 - With Docker support
