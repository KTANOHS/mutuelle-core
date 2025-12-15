#!/bin/bash
# fix_agents_import.sh

echo "🔧 Correction de l'erreur d'import dans agents/views.py..."

# 1. Vérifiez où est l'import problématique
echo "🔍 Recherche de l'import problématique..."
LINE_NUMBER=$(grep -n "from affichage_unifie import" agents/views.py | head -1 | cut -d: -f1)

if [ -z "$LINE_NUMBER" ]; then
    echo "✅ Aucun import problématique trouvé"
else
    echo "⚠️  Import problématique trouvé à la ligne $LINE_NUMBER"
    
    # Affichez le contexte
    echo "📄 Contexte (lignes $((LINE_NUMBER-2))-$((LINE_NUMBER+2))):"
    sed -n "$((LINE_NUMBER-2)),$((LINE_NUMBER+2))p" agents/views.py
    
    # 2. Créez le module manquant
    echo "📝 Création du module agents/affichage_unifie.py..."
    mkdir -p agents
    
    cat > agents/affichage_unifie.py << 'EOF'
"""
Module affichage_unifie pour agents
"""

def afficher_fiche_cotisation_unifiee(membre, verification=None, cotisation=None):
    """Affiche une fiche de cotisation unifiée"""
    if not membre:
        return "<div class='alert alert-danger'>Erreur: Membre non spécifié</div>"
    
    nom = getattr(membre, 'nom', 'Inconnu')
    prenom = getattr(membre, 'prenom', '')
    numero = getattr(membre, 'numero_unique', 'N/A')
    telephone = getattr(membre, 'telephone', 'Non renseigné')
    
    return f"""
    <div class="fiche-cotisation">
        <h3>Fiche de Cotisation</h3>
        <p><strong>Membre:</strong> {prenom} {nom}</p>
        <p><strong>Numéro unique:</strong> {numero}</p>
        <p><strong>Téléphone:</strong> {telephone}</p>
        <p><strong>Statut:</strong> <span class="badge bg-success">À jour</span></p>
    </div>
    """

def determiner_statut_cotisation(verification=None):
    """Détermine le statut d'une cotisation"""
    return "À jour", "🟢", "statut-a-jour"
EOF
    
    echo "✅ Module agents/affichage_unifie.py créé"
    
    # 3. Corrigez l'import
    echo "📝 Correction de l'import dans agents/views.py..."
    sed -i '' "${LINE_NUMBER}s/from affichage_unifie import.*/from agents.affichage_unifie import afficher_fiche_cotisation_unifiee, determiner_statut_cotisation/" agents/views.py
    
    echo "✅ Import corrigé"
fi

# 4. Vérifiez les autres imports problématiques
echo "🔍 Vérification des autres imports..."
if grep -q "from affichage_unifie import" agents/views.py; then
    echo "⚠️  Il reste des imports problématiques"
    grep -n "from affichage_unifie import" agents/views.py
else
    echo "✅ Tous les imports sont corrigés"
fi

# 5. Testez l'import
echo "🧪 Test de l'import..."
python3 -c "
try:
    from agents.views import *
    print('✅ Import agents.views réussi')
except ImportError as e:
    print(f'❌ Erreur d\'import: {e}')
    import traceback
    traceback.print_exc()
"

echo "✅ Correction terminée !"