#!/usr/bin/env python
"""
CORRECTION GLOBALE - TOUS LES PROBLÈMES
"""
import os
import sys
import django
import subprocess

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

def executer_commande(commande):
    """Exécute une commande shell et retourne le résultat"""
    print(f"🔄 Exécution: {commande}")
    try:
        result = subprocess.run(commande, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Succès: {result.stdout}")
            return True
        else:
            print(f"❌ Erreur: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def correction_globale():
    """Applique toutes les corrections nécessaires"""
    print("🎯 CORRECTION GLOBALE - DÉMARRAGE")
    print("=" * 70)
    
    # 1. Vérifier la syntaxe des fichiers Python
    print("\n1. 🔍 VÉRIFICATION SYNTAXE PYTHON:")
    fichiers_a_verifier = [
        'membres/views.py',
        'medecin/models.py', 
        'membres/models.py',
        'assureur/views.py'
    ]
    
    for fichier in fichiers_a_verifier:
        if os.path.exists(fichier):
            result = executer_commande(f"python -m py_compile {fichier}")
            if result:
                print(f"✅ {fichier} - Syntaxe OK")
            else:
                print(f"❌ {fichier} - Erreur de syntaxe")
        else:
            print(f"⚠️  {fichier} - Fichier non trouvé")
    
    # 2. Appliquer les corrections medecin/models.py
    print("\n2. 🔧 CORRECTION medecin/models.py:")
    try:
        from correction_medecin_models import corriger_medecin_models
        corriger_medecin_models()
    except Exception as e:
        print(f"❌ Erreur correction medecin: {e}")
    
    # 3. Tester les migrations
    print("\n3. 🗃️  VÉRIFICATION MIGRATIONS:")
    executer_commande("python manage.py makemigrations")
    executer_commande("python manage.py migrate")
    
    # 4. Tester les corrections
    print("\n4. 🧪 TEST DES CORRECTIONS:")
    executer_commande("python test_manuel_corrige.py")
    
    # 5. Test final
    print("\n5. ✅ TEST FINAL:")
    executer_commande("python manage.py test medecin.tests.MedecinTests.test_ordonnance_est_valide --settings=mutuelle_core.settings")

if __name__ == "__main__":
    correction_globale()
    
    print("\n" + "=" * 70)
    print("🎉 CORRECTIONS TERMINÉES")
    print("\n🎯 PROCHAINES ÉTAPES:")
    print("1. Connectez-vous avec: assureur_complet / password123")
    print("2. Accédez à: http://127.0.0.1:8000/assureur/bons/creer/5/")
    print("3. Si problème persiste, vérifiez les logs Django")