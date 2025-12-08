#!/usr/bin/env python
"""
Crée un vrai médecin de test avec profil complet
"""

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from medecin.models import Medecin, SpecialiteMedicale, EtablissementMedical

User = get_user_model()

def creer_medecin_complet():
    print("👨‍⚕️ CRÉATION D'UN VRAI MÉDECIN DE TEST")
    print("=" * 50)
    
    # 1. Créer les données de base si elles n'existent pas
    print("1. Préparation des données de base...")
    
    specialite, created = SpecialiteMedicale.objects.get_or_create(
        nom='Généraliste',
        defaults={'description': 'Médecine générale'}
    )
    if created:
        print("   ✅ Spécialité 'Généraliste' créée")
    
    etablissement, created = EtablissementMedical.objects.get_or_create(
        nom='Clinique du Test',
        defaults={
            'type_etablissement': 'CLINIQUE',
            'adresse': '123 Avenue du Médecin, Abidjan',
            'telephone': '+2250102030405',
            'ville': 'Abidjan'
        }
    )
    if created:
        print("   ✅ Établissement 'Clinique du Test' créé")
    
    # 2. Créer ou récupérer le groupe médecin
    groupe_medecin, created = Group.objects.get_or_create(name='medecin')
    if created:
        print("   ✅ Groupe 'medecin' créé")
    
    # 3. Créer l'utilisateur médecin
    print("2. Création de l'utilisateur médecin...")
    
    user, created = User.objects.get_or_create(
        username='dr.test',
        defaults={
            'email': 'dr.test@clinique.com',
            'first_name': 'Jean',
            'last_name': 'Test',
            'is_active': True,
            'is_staff': False
        }
    )
    
    if created:
        user.set_password('Medecin123!')
        user.save()
        print("   ✅ Utilisateur 'dr.test' créé")
    
    # 4. Ajouter au groupe médecin
    if not user.groups.filter(name='medecin').exists():
        user.groups.add(groupe_medecin)
        print("   ✅ Utilisateur ajouté au groupe 'medecin'")
    
    # 5. Créer le profil médecin
    print("3. Création du profil médecin...")
    
    medecin, created = Medecin.objects.get_or_create(
        user=user,
        defaults={
            'numero_ordre': 'MEDTEST2024',
            'specialite': specialite,
            'etablissement': etablissement,
            'telephone_pro': '+2250506070809',
            'email_pro': 'dr.test@clinique.com',
            'tarif_consultation': 15000,
            'actif': True,
            'disponible': True,
            'annees_experience': 5
        }
    )
    
    if created:
        print("   ✅ Profil médecin créé")
        print(f"   📋 Numéro d'ordre: MEDTEST2024")
    else:
        print("   ℹ️  Profil médecin existe déjà")
    
    # 6. Vérification finale
    print("4. Vérification finale...")
    
    # Vérifier que l'utilisateur a un profil médecin
    if hasattr(user, 'medecin_profile'):
        print("   ✅ Profil médecin accessible via user.medecin_profile")
        print(f"   👤 Médecin: Dr {user.get_full_name()}")
        print(f"   🏥 Établissement: {user.medecin_profile.etablissement.nom}")
        print(f"   📊 Spécialité: {user.medecin_profile.specialite.nom}")
        print(f"   ✅ Actif: {user.medecin_profile.actif}")
    else:
        print("   ❌ ERREUR: Profil médecin non accessible")
        return False
    
    # Vérifier le groupe
    groupes = user.groups.values_list('name', flat=True)
    print(f"   👥 Groupes: {list(groupes)}")
    
    print("\n🎉 MÉDECIN DE TEST CRÉÉ AVEC SUCCÈS!")
    print("=" * 50)
    print("🔐 IDENTIFIANTS DE TEST:")
    print("   Utilisateur: dr.test")
    print("   Mot de passe: Medecin123!")
    print("\n🌐 POUR TESTER:")
    print("1. Allez sur: http://localhost:8000/accounts/login/")
    print("2. Connectez-vous avec les identifiants ci-dessus")
    print("3. Vous devriez être redirigé vers /medecin/dashboard/")
    
    return True

def verifier_medecins_existants():
    """Vérifie tous les médecins existants dans la base"""
    print("\n📋 LISTE DES MÉDECINS EXISTANTS:")
    print("-" * 35)
    
    medecins = Medecin.objects.select_related('user', 'specialite', 'etablissement').all()
    
    if medecins:
        for medecin in medecins:
            statut = "✅ Actif" if medecin.actif else "❌ Inactif"
            print(f"👤 Dr {medecin.user.get_full_name()}")
            print(f"   📧 {medecin.user.username}")
            print(f"   🏥 {medecin.etablissement.nom}")
            print(f"   📊 {medecin.specialite.nom}")
            print(f"   📋 {medecin.numero_ordre}")
            print(f"   {statut}")
            print()
    else:
        print("❌ Aucun médecin trouvé dans la base")
    
    return len(medecins)

if __name__ == "__main__":
    # Vérifier d'abord les médecins existants
    total_medecins = verifier_medecins_existants()
    
    if total_medecins == 0:
        print("🚨 AUCUN MÉDECIN TROUVÉ - Création d'urgence...")
        creer_medecin_complet()
    else:
        print(f"✅ {total_medecins} médecin(s) trouvé(s) dans la base")
        print("\n💡 Pour créer un nouveau médecin de test, exécutez:")
        print("   python scripts/creer_medecin_test.py")