#!/bin/bash
# analyse_et_corrige_templates_pharmacien.sh

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

# Mapping des corrections d'URLs
declare -A URL_CORRECTIONS=(
    ["pharmacien:dashboard"]="pharmacien:dashboard_pharmacien"
    ["pharmacien:liste_ordonnances"]="pharmacien:liste_ordonnances_attente"
    ["pharmacien:recherche_ordonnances"]="pharmacien:rechercher_ordonnances"
    ["pharmacien:profil"]="pharmacien:profil_pharmacien"
    ["pharmacien:stock"]="pharmacien:stock"  # À commenter si n'existe pas
)

# URLs disponibles (d'après votre urls.py)
AVAILABLE_URLS=(
    "pharmacien:dashboard_pharmacien"
    "pharmacien:liste_ordonnances_attente"
    "pharmacien:detail_ordonnance"
    "pharmacien:valider_ordonnance"
    "pharmacien:refuser_ordonnance"
    "pharmacien:historique_validation"
    "pharmacien:rechercher_ordonnances"
    "pharmacien:filtrer_ordonnances"
    "pharmacien:profil_pharmacien"
    "pharmacien:export_historique"
    "pharmacien:api_ordonnances_attente"
    "pharmacien:api_statistiques_temps_reel"
    "pharmacien:api_statistiques_pharmacien"
    "pharmacien:tableau_de_bord"
    "pharmacien:historique_validations"
    "pharmacien:ordonnances"
    "pharmacien:servir_ordonnance"
)

echo -e "\n${BLUE}1. ANALYSE DES TEMPLATES${NC}"
echo "------------------------"

# Fonction pour vérifier si une URL est disponible
check_url_available() {
    local url_name="$1"
    for available_url in "${AVAILABLE_URLS[@]}"; do
        if [[ "$available_url" == "$url_name" ]]; then
            return 0
        fi
    done
    return 1
}

# Fonction pour extraire les URLs d'un template
analyze_template() {
    local template_file="$1"
    echo -e "\n${YELLOW}📄 Analyse de: $template_file${NC}"
    
    if [[ ! -f "$template_file" ]]; then
        echo -e "  ${RED}❌ Fichier non trouvé${NC}"
        return
    fi
    
    # Extraire toutes les références d'URL
    local url_references=$(grep -o "{% url ['\"][^'\"]*['\"] %}" "$template_file" 2>/dev/null || true)
    
    if [[ -z "$url_references" ]]; then
        echo -e "  ${GREEN}✅ Aucune référence d'URL trouvée${NC}"
        return
    fi
    
    local has_errors=0
    local line_number=0
    
    while IFS= read -r line; do
        line_number=$((line_number + 1))
        # Extraire le nom de l'URL
        local url_name=$(echo "$line" | sed -n "s/.*{% url ['\"]\([^'\"]*\)['\"].*/\1/p")
        
        if [[ -n "$url_name" ]]; then
            # Vérifier si l'URL existe
            if check_url_available "$url_name"; then
                echo -e "  ${GREEN}✅ Ligne $line_number: $url_name${NC}"
            else
                echo -e "  ${RED}❌ Ligne $line_number: $url_name - URL NON DISPONIBLE${NC}"
                has_errors=1
            fi
        fi
    done <<< "$url_references"
    
    return $has_errors
}

# Fonction pour corriger un template
correct_template() {
    local template_file="$1"
    local backup_file="${template_file}.backup.$(date +%Y%m%d_%H%M%S)"
    
    echo -e "\n${BLUE}🔧 Correction de: $template_file${NC}"
    
    # Créer une sauvegarde
    cp "$template_file" "$backup_file"
    echo -e "  ${GREEN}✅ Sauvegarde créée: $backup_file${NC}"
    
    local corrections_made=0
    
    # Appliquer les corrections
    for wrong_url in "${!URL_CORRECTIONS[@]}"; do
        local correct_url="${URL_CORRECTIONS[$wrong_url]}"
        
        # Compter les occurrences avant correction
        local count_before=$(grep -c "$wrong_url" "$template_file" 2>/dev/null || true)
        
        if [[ $count_before -gt 0 ]]; then
            # Remplacer l'URL incorrecte par la correcte
            if sed -i '' "s/{% url ['\"]${wrong_url}['\"] %}/{% url \"${correct_url}\" %}/g" "$template_file" 2>/dev/null; then
                # Compter après correction
                local count_after=$(grep -c "$wrong_url" "$template_file" 2>/dev/null || true)
                local corrected_count=$((count_before - count_after))
                
                if [[ $corrected_count -gt 0 ]]; then
                    echo -e "  ${GREEN}✅ Corrigé: $wrong_url → $correct_url ($corrected_count occurrence(s))${NC}"
                    corrections_made=$((corrections_made + corrected_count))
                fi
            fi
        fi
    done
    
    # Gérer les URLs qui n'existent pas du tout
    local problematic_urls=$(grep -o "{% url ['\"][^'\"]*['\"] %}" "$template_file" | sed -n "s/.*{% url ['\"]\([^'\"]*\)['\"].*/\1/p" | while read url; do
        if ! check_url_available "$url"; then
            echo "$url"
        fi
    done | sort -u)
    
    if [[ -n "$problematic_urls" ]]; then
        echo -e "  ${YELLOW}⚠️  URLs problématiques restantes:${NC}"
        while read -r url; do
            echo -e "    - $url"
            
            # Commenter les lignes avec des URLs problématiques
            if [[ "$url" == "pharmacien:stock" ]]; then
                sed -i '' "s/{% url ['\"]pharmacien:stock['\"] %}/{% comment %}URL non disponible: pharmacien:stock{% endcomment %}#/g" "$template_file"
                echo -e "    ${YELLOW}  → Ligne commentée (URL non disponible)${NC}"
            fi
        done <<< "$problematic_urls"
    fi
    
    if [[ $corrections_made -eq 0 ]]; then
        echo -e "  ${GREEN}✅ Aucune correction nécessaire${NC}"
    else
        echo -e "  ${GREEN}✅ Total corrections: $corrections_made${NC}"
    fi
}

# Analyser tous les templates
echo -e "\n${BLUE}📋 ANALYSE INITIALE DES TEMPLATES${NC}"
echo "=================================="

for template in "$TEMPLATES_DIR"/*.html; do
    if [[ -f "$template" ]]; then
        analyze_template "$template"
    fi
done

# Vérification des URLs disponibles
echo -e "\n${BLUE}2. VÉRIFICATION DES URLs DISPONIBLES${NC}"
echo "--------------------------------------"

python3 << 'EOF'
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath('.')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')

try:
    django.setup()
    
    from django.urls import reverse, NoReverseMatch
    
    print("🔍 URLs disponibles dans le namespace 'pharmacien':")
    print("=" * 50)
    
    available_urls = [
        'dashboard_pharmacien',
        'liste_ordonnances_attente',
        'detail_ordonnance', 
        'valider_ordonnance',
        'refuser_ordonnance',
        'historique_validation',
        'rechercher_ordonnances',
        'filtrer_ordonnances',
        'profil_pharmacien',
        'export_historique',
        'api_ordonnances_attente',
        'api_statistiques_temps_reel',
        'api_statistiques_pharmacien',
        'tableau_de_bord',
        'historique_validations',
        'ordonnances',
        'servir_ordonnance',
    ]
    
    for url_name in available_urls:
        try:
            full_name = f"pharmacien:{url_name}"
            url = reverse(full_name)
            print(f"✅ {full_name:40} → {url}")
        except NoReverseMatch as e:
            print(f"❌ {full_name:40} → NON TROUVÉE")
            
except Exception as e:
    print(f"❌ Erreur lors de la vérification: {e}")
EOF

# Demander confirmation pour la correction
echo -e "\n${YELLOW}⚠️  Voulez-vous corriger automatiquement les templates? (o/N)${NC}"
read -r response

if [[ "$response" =~ ^[oO](ui)?$ ]]; then
    echo -e "\n${BLUE}3. CORRECTION AUTOMATIQUE DES TEMPLATES${NC}"
    echo "=========================================="
    
    for template in "$TEMPLATES_DIR"/*.html; do
        if [[ -f "$template" ]]; then
            correct_template "$template"
        fi
    done
    
    echo -e "\n${GREEN}🎯 CORRECTIONS TERMINÉES${NC}"
    
    # Vérification finale
    echo -e "\n${BLUE}4. VÉRIFICATION FINALE${NC}"
    echo "====================="
    
    for template in "$TEMPLATES_DIR"/*.html; do
        if [[ -f "$template" ]]; then
            echo -e "\n${YELLOW}📄 Vérification finale: $(basename "$template")${NC}"
            analyze_template "$template"
        fi
    done
    
else
    echo -e "\n${YELLOW}⚠️  Correction annulée${NC}"
fi

# Générer un rapport des corrections appliquées
echo -e "\n${BLUE}5. RAPPORT DES CORRECTIONS${NC}"
echo "=========================="

cat > "rapport_corrections_pharmacien_$(date +%Y%m%d_%H%M%S).txt" << EOF
RAPPORT DE CORRECTION - TEMPLATES PHARMACIEN
Date: $(date)
============================================

MAPPING DES CORRECTIONS APPLIQUÉES:
-----------------------------------
EOF

for wrong_url in "${!URL_CORRECTIONS[@]}"; do
    echo "$wrong_url → ${URL_CORRECTIONS[$wrong_url]}" >> "rapport_corrections_pharmacien_$(date +%Y%m%d_%H%M%S).txt"
done

cat >> "rapport_corrections_pharmacien_$(date +%Y%m%d_%H%M%S).txt" << EOF

URLS DISPONIBLES:
-----------------
EOF

for url in "${AVAILABLE_URLS[@]}"; do
    echo "$url" >> "rapport_corrections_pharmacien_$(date +%Y%m%d_%H%M%S).txt"
done

echo -e "\n${GREEN}📊 Rapport sauvegardé: rapport_corrections_pharmacien_$(date +%Y%m%d_%H%M%S).txt${NC}"

# Script de vérification manuelle des URLs restantes
cat > "verifier_urls_manuellement.sh" << 'EOF'
#!/bin/bash
echo "🔍 VÉRIFICATION MANUELLE DES URLs DANS LES TEMPLATES"
for template in templates/pharmacien/*.html; do
    echo "=== $template ==="
    grep -n "{% url" "$template" | while read -r line; do
        echo "  $line"
    done
done
EOF

chmod +x "verifier_urls_manuellement.sh"
echo -e "\n${GREEN}🔧 Script de vérification créé: verifier_urls_manuellement.sh${NC}"

echo -e "\n${GREEN}✨ ANALYSE TERMINÉE${NC}"
echo "================"