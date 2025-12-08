#!/usr/bin/env python
import os
import sys
import django
from django.test import RequestFactory
from django.contrib.auth.models import User

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from medecin.views import creer_consultation
from medecin.models import Medecin

def test_consultation_view():
    """
    Test unitaire de la vue creer_consultation
    """
    print("=" * 50)
    print("🧪 TEST VUE CREER_CONSULTATION")
    print("=" * 50)
    
    # Créer une requête factice
    factory = RequestFactory()
    
    # 1. Test avec utilisateur normal (sans profil médecin)
    print("\n1. Test utilisateur sans profil médecin:")
    try:
        user = User.objects.filter(medecin_profile__isnull=True).first()
        if user:
            request = factory.get('/medecin/creer-consultation/')
            request.user = user
            request.method = 'GET'
            
            response = creer_consultation(request)
            print(f"   Status: {response.status_code}")
            print(f"   Redirection: {getattr(response, 'url', 'Non')}")
        else:
            print("   ⚠ Aucun utilisateur sans profil médecin trouvé")
    except Exception as e:
        print(f"   ✗ ERREUR: {e}")
    
    # 2. Test avec utilisateur médecin
    print("\n2. Test utilisateur avec profil médecin:")
    try:
        medecin_user = User.objects.filter(medecin_profile__isnull=False).first()
        if medecin_user:
            request = factory.get('/medecin/creer-consultation/')
            request.user = medecin_user
            request.method = 'GET'
            
            response = creer_consultation(request)
            print(f"   Status: {response.status_code}")
            print(f"   Template: {getattr(response, 'template_name', 'Non défini')}")
        else:
            print("   ⚠ Aucun utilisateur médecin trouvé")
    except Exception as e:
        print(f"   ✗ ERREUR: {e}")
    
    # 3. Vérifier le contexte
    print("\n3. Vérification du contexte:")
    try:
        if medecin_user:
            request = factory.get('/medecin/creer-consultation/')
            request.user = medecin_user
            request.method = 'GET'
            
            response = creer_consultation(request)
            if hasattr(response, 'context_data'):
                context = response.context_data
                print(f"   ✓ Contexte disponible")
                print(f"   - Patients: {len(context.get('patients', []))}")
                print(f"   - Types consultation: {len(context.get('types_consultation', []))}")
                print(f"   - Médecin: {context.get('medecin')}")
            else:
                print("   ⚠ Pas de contexte disponible")
    except Exception as e:
        print(f"   ✗ ERREUR Contexte: {e}")

if __name__ == "__main__":
    test_consultation_view()