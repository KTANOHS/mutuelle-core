#!/usr/bin/env python
"""
SCRIPT DE CORRECTION DES INTERACTIONS ENTRE ACTEURS
Résout les problèmes identifiés dans le diagnostic
"""

import os
import sys
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth.models import User
from django.db import transaction
from membres.models import Membre
from soins.models import BonDeSoin, Ordonnance

print("🔧 ===== CORRECTION DES INTERACTIONS ENTRE ACTEURS =====")
print()

# =============================================================================
# 1. CORRECTION DES BONS DE SOIN SANS MÉDECIN
# =============================================================================

print("1. 🏥 CORRECTION DES BONS DE SOIN SANS MÉDECIN")

try:
    # Récupérer un médecin pour assignation
    medecin_user = User.objects.filter(username__icontains='medecin').first()
    
    if medecin_user:
        # Récupérer les bons sans médecin assigné
        bons_sans_medecin = BonDeSoin.objects.filter(medecin__isnull=True)
        print(f"   📊 Bons sans médecin trouvés: {bons_sans_medecin.count()}")
        
        corrected_count = 0
        for bon in bons_sans_medecin:
            try:
                bon.medecin = medecin_user
                bon.save()
                corrected_count += 1
                print(f"      ✅ Bon #{bon.id} assigné au médecin {medecin_user.username}")
            except Exception as e:
                print(f"      ❌ Erreur correction bon #{bon.id}: {e}")
        
        print(f"   📈 Bons corrigés: {corrected_count}/{bons_sans_medecin.count()}")
    else:
        print("   ❌ Aucun médecin trouvé pour l'assignation")
        
except Exception as e:
    print(f"   ❌ Erreur correction bons: {e}")

print()

# =============================================================================
# 2. CRÉATION DE COTISATIONS DE TEST POUR ASSUREURS
# =============================================================================

print("2. 💰 CRÉATION DE COTISATIONS DE TEST")

try:
    # Essayer d'importer le modèle Cotisation
    from cotisations.models import Cotisation
    
    # Récupérer des membres pour créer des cotisations
    membres_test = Membre.objects.all()[:3]
    assureur_user = User.objects.filter(username__icontains='assureur').first()
    
    if assureur_user and membres_test:
        created_count = 0
        for membre in membres_test:
            try:
                # Vérifier si une cotisation existe déjà
                if not Cotisation.objects.filter(membre=membre, periode='2025-11').exists():
                    cotisation = Cotisation.objects.create(
                        membre=membre,
                        periode='2025-11',
                        type_cotisation='normale',
                        montant=5000.00,
                        date_echeance='2025-12-01',
                        enregistre_par=assureur_user
                    )
                    created_count += 1
                    print(f"      ✅ Cotisation créée pour {membre.prenom} {membre.nom}")
            except Exception as e:
                print(f"      ❌ Erreur création cotisation: {e}")
        
        print(f"   📈 Cotisations créées: {created_count}")
    else:
        print("   ℹ️  Module cotisations disponible mais données insuffisantes")
        
except ImportError:
    print("   ❌ Module cotisations non disponible - Installation nécessaire")
    print("   💡 Commande: pip install django-cotisations ou création manuelle")
except Exception as e:
    print(f"   ❌ Erreur création cotisations: {e}")

print()

# =============================================================================
# 3. CORRECTION DE LA STRUCTURE DES ORDONNANCES
# =============================================================================

print("3. 💊 CORRECTION DE LA STRUCTURE DES ORDONNANCES")

try:
    # Vérifier la structure du modèle Ordonnance
    ordonnance_fields = [f.name for f in Ordonnance._meta.get_fields()]
    print(f"   📋 Champs Ordonnance: {ordonnance_fields}")
    
    # Créer une ordonnance de test si possible
    if 'bon_de_soin' in ordonnance_fields:
        bon_test = BonDeSoin.objects.first()
        medecin_test = User.objects.filter(username__icontains='medecin').first()
        
        if bon_test and medecin_test:
            try:
                ordonnance, created = Ordonnance.objects.get_or_create(
                    bon_de_soin=bon_test,
                    defaults={
                        'date_prescription': datetime.now().date(),
                        'statut': 'active',
                    }
                )
                if created:
                    print(f"      ✅ Ordonnance de test créée (ID: {ordonnance.id})")
                else:
                    print(f"      ℹ️  Ordonnance existante (ID: {ordonnance.id})")
            except Exception as e:
                print(f"      ❌ Erreur création ordonnance: {e}")
    else:
        print("   ❌ Structure Ordonnance incorrecte - champ 'bon_de_soin' manquant")
        
except Exception as e:
    print(f"   ❌ Erreur analyse ordonnances: {e}")

print()

# =============================================================================
# 4. CRÉATION DE MOTS DE PASSE POUR LES TESTS
# =============================================================================

print("4. 🔐 CRÉATION DE MOTS DE PASSE POUR LES TESTS")

try:
    test_password = "test123"
    users_updated = 0
    
    # Mettre à jour les mots de passe des utilisateurs de test
    test_users = User.objects.filter(
        username__in=['test_agent', 'assureur_test', 'medecin_test', 'test_pharmacien']
    )
    
    for user in test_users:
        user.set_password(test_password)
        user.save()
        users_updated += 1
        print(f"      ✅ Mot de passe défini pour {user.username}")
    
    print(f"   📈 Utilisateurs mis à jour: {users_updated}")
    
except Exception as e:
    print(f"   ❌ Erreur mise à jour mots de passe: {e}")

print()

# =============================================================================
# 5. CRÉATION DE DONNÉES DE TEST POUR LE WORKFLOW COMPLET
# =============================================================================

print("5. 🔄 CRÉATION D'UN WORKFLOW COMPLET DE TEST")

try:
    with transaction.atomic():
        # 1. Membre créé par agent
        membre_workflow, created = Membre.objects.get_or_create(
            numero_unique="WORKFLOW_TEST",
            defaults={
                'nom': 'Workflow',
                'prenom': 'Test',
                'telephone': '0100000999',
                'statut': 'actif',
            }
        )
        
        if created:
            print("      ✅ Membre de workflow créé")
            
            # 2. Bon de soin créé par agent
            bon_workflow = BonDeSoin.objects.create(
                patient=membre_workflow,
                date_soin=datetime.now().date(),
                symptomes="Test symptômes",
                diagnostic="Test diagnostic",
                montant=7500.00,
                statut='attente'
            )
            print("      ✅ Bon de soin de workflow créé")
            
            # 3. Assigner un médecin au bon
            medecin_workflow = User.objects.filter(username__icontains='medecin').first()
            if medecin_workflow:
                bon_workflow.medecin = medecin_workflow
                bon_workflow.save()
                print("      ✅ Médecin assigné au bon")
            
            # 4. Créer une ordonnance si possible
            try:
                ordonnance_workflow = Ordonnance.objects.create(
                    bon_de_soin=bon_workflow,
                    date_prescription=datetime.now().date(),
                    statut='active'
                )
                print("      ✅ Ordonnance de workflow créée")
            except Exception as e:
                print(f"      ℹ️  Ordonnance non créée: {e}")
                
        else:
            print("      ℹ️  Membre de workflow existant")
            
except Exception as e:
    print(f"   ❌ Erreur création workflow: {e}")

print()

# =============================================================================
# 6. VÉRIFICATION DES CORRECTIONS APPLIQUÉES
# =============================================================================

print("6. ✅ VÉRIFICATION DES CORRECTIONS")

# Vérifier les bons avec médecin assigné
try:
    bons_avec_medecin = BonDeSoin.objects.filter(medecin__isnull=False).count()
    print(f"   🏥 Bons avec médecin assigné: {bons_avec_medecin}")
except:
    print("   🏥 Bons avec médecin: Erreur vérification")

# Vérifier les ordonnances
try:
    ordonnances_count = Ordonnance.objects.count()
    print(f"   💊 Ordonnances existantes: {ordonnances_count}")
except:
    print("   💊 Ordonnances: Erreur vérification")

# Vérifier les utilisateurs avec mot de passe
try:
    users_avec_password = User.objects.exclude(password='').count()
    print(f"   🔐 Utilisateurs avec mot de passe: {users_avec_password}")
except:
    print("   🔐 Utilisateurs: Erreur vérification")

print()

# =============================================================================
# 7. RECOMMANDATIONS FINALES
# =============================================================================

print("7. 🎯 RECOMMANDATIONS FINALES")

print("""
   🔧 ACTIONS IMMÉDIATES REQUISES:

   1. INSTALLATION MODULE COTISATIONS
      - pip install django-cotisations
      - Ou créer le modèle manuellement dans cotisations/models.py

   2. CORRECTION MODÈLE ORDONNANCE
      - Ajouter les champs manquants: patient, medecin_prescripteur
      - Mettre à jour les relations ForeignKey

   3. CONFIGURATION WORKFLOW COMPLET
      - Agent crée membre → Agent crée bon → Médecin traite bon → 
        Médecin crée ordonnance → Pharmacien voit ordonnance

   4. TEST DES INTERACTIONS
      - Relancer le diagnostic après corrections
      - Tester chaque étape du workflow manuellement

   📋 PROCHAINES ÉTAPES:

   • Tester la création de membre par agent
   • Vérifier que l'assureur voit les membres
   • Tester la création de bon par agent  
   • Vérifier que le médecin voit le bon
   • Tester la création d'ordonnance par médecin
   • Vérifier que le pharmacien voit l'ordonnance
""")

print("🔧 ===== CORRECTIONS TERMINÉES =====")