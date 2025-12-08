#!/usr/bin/env python
"""
TEST EN TEMPS RÉEL - CRÉATION/RECHERCHE MEMBRE (CORRIGÉ)
"""

import os
import sys
import django
from django.db.models import Q
import random
import string

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from membres.models import Membre
from django.utils import timezone
import time

def generer_numero_unique():
    """Génère un numéro unique aléatoire pour éviter les conflits"""
    lettres = ''.join(random.choices(string.ascii_uppercase, k=3))
    chiffres = ''.join(random.choices(string.digits, k=3))
    return f"MEM{lettres}{chiffres}"

def test_temps_reel():
    """Test de création et recherche immédiate d'un membre"""
    
    print("🧪 TEST TEMPS RÉEL - CRÉATION/RECHERCHE (CORRIGÉ)")
    print("=" * 60)
    
    # 1. Compter les membres avant
    avant = Membre.objects.count()
    print(f"📊 Membres avant test: {avant}")
    
    # 2. Créer un membre unique avec numéro unique aléatoire
    timestamp = int(time.time())
    numero_unique = generer_numero_unique()
    
    try:
        membre_test = Membre.objects.create(
            nom=f"TEST_{timestamp}",
            prenom=f"Recherche_{timestamp}",
            telephone=f"01{timestamp % 100000000:08d}",
            numero_unique=numero_unique,  # NUMÉRO UNIQUE UNIQUE !
            statut="actif"
        )
        
        print(f"✅ Membre créé - ID: {membre_test.id}")
        print(f"   📝 Nom: {membre_test.prenom} {membre_test.nom}")
        print(f"   📞 Téléphone: {membre_test.telephone}")
        print(f"   🔑 Numéro unique: {membre_test.numero_unique}")
        
        # 3. Recherche IMMÉDIATE par différents critères
        print("\n🔍 RECHERCHE IMMÉDIATE:")
        
        # Par ID exact
        result_id = Membre.objects.filter(id=membre_test.id)
        print(f"   • Par ID {membre_test.id}: {result_id.count()} résultat")
        
        # Par nom
        result_nom = Membre.objects.filter(nom__icontains=f"TEST_{timestamp}")
        print(f"   • Par nom 'TEST_{timestamp}': {result_nom.count()} résultat")
        
        # Par prénom  
        result_prenom = Membre.objects.filter(prenom__icontains=f"Recherche_{timestamp}")
        print(f"   • Par prénom 'Recherche_{timestamp}': {result_prenom.count()} résultat")
        
        # Par téléphone
        result_tel = Membre.objects.filter(telephone__icontains=membre_test.telephone)
        print(f"   • Par téléphone: {result_tel.count()} résultat")
        
        # Par numéro unique
        result_num = Membre.objects.filter(numero_unique=numero_unique)
        print(f"   • Par numéro unique: {result_num.count()} résultat")
        
        # Recherche combinée (comme dans l'API)
        result_api_style = Membre.objects.filter(
            Q(nom__icontains=f"TEST_{timestamp}") |
            Q(prenom__icontains=f"Recherche_{timestamp}") |
            Q(telephone__icontains=membre_test.telephone) |
            Q(numero_unique__icontains=numero_unique)
        )
        print(f"   • Recherche API style: {result_api_style.count()} résultat")
        
        # 4. Vérification finale
        apres = Membre.objects.count()
        print(f"\n📊 Membres après test: {apres}")
        print(f"📈 Différence: {apres - avant} membre(s) ajouté(s)")
        
        if result_api_style.count() == 1:
            print("🎉 SUCCÈS: Le membre est trouvable immédiatement après création!")
            return True
        else:
            print("❌ PROBLÈME: Le membre n'est pas trouvable après création!")
            return False
            
    except Exception as e:
        print(f"❌ ERREUR création membre: {e}")
        return False

if __name__ == "__main__":
    test_temps_reel()