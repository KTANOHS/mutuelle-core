#!/bin/bash
# correction_urgence.sh

echo "🔧 Correction des problèmes identifiés..."

# 1. Nettoyer les sessions
echo "🗑️  Nettoyage des sessions..."
python manage.py clearsessions

# 2. Créer l'app cotisations si nécessaire
if [ ! -d "cotisations" ]; then
    echo "📁 Création de l'application cotisations..."
    python manage.py startapp cotisations
    
    # Créer les modèles de base
    cat > cotisations/models.py << 'EOF'
from django.db import models

class Cotisation(models.Model):
    pass
    # Modèle minimal pour résoudre l'import
EOF
fi

# 3. Appliquer les migrations
echo "🔄 Application des migrations..."
python manage.py makemigrations
python manage.py migrate

echo "✅ Corrections appliquées avec succès!"