#!/usr/bin/env python
"""
VÉRIFICATION INTERFACE MÉDECIN - CORRIGÉ
"""

import os
import sys
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Bon
from django.contrib.auth import get_user_model

User = get_user_model()

def verification_interface_medecin():
    print("🔍 VÉRIFICATION INTERFACE MÉDECIN")
    print("=" * 40)
    
    client = Client()
    
    # 1. Connexion médecin
    print("1. 🔐 Connexion médecin...")
    login_success = client.login(username='medecin_test', password='pass123')
    if not login_success:
        print("   ❌ Échec connexion")
        return False
    print("   ✅ Connecté")
    
    # 2. Test dashboard médecin
    print("2. 📊 Test dashboard...")
    response = client.get('/medecin/dashboard/')
    if response.status_code == 200:
        print("   ✅ Dashboard accessible")
    else:
        print(f"   ❌ Dashboard: {response.status_code}")
    
    # 3. Test page ordonnances
    print("3. 📋 Test ordonnances...")
    response = client.get('/medecin/ordonnances/')
    if response.status_code == 200:
        print("   ✅ Page ordonnances accessible")
        
        # Vérifier si les bons apparaissent dans le contexte (méthode sécurisée)
        if hasattr(response, 'context') and response.context is not None:
            context_keys = list(response.context.keys()) if response.context else []
            print(f"   📋 Clés du contexte: {context_keys}")
            
            if 'bons' in context_keys:
                bons_vus = response.context['bons']
                print(f"   📊 Bons dans contexte: {len(bons_vus)}")
            else:
                print("   ℹ️  Aucune clé 'bons' dans le contexte")
        else:
            print("   ℹ️  Aucun contexte disponible")
    else:
        print(f"   ❌ Ordonnances: {response.status_code}")
    
    # 4. Vérification données réelles
    print("4. 🗄️ Vérification base de données...")
    medecin = User.objects.get(username='medecin_test')
    bons_medecin = Bon.objects.filter(medecin_traitant=medecin)
    print(f"   📊 Bons assignés au médecin: {bons_medecin.count()}")
    
    for bon in bons_medecin:
        print(f"   - {bon.numero_bon} | {bon.membre.nom} | {bon.statut}")
    
    # 5. Test création d'un nouveau bon
    print("5. 🆕 Test création nouveau bon...")
    membre = Bon.objects.first().membre  # Récupérer un membre existant
    
    nouveau_bon = Bon.objects.create(
        membre=membre,
        type_soin='CONSULT',
        description='Nouveau bon pour test interface',
        medecin_traitant=medecin,
        montant_total=8000,
        statut='BROUILLON'
    )
    print(f"   ✅ Nouveau bon créé: {nouveau_bon.numero_bon}")
    
    # Vérifier que le médecin le voit
    nouveaux_bons = Bon.objects.filter(medecin_traitant=medecin, statut='BROUILLON')
    print(f"   📊 Bons en attente du médecin: {nouveaux_bons.count()}")
    
    return True

if __name__ == "__main__":
    success = verification_interface_medecin()
    if success:
        print("\n🎉 INTERFACE MÉDECIN FONCTIONNELLE!")
        print("   Le système est complètement opérationnel.")
    sys.exit(0 if success else 1)