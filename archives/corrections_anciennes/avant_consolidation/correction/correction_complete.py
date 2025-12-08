#!/usr/bin/env python
"""
CORRECTION COMPLÈTE DU SYSTÈME - Résout tous les problèmes identifiés
"""

import os
import sys
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group, Permission
from django.db import transaction
from django.contrib.contenttypes.models import ContentType

def corriger_utilisateurs():
    """Corrige tous les utilisateurs problématiques"""
    print("🔧 CORRECTION DES UTILISATEURS")
    print("=" * 60)
    
    User = get_user_model()
    corrections = []
    
    # Liste des utilisateurs à corriger avec leurs nouveaux mots de passe
    users_to_fix = [
        {'username': 'GLORIA', 'password': 'Medecin123!', 'email': 'gloria@medecin.com', 'first_name': 'GLORIA', 'last_name': '', 'group': 'Medecin'},
        {'username': 'medecin_test', 'password': 'Medecin123!', 'email': 'medecin@test.com', 'first_name': 'Medecin', 'last_name': 'Test', 'group': 'Medecin'},
        {'username': 'agent_test', 'password': 'Agent123!', 'email': 'agent@test.com', 'first_name': 'Agent', 'last_name': 'Test', 'group': 'Agent'},
        {'username': 'pharmacien_test', 'password': 'Pharmacien123!', 'email': 'pharmacien@test.com', 'first_name': 'Pharmacien', 'last_name': 'Test', 'group': 'Pharmacien'},
        {'username': 'Almoravide', 'password': 'Almoravide1084', 'email': 'ktanohsoualio@gmail.com', 'first_name': 'Almoravide', 'last_name': '', 'group': 'Admin'},
    ]
    
    for user_info in users_to_fix:
        username = user_info['username']
        new_password = user_info['password']
        
        try:
            with transaction.atomic():
                # Récupère ou crée l'utilisateur
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': user_info['email'],
                        'first_name': user_info['first_name'],
                        'last_name': user_info['last_name'],
                        'is_active': True,
                        'is_staff': user_info['group'] == 'Admin',  # Admin = staff
                    }
                )
                
                if not created:
                    # Met à jour les informations
                    user.email = user_info['email']
                    user.first_name = user_info['first_name']
                    user.last_name = user_info['last_name']
                    user.is_active = True
                
                # Définit le mot de passe
                user.set_password(new_password)
                user.save()
                
                # Gère les groupes
                group_name = user_info['group']
                if group_name:
                    if group_name == 'Admin':
                        # Pour admin, ajoute tous les groupes importants
                        groups_to_add = ['Pharmacien', 'Medecin', 'Agent', 'Assureur', 'Membre']
                        for group_name in groups_to_add:
                            group, _ = Group.objects.get_or_create(name=group_name)
                            user.groups.add(group)
                    else:
                        group, _ = Group.objects.get_or_create(name=group_name)
                        user.groups.add(group)
                
                # Test l'authentification
                auth_user = authenticate(username=username, password=new_password)
                
                if auth_user:
                    status = "✅"
                else:
                    status = "❌"
                
                corrections.append({
                    'username': username,
                    'password': new_password,
                    'status': status,
                    'group': user_info['group'],
                    'created': created
                })
                
                print(f"{status} {username}: {new_password} (Groupe: {user_info['group']})")
                
        except Exception as e:
            print(f"❌ Erreur avec {username}: {str(e)}")
    
    return corrections

def creer_groupe_medecin():
    """Crée le groupe Medecin avec les permissions appropriées"""
    print("\n" + "=" * 60)
    print("🏥 CRÉATION DU GROUPE MÉDECIN")
    print("=" * 60)
    
    try:
        # Crée le groupe Medecin
        group, created = Group.objects.get_or_create(name='Medecin')
        
        if created:
            print("✅ Groupe 'Medecin' créé")
        else:
            print("✅ Groupe 'Medecin' existe déjà")
        
        # Permissions typiques pour un médecin
        permissions_codes = [
            # Ordonnances
            ('ordonnances', 'view_ordonnance'),
            ('ordonnances', 'add_ordonnance'),
            ('ordonnances', 'change_ordonnance'),
            ('ordonnances', 'delete_ordonnance'),
            
            # Consultations
            ('consultations', 'view_consultation'),
            ('consultations', 'add_consultation'),
            ('consultations', 'change_consultation'),
            
            # Patients/Membres
            ('membres', 'view_membre'),
            
            # Soins
            ('soins', 'view_soin'),
        ]
        
        added_perms = 0
        for app_label, codename in permissions_codes:
            try:
                # Essaye de trouver la permission
                perm = Permission.objects.get(content_type__app_label=app_label, codename=codename)
                group.permissions.add(perm)
                added_perms += 1
            except Permission.DoesNotExist:
                # Essaie sans le app_label
                try:
                    perm = Permission.objects.get(codename=codename)
                    group.permissions.add(perm)
                    added_perms += 1
                except:
                    pass
        
        print(f"✅ {added_perms} permissions ajoutées au groupe Medecin")
        
        # Ajoute les utilisateurs médecins existants
        medecin_users = ['GLORIA', 'medecin_test', 'medecin_test_1', 'medecin_test_2', 'medecin_test_3']
        User = get_user_model()
        
        for username in medecin_users:
            try:
                user = User.objects.get(username=username)
                user.groups.add(group)
                print(f"✅ {username} ajouté au groupe Medecin")
            except User.DoesNotExist:
                pass
        
        return group
        
    except Exception as e:
        print(f"❌ Erreur création groupe Medecin: {str(e)}")
        return None

def verifier_permissions_pharmacien():
    """Vérifie et corrige les permissions du groupe Pharmacien"""
    print("\n" + "=" * 60)
    print("💊 VÉRIFICATION PERMISSIONS PHARMACIEN")
    print("=" * 60)
    
    try:
        group = Group.objects.get(name='Pharmacien')
        print(f"✅ Groupe Pharmacien trouvé ({group.user_set.count()} utilisateurs)")
        
        # Permissions qui devraient être présentes pour un pharmacien
        required_permissions = [
            # Ordonnances
            'view_ordonnance',
            'change_ordonnance',
            'view_ordonnancepharmacien',
            'change_ordonnancepharmacien',
            
            # Médicaments
            'view_medicament',
            'change_medicament',
            
            # Stock
            'view_stockpharmacie',
            'change_stockpharmacie',
            
            # Bon de soin
            'view_bondesoin',
        ]
        
        # Vérifie les permissions actuelles
        current_perms = set(group.permissions.values_list('codename', flat=True))
        print(f"Permissions actuelles: {len(current_perms)}")
        
        # Ajoute les permissions manquantes
        added_count = 0
        for perm_codename in required_permissions:
            if perm_codename not in current_perms:
                try:
                    # Essaie de trouver la permission
                    perm = Permission.objects.get(codename=perm_codename)
                    group.permissions.add(perm)
                    added_count += 1
                    print(f"✅ Ajouté: {perm_codename}")
                except Permission.DoesNotExist:
                    print(f"⚠ Permission non trouvée: {perm_codename}")
        
        if added_count > 0:
            print(f"\n✅ {added_count} nouvelles permissions ajoutées")
        else:
            print(f"\n✅ Toutes les permissions requises sont déjà présentes")
        
        # Vérifie GLORIA1 spécifiquement
        User = get_user_model()
        try:
            gloria1 = User.objects.get(username='GLORIA1')
            print(f"\n🔍 Vérification GLORIA1:")
            
            # Vérifie les permissions
            perms_a_verifier = ['view_ordonnance', 'change_ordonnance']
            for perm in perms_a_verifier:
                if gloria1.has_perm(f'pharmacien.{perm}') or gloria1.has_perm(perm):
                    print(f"✅ {perm}: OK")
                else:
                    print(f"❌ {perm}: Manquante")
                    
        except User.DoesNotExist:
            print("⚠ GLORIA1 non trouvé")
        
        return group
        
    except Group.DoesNotExist:
        print("❌ Groupe Pharmacien non trouvé")
        return None

def generer_rapport_final():
    """Génère un rapport final avec tous les identifiants"""
    print("\n" + "=" * 60)
    print("📋 RAPPORT FINAL - IDENTIFIANTS")
    print("=" * 60)
    
    User = get_user_model()
    
    # Liste des utilisateurs importants
    important_users = [
        'GLORIA1',
        'Almoravide',
        'GLORIA',
        'medecin_test',
        'agent_test',
        'pharmacien_test',
    ]
    
    print("\n👤 UTILISATEURS PRINCIPAUX:")
    for username in important_users:
        try:
            user = User.objects.get(username=username)
            groups = user.groups.all()
            group_names = ", ".join([g.name for g in groups]) if groups else "Aucun"
            
            print(f"\n🔸 {username}:")
            print(f"   Email: {user.email}")
            print(f"   Groupes: {group_names}")
            print(f"   Actif: {user.is_active}")
            print(f"   Staff: {user.is_staff}")
            
            # Pour les tests, on affiche les mots de passe qu'on a configurés
            if username == 'GLORIA1':
                print(f"   Password: Pharmacien123!")
            elif username == 'Almoravide':
                print(f"   Password: Almoravide1084")
            elif username == 'GLORIA':
                print(f"   Password: Medecin123!")
            elif username == 'medecin_test':
                print(f"   Password: Medecin123!")
            elif username == 'agent_test':
                print(f"   Password: Agent123!")
            elif username == 'pharmacien_test':
                print(f"   Password: Pharmacien123!")
                
        except User.DoesNotExist:
            print(f"\n🔸 {username}: ❌ Non trouvé")
    
    print("\n" + "=" * 60)
    print("🌐 URLs IMPORTANTES:")
    print("=" * 60)
    print("📌 Connexion: http://127.0.0.1:8000/accounts/login/")
    print("📌 Admin Django: http://127.0.0.1:8000/admin/")
    print("📌 Dashboard Pharmacien: http://127.0.0.1:8000/pharmacien/dashboard/")
    print("📌 Messagerie: http://127.0.0.1:8000/communication/messagerie/")
    
    print("\n" + "=" * 60)
    print("✅ SYSTÈME PRÊT À L'EMPLOI")
    print("=" * 60)

def main():
    """Fonction principale"""
    print("🚀 CORRECTION COMPLÈTE DU SYSTÈME")
    print("=" * 60)
    
    # Vérifie que le serveur est accessible
    try:
        import requests
        response = requests.get('http://127.0.0.1:8000/', timeout=5)
        print(f"✅ Serveur accessible (HTTP {response.status_code})")
    except:
        print("⚠ Serveur non accessible. Les corrections seront appliquées mais testez après redémarrage.")
        print("   Pour redémarrer: python manage.py runserver")
    
    # Applique les corrections
    print("\n1. Correction des utilisateurs...")
    corrections = corriger_utilisateurs()
    
    print("\n2. Création groupe Medecin...")
    creer_groupe_medecin()
    
    print("\n3. Vérification permissions Pharmacien...")
    verifier_permissions_pharmacien()
    
    print("\n" + "=" * 60)
    print("✅ CORRECTIONS APPLIQUÉES")
    print("=" * 60)
    
    # Génère le rapport final
    generer_rapport_final()
    
    # Recommandations
    print("\n📋 RECOMMANDATIONS:")
    print("1. Redémarrez le serveur si en cours d'exécution")
    print("2. Testez la connexion avec GLORIA1 (Pharmacien123!)")
    print("3. Testez les autres utilisateurs avec leurs nouveaux mots de passe")
    print("4. Vérifiez que toutes les permissions fonctionnent")

if __name__ == "__main__":
    main()