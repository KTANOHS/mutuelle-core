#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC ET RÉPARATION - Problème GLORIA1
"""

import os
import sys
import django
import requests
import re

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group, Permission
from django.db import transaction

def diagnostic_complet():
    """Diagnostic complet de l'utilisateur GLORIA1"""
    print("🔍 DIAGNOSTIC COMPLET - UTILISATEUR GLORIA1")
    print("=" * 60)
    
    User = get_user_model()
    
    try:
        # 1. Récupère l'utilisateur
        user = User.objects.get(username='GLORIA1')
        
        print(f"📋 INFORMATIONS DE BASE:")
        print(f"   ID: {user.id}")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Prénom: {user.first_name}")
        print(f"   Nom: {user.last_name}")
        print(f"   Date joined: {user.date_joined}")
        print(f"   Dernière connexion: {user.last_login}")
        print(f"   Actif: {user.is_active}")
        print(f"   Staff: {user.is_staff}")
        print(f"   Superuser: {user.is_superuser}")
        
        # 2. Test d'authentification
        print(f"\n🔐 TEST D'AUTHENTIFICATION:")
        
        # Test avec le mot de passe actuel
        auth_user = authenticate(username='GLORIA1', password='Pharmacien123')
        if auth_user:
            print("   ✅ Authentification réussie avec 'Pharmacien123'")
        else:
            print("   ❌ Échec authentification avec 'Pharmacien123'")
            
            # Test sans mot de passe
            auth_user = authenticate(username='GLORIA1', password='')
            if auth_user:
                print("   ⚠ Authentification réussie avec mot de passe vide!")
            else:
                print("   ❌ Échec avec mot de passe vide")
        
        # 3. Vérifie les groupes
        print(f"\n👥 GROUPES:")
        groups = user.groups.all()
        if groups:
            for group in groups:
                print(f"   ✅ {group.name}")
                # Affiche les permissions du groupe
                for perm in group.permissions.all():
                    print(f"      - {perm.codename}")
        else:
            print("   ⚠ Aucun groupe")
        
        # 4. Vérifie les permissions directes
        print(f"\n🔑 PERMISSIONS DIRECTES:")
        permissions = user.user_permissions.all()
        if permissions:
            for perm in permissions:
                print(f"   - {perm.codename}")
        else:
            print("   ⚠ Aucune permission directe")
        
        # 5. Vérifie le profil associé
        print(f"\n👤 PROFIL ASSOCIÉ:")
        try:
            # Cherche un profil Membre
            from membres.models import Membre
            membre = Membre.objects.filter(user=user).first()
            if membre:
                print(f"   ✅ Membre trouvé:")
                print(f"      ID: {membre.id}")
                print(f"      Numéro: {membre.numero}")
                print(f"      Nom complet: {membre.nom_complet}")
                print(f"      Statut: {membre.statut}")
            else:
                print("   ⚠ Aucun membre associé")
        except Exception as e:
            print(f"   ⚠ Erreur recherche membre: {str(e)}")
        
        # 6. Vérifie le profil Pharmacien
        print(f"\n💊 PROFIL PHARMACIEN:")
        try:
            from pharmacien.models import Pharmacien
            pharmacien = Pharmacien.objects.filter(user=user).first()
            if pharmacien:
                print(f"   ✅ Pharmacien trouvé:")
                print(f"      ID: {pharmacien.id}")
                print(f"      Nom: {pharmacien.nom}")
                print(f"      Prénom: {pharmacien.prenom}")
                print(f"      Pharmacie: {pharmacien.pharmacie}")
            else:
                print("   ⚠ Aucun profil pharmacien associé")
        except Exception as e:
            print(f"   ⚠ Erreur recherche pharmacien: {str(e)}")
        
        return user
        
    except User.DoesNotExist:
        print("❌ Utilisateur GLORIA1 non trouvé dans la base de données!")
        return None
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def reinitialiser_gloria1():
    """Réinitialise complètement l'utilisateur GLORIA1"""
    print("\n" + "=" * 60)
    print("🔄 RÉINITIALISATION COMPLÈTE DE GLORIA1")
    print("=" * 60)
    
    User = get_user_model()
    
    try:
        with transaction.atomic():
            # 1. Récupère ou crée l'utilisateur
            user, created = User.objects.get_or_create(
                username='GLORIA1',
                defaults={
                    'email': 'gloria@pharmacie.com',
                    'first_name': 'GLORIA',
                    'last_name': 'NENE',
                    'is_active': True,
                    'is_staff': True,
                }
            )
            
            if created:
                print("✅ Utilisateur GLORIA1 créé")
            else:
                print("✅ Utilisateur GLORIA1 existant trouvé")
            
            # 2. Définit un mot de passe fort
            user.set_password('Pharmacien123!')
            
            # 3. Active l'utilisateur
            user.is_active = True
            user.is_staff = True
            user.is_superuser = False
            
            # 4. Sauvegarde
            user.save()
            print("✅ Mot de passe et paramètres mis à jour")
            
            # 5. Ajoute au groupe Pharmacien
            try:
                group, _ = Group.objects.get_or_create(name='Pharmacien')
                user.groups.add(group)
                print(f"✅ Ajouté au groupe '{group.name}'")
                
                # Ajoute les permissions nécessaires au groupe
                permissions_codes = [
                    'view_pharmacien', 'change_pharmacien',
                    'view_ordonnance', 'change_ordonnance',
                    'add_ordonnance', 'delete_ordonnance',
                ]
                
                for codename in permissions_codes:
                    try:
                        perm = Permission.objects.get(codename=codename)
                        group.permissions.add(perm)
                    except Permission.DoesNotExist:
                        pass
                
                print("✅ Permissions ajoutées au groupe Pharmacien")
                
            except Exception as e:
                print(f"⚠ Erreur gestion groupes: {str(e)}")
            
            # 6. Crée le profil Pharmacien associé
            try:
                from pharmacien.models import Pharmacien
                pharmacien, created_ph = Pharmacien.objects.get_or_create(
                    user=user,
                    defaults={
                        'nom': 'NENE',
                        'prenom': 'GLORIA',
                        'pharmacie': 'Pharmacie GLORIA',
                        'telephone': '+2250102030405',
                        'adresse': 'Abidjan, Côte d\'Ivoire',
                        'est_actif': True,
                    }
                )
                
                if created_ph:
                    print("✅ Profil Pharmacien créé")
                else:
                    print("✅ Profil Pharmacien existant mis à jour")
                    
            except Exception as e:
                print(f"⚠ Erreur création profil pharmacien: {str(e)}")
            
            # 7. Teste l'authentification
            print("\n🧪 TEST APRÈS RÉINITIALISATION:")
            auth_user = authenticate(username='GLORIA1', password='Pharmacien123!')
            if auth_user:
                print("✅ Authentification réussie!")
                print(f"   Username: {auth_user.username}")
                print(f"   Email: {auth_user.email}")
                print(f"   Groupes: {[g.name for g in auth_user.groups.all()]}")
            else:
                print("❌ Échec authentification après réinitialisation")
            
            return user
            
    except Exception as e:
        print(f"❌ Erreur réinitialisation: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_connexion_web():
    """Test de connexion via l'interface web"""
    print("\n" + "=" * 60)
    print("🌐 TEST DE CONNEXION VIA INTERFACE WEB")
    print("=" * 60)
    
    BASE_URL = "http://127.0.0.1:8000"
    session = requests.Session()
    
    try:
        # 1. Récupère la page de login
        print("1. Récupération de la page de login...")
        response = session.get(f"{BASE_URL}/accounts/login/")
        
        # 2. Extrait le token CSRF
        csrf_token = None
        csrf_match = re.search(r'csrfmiddlewaretoken[\'"] value=[\'"]([^\'"]+)', response.text)
        if csrf_match:
            csrf_token = csrf_match.group(1)
            print(f"✅ Token CSRF trouvé: {csrf_token[:20]}...")
        else:
            print("❌ Token CSRF non trouvé")
            return False
        
        # 3. Tente la connexion avec GLORIA1
        print("\n2. Tentative de connexion avec GLORIA1...")
        login_data = {
            'username': 'GLORIA1',
            'password': 'Pharmacien123!',  # Nouveau mot de passe
            'csrfmiddlewaretoken': csrf_token
        }
        
        response = session.post(
            f"{BASE_URL}/accounts/login/",
            data=login_data,
            headers={'Referer': f'{BASE_URL}/accounts/login/'},
            allow_redirects=False
        )
        
        print(f"📊 Réponse HTTP: {response.status_code}")
        print(f"📏 Taille réponse: {len(response.text)} caractères")
        
        if response.status_code == 302:
            print("✅ Connexion réussie! Redirection détectée")
            redirect_url = response.headers.get('Location', '')
            print(f"📍 Redirection vers: {redirect_url}")
            
            # Suit la redirection
            if redirect_url:
                response = session.get(f"{BASE_URL}{redirect_url}" if redirect_url.startswith('/') else redirect_url)
                print(f"✅ Page de redirection chargée (HTTP {response.status_code})")
                
                # Vérifie le contenu
                if 'GLORIA1' in response.text:
                    print("✅ Nom d'utilisateur trouvé dans la page")
                if 'Pharmacien' in response.text:
                    print("✅ Interface Pharmacien détectée")
                    
            return True
        else:
            print("❌ Pas de redirection - Connexion échouée")
            
            # Analyse l'erreur
            if 'error' in response.text.lower() or 'invalid' in response.text.lower():
                print("⚠ Message d'erreur détecté dans la page")
            
            # Affiche un extrait de la réponse
            print(f"\n📄 Extrait de la réponse (premiers 500 caractères):")
            print("-" * 50)
            print(response.text[:500])
            print("-" * 50)
            
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test web: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def generer_rapport():
    """Génère un rapport complet"""
    print("\n" + "=" * 60)
    print("📊 RAPPORT COMPLET")
    print("=" * 60)
    
    # Diagnostic initial
    user = diagnostic_complet()
    
    if not user:
        print("\n❌ GLORIA1 n'existe pas ou erreur de diagnostic")
        reponse = input("Voulez-vous créer GLORIA1 ? (o/N): ").lower()
        if reponse == 'o':
            user = reinitialiser_gloria1()
        else:
            return
    
    # Réinitialisation si nécessaire
    print("\n" + "=" * 60)
    reponse = input("Voulez-vous réinitialiser GLORIA1 ? (o/N): ").lower()
    if reponse == 'o':
        user = reinitialiser_gloria1()
    
    # Test de connexion web
    print("\n" + "=" * 60)
    reponse = input("Voulez-vous tester la connexion web ? (o/N): ").lower()
    if reponse == 'o':
        success = test_connexion_web()
        
        if success:
            print("\n✅ GLORIA1 peut maintenant se connecter!")
            print("\n🔧 POUR TESTER MANUELLEMENT:")
            print("1. Allez sur: http://127.0.0.1:8000/accounts/login/")
            print("2. Connectez-vous avec:")
            print("   - Username: GLORIA1")
            print("   - Password: Pharmacien123!")
            print("3. Vous devriez être redirigé vers /pharmacien/dashboard/")
        else:
            print("\n❌ Problème persistant avec GLORIA1")
            print("\n🔧 ACTIONS MANUELLES REQUISES:")
            print("1. Vérifiez dans l'admin Django: http://127.0.0.1:8000/admin/auth/user/")
            print("2. Cherchez GLORIA1 et vérifiez:")
            print("   - ✅ 'Active' est coché")
            print("   - ✅ 'Staff status' est coché")
            print("   - ✅ Le mot de passe est défini (click 'This user's password' pour vérifier)")

def main():
    """Fonction principale"""
    print("🚀 SCRIPT DE DIAGNOSTIC ET RÉPARATION - GLORIA1")
    print("=" * 60)
    
    # Vérifie que le serveur est accessible
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        print(f"✅ Serveur Django accessible (HTTP {response.status_code})")
    except:
        print("❌ Serveur non accessible. Démarrez-le avec:")
        print("   python manage.py runserver")
        return
    
    # Menu principal
    print("\n🔧 MENU PRINCIPAL:")
    print("1. Diagnostic complet de GLORIA1")
    print("2. Réinitialisation complète de GLORIA1")
    print("3. Test de connexion web")
    print("4. Génération de rapport complet")
    print("5. Quitter")
    
    choix = input("\nVotre choix (1-5): ").strip()
    
    if choix == "1":
        diagnostic_complet()
    elif choix == "2":
        reinitialiser_gloria1()
    elif choix == "3":
        test_connexion_web()
    elif choix == "4":
        generer_rapport()
    elif choix == "5":
        print("👋 Au revoir!")
        return
    else:
        print("❌ Choix invalide")
    
    print("\n" + "=" * 60)
    print("✅ OPÉRATION TERMINÉE")
    print("=" * 60)

if __name__ == "__main__":
    main()