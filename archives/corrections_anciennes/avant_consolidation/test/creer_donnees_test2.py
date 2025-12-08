# creer_donnees_test.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from membres.models import Membre
from assureur.models import Assureur
from django.utils import timezone

def creer_donnees_test():
    print("🧪 CRÉATION DE DONNÉES DE TEST")
    print("-" * 40)
    
    User = get_user_model()
    
    # Créer un assureur de test
    try:
        # Créer l'utilisateur
        user, created = User.objects.get_or_create(
            username='assureur_test',
            defaults={
                'email': 'assureur@test.com',
                'is_staff': True,
                'is_active': True
            }
        )
        if created:
            user.set_password('test123')
            user.save()
            print("✅ Utilisateur assureur_test créé")
        else:
            print("✅ Utilisateur assureur_test existe déjà")
        
        # Créer le profil assureur
        assureur, created = Assureur.objects.get_or_create(
            user=user,
            defaults={
                'nom': 'Assureur Test',
                'email': 'assureur@test.com',
                'telephone': '+2250102030405'
            }
        )
        if created:
            print("✅ Profil Assureur créé")
        else:
            print("✅ Profil Assureur existe déjà")
        
        # Créer quelques membres de test
        membres_data = [
            {'nom': 'Jean Dupont', 'numero_securite_sociale': '1234567890123'},
            {'nom': 'Marie Martin', 'numero_securite_sociale': '2345678901234'},
            {'nom': 'Pierre Durand', 'numero_securite_sociale': '3456789012345'},
        ]
        
        for data in membres_data:
            membre, created = Membre.objects.get_or_create(
                numero_securite_sociale=data['numero_securite_sociale'],
                defaults={
                    'nom': data['nom'],
                    'assureur': assureur,
                    'date_naissance': timezone.now().date(),
                    'email': f"{data['nom'].lower().replace(' ', '.')}@test.com",
                    'telephone': '+2250100000000'
                }
            )
            if created:
                print(f"✅ Membre {data['nom']} créé (ID: {membre.id})")
            else:
                print(f"✅ Membre {data['nom']} existe déjà (ID: {membre.id})")
                
    except Exception as e:
        print(f"❌ Erreur lors de la création des données: {e}")

if __name__ == "__main__":
    creer_donnees_test()