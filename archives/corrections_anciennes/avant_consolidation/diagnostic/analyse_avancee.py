# analyse_avancee.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Cotisation, Membre
from django.db.models import Count, Sum, Avg, Min, Max
from datetime import datetime

print("="*70)
print("📈 ANALYSE AVANCÉE DU SYSTÈME")
print("="*70)

# 1. Analyse des membres
membres = Membre.objects.all()
print("\n1. 📊 ANALYSE DES MEMBRES")
print("   " + "-"*40)

types_membres = membres.values('type_contrat').annotate(
    count=Count('id'),
    pourcentage=Count('id') * 100.0 / membres.count()
)

for type_m in types_membres:
    type_label = dict(Membre.TYPE_CONTRAT_CHOICES).get(type_m['type_contrat'], type_m['type_contrat'])
    print(f"   {type_label}: {type_m['count']} membres ({type_m['pourcentage']:.1f}%)")

# 2. Analyse des cotisations
cotisations = Cotisation.objects.all()
print("\n2. 💰 ANALYSE DES COTISATIONS")
print("   " + "-"*40)

# Statistiques générales
stats = cotisations.aggregate(
    total=Count('id'),
    somme=Sum('montant'),
    moyenne=Avg('montant'),
    min=Min('montant'),
    max=Max('montant')
)

print(f"   Nombre total: {stats['total']}")
print(f"   Montant total: {stats['somme']:,.0f} FCFA")
print(f"   Moyenne par cotisation: {stats['moyenne']:,.0f} FCFA")
print(f"   Montant minimum: {stats['min']:,.0f} FCFA")
print(f"   Montant maximum: {stats['max']:,.0f} FCFA")

# 3. Analyse temporelle
print("\n3. 📅 ANALYSE TEMPORELLE")
print("   " + "-"*40)

# Grouper par mois
cotisations_par_mois = cotisations.values('periode').annotate(
    count=Count('id'),
    total=Sum('montant')
).order_by('periode')

print("   Évolution mensuelle:")
for mois in cotisations_par_mois:
    print(f"   {mois['periode']}: {mois['count']} cotisations, {mois['total']:,.0f} FCFA")

# 4. Top membres (par montant total cotisé)
print("\n4. 🏆 TOP MEMBRES")
print("   " + "-"*40)

membres_cotisations = {}
for cotisation in cotisations.select_related('membre'):
    if cotisation.membre:
        membre_id = cotisation.membre.id
        if membre_id not in membres_cotisations:
            membres_cotisations[membre_id] = {
                'membre': cotisation.membre,
                'total': 0,
                'count': 0
            }
        membres_cotisations[membre_id]['total'] += cotisation.montant
        membres_cotisations[membre_id]['count'] += 1

# Trier par montant total
sorted_membres = sorted(membres_cotisations.values(), key=lambda x: x['total'], reverse=True)

for i, data in enumerate(sorted_membres[:5], 1):
    membre = data['membre']
    print(f"   {i}. {membre.numero_membre}: {membre.nom} {membre.prenom}")
    print(f"      {data['count']} cotisations, {data['total']:,.0f} FCFA")

# 5. Recommandations stratégiques
print("\n5. 🎯 RECOMMANDATIONS STRATÉGIQUES")
print("   " + "-"*40)

revenu_mensuel_moyen = stats['somme'] / max(len(cotisations_par_mois), 1)
print(f"   Revenu mensuel moyen: {revenu_mensuel_moyen:,.0f} FCFA")

# Projection annuelle
projection_annuelle = revenu_mensuel_moyen * 12
print(f"   Projection annuelle: {projection_annuelle:,.0f} FCFA")

# Taux de croissance
if len(cotisations_par_mois) > 1:
    premier_mois = cotisations_par_mois.first()
    dernier_mois = cotisations_par_mois.last()
    if premier_mois['total'] > 0:
        croissance = (dernier_mois['total'] - premier_mois['total']) / premier_mois['total'] * 100
        print(f"   Taux de croissance: {croissance:.1f}%")
    else:
        print(f"   Taux de croissance: N/A (premier mois = 0)")

print("\n" + "="*70)
print("📊 ANALYSE TERMINÉE - DONNÉES PRÊTES POUR DÉCISION")
print("="*70)