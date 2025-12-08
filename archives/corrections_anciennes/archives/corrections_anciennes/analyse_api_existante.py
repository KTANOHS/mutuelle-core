# analyse_api_existante.py
import os
import django
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyser_fichier_api(nom_fichier):
    """Analyse un fichier de l'application API"""
    chemin = Path('api') / nom_fichier
    if chemin.exists():
        print(f"\n📁 ANALYSE DE {nom_fichier}")
        print("=" * 50)
        with open(chemin, 'r') as f:
            contenu = f.read()
            if contenu.strip():
                print(contenu)
            else:
                print("⚪ Fichier vide")
        return True
    else:
        print(f"\n❌ Fichier {nom_fichier} non trouvé")
        return False

def analyser_structure_api():
    """Analyse complète de la structure API"""
    print("🔍 ANALYSE COMPLÈTE DE L'APP API EXISTANTE")
    print("=" * 60)
    
    # Liste des fichiers à analyser
    fichiers = [
        'views.py',
        'urls.py', 
        'serializers.py',
        'models.py',
        'docs.py',
        'apps.py',
        'admin.py'
    ]
    
    resultats = {}
    
    for fichier in fichiers:
        resultats[fichier] = analyser_fichier_api(fichier)
    
    return resultats

def generer_rapport_analyse():
    """Génère un rapport d'analyse"""
    print("\n🎯 RAPPORT D'ANALYSE DE L'API")
    print("=" * 60)
    
    resultats = analyser_structure_api()
    
    # Analyser les endpoints existants
    try:
        from django.urls import get_resolver
        from api import urls as api_urls
        
        print("\n🌐 ENDPOINTS API DÉTECTÉS:")
        resolver = get_resolver(api_urls)
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'pattern'):
                print(f"   🔗 {pattern.pattern} -> {pattern.name}")
    except Exception as e:
        print(f"\n⚠️  Impossible d'analyser les URLs: {e}")
    
    # Vérifier les vues
    try:
        from api import views
        print("\n🎯 VUES DISPONIBLES DANS views.py:")
        for attr in dir(views):
            if not attr.startswith('_'):
                obj = getattr(views, attr)
                if hasattr(obj, '__class__') and 'View' in str(obj.__class__):
                    print(f"   👁️  {attr}")
    except Exception as e:
        print(f"\n⚠️  Impossible d'analyser les vues: {e}")

if __name__ == "__main__":
    generer_rapport_analyse()