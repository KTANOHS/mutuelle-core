#!/bin/bash
# Script: diagnostic_render.sh
# Description: Diagnostic complet pour configuration Django sur Render.com
# Usage: chmod +x diagnostic_render.sh && ./diagnostic_render.sh

echo "=============================================="
echo "  DIAGNOSTIC POUR DÉPLOIEMENT RENDER.COM"
echo "=============================================="
echo "Date: $(date)"
echo ""

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les résultats
success() {
    echo -e "${GREEN}✓ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

error() {
    echo -e "${RED}✗ $1${NC}"
}

info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Vérification 1: Version de Python
echo "1. VÉRIFICATION DE L'ENVIRONNEMENT PYTHON"
echo "----------------------------------------"
python_version=$(python3 --version 2>/dev/null || python --version)
if [[ $? -eq 0 ]]; then
    success "Python détecté: $python_version"
    
    # Vérifier la version
    if [[ $python_version =~ "3.8"|"3.9"|"3.10"|"3.11"|"3.12" ]]; then
        success "Version de Python compatible avec Render"
    else
        warning "Version de Python potentiellement incompatible"
    fi
else
    error "Python non trouvé"
fi

echo ""

# Vérification 2: Fichiers critiques Django
echo "2. VÉRIFICATION DES FICHIERS DJANGO"
echo "-----------------------------------"

critical_files=(
    "manage.py"
    "requirements.txt"
    "runtime.txt"
    "build.sh"
    "render.yaml"
    "Procfile"
    "wsgi.py"
    "gunicorn.conf.py"
)

for file in "${critical_files[@]}"; do
    if [[ -f "$file" ]]; then
        success "$file - Présent"
        
        # Vérifications spécifiques
        case "$file" in
            "requirements.txt")
                if grep -q "Django\|django" "$file"; then
                    success "  → Django présent dans requirements.txt"
                else
                    error "  → Django manquant dans requirements.txt"
                fi
                
                if grep -q "gunicorn" "$file"; then
                    success "  → Gunicorn présent dans requirements.txt"
                else
                    error "  → Gunicorn manquant dans requirements.txt"
                fi
                
                if grep -q "psycopg2\|psycopg2-binary" "$file"; then
                    success "  → psycopg2 présent (PostgreSQL)"
                else
                    warning "  → psycopg2 manquant (nécessaire pour PostgreSQL)"
                fi
                ;;
                
            "runtime.txt")
                content=$(cat "$file")
                if [[ $content =~ "python-3" ]]; then
                    success "  → Version spécifiée: $content"
                else
                    warning "  → Version potentiellement incorrecte: $content"
                fi
                ;;
                
            "Procfile")
                if grep -q "web:" "$file"; then
                    success "  → Entrée 'web' présente"
                    web_cmd=$(grep "web:" "$file")
                    info "  → Commande web: ${web_cmd#web: }"
                else
                    error "  → Entrée 'web' manquante dans Procfile"
                fi
                ;;
                
            "render.yaml")
                if grep -q "service:" "$file"; then
                    success "  → Configuration Render détectée"
                fi
                ;;
        esac
    else
        if [[ "$file" == "Procfile" || "$file" == "requirements.txt" ]]; then
            error "$file - MANQUANT (CRITIQUE)"
        else
            warning "$file - Non présent (optionnel)"
        fi
    fi
done

echo ""

# Vérification 3: Structure du projet
echo "3. STRUCTURE DU PROJET"
echo "----------------------"

# Vérifier la présence de settings.py
find_settings() {
    find . -name "settings.py" -type f | head -5
}

settings_files=$(find_settings)
if [[ -n "$settings_files" ]]; then
    success "Fichiers settings.py trouvés:"
    echo "$settings_files" | while read file; do
        info "  → $file"
    done
    
    # Vérifier le settings principal
    main_settings=$(find . -path "*/settings.py" -type f | grep -v "__pycache__" | head -1)
    if [[ -n "$main_settings" ]]; then
        echo ""
        info "Analyse de $main_settings"
        
        # Vérifications importantes
        if grep -q "DEBUG\s*=\s*True" "$main_settings"; then
            error "  → DEBUG est True (à désactiver en production)"
        else
            success "  → DEBUG n'est pas True"
        fi
        
        if grep -q "SECRET_KEY" "$main_settings"; then
            if grep -q "SECRET_KEY\s*=\s*['\"]django-insecure-" "$main_settings"; then
                error "  → SECRET_KEY auto-généré (insécurisé)"
            else
                success "  → SECRET_KEY configuré"
            fi
        fi
        
        if grep -q "ALLOWED_HOSTS" "$main_settings"; then
            if grep -q "\*" "$main_settings" | grep -v "#"; then
                warning "  → ALLOWED_HOSTS contient '*' (peu sécurisé)"
            else
                success "  → ALLOWED_HOSTS configuré"
            fi
        fi
        
        if grep -q "DATABASE_URL" "$main_settings" || grep -q "os.environ.get.*DATABASE_URL" "$main_settings"; then
            success "  → Utilise DATABASE_URL (compatible Render)"
        else
            error "  → Ne semble pas utiliser DATABASE_URL"
        fi
        
        if grep -q "STATIC_ROOT" "$main_settings"; then
            success "  → STATIC_ROOT configuré"
        else
            error "  → STATIC_ROOT non configuré"
        fi
    fi
else
    error "Aucun fichier settings.py trouvé"
fi

echo ""

# Vérification 4: Base de données
echo "4. CONFIGURATION BASE DE DONNÉES"
echo "--------------------------------"

# Vérifier les variables d'environnement
echo "Variables d'environnement DATABASE:"
if [[ -n "$DATABASE_URL" ]]; then
    success "  → DATABASE_URL est défini"
    
    # Analyser l'URL
    if [[ $DATABASE_URL == postgresql://* ]]; then
        success "  → Utilise PostgreSQL (recommandé pour Render)"
    elif [[ $DATABASE_URL == postgres://* ]]; then
        warning "  → Utilise 'postgres://' (devrait être 'postgresql://')"
    else
        warning "  → Autre type de base de données: ${DATABASE_URL%%://*}"
    fi
else
    warning "  → DATABASE_URL non défini (sera défini par Render)"
fi

# Vérifier les migrations
echo ""
info "Vérification des migrations:"
python manage.py showmigrations --list 2>/dev/null
if [[ $? -eq 0 ]]; then
    success "Commandes de migration fonctionnelles"
else
    error "Erreur avec les commandes de migration"
fi

echo ""

# Vérification 5: Fichiers statiques
echo "5. FICHIERS STATIQUES"
echo "---------------------"

python manage.py collectstatic --dry-run --noinput 2>&1 | tail -20
if [[ $? -eq 0 ]]; then
    success "collectstatic fonctionne"
    
    # Vérifier STATIC_ROOT
    python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
try:
    django.setup()
    from django.conf import settings
    print(f\"STATIC_ROOT: {settings.STATIC_ROOT}\")
    print(f\"STATIC_URL: {settings.STATIC_URL}\")
    if settings.STATIC_ROOT:
        if os.path.exists(settings.STATIC_ROOT):
            print(\"✓ STATIC_ROOT existe\")
        else:
            print(\"⚠ STATIC_ROOT n'existe pas encore\")
except Exception as e:
    print(f\"Erreur: {e}\")
" 2>/dev/null
else
    error "Problème avec collectstatic"
fi

echo ""

# Vérification 6: Gunicorn
echo "6. CONFIGURATION GUNICORN"
echo "-------------------------"

# Vérifier si gunicorn est installé
python -c "import gunicorn" 2>/dev/null
if [[ $? -eq 0 ]]; then
    success "Gunicorn est installé"
    
    # Vérifier la version
    gunicorn_version=$(python -c "import gunicorn; print(gunicorn.__version__)" 2>/dev/null)
    info "  → Version: $gunicorn_version"
else
    error "Gunicorn n'est pas installé"
fi

# Vérifier la configuration gunicorn
if [[ -f "gunicorn.conf.py" ]]; then
    success "Fichier de configuration gunicorn trouvé"
    echo "Contenu de gunicorn.conf.py:"
    head -20 gunicorn.conf.py
elif [[ -f "gunicorn_config.py" ]]; then
    success "Fichier de configuration gunicorn trouvé (gunicorn_config.py)"
else
    warning "Aucun fichier de configuration gunicorn spécifique trouvé"
fi

echo ""

# Vérification 7: Sécurité
echo "7. VÉRIFICATION DE SÉCURITÉ"
echo "---------------------------"

# Exécuter le check de déploiement Django
echo "Vérification sécurité Django:"
python manage.py check --deploy 2>&1 | grep -A 20 "System check identified"

echo ""

# Vérification 8: Dépendances
echo "8. DÉPENDANCES"
echo "--------------"

# Analyser requirements.txt
if [[ -f "requirements.txt" ]]; then
    info "Analyse de requirements.txt:"
    echo "Nombre de paquets: $(wc -l < requirements.txt)"
    
    # Vérifier les versions critiques
    critical_packages=("Django" "gunicorn" "psycopg2" "psycopg2-binary" "whitenoise" "dj-database-url")
    
    for pkg in "${critical_packages[@]}"; do
        if grep -i "^$pkg" requirements.txt || grep -i "==.*$pkg" requirements.txt; then
            success "  → $pkg présent"
        else
            if [[ "$pkg" == "whitenoise" ]]; then
                warning "  → $pkg manquant (recommandé pour les fichiers statiques)"
            elif [[ "$pkg" == "dj-database-url" ]]; then
                warning "  → $pkg manquant (utile pour DATABASE_URL)"
            else
                error "  → $pkg manquant"
            fi
        fi
    done
    
    # Vérifier les versions de Django
    django_version=$(grep -i "django" requirements.txt | head -1)
    if [[ $django_version =~ "==4" || $django_version =~ "==5" ]]; then
        success "  → Version Django compatible: $django_version"
    else
        warning "  → Version Django potentiellement obsolète"
    fi
fi

echo ""

# Vérification 9: Script de build Render
echo "9. SCRIPT DE BUILD RENDER"
echo "-------------------------"

if [[ -f "build.sh" ]]; then
    success "build.sh présent"
    echo "Contenu de build.sh:"
    cat build.sh
else
    warning "build.sh manquant (optionnel mais recommandé)"
    info "Créer un fichier build.sh avec:"
    cat << 'EOF'
#!/usr/bin/env bash
# build.sh - Script de build pour Render

# Sortir en cas d'erreur
set -o errexit

# Installer les dépendances
pip install -r requirements.txt

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Appliquer les migrations
python manage.py migrate
EOF
fi

echo ""

# Vérification 10: Test de démarrage
echo "10. TEST DE DÉMARRAGE"
echo "---------------------"

info "Test de démarrage rapide:"
timeout 10 python manage.py check 2>&1
if [[ $? -eq 0 ]]; then
    success "Le projet peut être chargé par Django"
else
    error "Erreur lors du chargement du projet"
fi

echo ""

# Vérification 11: Ports et networking
echo "11. CONFIGURATION RÉSEAU"
echo "------------------------"

# Vérifier le port dans les configurations
info "Ports utilisés:"
grep -r "8000\|8080\|$PORT" . --include="*.py" --include="*.sh" --include="Procfile" --include="*.yaml" 2>/dev/null | head -5

if [[ -n "$PORT" ]]; then
    success "Variable PORT définie: $PORT"
else
    warning "Variable PORT non définie (Render définira PORT automatiquement)"
fi

echo ""

# Résumé
echo "=============================================="
echo "  RÉSUMÉ DU DIAGNOSTIC"
echo "=============================================="

# Compter les succès, avertissements, erreurs
total_success=$(grep -c "✓" <<< "$(cat $0)")
total_warnings=$(grep -c "⚠" <<< "$(cat $0)")
total_errors=$(grep -c "✗" <<< "$(cat $0)")

echo "Succès: $total_success | Avertissements: $total_warnings | Erreurs: $total_errors"
echo ""

# Recommandations finales
info "RECOMMANDATIONS POUR RENDER:"
echo "1. Assurez-vous que DEBUG=False en production"
echo "2. Utilisez une SECRET_KEY forte et sécurisée"
echo "3. Configurez ALLOWED_HOSTS avec votre domaine Render"
echo "4. Utilisez DATABASE_URL pour la connexion PostgreSQL"
echo "5. Ajoutez whitenoise pour servir les fichiers statiques"
echo "6. Configurez les variables d'environnement dans le dashboard Render:"
echo "   - DATABASE_URL"
echo "   - SECRET_KEY"
echo "   - DJANGO_ENV=production"
echo "7. Utilisez le plan gratuit PostgreSQL de Render"
echo ""

info "Fichier render.yaml recommandé:"
cat << 'EOF'
services:
  - type: web
    name: votre-app-django
    env: python
    buildCommand: "./build.sh"
    startCommand: "gunicorn mutuelle_core.wsgi:application"
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: votre-bdd
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: DJANGO_ENV
        value: production
      - key: PYTHON_VERSION
        value: 3.11.0

databases:
  - name: votre-bdd
    plan: free
EOF

echo ""
info "Pour tester localement avec les mêmes conditions que Render:"
echo "1. Créez un fichier .env.production avec vos variables"
echo "2. Exécutez: export \$(cat .env.production | xargs) && python manage.py runserver"
echo "3. Ou utilisez: python manage.py runserver --settings=mutuelle_core.settings.production"