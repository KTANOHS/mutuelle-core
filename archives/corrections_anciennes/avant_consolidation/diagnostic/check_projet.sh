#!/bin/bash
# Script de diagnostic rapide pour projet Django

echo "🔍 DIAGNOSTIC RAPIDE DU PROJET"
echo "================================"

# 1. Vérifier l'environnement
echo -e "\n1. Environnement Python:"
python --version
pip --version

# 2. Vérifier les dépendances
echo -e "\n2. Dépendances installées:"
pip list | grep -E "(Django|django|psycopg|mysql|Pillow)"

# 3. Vérifier la santé Django
echo -e "\n3. Vérification Django:"
python manage.py check

# 4. Vérifier les migrations
echo -e "\n4. État des migrations:"
python manage.py showmigrations | grep -E "\[ \]|\[X\]" | head -20

# 5. Vérifier la base de données
echo -e "\n5. Connexion base de données:"
python manage.py dbshell -- -c "SELECT 1;" 2>/dev/null && echo "✅ DB Connectée" || echo "❌ DB Erreur"

# 6. Vérifier les URLs
echo -e "\n6. URLs disponibles:"
python manage.py show_urls | head -10

# 7. Vérifier les permissions
echo -e "\n7. Permissions des fichiers:"
ls -la manage.py
ls -la mutuelle_core/settings.py

# 8. Vérifier l'espace disque
echo -e "\n8. Espace disque:"
df -h . | tail -1

# 9. Vérifier la mémoire
echo -e "\n9. Utilisation mémoire:"
free -h | head -2

# 10. Vérifier les logs d'erreur
echo -e "\n10. Dernières erreurs (logs):"
find . -name "*.log" -type f -exec tail -5 {} \; 2>/dev/null | head -20

echo -e "\n✅ Diagnostic terminé!"