#!/usr/bin/env python
"""
TEST COMPLET FINAL - Vérification de tous les systèmes
"""

import os
import sys
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Group

def test_authentification():
    """Test d'authentification de tous les utilisateurs clés"""
    print("🔐 TESTS D'AUTHENTIFICATION")
    print("=" * 60)
    
    User = get_user_model()
    
    # Liste des utilisateurs à tester
    test_users = [
        {'username': 'GLORIA1', 'password': 'Pharmacien123!', 'description': 'Pharmacien'},
        {'username': 'Almoravide', 'password': 'Almoravide1084', 'description': 'Admin'},
        {'username': 'GLORIA', 'password': 'GLORIA', 'description': 'Médecin'},
        {'username': 'medecin_test', 'password': 'medecin123', 'description': 'Médecin test'},
        {'username': 'agent_test', 'password': 'agent123', 'description': 'Agent'},
        {'username': 'pharmacien_test', 'password': 'pharmacien123', 'description': 'Pharmacien test'},
    ]
    
    for user_info in test_users:
        username = user_info['username']
        password = user_info['password']
        description = user_info['description']
        
        print(f"\n🧪 {description} ({username}):")
        
        # Vérifie si l'utilisateur existe
        try:
            user = User.objects.get(username=username)
            print(f"   ✅ Existe dans la DB")
            print(f"      Actif: {user.is_active}, Staff: {user.is_staff}")
            
            # Test d'authentification
            auth_user = authenticate(username=username, password=password)
            if auth_user:
                print(f"   ✅ Authentification réussie")
                
                # Affiche les groupes
                groups = user.groups.all()
                if groups:
                    print(f"      Groupes: {', '.join([g.name for g in groups])}")
                else:
                    print(f"      ⚠ Aucun groupe")
            else:
                print(f"   ❌ Échec authentification")
                
                # Test check_password
                if user.check_password(password):
                    print(f"      ⚠ check_password() réussie mais authenticate() échoue")
                else:
                    print(f"      ❌ check_password() échoue aussi")
                    
        except User.DoesNotExist:
            print(f"   ❌ Utilisateur non trouvé dans la DB")

def test_groupes_permissions():
    """Test des groupes et permissions"""
    print("\n" + "=" * 60)
    print("👥 TESTS DES GROUPES ET PERMISSIONS")
    print("=" * 60)
    
    User = get_user_model()
    
    # Liste des groupes importants
    groupes_importants = ['Pharmacien', 'Médecin', 'Agent', 'Assureur', 'Membre']
    
    for nom_groupe in groupes_importants:
        try:
            groupe = Group.objects.get(name=nom_groupe)
            users = groupe.user_set.all()
            print(f"\n📊 Groupe '{nom_groupe}':")
            print(f"   Utilisateurs: {users.count()}")
            
            # Liste les utilisateurs
            for user in users[:5]:  # Limite à 5 pour la lisibilité
                print(f"      - {user.username} ({user.email})")
            
            if users.count() > 5:
                print(f"      ... et {users.count() - 5} autres")
                
            # Liste les permissions
            permissions = groupe.permissions.all()
            print(f"   Permissions: {permissions.count()}")
            
            for perm in permissions[:5]:
                print(f"      - {perm.codename}")
            
            if permissions.count() > 5:
                print(f"      ... et {permissions.count() - 5} autres")
                
        except Group.DoesNotExist:
            print(f"\n⚠ Groupe '{nom_groupe}' n'existe pas")

def test_gloria1_complet():
    """Test complet de GLORIA1"""
    print("\n" + "=" * 60)
    print("💊 TEST COMPLET GLORIA1 - PHARMACIEN")
    print("=" * 60)
    
    User = get_user_model()
    
    try:
        user = User.objects.get(username='GLORIA1')
        
        print(f"📋 INFORMATIONS:")
        print(f"   ID: {user.id}")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Prénom: {user.first_name}")
        print(f"   Nom: {user.last_name}")
        print(f"   Actif: {user.is_active}")
        print(f"   Staff: {user.is_staff}")
        print(f"   Superuser: {user.is_superuser}")
        print(f"   Dernière connexion: {user.last_login}")
        
        print(f"\n🔐 AUTHENTIFICATION:")
        # Test avec le bon mot de passe
        auth_user = authenticate(username='GLORIA1', password='Pharmacien123!')
        if auth_user:
            print(f"   ✅ Succès avec 'Pharmacien123!'")
        else:
            print(f"   ❌ Échec avec 'Pharmacien123!'")
        
        # Test avec mauvais mot de passe
        auth_user_wrong = authenticate(username='GLORIA1', password='MauvaisMotDePasse')
        if not auth_user_wrong:
            print(f"   ✅ Rejet correct du mauvais mot de passe")
        
        print(f"\n👥 GROUPES:")
        groups = user.groups.all()
        if groups:
            for group in groups:
                print(f"   ✅ {group.name}")
        else:
            print(f"   ⚠ Aucun groupe")
        
        print(f"\n🔑 PERMISSIONS (via groupes):")
        all_perms = set()
        for group in groups:
            for perm in group.permissions.all():
                all_perms.add(perm.codename)
        
        if all_perms:
            for perm in sorted(list(all_perms))[:10]:
                print(f"   - {perm}")
            if len(all_perms) > 10:
                print(f"   ... et {len(all_perms) - 10} autres")
        else:
            print(f"   ⚠ Aucune permission via les groupes")
        
        # Vérifie les permissions spécifiques au pharmacien
        perms_requises = ['view_ordonnance', 'change_ordonnance', 'view_pharmacien']
        print(f"\n🔍 PERMISSIONS REQUISES POUR PHARMACIEN:")
        for perm in perms_requises:
            if user.has_perm(f'pharmacien.{perm}') or user.has_perm(perm):
                print(f"   ✅ {perm}")
            else:
                print(f"   ❌ {perm} (manquante)")
        
        return True
        
    except User.DoesNotExist:
        print(f"❌ GLORIA1 non trouvé")
        return False

def test_urls_access():
    """Test d'accès aux URLs importantes"""
    print("\n" + "=" * 60)
    print("🌐 TESTS D'ACCÈS AUX URLs")
    print("=" * 60)
    
    import requests
    
    urls = [
        ('/', 'Page d\'accueil'),
        ('/accounts/login/', 'Page de connexion'),
        ('/pharmacien/dashboard/', 'Dashboard pharmacien'),
        ('/communication/messagerie/', 'Messagerie'),
        ('/admin/', 'Admin Django'),
    ]
    
    for url_path, description in urls:
        url = f'http://127.0.0.1:8000{url_path}'
        try:
            response = requests.get(url, timeout=5)
            print(f"\n📡 {description} ({url_path}):")
            print(f"   HTTP {response.status_code} - {len(response.text)} caractères")
            
            if response.status_code == 200:
                print(f"   ✅ Accessible")
            elif response.status_code == 302:
                print(f"   🔄 Redirection (login requis)")
            elif response.status_code == 403:
                print(f"   ⛔ Interdit (permissions)")
            elif response.status_code == 404:
                print(f"   ❌ Non trouvé")
            else:
                print(f"   ⚠ Code inattendu")
                
        except Exception as e:
            print(f"\n📡 {description} ({url_path}):")
            print(f"   ❌ Erreur: {str(e)}")

def main():
    """Fonction principale"""
    print("🚀 TEST COMPLET DU SYSTÈME MUTUELLE")
    print("=" * 60)
    
    # Vérifie que le serveur est accessible
    try:
        import requests
        response = requests.get('http://127.0.0.1:8000/', timeout=5)
        print(f"✅ Serveur accessible (HTTP {response.status_code})")
    except:
        print("❌ Serveur non accessible. Démarrez-le avec:")
        print("   python manage.py runserver")
        return
    
    # Exécute les tests
    test_authentification()
    test_groupes_permissions()
    test_gloria1_complet()
    test_urls_access()
    
    print("\n" + "=" * 60)
    print("📋 RÉCAPITULATIF DES IDENTIFIANTS")
    print("=" * 60)
    print("💊 GLORIA1 (Pharmacien):")
    print("   URL:      http://127.0.0.1:8000/accounts/login/")
    print("   Username: GLORIA1")
    print("   Password: Pharmacien123!")
    print("   Redirection: /pharmacien/dashboard/")
    print()
    print("👨‍⚕️ Almoravide (Admin):")
    print("   Username: Almoravide")
    print("   Password: Almoravide1084")
    print()
    print("🏥 GLORIA (Médecin):")
    print("   Username: GLORIA")
    print("   Password: GLORIA")
    print()
    print("🔧 Pour l'admin Django:")
    print("   URL: http://127.0.0.1:8000/admin/")
    print("   Utilisez les identifiants Almoravide")

if __name__ == "__main__":
    main()