#!/bin/bash
# analyse_pharmacien.sh

echo "🔍 ANALYSE COMPLÈTE DE L'APPLICATION PHARMACIEN"
echo "================================================"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour vérifier l'existence des fichiers
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅ $1${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 - FICHIER MANQUANT${NC}"
        return 1
    fi
}

# Fonction pour vérifier l'existence des répertoires
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✅ $1${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 - RÉPERTOIRE MANQUANT${NC}"
        return 1
    fi
}

echo -e "\n${BLUE}1. VÉRIFICATION DE LA STRUCTURE DES FICHIERS${NC}"
echo "------------------------------------------------"

check_file "pharmacien/__init__.py"
check_file "pharmacien/admin.py"
check_file "pharmacien/apps.py"
check_file "pharmacien/models.py"
check_file "pharmacien/views.py"
check_file "pharmacien/urls.py"
check_file "pharmacien/forms.py"
check_dir "templates/pharmacien"

echo -e "\n${BLUE}2. ANALYSE DU FICHIER URLs${NC}"
echo "----------------------------------"

if check_file "pharmacien/urls.py"; then
    echo -e "\nContenu de pharmacien/urls.py:"
    echo "-------------------------------"
    cat pharmacien/urls.py
    
    # Extraction des noms d'URLs définis
    echo -e "\n${YELLOW}URLs définies dans pharmacien/urls.py:${NC}"
    grep -E "path\(.*name=" pharmacien/urls.py | sed 's/.*name=//g' | sed "s/['\"]//g" | sed 's/).*//g' | while read url_name; do
        echo -e "  ${GREEN}✓${NC} $url_name"
    done
    
    # Vérification du namespace
    if grep -q "app_name.*pharmacien" pharmacien/urls.py; then
        echo -e "\n${GREEN}✅ Namespace 'pharmacien' trouvé${NC}"
    else
        echo -e "\n${RED}❌ Namespace 'pharmacien' non trouvé${NC}"
    fi
fi

echo -e "\n${BLUE}3. ANALYSE DES VUES${NC}"
echo "------------------------"

if check_file "pharmacien/views.py"; then
    # Vérification des fonctions de vue
    echo -e "\n${YELLOW}Fonctions de vue trouvées:${NC}"
    grep -E "^def " pharmacien/views.py | sed 's/def //' | sed 's/.*//' | while read view_func; do
        echo -e "  ${GREEN}✓${NC} $view_func"
    done
    
    # Vérification spécifique de dashboard_pharmacien
    if grep -q "def dashboard_pharmacien" pharmacien/views.py; then
        echo -e "\n${GREEN}✅ Vue dashboard_pharmacien trouvée${NC}"
    else
        echo -e "\n${RED}❌ Vue dashboard_pharmacien NON TROUVÉE${NC}"
    fi
fi

echo -e "\n${BLUE}4. ANALYSE DES TEMPLATES${NC}"
echo "----------------------------"

if check_dir "templates/pharmacien"; then
    echo -e "\n${YELLOW}Templates trouvés:${NC}"
    find templates/pharmacien -name "*.html" | while read template; do
        echo -e "  ${GREEN}✓${NC} $template"
    done
    
    # Analyse des références d'URL dans les templates
    echo -e "\n${YELLOW}Références d'URL dans les templates:${NC}"
    find templates/pharmacien -name "*.html" -exec grep -H "{% url" {} \; | while read line; do
        template=$(echo "$line" | cut -d: -f1)
        url_ref=$(echo "$line" | sed 's/.*{% url //' | sed "s/['\"]//g" | sed 's/.*://' | sed 's/ .*//')
        echo -e "  ${BLUE}$template${NC} → $url_ref"
    done
    
    # Vérification spécifique du template dashboard
    if [ -f "templates/pharmacien/dashboard.html" ]; then
        echo -e "\n${GREEN}✅ Template dashboard.html trouvé${NC}"
    else
        echo -e "\n${YELLOW}⚠️  Template dashboard.html non trouvé${NC}"
    fi
fi

echo -e "\n${BLUE}5. VÉRIFICATION DES INCLUSIONS D'URLS${NC}"
echo "------------------------------------------"

# Vérifier si pharmacien est inclus dans les URLs principales
if check_file "projet/urls.py"; then
    echo -e "\n${YELLOW}Inclusion dans projet/urls.py:${NC}"
    if grep -q "include.*pharmacien" projet/urls.py; then
        echo -e "  ${GREEN}✅ Application pharmacien incluse${NC}"
        grep "include.*pharmacien" projet/urls.py
    else
        echo -e "  ${RED}❌ Application pharmacien NON INCLUSE${NC}"
    fi
fi

echo -e "\n${BLUE}6. TEST DE RÉSOLUTION DES URLs${NC}"
echo "----------------------------------"

# Création d'un script Python pour tester les URLs
cat > /tmp/test_urls_pharmacien.py << 'EOF'
import os
import sys
import django
from django.urls import reverse, NoReverseMatch

# Configuration de l'environnement Django
sys.path.append(os.path.dirname(os.path.abspath('.')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
django.setup()

# URLs à tester
urls_to_test = [
    'pharmacien:dashboard',
    'pharmacien:liste_ordonnances',
    'pharmacien:recherche_ordonnances', 
    'pharmacien:historique_validation',
    'pharmacien:detail_ordonnance',
    'pharmacien:valider_ordonnance',
    'pharmacien:rejeter_ordonnance',
    'pharmacien:api_statistiques',
]

print("🔧 Test de résolution des URLs:")
print("=" * 50)

for url_name in urls_to_test:
    try:
        url = reverse(url_name)
        print(f"✅ {url_name:35} -> {url}")
    except NoReverseMatch as e:
        print(f"❌ {url_name:35} -> NON TROUVÉE")
        print(f"   Message: {e}")

# Test des URLs avec paramètres
print("\n🔧 Test des URLs avec paramètres:")
print("=" * 40)

param_urls = [
    ('pharmacien:detail_ordonnance', {'ordonnance_id': 1}),
    ('pharmacien:valider_ordonnance', {'ordonnance_id': 1}),
    ('pharmacien:rejeter_ordonnance', {'ordonnance_id': 1}),
]

for url_name, kwargs in param_urls:
    try:
        url = reverse(url_name, kwargs=kwargs)
        print(f"✅ {url_name:35} -> {url}")
    except NoReverseMatch as e:
        print(f"❌ {url_name:35} -> NON TROUVÉE")
        print(f"   Message: {e}")
EOF

# Exécution du test
python /tmp/test_urls_pharmacien.py

echo -e "\n${BLUE}7. VÉRIFICATION DES MODÈLES${NC}"
echo "----------------------------"

if check_file "pharmacien/models.py"; then
    echo -e "\n${YELLOW}Modèles définis:${NC}"
    grep -E "^class " pharmacien/models.py | sed 's/class //' | sed 's/.*//' | while read model; do
        echo -e "  ${GREEN}✓${NC} $model"
    done
fi

echo -e "\n${BLUE}8. VÉRIFICATION DES FORMULAIRES${NC}"
echo "-------------------------------"

if check_file "pharmacien/forms.py"; then
    echo -e "\n${YELLOW}Formulaires définis:${NC}"
    grep -E "^class " pharmacien/forms.py | sed 's/class //' | sed 's/.*//' | while read form; do
        echo -e "  ${GREEN}✓${NC} $form"
    done
fi

echo -e "\n${BLUE}9. RÉCAPITULATIF DES PROBLÈMES${NC}"
echo "--------------------------------"

# Vérifications critiques
ERRORS=0

echo -e "\nVérifications critiques:"
echo "------------------------"

# Vérifier l'existence de urls.py
if [ ! -f "pharmacien/urls.py" ]; then
    echo -e "${RED}❌ CRITIQUE: pharmacien/urls.py manquant${NC}"
    ERRORS=$((ERRORS+1))
fi

# Vérifier l'inclusion dans les URLs principales
if ! grep -q "include.*pharmacien" projet/urls.py 2>/dev/null; then
    echo -e "${RED}❌ CRITIQUE: Application non incluse dans projet/urls.py${NC}"
    ERRORS=$((ERRORS+1))
fi

# Vérifier la vue dashboard
if ! grep -q "def dashboard_pharmacien" pharmacien/views.py 2>/dev/null; then
    echo -e "${RED}❌ CRITIQUE: Vue dashboard_pharmacien manquante${NC}"
    ERRORS=$((ERRORS+1))
fi

# Vérifier le namespace
if [ -f "pharmacien/urls.py" ] && ! grep -q "app_name.*pharmacien" pharmacien/urls.py; then
    echo -e "${YELLOW}⚠️  ATTENTION: Namespace non défini dans pharmacien/urls.py${NC}"
fi

# Vérifier le template dashboard
if [ ! -f "templates/pharmacien/dashboard.html" ]; then
    echo -e "${YELLOW}⚠️  ATTENTION: Template dashboard.html manquant${NC}"
fi

if [ $ERRORS -eq 0 ]; then
    echo -e "\n${GREEN}✅ Aucune erreur critique détectée${NC}"
else
    echo -e "\n${RED}❌ $ERRORS erreur(s) critique(s) détectée(s)${NC}"
fi

echo -e "\n${BLUE}10. RECOMMANDATIONS${NC}"
echo "---------------------"

if [ ! -f "pharmacien/urls.py" ]; then
    echo -e "${YELLOW}📋 Créer le fichier pharmacien/urls.py${NC}"
    cat > pharmacien/urls.py << 'EOF'
from django.urls import path
from . import views

app_name = 'pharmacien'

urlpatterns = [
    path('dashboard/', views.dashboard_pharmacien, name='dashboard'),
    path('ordonnances/', views.liste_ordonnances, name='liste_ordonnances'),
    path('recherche/', views.recherche_ordonnances, name='recherche_ordonnances'),
    path('historique/', views.historique_validation, name='historique_validation'),
    path('ordonnances/<int:ordonnance_id>/', views.detail_ordonnance, name='detail_ordonnance'),
    path('ordonnances/<int:ordonnance_id>/valider/', views.valider_ordonnance, name='valider_ordonnance'),
    path('ordonnances/<int:ordonnance_id>/rejeter/', views.rejeter_ordonnance, name='rejeter_ordonnance'),
    path('api/statistiques/', views.api_statistiques, name='api_statistiques'),
]
EOF
    echo -e "${GREEN}✅ Fichier pharmacien/urls.py créé${NC}"
fi

if ! grep -q "def dashboard_pharmacien" pharmacien/views.py 2>/dev/null; then
    echo -e "${YELLOW}📋 Ajouter la vue dashboard_pharmacien dans views.py${NC}"
    cat >> pharmacien/views.py << 'EOF'

@login_required
def dashboard_pharmacien(request):
    """Tableau de bord du pharmacien"""
    context = {
        'page_title': 'Tableau de bord Pharmacien',
        'active_tab': 'dashboard'
    }
    return render(request, 'pharmacien/dashboard.html', context)
EOF
    echo -e "${GREEN}✅ Vue dashboard_pharmacien ajoutée${NC}"
fi

if ! grep -q "include.*pharmacien" projet/urls.py 2>/dev/null; then
    echo -e "${YELLOW}📋 Ajouter l'inclusion dans projet/urls.py${NC}"
    echo -e "${BLUE}Ajoutez cette ligne dans projet/urls.py:${NC}"
    echo -e "path('pharmacien/', include('pharmacien.urls', namespace='pharmacien')),"
fi

echo -e "\n${GREEN}🎯 ANALYSE TERMINÉE${NC}"
echo "======================"

# Nettoyage
rm -f /tmp/test_urls_pharmacien.py