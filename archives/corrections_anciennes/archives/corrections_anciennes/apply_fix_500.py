# apply_fix_500.py
import os
import sys
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent

def sauvegarder_views_actuelles():
    """Sauvegarde la version actuelle de views.py"""
    views_path = BASE_DIR / 'agents' / 'views.py'
    backup_path = BASE_DIR / 'agents' / 'views.py.backup'
    
    if views_path.exists():
        shutil.copy2(views_path, backup_path)
        print(f"✅ Sauvegarde créée: {backup_path}")
        return True
    else:
        print("❌ Fichier views.py actuel introuvable")
        return False

def appliquer_corrections_views():
    """Applique les corrections à views.py"""
    views_path = BASE_DIR / 'agents' / 'views.py'
    views_corrige_path = BASE_DIR / 'agents' / 'views_corrige.py'
    
    if not views_corrige_path.exists():
        print("❌ Fichier views_corrige.py introuvable")
        return False
    
    try:
        # Lire le contenu corrigé
        with open(views_corrige_path, 'r') as f:
            contenu_corrige = f.read()
        
        # Écrire dans le fichier views.py
        with open(views_path, 'w') as f:
            f.write(contenu_corrige)
        
        print("✅ Corrections appliquées à views.py")
        return True
        
    except Exception as e:
        print(f"❌ Erreur application corrections: {e}")
        return False

def verifier_logs_django():
    """Donne des instructions pour vérifier les logs Django"""
    print("\n📋 POUR DEBUGUER L'ERREUR 500:")
    print("1. Vérifiez les logs Django dans la console où le serveur tourne")
    print("2. Ou ajoutez cette configuration dans settings.py pour les logs:")
    
    config_logs = '''
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'agents': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
'''
    print(config_logs)

def creer_route_test_simple():
    """Crée une route de test simple pour isoler le problème"""
    urls_path = BASE_DIR / 'agents' / 'urls.py'
    
    try:
        with open(urls_path, 'r') as f:
            contenu = f.read()
        
        # Ajouter une route de test si elle n'existe pas
        if 'api/test-simple' not in contenu:
            nouveau_contenu = contenu.replace(
                '# API endpoints',
                '''# API endpoints
    path('api/test-simple/', views.test_simple_api, name='test_simple_api'),'''
            )
            
            with open(urls_path, 'w') as f:
                f.write(nouveau_contenu)
            
            print("✅ Route de test simple ajoutée")
        else:
            print("✅ Route de test simple existe déjà")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur ajout route test: {e}")
        return False

def ajouter_vue_test_simple():
    """Ajoute une vue de test simple pour debuguer"""
    views_path = BASE_DIR / 'agents' / 'views.py'
    
    try:
        with open(views_path, 'a') as f:
            vue_test = '''

# =============================================================================
# VUE DE TEST POUR DEBUG
# =============================================================================

@login_required
def test_simple_api(request):
    """API de test simple pour debuguer l'erreur 500"""
    try:
        return JsonResponse({
            'success': True,
            'message': 'API de test fonctionnelle',
            'user': request.user.username,
            'timestamp': timezone.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
'''
            f.write(vue_test)
        
        print("✅ Vue de test simple ajoutée")
        return True
        
    except Exception as e:
        print(f"❌ Erreur ajout vue test: {e}")
        return False

def appliquer_corrections_completes():
    """Applique toutes les corrections"""
    print("🔧 APPLICATION DES CORRECTIONS ERREUR 500")
    print("=" * 60)
    
    # Sauvegarder d'abord
    sauvegarder_views_actuelles()
    
    corrections = [
        ("Application corrections views.py", appliquer_corrections_views),
        ("Ajout route test simple", creer_route_test_simple),
        ("Ajout vue test simple", ajouter_vue_test_simple),
    ]
    
    for nom, fonction in corrections:
        print(f"\n📝 {nom}...")
        if fonction():
            print("   ✅ SUCCÈS")
        else:
            print("   ⚠️  ÉCHEC partiel")
    
    verifier_logs_django()
    
    print("\n🎯 CORRECTIONS APPLIQUÉES!")
    print("\n📋 PROCHAINES ÉTAPES:")
    print("1. Redémarrez le serveur: python manage.py runserver")
    print("2. Testez d'abord: http://localhost:8000/agents/api/test-simple/")
    print("3. Si ça marche, testez la recherche normale")
    print("4. Si l'erreur persiste, vérifiez les logs Django")

if __name__ == "__main__":
    appliquer_corrections_completes()