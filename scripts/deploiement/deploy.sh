#!/bin/bash
# Script de déploiement pour production

set -e  # Arrêter en cas d'erreur

echo "🚀 Déploiement du projet Django en production"

# Variables
PROJECT_DIR="/var/www/mutuelle"
VENV_DIR="$PROJECT_DIR/venv"
REPO_URL="https://github.com/votre-username/mutuelle.git"
BRANCH="main"

# Couleurs pour le logging
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier les prérequis
check_prerequisites() {
    log_info "Vérification des prérequis..."
    
    # Vérifier Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 n'est pas installé"
        exit 1
    fi
    
    # Vérifier pip
    if ! command -v pip3 &> /dev/null; then
        log_error "pip3 n'est pas installé"
        exit 1
    fi
    
    # Vérifier PostgreSQL
    if ! command -v psql &> /dev/null; then
        log_warn "PostgreSQL n'est pas installé"
    fi
    
    # Vérifier Nginx
    if ! command -v nginx &> /dev/null; then
        log_warn "Nginx n'est pas installé"
    fi
    
    log_info "Prérequis vérifiés"
}

# Créer la structure de dossiers
create_directory_structure() {
    log_info "Création de la structure de dossiers..."
    
    sudo mkdir -p $PROJECT_DIR
    sudo mkdir -p $PROJECT_DIR/logs
    sudo mkdir -p $PROJECT_DIR/staticfiles
    sudo mkdir -p $PROJECT_DIR/media
    sudo mkdir -p $PROJECT_DIR/backups
    
    # Permissions
    sudo chown -R $USER:$USER $PROJECT_DIR
    sudo chmod -R 755 $PROJECT_DIR
    
    log_info "Structure créée"
}

# Cloner ou mettre à jour le projet
setup_project() {
    log_info "Configuration du projet..."
    
    cd $PROJECT_DIR
    
    if [ -d ".git" ]; then
        log_info "Mise à jour du dépôt existant..."
        git pull origin $BRANCH
    else
        log_info "Clonage du dépôt..."
        git clone -b $BRANCH $REPO_URL .
    fi
    
    # Créer l'environnement virtuel
    if [ ! -d "$VENV_DIR" ]; then
        log_info "Création de l'environnement virtuel..."
        python3 -m venv $VENV_DIR
    fi
    
    # Activer l'environnement virtuel et installer les dépendances
    source $VENV_DIR/bin/activate
    pip install --upgrade pip
    pip install -r requirements_production.txt
    
    log_info "Projet configuré"
}

# Configurer les variables d'environnement
setup_environment() {
    log_info "Configuration de l'environnement..."
    
    # Créer le fichier .env si il n'existe pas
    if [ ! -f "$PROJECT_DIR/.env" ]; then
        cat > $PROJECT_DIR/.env << 'ENVEOF'
# Django
DEBUG=False
SECRET_KEY=votre-secret-key-production
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com

# Database
DB_NAME=mutuelle_db
DB_USER=mutuelle_user
DB_PASSWORD=votre-mot-de-passe
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app
DEFAULT_FROM_EMAIL=noreply@votre-domaine.com

# Redis
REDIS_URL=redis://localhost:6379/1

# Autres
TIME_ZONE=Africa/Abidjan
ENVEOF
        
        log_warn "Fichier .env créé avec des valeurs par défaut. Mettez à jour les informations sensibles!"
    fi
    
    log_info "Environnement configuré"
}

# Configurer la base de données
setup_database() {
    log_info "Configuration de la base de données..."
    
    source $VENV_DIR/bin/activate
    cd $PROJECT_DIR
    
    # Appliquer les migrations
    python manage.py migrate --settings=mutuelle_core.settings_production
    
    # Collecter les fichiers statiques
    python manage.py collectstatic --noinput --settings=mutuelle_core.settings_production
    
    # Créer un superutilisateur si nécessaire
    if [ ! -f "$PROJECT_DIR/.superuser_created" ]; then
        log_info "Création du superutilisateur..."
        echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell --settings=mutuelle_core.settings_production
        touch $PROJECT_DIR/.superuser_created
    fi
    
    log_info "Base de données configurée"
}

# Configurer Gunicorn
setup_gunicorn() {
    log_info "Configuration de Gunicorn..."
    
    cat > $PROJECT_DIR/gunicorn_config.py << 'GUNICORNEOF'
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "/var/www/mutuelle/logs/gunicorn_access.log"
errorlog = "/var/www/mutuelle/logs/gunicorn_error.log"
loglevel = "info"

# Process naming
proc_name = "mutuelle_gunicorn"
GUNICORNEOF
    
    # Créer le service systemd
    sudo tee /etc/systemd/system/mutuelle.service > /dev/null << 'SYSTEMDEOF'
[Unit]
Description=Gunicorn daemon for Mutuelle Django
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/mutuelle
Environment="PATH=/var/www/mutuelle/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=mutuelle_core.settings_production"
ExecStart=/var/www/mutuelle/venv/bin/gunicorn --config /var/www/mutuelle/gunicorn_config.py mutuelle_core.wsgi:application

[Install]
WantedBy=multi-user.target
SYSTEMDEOF
    
    sudo systemctl daemon-reload
    sudo systemctl enable mutuelle.service
    sudo systemctl start mutuelle.service
    
    log_info "Gunicorn configuré"
}

# Configurer Nginx
setup_nginx() {
    log_info "Configuration de Nginx..."
    
    sudo tee /etc/nginx/sites-available/mutuelle > /dev/null << 'NGINXEOF'
server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/mutuelle;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        root /var/www/mutuelle;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location / {
        include proxy_params;
        proxy_pass http://0.0.0.0:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    client_max_body_size 100M;
    
    # SSL (à décommenter après avoir configuré SSL)
    # listen 443 ssl http2;
    # ssl_certificate /etc/letsencrypt/live/votre-domaine.com/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/votre-domaine.com/privkey.pem;
    # include /etc/letsencrypt/options-ssl-nginx.conf;
    # ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}
NGINXEOF
    
    # Activer le site
    sudo ln -sf /etc/nginx/sites-available/mutuelle /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    
    log_info "Nginx configuré"
}

# Configurer le backup automatique
setup_backup() {
    log_info "Configuration des sauvegardes..."
    
    # Script de backup
    cat > $PROJECT_DIR/scripts/backup.sh << 'BACKUPEOF'
#!/bin/bash
# Script de sauvegarde automatique

BACKUP_DIR="/var/www/mutuelle/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="mutuelle_db"

# Créer le dossier de backup
mkdir -p $BACKUP_DIR

# Sauvegarder la base de données PostgreSQL
pg_dump $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# Sauvegarder les fichiers media
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz -C /var/www/mutuelle media/

# Sauvegarder les fichiers importants
tar -czf $BACKUP_DIR/files_backup_$DATE.tar.gz \
    --exclude=venv \
    --exclude=__pycache__ \
    --exclude=*.pyc \
    /var/www/mutuelle/

# Supprimer les vieux backups (plus de 30 jours)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Backup du $DATE terminé"
BACKUPEOF
    
    chmod +x $PROJECT_DIR/scripts/backup.sh
    
    # Ajouter une tâche cron pour les backups quotidiens
    (crontab -l 2>/dev/null; echo "0 2 * * * /var/www/mutuelle/scripts/backup.sh >> /var/www/mutuelle/logs/backup.log 2>&1") | crontab -
    
    log_info "Sauvegardes configurées"
}

# Fonction principale
main() {
    log_info "Début du déploiement..."
    
    check_prerequisites
    create_directory_structure
    setup_project
    setup_environment
    setup_database
    setup_gunicorn
    setup_nginx
    setup_backup
    
    log_info "✅ Déploiement terminé avec succès!"
    log_info "📋 Vérifications:"
    log_info "  1. Vérifiez le service: sudo systemctl status mutuelle"
    log_info "  2. Vérifiez Nginx: sudo systemctl status nginx"
    log_info "  3. Accédez au site: http://votre-domaine.com"
    log_info "  4. Vérifiez les logs: tail -f /var/www/mutuelle/logs/*.log"
}

# Exécuter la fonction principale
main
