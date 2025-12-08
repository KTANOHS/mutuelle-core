# debug_connection.py
# Placez ce fichier à la racine de votre projet et exécutez: python debug_connection.py

import os
import django
import sys

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from django.urls import reverse, resolve, Resolver404
from django.conf import settings

def analyze_authentication():
    """Analyse complète du système d'authentification"""
    print("=" * 60)
    print("🔍 ANALYSE DU SYSTÈME D'AUTHENTIFICATION")
    print("=" * 60)
    
    # 1. Vérification des groupes
    print("\n1. 📊 GROUPES EXISTANTS:")
    groups = Group.objects.all()
    if groups:
        for group in groups:
            users_count = group.user_set.count()
            print(f"   • {group.name}: {users_count} utilisateur(s)")
    else:
        print("   ❌ Aucun groupe trouvé!")
    
    # 2. Vérification des utilisateurs
    print("\n2. 👥 UTILISATEURS EXISTANTS:")
    users = User.objects.all()
    for user in users:
        user_groups = [g.name for g in user.groups.all()]
        print(f"   • {user.username} (Active: {user.is_active}) - Groupes: {user_groups}")
    
    # 3. Vérification des URLs de redirection
    print("\n3. 🎯 URLS DE REDIRECTION:")
    urls_to_check = [
        'home',
        'default_dashboard',
        'assureur:dashboard',
        'medecin:dashboard', 
        'pharmacien:dashboard',
        'membres:dashboard',
        'login',
        'logout'
    ]
    
    for url_name in urls_to_check:
        try:
            url = reverse(url_name)
            print(f"   • {url_name}: {url}")
        except Exception as e:
            print(f"   • {url_name}: ❌ ERREUR - {e}")
    
    # 4. Vérification des paramètres Django
    print("\n4. ⚙️ PARAMÈTRES DJANGO:")
    print(f"   • LOGIN_REDIRECT_URL: {getattr(settings, 'LOGIN_REDIRECT_URL', 'Non défini')}")
    print(f"   • LOGOUT_REDIRECT_URL: {getattr(settings, 'LOGOUT_REDIRECT_URL', 'Non défini')}")
    print(f"   • AUTHENTICATION_BACKENDS: {settings.AUTHENTICATION_BACKENDS}")

def test_user_redirection(username):
    """Test la redirection pour un utilisateur spécifique"""
    print(f"\n{'='*60}")
    print(f"🧪 TEST DE REDIRECTION POUR: {username}")
    print(f"{'='*60}")
    
    try:
        user = User.objects.get(username=username)
        
        # Import des utilitaires
        from core.utils import get_user_primary_group, get_user_redirect_url
        
        primary_group = get_user_primary_group(user)
        redirect_url = get_user_redirect_url(user)
        
        print(f"   • Utilisateur: {user.username}")
        print(f"   • Groupe principal: {primary_group}")
        print(f"   • URL de redirection: {redirect_url}")
        print(f"   • Groupes: {[g.name for g in user.groups.all()]}")
        
        # Test si l'URL est accessible
        try:
            resolve(redirect_url)
            print(f"   • ✅ URL accessible")
        except Resolver404:
            print(f"   • ❌ URL non trouvée")
            
    except User.DoesNotExist:
        print(f"   ❌ Utilisateur '{username}' non trouvé")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

def create_test_users():
    """Crée des utilisateurs de test s'ils n'existent pas"""
    print(f"\n{'='*60}")
    print("👤 CRÉATION D'UTILISATEURS DE TEST")
    print(f"{'='*60}")
    
    test_users = [
        {'username': 'assureur', 'group': 'Assureur'},
        {'username': 'medecin', 'group': 'Medecin'},
        {'username': 'pharmacien', 'group': 'Pharmacien'},
        {'username': 'membre', 'group': 'Membre'},
    ]
    
    for user_info in test_users:
        username = user_info['username']
        group_name = user_info['group']
        
        # Créer l'utilisateur s'il n'existe pas
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'is_active': True}
        )
        
        if created:
            user.set_password('password123')
            user.save()
            print(f"   ✅ Créé: {username} (mot de passe: password123)")
        else:
            print(f"   ℹ️ Existe déjà: {username}")
        
        # Assigner au groupe
        group, group_created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        
        if group_created:
            print(f"   ✅ Groupe créé: {group_name}")
    
    print(f"\n   🔑 Identifiants de test:")
    for user_info in test_users:
        print(f"      • {user_info['username']} / password123")

if __name__ == "__main__":
    print("🚀 LANCEMENT DE L'ANALYSE DE CONNEXION")
    print("=" * 60)
    
    # Analyse complète
    analyze_authentication()
    
    # Test des redirections pour chaque type d'utilisateur
    print(f"\n{'='*60}")
    print("🎯 TEST DES REDIRECTIONS")
    print(f"{'='*60}")
    
    for username in ['assureur', 'medecin', 'pharmacien', 'membre']:
        test_user_redirection(username)
    
    # Option: Créer les utilisateurs de test
    response = input("\n🤔 Voulez-vous créer les utilisateurs de test? (o/n): ")
    if response.lower() in ['o', 'oui', 'y', 'yes']:
        create_test_users()
    
    print(f"\n{'='*60}")
    print("✅ ANALYSE TERMINÉE")
    print(f"{'='*60}")