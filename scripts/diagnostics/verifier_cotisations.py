#!/usr/bin/env python
"""
VÉRIFICATEUR RAPIDE - Vérifie l'état des cotisations
"""

import os
import sys

def verifier_cotisations():
    """Vérifier rapidement l'état des cotisations"""
    
    import django
    from datetime import datetime
    from django.db.models import Sum, Count
    
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.abspath(os.path.join(current_dir, '..'))
        sys.path.append(project_dir)
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        django.setup()
        
        from assureur.models import Cotisation
        from membres.models import Membre
        
        print("\n" + "="*60)
        print("🔍 VÉRIFICATION RAPIDE DES COTISATIONS")
        print("="*60)
        
        # Totaux
        total_cotisations = Cotisation.objects.count()
        total_membres = Membre.objects.filter(statut='actif').count()
        
        if total_cotisations == 0:
            print("❌ Aucune cotisation enregistrée")
            return
        
        # Montant total
        total_montant = Cotisation.objects.aggregate(total=Sum('montant'))['total'] or 0
        
        print(f"📊 COTISATIONS: {total_cotisations}")
        print(f"👥 MEMBRES ACTIFS: {total_membres}")
        print(f"💰 MONTANT TOTAL: {total_montant:,.0f} FCFA")
        print(f"📈 MOYENNE PAR MEMBRE: {total_montant/total_membres if total_membres > 0 else 0:,.0f} FCFA")
        
        # Dernières périodes
        print(f"\n📅 DERNIÈRES PÉRIODES:")
        periodes = Cotisation.objects.values('periode').distinct().order_by('-periode')[:3]
        for periode in periodes:
            stats = Cotisation.objects.filter(periode=periode['periode']).aggregate(
                count=Count('id'),
                total=Sum('montant')
            )
            print(f"  • {periode['periode']}: {stats['count']} cotisations = {stats['total']:,.0f} FCFA")
        
        # Membres sans cotisations
        membres_avec_cot = Cotisation.objects.values('membre').distinct().count()
        membres_sans_cot = total_membres - membres_avec_cot
        
        print(f"\n👤 COUVERTURE:")
        print(f"  • Membres avec cotisations: {membres_avec_cot}/{total_membres}")
        print(f"  • Membres sans cotisations: {membres_sans_cot}")
        
        if membres_sans_cot > 0:
            print(f"  ⚠️  {membres_sans_cot} membre(s) sans cotisations")
        
        print(f"\n✅ Vérification terminée à {datetime.now().strftime('%H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    verifier_cotisations()