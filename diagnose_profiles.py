#!/usr/bin/env python
"""
DIAGNOSTIC DES RELATIONS DE PROFIL
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model

def diagnose_profiles():
    print("🔧 DIAGNOSTIC DES RELATIONS DE PROFIL")
    print("=" * 50)
    
    User = get_user_model()
    
    try:
        user = User.objects.get(username='test_agent')
        print(f"👤 Utilisateur: {user.username} (ID: {user.id})")
        
        # Vérifier toutes les relations possibles
        relations = ['agent', 'membre', 'assureur', 'medecin', 'pharmacien']
        
        for relation in relations:
            try:
                has_relation = hasattr(user, relation)
                relation_obj = getattr(user, relation, None)
                exists = relation_obj is not None
                
                print(f"🔍 {relation}: {has_relation} (existe: {exists})")
                
                if exists:
                    print(f"   📝 Détails: {relation_obj}")
                    
            except Exception as e:
                print(f"❌ Erreur vérification {relation}: {e}")
        
        # Vérifier les groupes
        print(f"🔍 Groupes: {list(user.groups.all().values_list('name', flat=True))}")
        
    except Exception as e:
        print(f"❌ Erreur diagnostic: {e}")

if __name__ == "__main__":
    diagnose_profiles()