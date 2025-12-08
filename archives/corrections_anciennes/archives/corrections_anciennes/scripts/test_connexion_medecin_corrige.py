#!/usr/bin/env python
"""
Script de test CORRIGÉ pour la connexion médecin - Adapté à la structure existante
"""

import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from medecin.models import Medecin, SpecialiteMedicale, EtablissementMedical

User = get_user_model()

def initialiser_donnees_test():
    """Initialise les données de test nécessaires"""
    print("🔧 Initialisation des données de test...")
    
    # Créer la spécialité médicale si elle n'existe pas
    specialite, created = SpecialiteMedicale.objects.get_or_create(
        nom='Généraliste',
        defaults={'description': 'Médecine générale'}
    )
    if created:
        print("   ✅ Spécialité 'Généraliste' créée")
    
    # Créer l'établissement médical si il n'existe pas
    etablissement, created = EtablissementMedical.objects.get_or_create(
        nom='Clinique Test',
        defaults={
            'type_etablissement': 'CLINIQUE',
            'adresse': '123 Rue Test, Abidjan',
            'telephone': '+2250102030405',
            'ville': 'Abidjan'
        }
    )
    if created:
        print("   ✅ Établissement 'Clinique Test' créé")
    
    # Créer le groupe médecin si il n'existe pas
    groupe_medecin, created = Group.objects.get_or_create(name='medecin')
    if created:
        print("   ✅ Groupe 'medecin' créé")
    
    return specialite, etablissement, groupe_medecin

def creer_medecin_test():
    """Crée un médecin de test avec la structure existante"""
    print("👨‍⚕️ Création du médecin de test...")
    
    specialite, etablissement, groupe_medecin = initialiser_donnees_test()
    
    try:
        # Créer l'utilisateur médecin
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
            
            # Ajouter l'utilisateur au groupe médecin
            user.groups.add(groupe_medecin)
            
            # Créer le profil médecin
            medecin, med_created = Medecin.objects.get_or_create(
                user=user,
                defaults={
                    'numero_ordre': 'MEDTEST001',
                    'specialite': specialite,
                    'etablissement': etablissement,
                    'telephone_pro': '+2250506070809',
                    'email_pro': 'dr.test@clinique.com',
                    'tarif_consultation': 15000,
                    'actif': True,
                    'disponible': True
                }
            )
            
            if med_created:
                print("   ✅ Médecin de test créé avec succès")
                print(f"   👤 Identifiants: dr.test / Medecin123!")
            else:
                print("   ℹ️  Médecin de test existe déjà")
        
        return user
        
    except Exception as e:
        print(f"   ❌ Erreur création médecin: {e}")
        return None

def test_connexion_medecin():
    """Tests de connexion pour l'application médecin"""
    print("\n🧪 TESTS DE CONNEXION MÉDECIN")
    print("=" * 60)
    
    client = Client()
    
    # 1. Test d'accès à la page de connexion
    print("1. Test page de connexion...")
    try:
        response = client.get('/medecin/connexion/')
        if response.status_code == 200:
            print("   ✅ Page connexion accessible")
        else:
            print(f"   ❌ Page connexion inaccessible (code: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # 2. Test de connexion avec identifiants valides
    print("2. Test connexion valide...")
    try:
        medecin_user = creer_medecin_test()
        
        response = client.post('/medecin/connexion/', {
            'username': 'dr.test',
            'password': 'Medecin123!'
        }, follow=True)
        
        if response.status_code == 200 and response.context['user'].is_authenticated:
            user = response.context['user']
            print(f"   ✅ Connexion réussie - Utilisateur: {user.username}")
            
            # Vérifier si l'utilisateur a un profil médecin
            if hasattr(user, 'medecin_profile'):
                print(f"   ✅ Profil médecin trouvé - Dr {user.get_full_name()}")
            else:
                print("   ⚠️  Aucun profil médecin trouvé")
                
        else:
            print("   ❌ Connexion échouée")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # 3. Test de connexion avec identifiants invalides
    print("3. Test connexion invalide...")
    try:
        response = client.post('/medecin/connexion/', {
            'username': 'utilisateur.inexistant',
            'password': 'MauvaisPassword123!'
        })
        
        if not response.context['user'].is_authenticated:
            print("   ✅ Connexion invalide correctement rejetée")
        else:
            print("   ❌ Connexion invalide anormalement acceptée")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # 4. Test d'accès au dashboard sans connexion
    print("4. Test accès dashboard sans connexion...")
    try:
        response = client.get('/medecin/dashboard/', follow=True)
        
        # Doit rediriger vers la page de connexion
        if response.redirect_chain and any('connexion' in url for url, status in response.redirect_chain):
            print("   ✅ Redirection vers connexion pour accès non authentifié")
        else:
            print("   ❌ Aucune redirection pour accès non authentifié")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # 5. Test de déconnexion
    print("5. Test déconnexion...")
    try:
        # Se connecter d'abord
        client.login(username='dr.test', password='Medecin123!')
        
        # Vérifier qu'on est connecté
        response = client.get('/medecin/dashboard/')
        est_connecte_avant = response.status_code == 200
        
        # Se déconnecter
        response = client.get('/medecin/deconnexion/', follow=True)
        est_connecte_apres = response.context['user'].is_authenticated
        
        if est_connecte_avant and not est_connecte_apres:
            print("   ✅ Déconnexion réussie")
        else:
            print(f"   ❌ Problème déconnexion - Avant: {est_connecte_avant}, Après: {est_connecte_apres}")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # 6. Test médecin inactif
    print("6. Test médecin inactif...")
    try:
        # Créer un médecin inactif
        user_inactif, created = User.objects.get_or_create(
            username='dr.inactif',
            defaults={
                'email': 'inactif@clinique.com',
                'first_name': 'Docteur',
                'last_name': 'Inactif',
                'is_active': True
            }
        )
        
        if created:
            user_inactif.set_password('Medecin123!')
            user_inactif.save()
            user_inactif.groups.add(Group.objects.get(name='medecin'))
            
            Medecin.objects.create(
                user=user_inactif,
                numero_ordre='MEDINACT001',
                specialite=specialite,
                etablissement=etablissement,
                telephone_pro='+2250102030405',
                actif=False,  # Médecin inactif
                disponible=False
            )
        
        # Tentative de connexion
        response = client.post('/medecin/connexion/', {
            'username': 'dr.inactif',
            'password': 'Medecin123!'
        })
        
        if not response.context['user'].is_authenticated:
            print("   ✅ Accès refusé pour médecin inactif")
        else:
            print("   ❌ Accès anormal pour médecin inactif")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("=" * 60)
    print("✅ TESTS TERMINÉS")

def verifier_structure_medecin():
    """Vérifie la structure des données médecin"""
    print("\n🔍 VÉRIFICATION STRUCTURE MÉDECIN")
    print("-" * 40)
    
    # Compter les médecins
    total_medecins = Medecin.objects.count()
    medecins_actifs = Medecin.objects.filter(actif=True).count()
    
    print(f"Total médecins dans la base: {total_medecins}")
    print(f"Médecins actifs: {medecins_actifs}")
    
    # Lister les médecins
    if total_medecins > 0:
        print("\n📋 Liste des médecins:")
        for medecin in Medecin.objects.all()[:5]:  # Premier 5 seulement
            statut = "✅ Actif" if medecin.actif else "❌ Inactif"
            print(f"   - Dr {medecin.user.get_full_name()} ({medecin.numero_ordre}) - {statut}")
    
    # Vérifier les groupes
    groupe_medecin = Group.objects.filter(name='medecin').first()
    if groupe_medecin:
        users_dans_groupe = groupe_medecin.user_set.count()
        print(f"\n👥 Utilisateurs dans le groupe 'medecin': {users_dans_groupe}")

if __name__ == "__main__":
    # Vérifier d'abord la structure
    verifier_structure_medecin()
    
    # Exécuter les tests
    test_connexion_medecin()
    
    print("\n📊 RÉSUMÉ:")
    print("Les tests vérifient:")
    print("  ✅ Page connexion accessible")
    print("  ✅ Connexion avec identifiants valides")
    print("  ✅ Rejet identifiants invalides")
    print("  ✅ Protection pages protégées")
    print("  ✅ Déconnexion fonctionnelle")
    print("  ✅ Gestion médecins inactifs")