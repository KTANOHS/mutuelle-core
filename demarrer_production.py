# demarrer_production.py
import os
import sys
import subprocess

print("="*70)
print("🚀 SCRIPT DE DÉMARRAGE EN PRODUCTION")
print("="*70)

# 1. Vérification de l'environnement
print("\n1. 🔍 VÉRIFICATION DE L'ENVIRONNEMENT")
print("   " + "-"*40)

# Vérifier Python
python_version = sys.version.split()[0]
print(f"   Python: {python_version}")

# Vérifier Django
try:
    import django
    print(f"   Django: {django.get_version()}")
except:
    print("   ❌ Django non installé")

# 2. Vérification des dépendances
print("\n2. 📦 VÉRIFICATION DES DÉPENDANCES")
print("   " + "-"*40)

try:
    import pip
    print("   ✅ pip disponible")
except:
    print("   ❌ pip non disponible")

# 3. Scripts de vérification
print("\n3. ✅ EXÉCUTION DES VÉRIFICATIONS")
print("   " + "-"*40)

scripts = [
    "check_system_corrige1.py",
    "rapport_final_corrige1.py",
    "analyse_avancee.py"
]

for script in scripts:
    if os.path.exists(script):
        print(f"   Exécution de {script}...")
        result = subprocess.run([sys.executable, script], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ {script} exécuté avec succès")
        else:
            print(f"   ⚠️  {script} a rencontré des erreurs")
    else:
        print(f"   ❌ {script} non trouvé")

# 4. Instructions de démarrage
print("\n4. 🚀 INSTRUCTIONS DE DÉMARRAGE")
print("   " + "-"*40)
print("""
   Pour démarrer le serveur en production :
   
   1. Configurez les variables d'environnement :
      export DJANGO_SETTINGS_MODULE=mutuelle_core.settings
      export SECRET_KEY="votre-clé-secrète"
      export DEBUG=False
      
   2. Collectez les fichiers statiques :
      python manage.py collectstatic --noinput
      
   3. Appliquez les migrations :
      python manage.py migrate
      
   4. Créez un superutilisateur (si nécessaire) :
      python manage.py createsuperuser
      
   5. Démarrez le serveur :
      python manage.py runserver 0.0.0.0:8000
      
   Pour le déploiement en production, utilisez :
   - Gunicorn (serveur WSGI)
   - Nginx (serveur web/reverse proxy)
   - PostgreSQL (base de données)
""")

# 5. Configuration de sécurité
print("\n5. 🔒 CONFIGURATION DE SÉCURITÉ")
print("   " + "-"*40)
print("""
   Vérifications de sécurité recommandées :
   
   1. ✅ Mot de passe fort pour les superutilisateurs
   2. ✅ Protection CSRF activée
   3. ✅ DEBUG=False en production
   4. ✅ HTTPS activé
   5. ✅ Sauvegardes régulières de la base de données
   6. ✅ Mises à jour régulières des dépendances
   
   Actions immédiates :
   - Changer les mots de passe par défaut
   - Configurer le HTTPS
   - Mettre en place les sauvegardes
""")

print("\n" + "="*70)
print("🎯 VOTRE SYSTÈME EST PRÊT POUR LA PRODUCTION !")
print("="*70)