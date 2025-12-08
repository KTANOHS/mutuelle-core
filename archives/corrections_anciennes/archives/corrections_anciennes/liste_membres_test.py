# liste_membres_test.py
import os
import django
import sys

sys.path.append('/Users/koffitanohsoualiho/Documents/projet')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Membre

def lister_tous_les_membres():
    print("📋 LISTE DE TOUS LES MEMBRES DISPONIBLES")
    print("=" * 60)
    
    membres = Membre.objects.all().order_by('id')
    
    if not membres:
        print("❌ Aucun membre trouvé dans la base de données")
        return
    
    print(f"📊 Total: {membres.count()} membre(s)")
    print()
    
    for membre in membres:
        print(f"🔹 ID: {membre.id}")
        print(f"   Numéro: {membre.numero_membre}")
        print(f"   Nom: {membre.prenom} {membre.nom}")
        print(f"   Email: {membre.email}")
        print(f"   URL test: http://127.0.0.1:8000/assureur/creer-bon/{membre.id}/")
        print("-" * 40)

if __name__ == "__main__":
    lister_tous_les_membres()