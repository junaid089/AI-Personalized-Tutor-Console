# Deployment Guide - AI Personalized Tutor Console

## Deployment Options

This guide covers multiple deployment strategies for the AI Personalized Tutor Console.

---

## Option 1: Local Development Setup (Recommended for Testing)

### Requirements
- Python 3.8+
- PostgreSQL 12+
- 4GB RAM minimum

### Steps
1. Follow [QUICKSTART.md](QUICKSTART.md) guide
2. Access at `http://localhost:8001`

**Best for**: Development, testing, demos

---

## Option 2: Production Server Deployment (VPS/Cloud)

### Requirements
- Ubuntu 20.04+ / Debian 11+
- 2 CPU cores, 4GB RAM
- PostgreSQL 12+
- Supervisor
- Nginx (optional, for SSL/domain)

### Step 1: Server Setup

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y python3-pip python3-venv postgresql postgresql-contrib nginx supervisor git

# Start PostgreSQL
sudo service postgresql start
```

### Step 2: Clone and Configure

```bash
# Clone repository
cd /var/www
sudo git clone git@github.com:junaid089/AI-Personalized-Tutor-Console.git
cd AI-Personalized-Tutor-Console

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt
```

### Step 3: Database Setup

```bash
# Create database
sudo -u postgres psql -c "CREATE DATABASE tutor_db;"
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'your-secure-password';"

# Update backend/.env with secure credentials
nano backend/.env
```

**backend/.env**:
```bash
EMERGENT_LLM_KEY=sk-emergent-347D1Bc865f97F4353
DATABASE_URL=postgresql://postgres:your-secure-password@localhost:5432/tutor_db
```

### Step 4: Supervisor Configuration

```bash
# Create supervisor config
sudo nano /etc/supervisor/conf.d/tutor-backend.conf
```

**tutor-backend.conf**:
```ini
[program:tutor-backend]
command=/var/www/AI-Personalized-Tutor-Console/venv/bin/python /var/www/AI-Personalized-Tutor-Console/backend/server.py
directory=/var/www/AI-Personalized-Tutor-Console/backend
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/supervisor/tutor-backend.err.log
stdout_logfile=/var/log/supervisor/tutor-backend.out.log
environment=PATH="/var/www/AI-Personalized-Tutor-Console/venv/bin"
```

```bash
# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start tutor-backend
```

### Step 5: Nginx Configuration (Optional - for domain/SSL)

```bash
sudo nano /etc/nginx/sites-available/tutor
```

**/etc/nginx/sites-available/tutor**:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static {
        alias /var/www/AI-Personalized-Tutor-Console/frontend/static;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/tutor /etc/nginx/sites-enabled/
sudo nginx -t
sudo service nginx restart
```

### Step 6: SSL with Let's Encrypt (Optional)

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

### Step 7: Firewall Configuration

```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Access
- With domain: `https://your-domain.com`
- With IP: `http://your-server-ip:8001`

---

## Option 3: Docker Deployment

### Requirements
- Docker
- Docker Compose

### Step 1: Create Dockerfile

**Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY prompts/ ./prompts/

WORKDIR /app/backend

EXPOSE 8001

CMD ["python", "server.py"]
```

### Step 2: Docker Compose

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: tutor_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: .
    ports:
      - "8001:8001"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/tutor_db
      EMERGENT_LLM_KEY: sk-emergent-347D1Bc865f97F4353
    depends_on:
      - postgres
    volumes:
      - ./backend:/app/backend
      - ./frontend:/app/frontend

volumes:
  postgres_data:
```

### Step 3: Deploy

```bash
# Build and start
docker-compose up -d

# Check logs
docker-compose logs -f

# Access at http://localhost:8001
```

### Step 4: Update

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

---

## Option 4: Cloud Platform Deployment

### Heroku

**Procfile**:
```
web: cd backend && python server.py
```

**runtime.txt**:
```
python-3.11.0
```

```bash
# Create Heroku app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set EMERGENT_LLM_KEY=sk-emergent-347D1Bc865f97F4353

# Deploy
git push heroku main

# Open app
heroku open
```

### AWS Elastic Beanstalk

1. Install EB CLI: `pip install awsebcli`
2. Initialize: `eb init`
3. Create environment: `eb create tutor-env`
4. Deploy: `eb deploy`
5. Open: `eb open`

### Google Cloud Run

```bash
# Build image
gcloud builds submit --tag gcr.io/your-project/tutor

# Deploy
gcloud run deploy tutor \
  --image gcr.io/your-project/tutor \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Environment Variables for Production

**Required**:
- `EMERGENT_LLM_KEY`: Your LLM API key
- `DATABASE_URL`: PostgreSQL connection string

**Optional**:
- `PORT`: Server port (default: 8001)
- `HOST`: Server host (default: 0.0.0.0)
- `LOG_LEVEL`: Logging level (default: INFO)

**Security Best Practices**:
- Never commit `.env` file
- Use environment-specific keys
- Rotate keys regularly
- Use secrets management (AWS Secrets Manager, etc.)

---

## Database Migration for Production

### Backup
```bash
# Backup before deployment
pg_dump tutor_db > backup_$(date +%Y%m%d).sql

# Or using Docker
docker-compose exec postgres pg_dump -U postgres tutor_db > backup.sql
```

### Restore
```bash
# Restore from backup
psql tutor_db < backup.sql

# Or using Docker
docker-compose exec -T postgres psql -U postgres tutor_db < backup.sql
```

---

## Monitoring and Logging

### Supervisor Logs
```bash
# View logs
tail -f /var/log/supervisor/tutor-backend.out.log
tail -f /var/log/supervisor/tutor-backend.err.log

# Rotate logs (add to crontab)
0 0 * * * /usr/bin/supervisorctl restart tutor-backend
```

### Application Monitoring
```python
# Add to server.py for production logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/tutor/app.log'),
        logging.StreamHandler()
    ]
)
```

### Database Monitoring
```bash
# Check connections
sudo -u postgres psql tutor_db -c "SELECT count(*) FROM pg_stat_activity;"

# Database size
sudo -u postgres psql tutor_db -c "SELECT pg_size_pretty(pg_database_size('tutor_db'));"
```

---

## Performance Optimization

### Database Optimization
```sql
-- Add indexes for frequently queried fields
CREATE INDEX idx_students_grade ON students(grade_level);
CREATE INDEX idx_progress_student ON progress(student_id);
CREATE INDEX idx_sessions_student ON learning_sessions(student_id);

-- Analyze tables
ANALYZE students;
ANALYZE progress;
```

### Caching (Future Enhancement)
```python
# Add Redis for caching AI responses
# pip install redis
from redis import Redis
cache = Redis(host='localhost', port=6379)
```

### Load Balancing (High Traffic)
```nginx
# Nginx upstream for multiple instances
upstream tutor_backend {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}
```

---

## Backup Strategy

### Automated Daily Backups
```bash
# Create backup script
cat > /usr/local/bin/backup-tutor.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/tutor"
mkdir -p $BACKUP_DIR

# Database backup
pg_dump tutor_db | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
EOF

chmod +x /usr/local/bin/backup-tutor.sh

# Add to crontab (daily at 2 AM)
echo "0 2 * * * /usr/local/bin/backup-tutor.sh" | crontab -
```

---

## Health Checks

### Uptime Monitoring
```bash
# Simple health check script
curl -f http://localhost:8001/api/health || systemctl restart tutor-backend
```

### External Monitoring Services
- UptimeRobot
- Pingdom
- StatusCake
- CloudWatch (AWS)

---

## Troubleshooting Deployment Issues

### Backend won't start
```bash
# Check logs
sudo supervisorctl tail -f tutor-backend stderr

# Common issues:
# 1. Wrong Python path in supervisor config
# 2. Missing dependencies
# 3. Database connection error
# 4. Port already in use
```

### Database connection errors
```bash
# Test connection
psql -h localhost -U postgres -d tutor_db

# Check PostgreSQL is running
sudo service postgresql status

# Check firewall
sudo ufw status
```

### High memory usage
```bash
# Monitor resources
htop

# Optimize PostgreSQL
# Edit /etc/postgresql/15/main/postgresql.conf
shared_buffers = 256MB
effective_cache_size = 1GB
```

---

## Scaling for Production

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize database queries
- Add database indexes

### Horizontal Scaling
- Multiple backend instances behind load balancer
- Read replicas for database
- Separate AI processing to queue workers

### CDN Integration
- Serve static files from CDN
- Use CloudFlare or AWS CloudFront
- Cache API responses (carefully)

---

## Security Checklist

- ✅ Use strong database passwords
- ✅ Enable firewall (UFW/iptables)
- ✅ Install SSL certificate
- ✅ Keep system updated
- ✅ Disable root SSH access
- ✅ Use SSH keys instead of passwords
- ✅ Enable rate limiting
- ✅ Regular security updates
- ✅ Monitor logs for suspicious activity
- ✅ Backup regularly

---

## Rollback Strategy

### Quick Rollback
```bash
# Tag current version
git tag -a v1.0.0 -m "Stable version"

# If deployment fails, rollback
git checkout v1.0.0
sudo supervisorctl restart tutor-backend
```

### Database Rollback
```bash
# Restore from backup
psql tutor_db < backup_20251031.sql
```

---

## Support and Maintenance

### Regular Maintenance Tasks
- **Daily**: Check logs, monitor errors
- **Weekly**: Review performance, check disk space
- **Monthly**: Update dependencies, security patches
- **Quarterly**: Database optimization, backup testing

### Update Procedure
```bash
# 1. Backup
./backup-tutor.sh

# 2. Pull updates
git pull origin main

# 3. Update dependencies
source venv/bin/activate
pip install -r backend/requirements.txt

# 4. Restart
sudo supervisorctl restart tutor-backend

# 5. Test
curl http://localhost:8001/api/health
```

---

## Contact for Deployment Issues

- GitHub Issues: https://github.com/junaid089/AI-Personalized-Tutor-Console/issues
- Documentation: [README.md](README.md)
- API Docs: http://your-domain.com/docs
