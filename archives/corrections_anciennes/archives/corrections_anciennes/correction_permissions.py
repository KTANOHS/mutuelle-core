#!/usr/bin/env python
"""
SCRIPT DE CORRECTION DES PERMISSIONS ASSUREUR
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.test import RequestFactory
from membres.models import Membre

def verifier_permissions_assureur():
    """Vérifie les permissions de l'utilisateur assureur"""
    print("🔐 VÉRIFICATION DES PERMISSIONS ASSUREUR")
    print("=" * 60)
    
    # 1. Vérifier le groupe Assureur
    try:
        groupe_assureur, created = Group.objects.get_or_create(name='Assureur')
        if created:
            print("✅ Groupe 'Assureur' créé")
        else:
            print("✅ Groupe 'Assureur' existe déjà")
    except Exception as e:
        print(f"❌ Erreur groupe Assureur: {e}")
    
    # 2. Vérifier les utilisateurs assureurs
    print("\n👥 UTILISATEURS ASSUREURS:")
    assureurs = User.objects.filter(groups__name='Assureur')
    
    if not assureurs.exists():
        print("❌ Aucun utilisateur avec le groupe 'Assureur'")
        print("🔧 Attribution du groupe à l'utilisateur test...")
        
        # Attribuer le groupe à l'utilisateur test_assureur
        try:
            user_assureur = User.objects.get(username='test_assureur')
            user_assureur.groups.add(groupe_assureur)
            print(f"✅ Groupe 'Assureur' attribué à: {user_assureur.username}")
        except User.DoesNotExist:
            print("❌ Utilisateur test_assureur non trouvé")
    else:
        for user in assureurs:
            print(f"✅ {user.username} - {user.first_name} {user.last_name}")
    
    # 3. Tester la permission avec le décorateur
    print("\n🔍 TEST DU DÉCORATEUR DE PERMISSION:")
    
    # Fonction test pour vérifier le décorateur
    @user_passes_test(lambda u: u.groups.filter(name='Assureur').exists())
    def test_vue_assureur():
        return "ACCÈS AUTORISÉ"
    
    # Tester avec un utilisateur assureur
    try:
        user_assureur = User.objects.filter(groups__name='Assureur').first()
        if user_assureur:
            factory = RequestFactory()
            request = factory.get('/')
            request.user = user_assureur
            
            # Tester la fonction
            result = test_vue_assureur()
            print(f"✅ Test permission assureur: {result}")
        else:
            print("❌ Aucun utilisateur assureur pour tester")
    except Exception as e:
        print(f"❌ Erreur test permission: {e}")

def creer_utilisateur_assureur_complet():
    """Crée un utilisateur assureur complet si nécessaire"""
    print("\n🔧 CRÉATION UTILISATEUR ASSUREUR COMPLET:")
    
    try:
        # Créer ou récupérer le groupe Assureur
        groupe_assureur, _ = Group.objects.get_or_create(name='Assureur')
        
        # Créer un utilisateur assureur complet
        user, created = User.objects.get_or_create(
            username='assureur_complet',
            defaults={
                'first_name': 'Assureur',
                'last_name': 'Professionnel',
                'email': 'assureur@mutuelle.com',
                'password': 'password123',
                'is_staff': True
            }
        )
        
        if created:
            user.groups.add(groupe_assureur)
            print(f"✅ Utilisateur assureur créé: {user.username}")
        else:
            print(f"ℹ️ Utilisateur assureur existe déjà: {user.username}")
            
        return user
        
    except Exception as e:
        print(f"❌ Erreur création utilisateur assureur: {e}")
        return None

def tester_acces_membre_5():
    """Teste l'accès au membre ID 5"""
    print("\n🔍 TEST ACCÈS MEMBRE ID 5:")
    
    try:
        membre = Membre.objects.get(id=5)
        print(f"✅ Membre ID 5 trouvé: {membre.nom_complet}")
        print(f"   Numéro: {membre.numero_unique}")
        print(f"   Email: {membre.email}")
        print(f"   Statut: {membre.get_statut_display()}")
        
        # Vérifier si le membre peut avoir des bons
        if membre.est_a_jour():
            print("✅ Membre à jour de cotisation")
        else:
            print("⚠️  Membre non à jour de cotisation")
            
        if membre.est_document_valide():
            print("✅ Documents validés")
        else:
            print("⚠️  Documents en attente de validation")
            
    except Membre.DoesNotExist:
        print("❌ Membre ID 5 non trouvé")
    except Exception as e:
        print(f"❌ Erreur accès membre 5: {e}")

if __name__ == "__main__":
    print("🎯 CORRECTION PERMISSIONS ASSUREUR")
    print("=" * 60)
    
    verifier_permissions_assureur()
    creer_utilisateur_assureur_complet()
    tester_acces_membre_5()
    
    print("\n" + "=" * 60)
    print("🎯 INSTRUCTIONS:")
    print("1. Connectez-vous avec l'utilisateur: assureur_complet / password123")
    print("2. OU avec: test_assureur (si le mot de passe est connu)")
    print("3. Accédez à: http://127.0.0.1:8000/assureur/bons/creer/5/")