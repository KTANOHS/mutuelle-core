# Créez un fichier recreate_test_data.py
#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from membres.models import Membre
from django.utils import timezone
import random
import string

def recreer_donnees_test():
    print("🎯 RECRÉATION DES DONNÉES DE TEST")
    
    # 1. Créer les groupes
    groupes = ['Membres', 'Agents', 'Médecins', 'Pharmaciens', 'Assureurs']
    for nom_groupe in groupes:
        Group.objects.get_or_create(name=nom_groupe)
        print(f"✅ Groupe créé: {nom_groupe}")
    
    # 2. Créer les utilisateurs de test
    users_data = [
        {'username': 'test_agent', 'password': 'pass123', 'groups': ['Agents'], 'is_staff': True},
        {'username': 'assureur_test', 'password': 'pass123', 'groups': ['Assureurs'], 'is_staff': True},
        {'username': 'medecin_test', 'password': 'pass123', 'groups': ['Médecins']},
        {'username': 'test_pharmacien', 'password': 'pass123', 'groups': ['Pharmaciens']},
        {'username': 'membre_test', 'password': 'pass123', 'groups': ['Membres']},
    ]
    
    for user_info in users_data:
        user, created = User.objects.get_or_create(
            username=user_info['username'],
            defaults={'email': f"{user_info['username']}@test.com", 'is_staff': user_info.get('is_staff', False)}
        )
        if created:
            user.set_password(user_info['password'])
            user.save()
            # Ajouter aux groupes
            for group_name in user_info['groups']:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
            print(f"✅ Utilisateur créé: {user_info['username']}")
    
    # 3. Créer quelques membres de test
    membres_data = [
        {'nom': 'Doe', 'prenom': 'John', 'email': 'john.doe@test.com', 'telephone': '0102030405'},
        {'nom': 'Smith', 'prenom': 'Jane', 'email': 'jane.smith@test.com', 'telephone': '0203040506'},
        {'nom': 'Test', 'prenom': 'Correction', 'email': 'correction@test.com', 'telephone': '0304050607'},
    ]
    
    for membre_info in membres_data:
        # Générer numéro unique
        while True:
            numero = f"MEM{timezone.now().strftime('%Y')}{random.randint(1000, 9999)}"
            if not Membre.objects.filter(numero_unique=numero).exists():
                break
        
        membre = Membre.objects.create(
            nom=membre_info['nom'],
            prenom=membre_info['prenom'],
            email=membre_info['email'],
            telephone=membre_info['telephone'],
            numero_unique=numero,
            statut='actif',
            categorie='standard',
            date_inscription=timezone.now().date(),
            date_derniere_cotisation=timezone.now().date(),
        )
        print(f"✅ Membre créé: {membre.prenom} {membre.nom} - {membre.numero_unique}")
    
    print("🎉 DONNÉES DE TEST RECRÉÉES AVEC SUCCÈS!")

if __name__ == "__main__":
    recreer_donnees_test()