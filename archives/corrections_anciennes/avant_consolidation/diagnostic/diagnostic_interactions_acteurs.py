#!/usr/bin/env python
"""
DIAGNOSTIC COMPLET DES INTERACTIONS ENTRE ACTEURS
Vérifie la visibilité et synchronisation des données entre tous les acteurs
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q

print("🔍 ===== DIAGNOSTIC DES INTERACTIONS ENTRE ACTEURS =====")
print()

# =============================================================================
# 1. VÉRIFICATION DES MODÈLES ET ACTEURS
# =============================================================================

print("1. 👥 VÉRIFICATION DES ACTEURS ET MODÈLES")

# Récupération des utilisateurs par rôle
try:
    # Agents
    agents = User.objects.filter(
        Q(groups__name='Agents') | 
        Q(username__icontains='agent') |
        Q(email__icontains='agent')
    )
    print(f"   ✅ Agents trouvés: {agents.count()}")
    for agent in agents[:3]:
        print(f"      - {agent.username} ({agent.email})")
    
    # Assureurs
    assureurs = User.objects.filter(
        Q(groups__name='Assureurs') |
        Q(username__icontains='assureur') |
        Q(email__icontains='assureur')
    )
    print(f"   ✅ Assureurs trouvés: {assureurs.count()}")
    for assureur in assureurs[:3]:
        print(f"      - {assureur.username} ({assureur.email})")
    
    # Médecins
    medecins = User.objects.filter(
        Q(groups__name='Médecins') |
        Q(username__icontains='medecin') |
        Q(email__icontains='medecin')
    )
    print(f"   ✅ Médecins trouvés: {medecins.count()}")
    for medecin in medecins[:3]:
        print(f"      - {medecin.username} ({medecin.email})")
    
    # Pharmaciens
    pharmaciens = User.objects.filter(
        Q(groups__name='Pharmaciens') |
        Q(username__icontains='pharmacien') |
        Q(email__icontains='pharmacien')
    )
    print(f"   ✅ Pharmaciens trouvés: {pharmaciens.count()}")
    for pharmacien in pharmaciens[:3]:
        print(f"      - {pharmacien.username} ({pharmacien.email})")
        
except Exception as e:
    print(f"   ❌ Erreur récupération acteurs: {e}")

print()

# =============================================================================
# 2. DIAGNOSTIC MEMBRES - VISIBILITÉ
# =============================================================================

print("2. 👤 DIAGNOSTIC MEMBRES - VISIBILITÉ ENTRE ACTEURS")

try:
    from membres.models import Membre
    
    # Membres créés récemment
    membres_recents = Membre.objects.order_by('-date_inscription')[:5]
    print(f"   📊 Membres récents trouvés: {membres_recents.count()}")
    
    for membre in membres_recents:
        print(f"      👤 {membre.prenom} {membre.nom} (ID: {membre.id})")
        print(f"         📅 Créé le: {membre.date_inscription}")
        print(f"         🔢 Numéro: {getattr(membre, 'numero_unique', 'N/A')}")
        print(f"         📞 Téléphone: {getattr(membre, 'telephone', 'N/A')}")
        print(f"         ✅ Statut: {getattr(membre, 'statut', 'N/A')}")
        
        # Vérifier si le membre a des cotisations
        try:
            from cotisations.models import Cotisation
            cotisations = Cotisation.objects.filter(membre=membre)
            print(f"         💰 Cotisations: {cotisations.count()}")
        except ImportError:
            print("         💰 Cotisations: Module non disponible")
        
        # Vérifier si le membre a des bons
        try:
            from soins.models import BonDeSoin
            bons = BonDeSoin.objects.filter(patient=membre)
            print(f"         🏥 Bons de soin: {bons.count()}")
        except ImportError:
            print("         🏥 Bons de soin: Module non disponible")
            
        print()
        
except Exception as e:
    print(f"   ❌ Erreur diagnostic membres: {e}")

print()

# =============================================================================
# 3. DIAGNOSTIC COTISATIONS - SYNCHRONISATION
# =============================================================================

print("3. 💰 DIAGNOSTIC COTISATIONS - SYNCHRONISATION ASSUREUR/AGENT")

try:
    from cotisations.models import Cotisation
    
    cotisations = Cotisation.objects.select_related('membre', 'enregistre_par')[:5]
    print(f"   📊 Cotisations trouvées: {cotisations.count()}")
    
    for cotisation in cotisations:
        print(f"      💳 Cotisation #{getattr(cotisation, 'reference', cotisation.id)}")
        print(f"         👤 Membre: {cotisation.membre.prenom} {cotisation.membre.nom}")
        print(f"         👨‍💼 Enregistrée par: {getattr(cotisation.enregistre_par, 'username', 'N/A')}")
        print(f"         💵 Montant: {getattr(cotisation, 'montant', 'N/A')}")
        print(f"         📅 Échéance: {getattr(cotisation, 'date_echeance', 'N/A')}")
        print(f"         ✅ Statut: {getattr(cotisation, 'statut', 'N/A')}")
        
        # Vérifier si l'agent peut voir cette cotisation
        try:
            from agents.views import verifier_statut_cotisation_simple
            statut_agent = verifier_statut_cotisation_simple(cotisation.membre)
            print(f"         🔍 Statut visible par agent: {'✅ OUI' if statut_agent is not None else '❌ NON'}")
        except Exception as e:
            print(f"         🔍 Statut visible par agent: ❌ Erreur - {e}")
            
        print()
        
except ImportError:
    print("   ❌ Module cotisations non disponible")
except Exception as e:
    print(f"   ❌ Erreur diagnostic cotisations: {e}")

print()

# =============================================================================
# 4. DIAGNOSTIC BONS DE SOIN - VISIBILITÉ AGENT/MÉDECIN
# =============================================================================

print("4. 🏥 DIAGNOSTIC BONS DE SOIN - VISIBILITÉ AGENT/MÉDECIN")

try:
    from soins.models import BonDeSoin
    
    bons = BonDeSoin.objects.select_related('patient', 'medecin')[:5]
    print(f"   📊 Bons de soin trouvés: {bons.count()}")
    
    for bon in bons:
        print(f"      📋 Bon #{bon.id}")
        print(f"         👤 Patient: {bon.patient.prenom} {bon.patient.nom}")
        print(f"         👨‍⚕️ Médecin: {getattr(bon.medecin, 'username', 'Non assigné')}")
        print(f"         📅 Date soin: {getattr(bon, 'date_soin', 'N/A')}")
        print(f"         💵 Montant: {getattr(bon, 'montant', 'N/A')}")
        print(f"         ✅ Statut: {getattr(bon, 'statut', 'N/A')}")
        
        # Vérifier la création par agent
        print(f"         👨‍💼 Créé par agent: {'✅ OUI' if hasattr(bon, 'created_by') and bon.created_by else '❌ NON'}")
        
        # Vérifier la visibilité par médecin
        medecin_peut_voir = hasattr(bon, 'medecin') and bon.medecin
        print(f"         👨‍⚕️ Visible par médecin: {'✅ OUI' if medecin_peut_voir else '❌ NON'}")
        
        print()
        
except ImportError:
    print("   ❌ Module soins non disponible")
except Exception as e:
    print(f"   ❌ Erreur diagnostic bons de soin: {e}")

print()

# =============================================================================
# 5. DIAGNOSTIC ORDONNANCES - VISIBILITÉ MÉDECIN/PHARMACIEN
# =============================================================================

print("5. 💊 DIAGNOSTIC ORDONNANCES - VISIBILITÉ MÉDECIN/PHARMACIEN")

try:
    from soins.models import Ordonnance
    
    ordonnances = Ordonnance.objects.select_related('patient', 'medecin_prescripteur')[:5]
    print(f"   📊 Ordonnances trouvées: {ordonnances.count()}")
    
    for ordonnance in ordonnances:
        print(f"      📝 Ordonnance #{ordonnance.id}")
        print(f"         👤 Patient: {ordonnance.patient.prenom} {ordonnance.patient.nom}")
        print(f"         👨‍⚕️ Médecin: {getattr(ordonnance.medecin_prescripteur, 'username', 'Non assigné')}")
        print(f"         📅 Date: {getattr(ordonnance, 'date_prescription', 'N/A')}")
        print(f"         ✅ Statut: {getattr(ordonnance, 'statut', 'N/A')}")
        
        # Vérifier la visibilité par pharmacien
        try:
            from pharmacien.views import peut_voir_ordonnance
            visible_pharmacien = peut_voir_ordonnance(ordonnance)
            print(f"         🏥 Visible par pharmacien: {'✅ OUI' if visible_pharmacien else '❌ NON'}")
        except:
            print(f"         🏥 Visible par pharmacien: {'✅ Structure OK' if hasattr(ordonnance, 'patient') else '❌ Structure incomplète'}")
        
        print()
        
except ImportError:
    print("   ❌ Module ordonnances non disponible")
except Exception as e:
    print(f"   ❌ Erreur diagnostic ordonnances: {e}")

print()

# =============================================================================
# 6. TEST DE CRÉATION ET VISIBILITÉ CROISÉE
# =============================================================================

print("6. 🔄 TEST DE CRÉATION ET VISIBILITÉ CROISÉE")

# Test avec un membre spécifique
try:
    from membres.models import Membre
    test_membre = Membre.objects.first()
    
    if test_membre:
        print(f"   🧪 Test avec membre: {test_membre.prenom} {test_membre.nom}")
        
        # Test visibilité assureur
        try:
            from assureur.views import get_assureur_connecte
            print("   ✅ Module assureur: Disponible")
        except ImportError:
            print("   ❌ Module assureur: Indisponible")
            
        # Test visibilité agent
        try:
            from agents.views import verifier_statut_cotisation_simple
            statut = verifier_statut_cotisation_simple(test_membre)
            print(f"   ✅ Module agent: Disponible (Statut: {statut})")
        except ImportError:
            print("   ❌ Module agent: Indisponible")
            
        # Test visibilité médecin
        try:
            from medecin.views import peut_voir_membre
            print("   ✅ Module médecin: Disponible")
        except ImportError:
            print("   ❌ Module médecin: Indisponible")
            
        # Test visibilité pharmacien
        try:
            from pharmacien.views import peut_voir_membre
            print("   ✅ Module pharmacien: Disponible")
        except ImportError:
            print("   ❌ Module pharmacien: Indisponible")
            
    else:
        print("   ❌ Aucun membre trouvé pour le test")
        
except Exception as e:
    print(f"   ❌ Erreur test visibilité: {e}")

print()

# =============================================================================
# 7. RAPPORT DE SYNTHÈSE
# =============================================================================

print("7. 📊 RAPPORT DE SYNTHÈSE DES INTERACTIONS")

synthese = {
    'membres_agents': '✅' if 'verifier_statut_cotisation_simple' in globals() else '❌',
    'cotisations_assureurs': '✅' if 'Cotisation' in globals() else '❌', 
    'bons_medecins': '✅' if 'BonDeSoin' in globals() else '❌',
    'ordonnances_pharmaciens': '✅' if 'Ordonnance' in globals() else '❌',
    'synchronisation_globale': '🔄'
}

print("   📋 État des interactions:")
print(f"      👤 Membres → Agents: {synthese['membres_agents']}")
print(f"      💰 Cotisations → Assureurs: {synthese['cotisations_assureurs']}")
print(f"      🏥 Bons → Médecins: {synthese['bons_medecins']}")
print(f"      💊 Ordonnances → Pharmaciens: {synthese['ordonnances_pharmaciens']}")
print(f"      🔄 Synchronisation globale: {synthese['synchronisation_globale']}")

print()
print("8. 🎯 RECOMMANDATIONS")

print("   🔧 Si problèmes de visibilité:")
print("      - Vérifier les permissions dans les modèles")
print("      - Vérifier les décorateurs de permission (@est_agent, @est_medecin, etc.)")
print("      - Vérifier les relations ForeignKey entre modèles")
print("      - Vérifier les méthodes get_queryset() dans les vues")

print("   🔧 Si problèmes de synchronisation:")
print("      - Vérifier les signaux post_save pour la synchronisation automatique")
print("      - Vérifier les tâches Celery si utilisées")
print("      - Vérifier les webhooks entre microservices")

print()
print("🔍 ===== DIAGNOSTIC TERMINÉ =====")