#!/bin/bash
# Script d'analyse rapide d'arborescence Django

echo "🔍 ANALYSE RAPIDE DU PROJET"
echo "============================"

# Vérifications de base
echo ""
echo "📁 STRUCTURE DE BASE:"
if [ -f "manage.py" ]; then
    echo "✅ manage.py présent"
else
    echo "❌ manage.py MANQUANT"
fi

if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt présent"
    echo "   Détails:"
    grep -E "Django|gunicorn|whitenoise|psycopg2" requirements.txt || echo "   (dépendances critiques non trouvées)"
else
    echo "❌ requirements.txt MANQUANT"
fi

if [ -f "render.yaml" ]; then
    echo "✅ render.yaml présent"
else
    echo "⚠️  render.yaml manquant (recommandé pour Render)"
fi

# Arborescence limitée
echo ""
echo "🌳 ARBORESCENCE (max 3 niveaux):"
find . -maxdepth 3 -type d | sort | sed 's|\./||' | grep -v "^\.\|__pycache__\|\.git\|\.venv\|venv\|node_modules" | while read dir; do
    if [ -n "$dir" ]; then
        echo "📁 $dir/"
        find "$dir" -maxdepth 1 -type f -name "*.py" -o -name "*.html" -o -name "*.css" -o -name "*.js" 2>/dev/null | head -5 | sed 's|^|    📄 |'
    fi
done | head -50

# Applications Django
echo ""
echo "📦 APPLICATIONS DJANGO:"
find . -name "apps.py" -type f | sed 's|/apps.py||' | sed 's|^\./||' | while read app; do
    if [ -f "$app/__init__.py" ]; then
        count=$(find "$app" -name "*.py" -type f | wc -l)
        echo "  • $app ($count fichiers Python)"
    fi
done

# Fichiers critiques
echo ""
echo "📄 FICHIERS CRITIQUES:"
critical_files=("gunicorn_config.py" "Procfile" "runtime.txt" ".env.example" "start_prod.sh")
for file in "${critical_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ⚠️  $file (manquant)"
    fi
done

# Taille du projet
echo ""
echo "📊 STATISTIQUES:"
echo "  Fichiers Python: $(find . -name "*.py" -type f | wc -l)"
echo "  Templates HTML: $(find . -name "*.html" -type f | wc -l)"
echo "  Fichiers Static: $(find . -name "*.css" -o -name "*.js" -type f | wc -l)"
echo "  Total fichiers: $(find . -type f | wc -l)"
echo "  Total dossiers: $(find . -type d | wc -l)"

echo ""
echo "✅ Analyse terminée"