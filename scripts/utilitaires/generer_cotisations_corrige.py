#!/usr/bin/env python
"""
SCRIPT CORRIGÉ DE GÉNÉRATION DE COTISATIONS
Utilise le bon modèle: assureur.models.Cotisation
"""

import os
import sys
import django
from datetime import datetime, timedelta
import random

# Configuration Django
def setup_django():
    """Configuration de l'environnement Django"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.abspath(os.path.join(current_dir, '..'))
        sys.path.append(project_dir)
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        django.setup()
        print("✅ Django configuré avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def generer_cotisations_corrige():
    """Générer des cotisations pour tous les membres actifs"""
    
    if not setup_django():
        return
    
    print("\n" + "="*60)
    print("🚀 GÉNÉRATION DE COTISATIONS (CORRIGÉ)")
    print("="*60)
    
    # Import des bons modèles
    from membres.models import Membre
    from assureur.models import Cotisation
    from django.contrib.auth.models import User
    
    # Trouver l'utilisateur admin
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.first()
        print(f"👤 Utilisateur pour la création: {admin_user.username}")
    except:
        admin_user = None
    
    # Récupérer tous les membres actifs
    membres_actifs = Membre.objects.filter(statut='actif')
    total_membres = membres_actifs.count()
    
    print(f"👥 Membres actifs trouvés: {total_membres}")
    
    if total_membres == 0:
        print("❌ Aucun membre actif trouvé")
        return
    
    # Nettoyer les anciennes cotisations (optionnel)
    print("\n🧹 Nettoyage des cotisations existantes...")
    Cotisation.objects.all().delete()
    print("✅ Anciennes cotisations supprimées")
    
    # Périodes à générer (6 derniers mois)
    aujourdhui = datetime.now()
    periodes = []
    
    for i in range(6):
        mois = aujourdhui.month - i
        annee = aujourdhui.year
        
        if mois <= 0:
            mois += 12
            annee -= 1
        
        periode = f"{annee}-{mois:02d}"
        periodes.append(periode)
    
    print(f"\n📅 Périodes à générer: {periodes}")
    
    total_cree = 0
    
    # Générer les cotisations pour chaque période
    for periode in periodes:
        print(f"\n🔄 Génération pour {periode}...")
        
        for membre in membres_actifs:
            try:
                # Générer un montant aléatoire (entre 3000 et 15000 FCFA)
                montant_total = random.randint(3000, 15000)
                
                # Déterminer la date de cotisation (15 du mois)
                annee, mois = map(int, periode.split('-'))
                date_cotisation = datetime(annee, mois, 15).date()
                
                # Créer la cotisation AVEC LES BONS CHAMPS
                cotisation = Cotisation.objects.create(
                    membre=membre,
                    periode=periode,
                    type_cotisation='mensuelle',  # Utiliser le champ existant
                    montant=montant_total,
                    date_cotisation=date_cotisation,
                    date_echeance=date_cotisation + timedelta(days=30),
                    statut='payee',  # Ajouter le statut si le champ existe
                    # NOTE: Ne pas utiliser les champs qui n'existent pas !
                    # montant_clinique=...,  # CHAMP INEXISTANT
                    # montant_pharmacie=..., # CHAMP INEXISTANT
                    # montant_charges_mutuelle=..., # CHAMP INEXISTANT
                )
                
                print(f"  ✅ {membre.nom} {membre.prenom}: {montant_total} FCFA")
                total_cree += 1
                
            except Exception as e:
                print(f"  ❌ Erreur pour {membre.nom}: {e}")
                # Afficher les champs disponibles pour debug
                print(f"     Champs disponibles: {[f.name for f in Cotisation._meta.fields]}")
    
    # Vérification
    print("\n" + "="*60)
    print("📊 VÉRIFICATION DES COTISATIONS")
    print("="*60)
    
    total_base = Cotisation.objects.count()
    total_montant = Cotisation.objects.aggregate(total=Sum('montant'))['total'] or 0
    
    print(f"✅ Cotisations créées: {total_cree}")
    print(f"📈 Cotisations en base: {total_base}")
    print(f"💰 Montant total: {total_montant:,.0f} FCFA")
    
    if total_base > 0:
        print(f"\n📅 RÉCAPITULATIF PAR PÉRIODE:")
        stats = Cotisation.objects.values('periode').annotate(
            count=Count('id'),
            total=Sum('montant')
        ).order_by('-periode')
        
        for stat in stats:
            print(f"  • {stat['periode']}: {stat['count']} cotisations = {stat['total']:,.0f} FCFA")
    
    print("\n🎉 Génération terminée avec succès !")

def generer_cotisations_simple():
    """Version simplifiée pour tester"""
    
    if not setup_django():
        return
    
    print("\n" + "="*60)
    print("🚀 GÉNÉRATION SIMPLE DE COTISATIONS")
    print("="*60)
    
    from membres.models import Membre
    from assureur.models import Cotisation
    
    # Nettoyer
    Cotisation.objects.all().delete()
    
    # Un seul membre pour test
    membre = Membre.objects.first()
    
    if not membre:
        print("❌ Aucun membre trouvé")
        return
    
    print(f"👤 Membre test: {membre.nom} {membre.prenom}")
    
    # Créer une seule cotisation
    try:
        cotisation = Cotisation.objects.create(
            membre=membre,
            periode="2025-12",
            type_cotisation="mensuelle",
            montant=5000,
            date_cotisation=datetime.now().date(),
            date_echeance=datetime.now().date() + timedelta(days=30),
            statut="payee"
        )
        
        print(f"✅ Cotisation créée: {cotisation.id}")
        print(f"💰 Montant: {cotisation.montant} FCFA")
        print(f"📅 Période: {cotisation.periode}")
        
        # Vérifier les champs
        print(f"\n🔍 CHAMPS DE LA COTISATION:")
        for field in Cotisation._meta.fields:
            value = getattr(cotisation, field.name, "N/A")
            print(f"  • {field.name}: {value}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print(f"\n🔍 CHAMPS DISPONIBLES DANS Cotisation:")
        for field in Cotisation._meta.fields:
            print(f"  • {field.name} ({field.get_internal_type()})")

if __name__ == "__main__":
    # Pour tester une création simple d'abord
    # generer_cotisations_simple()
    
    # Pour générer toutes les cotisations
    generer_cotisations_corrige()