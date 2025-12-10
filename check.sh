#!/usr/bin/env bash
# check.sh - Script de vérification complète pour projet Django
# Vérifie la configuration, les dépendances, la sécurité et la structure

set -o errexit
set -o pipefail
set -o nounset

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Niveaux de sévérité
SUCCESS=0
WARNING=1
ERROR=2

# Variables globales
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNINGS=0

# Fonctions d'affichage
print_header() {
    echo -e "\n${BLUE}══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}══════════════════════════════════════════════════════════════${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
    ((PASSED_CHECKS++))
    ((TOTAL_CHECKS++))
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    ((WARNINGS++))
    ((TOTAL_CHECKS++))
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
    ((FAILED_CHECKS++))
    ((TOTAL_CHECKS++))
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

# ==================== VÉRIFICATIONS SYSTÈME ====================
check_system() {
    print_header "VÉRIFICATION SYSTÈME"
    
    # Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        print_success "Python $PYTHON_VERSION installé"
        
        # Vérifier version Python
        if [[ "$PYTHON_VERSION" =~ ^3\.(11|12)\..* ]]; then
            print_success "Python $PYTHON_VERSION compatible (3.11 ou 3.12)"
        else
            print_warning "Python $PYTHON_VERSION - Recommandé: 3.11 ou 3.12"
        fi
    else
        print_error "Python3 non installé"
    fi
    
    # pip
    if command -v pip3 &> /dev/null; then
        PIP_VERSION=$(pip3 --version 2>&1 | awk '{print $2}')
        print_success "pip $PIP_VERSION installé"
    else
        print_warning "pip3 non installé"
    fi
    
    # Git
    if command -v git &> /dev/null; then
        GIT_VERSION=$(git --version | awk '{print $3}')
        print_success "Git $GIT_VERSION installé"
    else
        print_warning "Git non installé"
    fi
    
    # Mémoire disponible
    if [[ "$OSTYPE" == "darwin"* ]]; then
        TOTAL_MEM=$(sysctl hw.memsize | awk '{print $2}')
        TOTAL_MEM_MB=$((TOTAL_MEM / 1024 / 1024))
    else
        TOTAL_MEM=$(free -m | awk '/^Mem:/{print $2}')
        TOTAL_MEM_MB=$TOTAL_MEM
    fi
    
    if [ "$TOTAL_MEM_MB" -ge 1024 ]; then
        print_success "Mémoire disponible: ${TOTAL_MEM_MB}MB"
    else
        print_warning "Mémoire limitée: ${TOTAL_MEM_MB}MB (Recommandé: 2GB minimum)"
    fi
    
    # Espace disque
    DISK_SPACE=$(df -h . | awk 'NR==2 {print $4}')
    print_info "Espace disque disponible: $DISK_SPACE"
}

# ==================== VÉRIFICATIONS PROJET DJANGO ====================
check_django_project() {
    print_header "VÉRIFICATION PROJET DJANGO"
    
    # Vérifier si manage.py existe
    if [ -f "manage.py" ]; then
        print_success "Fichier manage.py présent"
        
        # Vérifier les permissions
        if [ -x "manage.py" ]; then
            print_success "manage.py exécutable"
        else
            print_warning "manage.py non exécutable, correction..."
            chmod +x manage.py 2>/dev/null || true
        fi
    else
        print_error "manage.py non trouvé - Pas un projet Django?"
        return $ERROR
    fi
    
    # Vérifier structure Django
    REQUIRED_FILES=(
        "mutuelle_core/__init__.py"
        "mutuelle_core/settings.py"
        "mutuelle_core/urls.py"
        "mutuelle_core/wsgi.py"
    )
    
    for file in "${REQUIRED_FILES[@]}"; do
        if [ -f "$file" ]; then
            print_success "$file présent"
        else
            print_error "$file manquant"
        fi
    done
    
    # Vérifier applications
    print_info "Recherche d'applications Django..."
    APP_COUNT=$(find . -name "apps.py" -type f | wc -l)
    if [ "$APP_COUNT" -gt 0 ]; then
        print_success "$APP_COUNT application(s) Django trouvée(s)"
    else
        print_error "Aucune application Django trouvée"
    fi
    
    # Vérifier settings de production
    if [ -f "mutuelle_core/settings_production.py" ]; then
        print_success "Settings de production présents"
        
        # Vérifier variables critiques
        PROD_CHECK=$(grep -c "DEBUG = False" mutuelle_core/settings_production.py || true)
        if [ "$PROD_CHECK" -gt 0 ]; then
            print_success "DEBUG = False en production"
        else
            print_warning "DEBUG pas forcé à False en production"
        fi
    else
        print_warning "Settings de production manquants (mutuelle_core/settings_production.py)"
    fi
}

# ==================== VÉRIFICATIONS DÉPENDANCES ====================
check_dependencies() {
    print_header "VÉRIFICATION DÉPENDANCES"
    
    # Vérifier requirements.txt
    if [ -f "requirements.txt" ]; then
        print_success "requirements.txt présent"
        
        # Compter les dépendances
        DEP_COUNT=$(grep -c "^[^#]" requirements.txt 2>/dev/null || echo "0")
        print_info "$DEP_COUNT dépendance(s) listée(s)"
        
        # Vérifier dépendances critiques
        CRITICAL_DEPS=("Django" "gunicorn" "psycopg2-binary" "whitenoise")
        for dep in "${CRITICAL_DEPS[@]}"; do
            if grep -q "$dep" requirements.txt; then
                print_success "$dep dans requirements.txt"
            else
                print_warning "$dep manquant dans requirements.txt"
            fi
        done
    else
        print_error "requirements.txt manquant"
    fi
    
    # Vérifier runtime.txt pour Render
    if [ -f "runtime.txt" ]; then
        print_success "runtime.txt présent"
        RUNTIME_VERSION=$(cat runtime.txt | cut -d'-' -f2)
        print_info "Python $RUNTIME_VERSION spécifié"
    else
        print_warning "runtime.txt manquant (nécessaire pour Render)"
    fi
    
    # Vérifier installation pip
    if command -v pip3 &> /dev/null; then
        print_info "Vérification des packages installés..."
        
        # Vérifier Django installé
        if python3 -c "import django" 2>/dev/null; then
            DJANGO_VERSION=$(python3 -c "import django; print(django.__version__)")
            print_success "Django $DJANGO_VERSION installé"
        else
            print_error "Django non installé"
        fi
        
        # Vérifier autres packages critiques
        CRITICAL_PACKAGES=(
            "gunicorn" 
            "psycopg2"
            "whitenoise"
            "PIL"
        )
        
        for package in "${CRITICAL_PACKAGES[@]}"; do
            if python3 -c "import $package" 2>/dev/null; then
                print_success "$package installé"
            else
                print_warning "$package non installé"
            fi
        done
    fi
}

# ==================== VÉRIFICATIONS BASE DE DONNÉES ====================
check_database() {
    print_header "VÉRIFICATION BASE DE DONNÉES"
    
    # Vérifier si SQLite est utilisé en développement
    if [ -f "db.sqlite3" ]; then
        DB_SIZE=$(du -h db.sqlite3 | cut -f1)
        print_success "Base SQLite présente ($DB_SIZE)"
        
        # Vérifier taille
        if [ -f "db.sqlite3" ] && [ $(du -k db.sqlite3 | cut -f1) -gt 10485760 ]; then
            print_warning "Base SQLite > 10GB - Pensez à migrer vers PostgreSQL en production"
        fi
    else
        print_info "Pas de base SQLite locale"
    fi
    
    # Vérifier les migrations
    print_info "Vérification des migrations..."
    
    if python3 manage.py showmigrations --list 2>/dev/null | grep -q "\[ \]"; then
        UNAPPLIED=$(python3 manage.py showmigrations --list 2>/dev/null | grep "\[ \]" | wc -l)
        print_warning "$UNAPPLIED migration(s) non appliquée(s)"
        
        # Afficher les migrations manquantes
        if [ "$UNAPPLIED" -gt 0 ]; then
            echo -e "${YELLOW}Migrations en attente:${NC}"
            python3 manage.py showmigrations --list 2>/dev/null | grep "\[ \]" | head -5
        fi
    else
        print_success "Toutes les migrations sont appliquées"
    fi
    
    # Vérifier la connexion à la base
    print_info "Test de connexion à la base de données..."
    
    if python3 -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute('SELECT 1')
    result = cursor.fetchone()
    if result and result[0] == 1:
        print('✅ Connexion BD OK')
    else:
        print('❌ Erreur connexion BD')
" 2>&1 | grep -q "✅"; then
        print_success "Connexion à la base de données établie"
    else
        print_error "Impossible de se connecter à la base de données"
    fi
}

# ==================== VÉRIFICATIONS SÉCURITÉ ====================
check_security() {
    print_header "VÉRIFICATION SÉCURITÉ"
    
    # Vérifier SECRET_KEY
    print_info "Vérification SECRET_KEY..."
    
    if python3 -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()
from django.conf import settings
key = settings.SECRET_KEY
if len(key) >= 50 and not key.startswith('django-insecure-'):
    print('✅ SECRET_KEY sécurisée')
else:
    print('❌ SECRET_KEY faible ou par défaut')
" 2>&1 | grep -q "✅"; then
        print_success "SECRET_KEY sécurisée"
    else
        print_error "SECRET_KEY trop courte ou par défaut"
    fi
    
    # Vérifier DEBUG mode
    if python3 -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()
from django.conf import settings
print('DEBUG =', settings.DEBUG)
" 2>&1 | grep -q "DEBUG = False"; then
        print_success "DEBUG = False (production)"
    else
        print_warning "DEBUG = True (développement)"
    fi
    
    # Exécuter django check --deploy
    print_info "Exécution de django check --deploy..."
    
    CHECK_OUTPUT=$(python3 manage.py check --deploy 2>&1 || true)
    
    if echo "$CHECK_OUTPUT" | grep -q "System check identified no issues"; then
        print_success "Aucun problème de sécurité identifié"
    else
        # Compter les warnings
        WARN_COUNT=$(echo "$CHECK_OUTPUT" | grep -c "WARNINGS:" || true)
        if [ "$WARN_COUNT" -gt 0 ]; then
            print_warning "$WARN_COUNT avertissement(s) de sécurité"
            echo -e "${YELLOW}Aperçu:${NC}"
            echo "$CHECK_OUTPUT" | grep -A5 "WARNINGS:" | head -10
        fi
        
        # Compter les erreurs
        ERR_COUNT=$(echo "$CHECK_OUTPUT" | grep -c "ERRORS:" || true)
        if [ "$ERR_COUNT" -gt 0 ]; then
            print_error "$ERR_COUNT erreur(s) de sécurité"
        fi
    fi
    
    # Vérifier les settings de sécurité en production
    if [ -f "mutuelle_core/settings_production.py" ]; then
        SECURITY_SETTINGS=(
            "SECURE_SSL_REDIRECT"
            "SESSION_COOKIE_SECURE"
            "CSRF_COOKIE_SECURE"
            "SECURE_HSTS_SECONDS"
        )
        
        for setting in "${SECURITY_SETTINGS[@]}"; do
            if grep -q "$setting = True" mutuelle_core/settings_production.py || \
               grep -q "$setting = 31536000" mutuelle_core/settings_production.py; then
                print_success "$setting configuré"
            else
                print_warning "$setting non configuré en production"
            fi
        done
    fi
}

# ==================== VÉRIFICATIONS FICHIERS STATIQUES ====================
check_static_files() {
    print_header "VÉRIFICATION FICHIERS STATIQUES"
    
    # Vérifier static et media
    for dir in "static" "media" "staticfiles"; do
        if [ -d "$dir" ]; then
            FILE_COUNT=$(find "$dir" -type f | wc -l)
            DIR_SIZE=$(du -sh "$dir" 2>/dev/null | cut -f1 || echo "0")
            print_success "Dossier $dir présent (${FILE_COUNT} fichiers, ${DIR_SIZE})"
        else
            print_warning "Dossier $dir manquant"
        fi
    done
    
    # Vérifier collectstatic
    print_info "Test de collectstatic..."
    
    if python3 manage.py collectstatic --noinput --dry-run 2>&1 | grep -q "0 static files copied"; then
        print_success "collectstatic configuré correctement"
    else
        STATIC_COUNT=$(python3 manage.py collectstatic --noinput --dry-run 2>&1 | grep -o "[0-9]\+ static files" | grep -o "[0-9]\+" || echo "0")
        if [ "$STATIC_COUNT" -gt 0 ]; then
            print_success "$STATIC_COUNT fichier(s) static à collecter"
        else
            print_warning "collectstatic ne trouve pas de fichiers"
        fi
    fi
    
    # Vérifier WhiteNoise
    if grep -q "whitenoise" requirements.txt 2>/dev/null || \
       python3 -c "import whitenoise" 2>/dev/null; then
        print_success "WhiteNoise configuré"
        
        # Vérifier middleware
        if grep -q "WhiteNoiseMiddleware" mutuelle_core/settings.py 2>/dev/null || \
           grep -q "whitenoise.middleware.WhiteNoiseMiddleware" mutuelle_core/settings.py 2>/dev/null; then
            print_success "WhiteNoise middleware activé"
        else
            print_warning "WhiteNoise middleware non activé"
        fi
    else
        print_warning "WhiteNoise non installé"
    fi
}

# ==================== VÉRIFICATIONS URLS ET VUES ====================
check_urls() {
    print_header "VÉRIFICATION URLS ET VUES"
    
    # Vérifier urls.py principal
    if [ -f "mutuelle_core/urls.py" ]; then
        URL_COUNT=$(grep -c "^urlpatterns = \|^path(\|^re_path(" mutuelle_core/urls.py 2>/dev/null || echo "0")
        print_info "$URL_COUNT motif(s) d'URL dans mutuelle_core/urls.py"
    fi
    
    # Tester les URLs de base
    print_info "Test des URLs de base..."
    
    # URLs à tester
    BASE_URLS=(
        "/admin/"
        "/"
        "/health/"
        "/api/"
    )
    
    # Démarrer un serveur test en arrière-plan
    python3 manage.py runserver 0.0.0.0:9999 --noreload --nothreading 2>/dev/null &
    SERVER_PID=$!
    
    # Attendre que le serveur démarre
    sleep 2
    
    for url in "${BASE_URLS[@]}"; do
        if curl -s -o /dev/null -w "%{http_code}" "http://localhost:9999$url" 2>/dev/null | grep -q "200\|302\|301"; then
            print_success "URL accessible: $url"
        else
            print_warning "URL non accessible: $url"
        fi
    done
    
    # Arrêter le serveur test
    kill $SERVER_PID 2>/dev/null || true
    wait $SERVER_PID 2>/dev/null || true
    
    # Vérifier les applications avec urls.py
    APP_URLS=$(find . -name "urls.py" -type f | grep -v __pycache__ | wc -l)
    print_info "$APP_URLS fichier(s) urls.py trouvé(s)"
}

# ==================== VÉRIFICATIONS PERFORMANCE ====================
check_performance() {
    print_header "VÉRIFICATION PERFORMANCE"
    
    # Vérifier les fichiers volumineux
    print_info "Recherche de fichiers volumineux..."
    
    LARGE_FILES=$(find . -type f -size +10M 2>/dev/null | head -5)
    if [ -n "$LARGE_FILES" ]; then
        print_warning "Fichiers volumineux trouvés:"
        for file in $LARGE_FILES; do
            SIZE=$(du -h "$file" | cut -f1)
            echo -e "  ${YELLOW}• $file ($SIZE)${NC}"
        done
    else
        print_success "Aucun fichier > 10MB trouvé"
    fi
    
    # Vérifier les fichiers .pyc et cache
    PYC_COUNT=$(find . -name "*.pyc" -type f | wc -l)
    if [ "$PYC_COUNT" -gt 0 ]; then
        print_warning "$PYC_COUNT fichier(s) .pyc trouvé(s)"
    else
        print_success "Aucun fichier .pyc trouvé"
    fi
    
    # Vérifier la taille totale du projet
    TOTAL_SIZE=$(du -sh . 2>/dev/null | cut -f1)
    print_info "Taille totale du projet: $TOTAL_SIZE"
    
    # Recommandations
    if [ -f "db.sqlite3" ]; then
        DB_SIZE=$(du -h db.sqlite3 | cut -f1)
        print_info "Base SQLite: $DB_SIZE"
        
        if [[ "$DB_SIZE" =~ G ]]; then
            print_warning "Base SQLite > 1GB - Pensez à PostgreSQL en production"
        fi
    fi
}

# ==================== VÉRIFICATIONS DÉPLOIEMENT ====================
check_deployment() {
    print_header "VÉRIFICATION DÉPLOIEMENT"
    
    # Vérifier les fichiers de déploiement
    DEPLOYMENT_FILES=(
        "Dockerfile"
        "docker-compose.yml"
        "render.yaml"
        "Procfile"
        "gunicorn.conf.py"
    )
    
    for file in "${DEPLOYMENT_FILES[@]}"; do
        if [ -f "$file" ]; then
            print_success "$file présent"
        else
            print_info "$file manquant (optionnel)"
        fi
    done
    
    # Vérifier Gunicorn
    if grep -q "gunicorn" requirements.txt 2>/dev/null || \
       python3 -c "import gunicorn" 2>/dev/null; then
        print_success "Gunicorn installé"
    else
        print_warning "Gunicorn non installé (nécessaire pour production)"
    fi
    
    # Vérifier configuration Gunicorn
    if [ -f "gunicorn.conf.py" ]; then
        print_success "Configuration Gunicorn présente"
    else
        print_info "Pas de configuration Gunicorn spécifique"
    fi
    
    # Vérifier les variables d'environnement
    print_info "Variables d'environnement requises:"
    REQUIRED_ENV_VARS=(
        "DJANGO_SETTINGS_MODULE"
        "SECRET_KEY"
        "DATABASE_URL"
        "ALLOWED_HOSTS"
    )
    
    for var in "${REQUIRED_ENV_VARS[@]}"; do
        if [ -n "${!var:-}" ]; then
            print_success "$var définie"
        else
            if [ "$var" = "SECRET_KEY" ]; then
                print_error "$var non définie (CRITIQUE)"
            else
                print_warning "$var non définie"
            fi
        fi
    done
    
    # Vérifier .env
    if [ -f ".env" ] || [ -f ".env.example" ]; then
        print_success "Fichier .env ou .env.example présent"
    else
        print_warning "Aucun fichier .env trouvé"
    fi
}

# ==================== RAPPORT FINAL ====================
generate_report() {
    print_header "RAPPORT FINAL"
    
    echo -e "\n${GREEN}══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  📊 RÉSUMÉ DES VÉRIFICATIONS${NC}"
    echo -e "${GREEN}══════════════════════════════════════════════════════════════${NC}"
    
    echo -e "\n${CYAN}Statistiques:${NC}"
    echo -e "  ${GREEN}✅ $PASSED_CHECKS vérification(s) réussie(s)${NC}"
    echo -e "  ${YELLOW}⚠️  $WARNINGS avertissement(s)${NC}"
    echo -e "  ${RED}❌ $FAILED_CHECKS erreur(s)${NC}"
    echo -e "  ${BLUE}📋 $TOTAL_CHECKS vérification(s) totale(s)${NC}"
    
    # Calculer le score
    if [ "$TOTAL_CHECKS" -gt 0 ]; then
        SCORE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))
    else
        SCORE=0
    fi
    
    echo -e "\n${CYAN}Score: $SCORE/100${NC}"
    
    # Afficher le niveau de préparation
    if [ "$SCORE" -ge 90 ] && [ "$FAILED_CHECKS" -eq 0 ]; then
        echo -e "\n${GREEN}🎉 EXCELLENT - Prêt pour la production!${NC}"
        STATUS=$SUCCESS
    elif [ "$SCORE" -ge 70 ] && [ "$FAILED_CHECKS" -le 2 ]; then
        echo -e "\n${YELLOW}👍 BON - Presque prêt, vérifiez les avertissements${NC}"
        STATUS=$WARNING
    elif [ "$SCORE" -ge 50 ]; then
        echo -e "\n${YELLOW}⚠️  MOYEN - Des corrections sont nécessaires${NC}"
        STATUS=$WARNING
    else
        echo -e "\n${RED}🚨 CRITIQUE - Le projet n'est pas prêt pour la production${NC}"
        STATUS=$ERROR
    fi
    
    # Recommandations
    echo -e "\n${CYAN}🔧 Recommandations:${NC}"
    
    if [ "$FAILED_CHECKS" -gt 0 ]; then
        echo -e "  ${RED}• Corriger les $FAILED_CHECKS erreur(s) ci-dessus${NC}"
    fi
    
    if [ "$WARNINGS" -gt 0 ]; then
        echo -e "  ${YELLOW}• Examiner les $WARNINGS avertissement(s)${NC}"
    fi
    
    if [ ! -f "mutuelle_core/settings_production.py" ]; then
        echo -e "  ${YELLOW}• Créer mutuelle_core/settings_production.py${NC}"
    fi
    
    if [ ! -f "requirements.txt" ]; then
        echo -e "  ${RED}• Créer requirements.txt${NC}"
    fi
    
    # Prochaines étapes
    echo -e "\n${CYAN}📋 Prochaines étapes:${NC}"
    echo -e "  1. python manage.py check --deploy"
    echo -e "  2. python manage.py migrate"
    echo -e "  3. python manage.py collectstatic"
    echo -e "  4. gunicorn mutuelle_core.wsgi:application"
    
    # Générer un fichier de rapport
    REPORT_FILE="verification_report_$(date +%Y%m%d_%H%M%S).txt"
    {
        echo "Rapport de vérification Django - $(date)"
        echo "=========================================="
        echo "Score: $SCORE/100"
        echo "Succès: $PASSED_CHECKS"
        echo "Avertissements: $WARNINGS"
        echo "Erreurs: $FAILED_CHECKS"
        echo ""
        echo "Projet: $(pwd)"
        echo "Python: $(python3 --version 2>/dev/null || echo 'N/A')"
        echo "Django: $(python3 -c 'import django; print(django.__version__)' 2>/dev/null || echo 'N/A')"
        echo ""
    } > "$REPORT_FILE"
    
    echo -e "\n${BLUE}📄 Rapport détaillé sauvegardé dans: $REPORT_FILE${NC}"
    
    return $STATUS
}

# ==================== FONCTION PRINCIPALE ====================
main() {
    echo -e "${MAGENTA}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                 VÉRIFICATEUR DJANGO PRO                      ║"
    echo "║                 Version 2.0 - Production Ready               ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    # Date et heure
    echo -e "${CYAN}Date: $(date)${NC}"
    echo -e "${CYAN}Répertoire: $(pwd)${NC}"
    echo ""
    
    # Exécuter toutes les vérifications
    check_system
    check_django_project
    check_dependencies
    check_database
    check_security
    check_static_files
    check_urls
    check_performance
    check_deployment
    
    # Générer le rapport final
    generate_report
    
    return $?
}

# Exécuter le script principal
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
    EXIT_CODE=$?
    
    echo -e "\n${BLUE}══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  🏁 Vérification terminée avec le code: $EXIT_CODE${NC}"
    echo -e "${BLUE}══════════════════════════════════════════════════════════════${NC}"
    
    exit $EXIT_CODE
fi