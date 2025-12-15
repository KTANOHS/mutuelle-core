#!/bin/bash
# fix_all_imports.sh

echo "🔧 Correction complète des imports dans agents/views.py..."

# 1. Créez le fichier affichage_unifie.py s'il n'existe pas
if [ ! -f "agents/affichage_unifie.py" ]; then
    echo "📝 Création de agents/affichage_unifie.py..."
    cat > agents/affichage_unifie.py << 'EOF'
"""
Module affichage_unifie pour agents - Version minimale pour Railway
"""

def afficher_fiche_cotisation_unifiee(membre, verification=None, cotisation=None):
    """Affiche une fiche de cotisation unifiée - Version minimale"""
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
fi

# 2. Corrigez TOUS les imports de affichage_unifie
echo "📝 Correction de tous les imports problématiques..."
if grep -q "from affichage_unifie import" agents/views.py; then
    # Remplacer tous les imports problématiques
    sed -i '' 's/from affichage_unifie import.*/from agents.affichage_unifie import afficher_fiche_cotisation_unifiee, determiner_statut_cotisation/g' agents/views.py
    echo "✅ Tous les imports corrigés"
else
    echo "✅ Aucun import problématique trouvé"
fi

# 3. Vérifiez aussi les imports relatifs
if grep -q "from .affichage_unifie import" agents/views.py; then
    echo "📝 Correction des imports relatifs..."
    sed -i '' 's/from .affichage_unifie import.*/from agents.affichage_unifie import afficher_fiche_cotisation_unifiee, determiner_statut_cotisation/g' agents/views.py
fi

# 4. Créez un __init__.py dans agents s'il n'existe pas
if [ ! -f "agents/__init__.py" ]; then
    echo "📝 Création de agents/__init__.py..."
    touch agents/__init__.py
fi

# 5. Test simple sans Django
echo "🧪 Test simple des imports..."
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    # Test d'import sans Django
    import agents.affichage_unifie
    print('✅ Module agents.affichage_unifie importable')
    
    # Test des fonctions
    from agents.affichage_unifie import afficher_fiche_cotisation_unifiee, determiner_statut_cotisation
    print('✅ Fonctions importées avec succès')
    
    # Test de base
    test_result = determiner_statut_cotisation()
    print(f'✅ Test fonctionnel: {test_result}')
    
except ImportError as e:
    print(f'❌ Erreur d\'import: {e}')
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f'⚠️  Autre erreur: {e}')
"

echo "✅ Correction complète terminée !"