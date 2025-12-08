# verification_prerequis.py
import os
import sys
import subprocess
import importlib

def verifier_prerequis():
    """Vérifie les prérequis techniques pour les nouvelles fonctionnalités"""
    print("🔧 VÉRIFICATION DES PRÉREQUIS TECHNIQUES")
    print("=" * 50)
    
    prerequis = {
        'python_version': verifier_version_python(),
        'django_version': verifier_django(),
        'packages_requis': verifier_packages(),
        'structure_projet': verifier_structure_projet(),
        'base_donnees': verifier_base_donnees()
    }
    
    return prerequis

def verifier_version_python():
    """Vérifie la version de Python"""
    version = sys.version_info
    statut = version.major >= 3 and version.minor >= 8
    return {
        'statut': statut,
        'message': f"Python {version.major}.{version.minor}.{version.micro}",
        'recommandation': "Python 3.8+ requis" if not statut else "✅ Version compatible"
    }

def verifier_django():
    """Vérifie la version de Django"""
    try:
        import django
        version = django.get_version()
        return {
            'statut': True,
            'message': f"Django {version}",
            'recommandation': "✅ Version Django compatible"
        }
    except ImportError:
        return {
            'statut': False,
            'message': "Django non installé",
            'recommandation': "❌ Installer Django"
        }

def verifier_packages():
    """Vérifie les packages requis"""
    packages = [
        'djangorestframework',
        'django-cors-headers', 
        'channels',
        'celery',
        'redis',
        'psycopg2-binary',
        'whitenoise'
    ]
    
    resultats = []
    for package in packages:
        try:
            spec = importlib.util.find_spec(package.replace('-', '_'))
            statut = spec is not None
            resultats.append({
                'package': package,
                'statut': statut,
                'message': "✅ Installé" if statut else "❌ Manquant"
            })
        except:
            resultats.append({
                'package': package,
                'statut': False,
                'message': "❌ Erreur vérification"
            })
    
    return resultats

def verifier_structure_projet():
    """Vérifie la structure du projet"""
    dossiers_requis = [
        '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/api',
        '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/static/js',
        '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/static/css',
        '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates'
    ]
    
    resultats = []
    for dossier in dossiers_requis:
        existe = os.path.exists(dossier)
        resultats.append({
            'dossier': dossier.split('/')[-1],
            'statut': existe,
            'message': "✅ Existe" if existe else "⚠️  À créer"
        })
    
    return resultats

def verifier_base_donnees():
    """Vérifie la configuration de la base de données"""
    try:
        from django.conf import settings
        db_config = settings.DATABASES['default']
        
        return {
            'statut': True,
            'message': f"Base: {db_config['ENGINE'].split('.')[-1]}",
            'recommandation': "✅ Configuration DB OK"
        }
    except Exception as e:
        return {
            'statut': False,
            'message': f"Erreur: {e}",
            'recommandation': "❌ Vérifier settings.DATABASES"
        }

def afficher_resultats(prerequis):
    """Affiche les résultats de la vérification"""
    print("\n📊 RÉSULTATS DE LA VÉRIFICATION:")
    
    for categorie, resultat in prerequis.items():
        print(f"\n{categorie.upper().replace('_', ' ')}:")
        
        if isinstance(resultat, list):
            for item in resultat:
                statut = "✅" if item['statut'] else "❌"
                print(f"   {statut} {item['package'] if 'package' in item else item['dossier']}: {item['message']}")
        else:
            statut = "✅" if resultat['statut'] else "❌"
            print(f"   {statut} {resultat['message']}")

if __name__ == "__main__":
    resultats = verifier_prerequis()
    afficher_resultats(resultats)