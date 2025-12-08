import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMMUNICATION_DIR = os.path.join(BASE_DIR, 'communication')

print("📁 Vérification de la structure de l'application communication...")

fichiers_requis = [
    '__init__.py',
    'admin.py', 
    'apps.py',
    'models.py',
    'views.py',
    'urls.py',
    'services.py'  # Nouveau fichier
]

for fichier in fichiers_requis:
    chemin = os.path.join(COMMUNICATION_DIR, fichier)
    if os.path.exists(chemin):
        print(f"✅ {fichier}")
    else:
        print(f"❌ {fichier} - MANQUANT")

print(f"\n📊 Résultat: {len([f for f in fichiers_requis if os.path.exists(os.path.join(COMMUNICATION_DIR, f))])}/{len(fichiers_requis)} fichiers présents")