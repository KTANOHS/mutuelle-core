#!/bin/bash
# analyse_et_corrige_templates_pharmacien_fixed.sh

echo "🔍 ANALYSE ET CORRECTION DES TEMPLATES PHARMACIEN"
echo "=================================================="

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Répertoire des templates
TEMPLATES_DIR="templates/pharmacien"

echo -e "\n${BLUE}1. ANALYSE DES TEMPLATES${NC}"
echo "------------------------"

# Fonction pour analyser un template
analyze_template() {
    local template_file="$1"
    echo -e "\n${YELLOW}📄 Analyse de: $template_file${NC}"
    
    if [[ ! -f "$template_file" ]]; then
        echo -e "  ${RED}❌ Fichier non trouvé${NC}"
        return
    fi
    
    # Extraire toutes les références d'URL
    local url_references=$(grep -n "{% url" "$template_file" 2>/dev/null || true)
    
    if [[ -z "$url_references" ]]; then
        echo -e "  ${GREEN}✅ Aucune référence d'URL trouvée${NC}"
        return
    fi
    
    local has_errors=0
    
    while IFS= read -r line; do
        # Extraire le nom de l'URL
        local url_name=$(echo "$line" | sed -n "s/.*{% url ['\"]\([^'\"]*\)['\"].*/\1/p")
        
        if [[ -n "$url_name" ]]; then
            # Vérifier les URLs problématiques connues
            case "$url_name" in
                "pharmacien:dashboard"|"pharmacien:liste_ordonnances"|"pharmacien:recherche_ordonnances"|"pharmacien:profil"|"pharmacien:stock")
                    echo -e "  ${RED}❌ $line - URL NON DISPONIBLE${NC}"
                    has_errors=1
                    ;;
                "home"|"logout"|"pharmacien:export_stock"|"pharmacien:ajouter_stock"|"pharmacien:importer_stock")
                    echo -e "  ${RED}❌ $line - URL NON DISPONIBLE${NC}"
                    has_errors=1
                    ;;
                *)
                    echo -e "  ${GREEN}✅ $line${NC}"
                    ;;
            esac
        fi
    done <<< "$url_references"
    
    return $has_errors
}

# Analyser tous les templates
for template in "$TEMPLATES_DIR"/*.html; do
    if [[ -f "$template" ]]; then
        analyze_template "$template"
    fi
done

echo -e "\n${BLUE}2. CORRECTION AUTOMATIQUE DES TEMPLATES${NC}"
echo "=========================================="

# Fonction pour corriger un template
correct_template() {
    local template_file="$1"
    local backup_file="${template_file}.backup.$(date +%Y%m%d_%H%M%S)"
    
    echo -e "\n${BLUE}🔧 Correction de: $template_file${NC}"
    
    # Créer une sauvegarde
    cp "$template_file" "$backup_file"
    echo -e "  ${GREEN}✅ Sauvegarde créée: $backup_file${NC}"
    
    local corrections_made=0
    
    # Appliquer les corrections une par une
    if grep -q "{% url .pharmacien:dashboard. %}" "$template_file"; then
        sed -i '' 's/{% url .pharmacien:dashboard. %}/{% url "pharmacien:dashboard_pharmacien" %}/g' "$template_file"
        echo -e "  ${GREEN}✅ Corrigé: pharmacien:dashboard → pharmacien:dashboard_pharmacien${NC}"
        corrections_made=$((corrections_made + 1))
    fi
    
    if grep -q "{% url .pharmacien:liste_ordonnances. %}" "$template_file"; then
        sed -i '' 's/{% url .pharmacien:liste_ordonnances. %}/{% url "pharmacien:liste_ordonnances_attente" %}/g' "$template_file"
        echo -e "  ${GREEN}✅ Corrigé: pharmacien:liste_ordonnances → pharmacien:liste_ordonnances_attente${NC}"
        corrections_made=$((corrections_made + 1))
    fi
    
    if grep -q "{% url .pharmacien:recherche_ordonnances. %}" "$template_file"; then
        sed -i '' 's/{% url .pharmacien:recherche_ordonnances. %}/{% url "pharmacien:rechercher_ordonnances" %}/g' "$template_file"
        echo -e "  ${GREEN}✅ Corrigé: pharmacien:recherche_ordonnances → pharmacien:rechercher_ordonnances${NC}"
        corrections_made=$((corrections_made + 1))
    fi
    
    if grep -q "{% url .pharmacien:profil. %}" "$template_file"; then
        sed -i '' 's/{% url .pharmacien:profil. %}/{% url "pharmacien:profil_pharmacien" %}/g' "$template_file"
        echo -e "  ${GREEN}✅ Corrigé: pharmacien:profil → pharmacien:profil_pharmacien${NC}"
        corrections_made=$((corrections_made + 1))
    fi
    
    # Commenter les URLs qui n'existent pas
    if grep -q "{% url .pharmacien:stock. %}" "$template_file"; then
        sed -i '' 's/{% url .pharmacien:stock. %}/{% comment %}URL non disponible: pharmacien:stock{% endcomment %}#/g' "$template_file"
        echo -e "  ${YELLOW}⚠️  Commenté: pharmacien:stock (URL non disponible)${NC}"
        corrections_made=$((corrections_made + 1))
    fi
    
    if [[ $corrections_made -eq 0 ]]; then
        echo -e "  ${GREEN}✅ Aucune correction nécessaire${NC}"
    else
        echo -e "  ${GREEN}✅ Total corrections: $corrections_made${NC}"
    fi
}

# Corriger les templates problématiques identifiés
problem_templates=(
    "templates/pharmacien/_sidebar_pharmacien.html"
    "templates/pharmacien/_sidebar_pharmacien_updated.html"
    "templates/pharmacien/_navbar_pharmacien.html"
    "templates/pharmacien/stock.html"
)

for template in "${problem_templates[@]}"; do
    if [[ -f "$template" ]]; then
        correct_template "$template"
    fi
done

echo -e "\n${BLUE}3. VÉRIFICATION FINALE${NC}"
echo "====================="

# Vérification finale
for template in "${problem_templates[@]}"; do
    if [[ -f "$template" ]]; then
        echo -e "\n${YELLOW}📄 Vérification finale: $template${NC}"
        analyze_template "$template"
    fi
done

echo -e "\n${GREEN}✨ CORRECTIONS TERMINÉES${NC}"
echo "========================"

# Créer un script pour les URLs manquantes
cat > ajouter_urls_manquantes.py << 'EOF'
"""
Script pour ajouter les URLs manquantes dans pharmacien/urls.py
"""
import os

urls_manquantes = [
    "path('stock/', views.gestion_stock, name='stock'),",
    "path('export-stock/', views.export_stock, name='export_stock'),",
    "path('ajouter-stock/', views.ajouter_stock, name='ajouter_stock'),", 
    "path('importer-stock/', views.importer_stock, name='importer_stock'),",
    "path('home/', views.home, name='home'),",
    "path('logout/', views.logout_view, name='logout'),",
]

print("📋 URLs manquantes à ajouter dans pharmacien/urls.py:")
print("=" * 50)
for url in urls_manquantes:
    print(url)

print("\n💡 Pour ajouter ces URLs, éditez pharmacien/urls.py et ajoutez:")
print("   from . import views")
print("   Puis ajoutez les paths ci-dessus dans urlpatterns")
EOF

echo -e "\n${YELLOW}📋 URLs manquantes détectées:${NC}"
python3 ajouter_urls_manquantes.py

# Nettoyer
rm -f ajouter_urls_manquantes.py

echo -e "\n${GREEN}🎯 RÉSUMÉ DES ACTIONS:${NC}"
echo "-----------------------"
echo "✅ Templates corrigés:"
echo "   - _sidebar_pharmacien.html"
echo "   - _sidebar_pharmacien_updated.html" 
echo "   - _navbar_pharmacien.html"
echo "   - stock.html"
echo ""
echo "⚠️  URLs à implémenter:"
echo "   - pharmacien:stock"
echo "   - pharmacien:export_stock"
echo "   - pharmacien:ajouter_stock"
echo "   - pharmacien:importer_stock"
echo "   - home"
echo "   - logout"
echo ""
echo "🔧 Prochaine étape: Redémarrez le serveur et testez:"
echo "   python manage.py runserver"