# test_creation_membre.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from django.utils import timezone
import random
import string

def test_creation_membre():
    print("🧪 TEST CRÉATION MEMBRE")
    print("=" * 40)
    
    # Compter avant
    avant = Membre.objects.count()
    print(f"📊 Membres avant: {avant}")
    
    # Créer un membre
    try:
        # Générer numéro unique
        lettres = ''.join(random.choices(string.ascii_uppercase, k=3))
        chiffres = ''.join(random.choices(string.digits, k=3))
        numero_unique = f"TEST{lettres}{chiffres}"
        
        nouveau_membre = Membre.objects.create(
            nom="TEST",
            prenom="Roger",
            telephone="0102030405",
            numero_unique=numero_unique,
            statut='actif'
        )
        
        print(f"✅ Membre créé - ID: {nouveau_membre.id}")
        print(f"   📝 Nom: {nouveau_membre.prenom} {nouveau_membre.nom}")
        print(f"   🔑 Numéro: {numero_unique}")
        
        # Compter après
        apres = Membre.objects.count()
        print(f"📊 Membres après: {apres}")
        print(f"📈 Différence: {apres - avant}")
        
        # Test recherche immédiate
        from django.db.models import Q
        resultats = Membre.objects.filter(
            Q(nom__icontains="TEST") | 
            Q(prenom__icontains="Roger")
        )
        print(f"🔍 Recherche 'Roger': {resultats.count()} résultat(s)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur création: {e}")
        return False

if __name__ == "__main__":
    test_creation_membre()