#!/usr/bin/env python
"""
SCRIPT ULTRA-SIMPLE - Juste créer quelques cotisations
"""

import os
import sys
import django
from datetime import datetime, timedelta

def setup_django():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.abspath(os.path.join(current_dir, '..'))
        sys.path.append(project_dir)
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        django.setup()
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def creer_cotisations_minimales():
    """Créer seulement 7 cotisations (une par membre)"""
    
    if not setup_django():
        return
    
    from membres.models import Membre
    from assureur.models import Cotisation
    
    print("\n" + "="*60)
    print("MINI-GÉNÉRATION DE COTISATIONS")
    print("="*60)
    
    # Nettoyer d'abord
    Cotisation.objects.all().delete()
    print("✅ Anciennes cotisations supprimées")
    
    membres = Membre.objects.all()
    print(f"👥 Membres trouvés: {membres.count()}")
    
    cotisations_creees = []
    
    for i, membre in enumerate(membres, 1):
        try:
            # Créer une cotisation simple
            cotisation = Cotisation(
                membre=membre,
                periode="2025-12",
                type_cotisation="mensuelle",
                montant=5000 + (i * 1000),  # Montants différents pour chaque membre
                date_emission=datetime.now().date(),
                date_echeance=datetime.now().date() + timedelta(days=30),
                statut="payee",
                reference=f"COT-202512-{membre.id:03d}"
            )
            
            cotisation.save()
            cotisations_creees.append(cotisation)
            
            print(f"  ✅ {membre.nom} {membre.prenom}: {cotisation.montant} FCFA")
            
        except Exception as e:
            print(f"  ❌ Erreur pour {membre.nom}: {e}")
    
    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ")
    print("="*60)
    
    total = Cotisation.objects.count()
    print(f"✅ Cotisations créées: {total}")
    
    if total > 0:
        montant_total = sum(c.montant for c in cotisations_creees)
        print(f"💰 Montant total: {montant_total:,} FCFA")
        print(f"📈 Moyenne par membre: {montant_total/total:,.0f} FCFA")
        
        # Afficher toutes les cotisations
        print(f"\n📄 LISTE DES COTISATIONS:")
        for i, cot in enumerate(Cotisation.objects.all(), 1):
            membre_nom = f"{cot.membre.prenom} {cot.membre.nom}" if cot.membre else "N/A"
            print(f"  {i}. {membre_nom} - {cot.periode}: {cot.montant} FCFA")

if __name__ == "__main__":
    creer_cotisations_minimales()