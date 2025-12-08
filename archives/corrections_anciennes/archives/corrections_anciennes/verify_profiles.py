#!/usr/bin/env python
"""
VÉRIFICATION FINALE DES PROFILS
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.utils import *

def verify_all_profiles():
    print("🔍 VÉRIFICATION COMPLÈTE DES PROFILS")
    print("=" * 50)
    
    User = get_user_model()
    
    test_users = [
        'test_agent', 'test_membre', 'test_assureur', 'test_medecin', 'test_pharmacien'
    ]
    
    results = {}
    
    for username in test_users:
        print(f"\n--- Vérification: {username} ---")
        
        try:
            user = User.objects.get(username=username)
            
            # Test de base
            group = get_user_primary_group(user)
            redirect_url = get_user_redirect_url(user)
            has_profile = user_has_profile(user, group.lower())
            
            print(f"✅ Groupe détecté: {group}")
            print(f"✅ Redirection: {redirect_url}")
            print(f"✅ Profil existant: {has_profile}")
            
            # Informations détaillées
            profile_data = get_user_profile_data(user)
            print(f"✅ Données profil: {profile_data}")
            
            # Vérification de la cohérence
            expected_type = username.split('_')[1].upper()  # 'test_agent' -> 'AGENT'
            is_correct = group == expected_type
            
            if is_correct:
                print("🎯 PROFIL CORRECT!")
                results[username] = True
            else:
                print(f"⚠️  INCOHÉRENCE: Attendu {expected_type}, obtenu {group}")
                results[username] = False
                
        except User.DoesNotExist:
            print(f"❌ Utilisateur non trouvé")
            results[username] = False
        except Exception as e:
            print(f"❌ Erreur: {e}")
            results[username] = False
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSULTATS DE VÉRIFICATION")
    print("=" * 50)
    
    total_success = sum(results.values())
    total_tests = len(results)
    
    for username, success in results.items():
        status = "✅ SUCCÈS" if success else "❌ ÉCHEC"
        print(f"{username}: {status}")
    
    print(f"\n🎯 SCORE: {total_success}/{total_tests}")
    
    if total_success == total_tests:
        print("🎉 TOUS LES PROFILS SONT CORRECTEMENT CONFIGURÉS!")
    else:
        print("⚠️  Certains profils nécessitent une correction")
    
    return total_success == total_tests

if __name__ == "__main__":
    success = verify_all_profiles()
    sys.exit(0 if success else 1)