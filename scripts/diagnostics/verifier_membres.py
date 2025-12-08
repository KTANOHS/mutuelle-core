import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre

def lister_membres():
    print("👥 LISTE DES MEMBRES EXISTANTS")
    print("=" * 40)
    
    membres = Membre.objects.all()
    print(f"📊 Total membres: {membres.count()}")
    
    for membre in membres:
        print(f"  - {membre.prenom} {membre.nom} (ID: {membre.id})")
        
    print(f"\n🎯 POUR TESTER LA RECHERCHE, UTILISEZ:")
    for membre in membres[:5]:  # Afficher les 5 premiers
        print(f"   🔍 '{membre.prenom}' ou '{membre.nom}'")

if __name__ == "__main__":
    lister_membres()