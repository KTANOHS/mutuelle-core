"""
CORRECTEUR AUTOMATIQUE SIMPLIFIÉ - Mutuelle Core
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# Ajouter le chemin du projet Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

def setup_django():
    """Configurer l'environnement Django"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        import django
        django.setup()
        return True
    except Exception as e:
        print(f"❌ Erreur Django: {e}")
        return False

def creer_repertoires():
    """Créer les répertoires manquants"""
    print("📁 Création des répertoires manquants...")
    
    repertoires = [
        BASE_DIR / 'media',
        BASE_DIR / 'staticfiles',
        BASE_DIR / 'logs',
        BASE_DIR / 'media/uploads',
        BASE_DIR / 'media/profile_pics',
        BASE_DIR / 'media/documents',
        BASE_DIR / 'backups',
    ]
    
    crees = 0
    for rep in repertoires:
        if not rep.exists():
            rep.mkdir(parents=True, exist_ok=True)
            print(f"✅ Créé: {rep.relative_to(BASE_DIR)}")
            crees += 1
    
    return crees

def corriger_import_bonsoin():
    """Corriger l'import du modèle BonSoin -> BonDeSoin"""
    print("🔄 Correction de l'import BonSoin...")
    
    corrections = 0
    
    # Fichiers communs à vérifier
    fichiers_importants = [
        BASE_DIR / 'diagnostic_assureur7.py',
        BASE_DIR / 'corrector_automatico.py',
    ]
    
    for fichier in fichiers_importants:
        if fichier.exists():
            try:
                with open(fichier, 'r', encoding='utf-8') as f:
                    contenu = f.read()
                
                if 'BonSoin' in contenu:
                    nouveau_contenu = contenu.replace('BonSoin', 'BonDeSoin')
                    if nouveau_contenu != contenu:
                        with open(fichier, 'w', encoding='utf-8') as f:
                            f.write(nouveau_contenu)
                        print(f"✅ Corrigé: {fichier.name}")
                        corrections += 1
            except Exception as e:
                print(f"⚠️  Erreur avec {fichier.name}: {e}")
    
    return corrections

def verifier_bondesoin():
    """Vérifier que BonDeSoin fonctionne"""
    print("🧪 Test de BonDeSoin...")
    
    try:
        from soins.models import BonDeSoin
        count = BonDeSoin.objects.count()
        print(f"✅ BonDeSoin: {count} enregistrements")
        return True
    except Exception as e:
        print(f"❌ Erreur BonDeSoin: {e}")
        
        # Essayer d'importer BonSoin (peut-être que c'est le bon nom)
        try:
            from soins.models import BonSoin
            count = BonSoin.objects.count()
            print(f"✅ BonSoin: {count} enregistrements (nom correct: BonSoin)")
            return True
        except:
            print("❌ Ni BonSoin ni BonDeSoin ne fonctionnent")
            return False

def creer_script_backup_simple():
    """Créer un script de backup simple"""
    print("💾 Création script de backup simple...")
    
    script_backup = BASE_DIR / 'backup_simple.py'
    
    script_content = '''#!/usr/bin/env python3
"""
SCRIPT DE BACKUP SIMPLE - Mutuelle Core
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
BACKUP_DIR = BASE_DIR / 'backups'

def backup_database():
    """Créer un backup de la base de données"""
    # Créer le dossier backup
    BACKUP_DIR.mkdir(exist_ok=True)
    
    # Nom du fichier
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    db_path = BASE_DIR / 'db.sqlite3'
    
    if db_path.exists():
        backup_file = BACKUP_DIR / f'db_backup_{timestamp}.sqlite3'
        
        try:
            # Copier la base de données
            shutil.copy2(db_path, backup_file)
            
            # Taille en MB
            file_size = backup_file.stat().st_size / 1024 / 1024
            
            print(f"✅ Backup créé: {backup_file.name}")
            print(f"📊 Taille: {file_size:.2f} MB")
            
            # Garder seulement les 5 derniers backups
            backups = sorted(BACKUP_DIR.glob('db_backup_*.sqlite3'))
            if len(backups) > 5:
                for old_backup in backups[:-5]:
                    old_backup.unlink()
                    print(f"🗑️  Supprimé: {old_backup.name}")
                    
        except Exception as e:
            print(f"❌ Erreur: {e}")
    else:
        print("❌ Base de données non trouvée")

if __name__ == "__main__":
    print("🔍 Début du backup...")
    backup_database()
    print("✅ Backup terminé !")
'''

    with open(script_backup, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # Rendre le script exécutable
    os.chmod(script_backup, 0o755)
    
    print(f"✅ Script créé: {script_backup}")
    return script_backup

def creer_fichier_env():
    """Créer un fichier .env.example"""
    print("📋 Création .env.example...")
    
    env_example = BASE_DIR / '.env.example'
    
    env_content = """# Configuration Django
DEBUG=False
SECRET_KEY=votre_secret_key_ici_au_moins_50_caracteres
DJANGO_ALLOWED_HOSTS=votre-domaine.com,localhost,127.0.0.1

# Configuration mutuelle
COTISATION_STANDARD=5000
COTISATION_FEMME_ENCEINTE=7500
FRAIS_CARTE=2000
AVANCE=10000
CMU_OPTION=1000
REVERSION_CLINIQUE=2000
REVERSION_PHARMACIE=2000
CAISSE_MUTUELLE=1000
LIMITE_BONS_QUOTIDIENNE=10
DUREE_VALIDITE_BON=24
"""

    with open(env_example, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print(f"✅ Fichier créé: {env_example}")
    return env_example

def executer_migrations():
    """Exécuter les migrations"""
    print("🔄 Exécution des migrations...")
    
    try:
        import subprocess
        
        result = subprocess.run(
            ['python', 'manage.py', 'migrate'],
            capture_output=True,
            text=True,
            cwd=BASE_DIR
        )
        
        if result.returncode == 0:
            print("✅ Migrations appliquées avec succès")
        else:
            print(f"⚠️  Problème migrations: {result.stderr[:200]}")
            
    except Exception as e:
        print(f"⚠️  Erreur: {e}")

def collecter_static():
    """Collecter les fichiers statiques"""
    print("🎨 Collecte des fichiers statiques...")
    
    try:
        import subprocess
        
        result = subprocess.run(
            ['python', 'manage.py', 'collectstatic', '--noinput'],
            capture_output=True,
            text=True,
            cwd=BASE_DIR
        )
        
        if result.returncode == 0:
            print("✅ Fichiers statiques collectés")
        else:
            print(f"⚠️  Problème statiques: {result.stderr[:200]}")
            
    except Exception as e:
        print(f"⚠️  Erreur: {e}")

def verifier_systeme():
    """Vérifier le système"""
    print("💻 Vérification système...")
    
    import platform
    
    print(f"Système: {platform.system()} {platform.release()}")
    print(f"Python: {platform.python_version()}")
    
    # Vérifier Django
    try:
        import django
        print(f"Django: {django.get_version()}")
    except:
        print("Django: Non trouvé")
    
    # Vérifier l'espace disque
    try:
        import shutil
        total, used, free = shutil.disk_usage("/")
        print(f"Espace disque: {free // (2**30)} GB libre")
    except:
        print("Espace disque: Non vérifié")

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🔧 CORRECTEUR AUTOMATIQUE SIMPLIFIÉ")
    print("=" * 60)
    print(f"Début: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # 1. Vérifier système
    verifier_systeme()
    print()
    
    # 2. Configurer Django
    if not setup_django():
        print("⚠️  Django non configuré, certaines vérifications limitées")
    print()
    
    # 3. Créer répertoires
    rep_crees = creer_repertoires()
    print()
    
    # 4. Vérifier BonDeSoin
    bon_ok = verifier_bondesoin()
    print()
    
    # 5. Corriger imports
    if not bon_ok:
        corrections = corriger_import_bonsoin()
        print(f"✅ {corrections} fichiers corrigés")
    print()
    
    # 6. Exécuter migrations
    executer_migrations()
    print()
    
    # 7. Collecter statiques
    collecter_static()
    print()
    
    # 8. Créer script backup
    backup_script = creer_script_backup_simple()
    print()
    
    # 9. Créer .env.example
    env_example = creer_fichier_env()
    print()
    
    # 10. Résumé
    print("=" * 60)
    print("📊 RÉSUMÉ DES ACTIONS")
    print("=" * 60)
    print(f"• Répertoires créés: {rep_crees}")
    print(f"• Modèle BonDeSoin: {'✅ OK' if bon_ok else '❌ Problème'}")
    print(f"• Script backup: {backup_script.name}")
    print(f"• Fichier .env: {env_example.name}")
    print()
    
    # 11. Tester le serveur
    print("🎯 POUR TESTER VOTRE APPLICATION:")
    print("1. Lancez le serveur: python manage.py runserver")
    print("2. Accédez à: http://127.0.0.1:8000/")
    print("3. Testez le backup: python backup_simple.py")
    print("4. Vérifiez les logs: ls -la logs/")
    print()
    
    # 12. URLs importantes
    print("🌐 URLS IMPORTANTES À TESTER:")
    print("  • Admin: /admin/")
    print("  • Agents: /agents/tableau-de-bord/")
    print("  • Assureur: /assureur/")
    print("  • Dashboard: /dashboard/")
    print()
    
    print("✅ CORRECTIONS TERMINÉES - " + datetime.now().strftime("%H:%M:%S"))

if __name__ == "__main__":
    main()