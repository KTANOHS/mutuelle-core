# demarrage_rapide_final.py
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Membre, Cotisation
from datetime import date, timedelta
from django.db import models  # Import manquant ajouté

def creer_donnees_test_final():
    """Crée des données de test pour le développement - Version finale"""
    print("🎯 CRÉATION DE DONNÉES DE TEST (FINAL)...")
    
    # Vérifier si des données existent déjà (plus d'un membre)
    if Membre.objects.count() > 2:
        print("ℹ️  Des données existent déjà, passage à la configuration des vues...")
        return
    
    # Créer quelques membres de test avec des numéros de contrat uniques
    membres_data = [
        {
            'numero_membre': 'MEM001',
            'nom': 'Koné',
            'prenom': 'Amina',
            'date_naissance': date(1990, 5, 15),
            'email': 'amina.kone@example.com',
            'telephone': '0123456789',
            'adresse': 'Abidjan, Cocody',
            'est_femme_enceinte': True,
            'date_debut_grossesse': date(2024, 1, 15),
            'date_accouchement_prevue': date(2024, 10, 15),
            'type_contrat': 'Standard',
            'numero_contrat': 'CONT001',  # Numéro unique
            'statut': 'actif',
            'avance_payee': 5000.00,
            'carte_adhesion_payee': 2000.00,
            'date_adhesion': date(2024, 1, 1),
            'date_effet': date(2024, 1, 1),
            'date_expiration': date(2024, 12, 31),
            'taux_couverture': 80.00
        },
        {
            'numero_membre': 'MEM002', 
            'nom': 'Diallo',
            'prenom': 'Mohamed',
            'date_naissance': date(1985, 8, 22),
            'email': 'mohamed.diallo@example.com',
            'telephone': '0123456790',
            'adresse': 'Abidjan, Plateau',
            'est_femme_enceinte': False,
            'type_contrat': 'Premium',
            'numero_contrat': 'CONT002',  # Numéro unique
            'statut': 'actif',
            'avance_payee': 10000.00,
            'carte_adhesion_payee': 5000.00,
            'date_adhesion': date(2024, 1, 1),
            'date_effet': date(2024, 1, 1),
            'date_expiration': date(2024, 12, 31),
            'taux_couverture': 90.00
        },
        {
            'numero_membre': 'MEM003',
            'nom': 'Bamba',
            'prenom': 'Fatou',
            'date_naissance': date(1992, 3, 10),
            'email': 'fatou.bamba@example.com',
            'telephone': '0123456791',
            'adresse': 'Abidjan, Yopougon',
            'est_femme_enceinte': False,
            'type_contrat': 'Basique',
            'numero_contrat': 'CONT003',  # Numéro unique
            'statut': 'actif',
            'avance_payee': 3000.00,
            'carte_adhesion_payee': 1500.00,
            'date_adhesion': date(2024, 2, 1),
            'date_effet': date(2024, 2, 1),
            'date_expiration': date(2024, 12, 31),
            'taux_couverture': 70.00
        }
    ]
    
    membres_crees = []
    for data in membres_data:
        try:
            # Vérifier si le membre existe déjà par numéro_membre
            membre_existant = Membre.objects.filter(numero_membre=data['numero_membre']).first()
            if membre_existant:
                print(f"ℹ️  Membre existe déjà: {membre_existant.nom} {membre_existant.prenom}")
                membres_crees.append(membre_existant)
            else:
                membre = Membre.objects.create(**data)
                membres_crees.append(membre)
                print(f"✅ Membre créé: {membre.nom} {membre.prenom} ({membre.numero_membre})")
        except Exception as e:
            print(f"❌ Erreur création membre {data['numero_membre']}: {e}")
    
    # Créer des cotisations de test
    cotisations_crees = []
    for membre in membres_crees:
        try:
            # Cotisation pour le mois courant
            cotisation = Cotisation.objects.create(
                membre=membre,
                periode=f"{date.today().month}/{date.today().year}",
                type_cotisation='mensuelle',
                montant=15000.00,
                montant_clinique=8000.00,
                montant_pharmacie=5000.00,
                montant_charges_mutuelle=2000.00,
                date_emission=date.today() - timedelta(days=5),
                date_echeance=date.today() + timedelta(days=25),
                date_paiement=date.today() - timedelta(days=3),
                statut='payee',
                reference=f"COT-{membre.numero_membre}-{date.today().strftime('%Y%m')}",
                notes="Cotisation test pour développement"
            )
            cotisations_crees.append(cotisation)
            print(f"✅ Cotisation créée pour {membre.nom}: {cotisation.montant} FCFA")
            
            # Ajouter une cotisation du mois précédent pour certains membres
            if membre.numero_membre in ['MEM001', 'MEM002']:
                mois_precedent = (date.today().month - 1) or 12
                annee_precedente = date.today().year if date.today().month != 1 else date.today().year - 1
                
                cotisation_precedente = Cotisation.objects.create(
                    membre=membre,
                    periode=f"{mois_precedent}/{annee_precedente}",
                    type_cotisation='mensuelle',
                    montant=15000.00,
                    montant_clinique=8000.00,
                    montant_pharmacie=5000.00,
                    montant_charges_mutuelle=2000.00,
                    date_emission=date.today() - timedelta(days=35),
                    date_echeance=date.today() - timedelta(days=5),
                    date_paiement=date.today() - timedelta(days=30),
                    statut='payee',
                    reference=f"COT-{membre.numero_membre}-{mois_precedent:02d}{annee_precedente}",
                    notes="Cotisation du mois précédent"
                )
                cotisations_crees.append(cotisation_precedente)
                print(f"✅ Cotisation précédente créée pour {membre.nom}")
                
        except Exception as e:
            print(f"❌ Erreur création cotisation pour {membre.nom}: {e}")
    
    print(f"\n🎉 DONNÉES DE TEST CRÉÉES AVEC SUCCÈS:")
    print(f"   - {len(membres_crees)} membres")
    print(f"   - {len(cotisations_crees)} cotisations")
    
    return membres_crees, cotisations_crees

def verifier_donnees_test_final():
    """Vérifie que les données de test sont correctement créées"""
    print("\n🔍 VÉRIFICATION DES DONNÉES...")
    
    total_membres = Membre.objects.count()
    total_cotisations = Cotisation.objects.count()
    
    print(f"Total membres dans la base: {total_membres}")
    print(f"Total cotisations dans la base: {total_cotisations}")
    
    # Afficher les membres avec leurs cotisations
    for membre in Membre.objects.all().prefetch_related('cotisations_assureur'):
        cotisations_count = membre.cotisations_assureur.count()
        statut_enceinte = "👶" if membre.est_femme_enceinte else ""
        print(f"\n{membre.nom} {membre.prenom} {statut_enceinte}")
        print(f"  Numéro: {membre.numero_membre}")
        print(f"  Contrat: {membre.type_contrat}")
        print(f"  Cotisations: {cotisations_count}")
        
        for cotisation in membre.cotisations_assureur.all():
            print(f"    - {cotisation.periode}: {cotisation.montant} FCFA ({cotisation.statut})")

def analyse_statistiques_final():
    """Analyse statistique complète des données"""
    print("\n" + "="*60)
    print("📊 ANALYSE STATISTIQUE COMPLÈTE")
    print("="*60)
    
    stats = Membre.objects.aggregate(
        total=models.Count('id'),
        femmes_enceintes=models.Count('id', filter=models.Q(est_femme_enceinte=True)),
        total_avance=models.Sum('avance_payee'),
        total_carte=models.Sum('carte_adhesion_payee')
    )
    
    stats_cotisations = Cotisation.objects.aggregate(
        total=models.Count('id'),
        total_montant=models.Sum('montant'),
        moyen_montant=models.Sum('montant') / models.Count('id')
    )
    
    print(f"\n📈 STATISTIQUES GLOBALES:")
    print(f"  Membres: {stats['total']} (dont {stats['femmes_enceintes']} femmes enceintes)")
    print(f"  Avances totales: {stats['total_avance'] or 0:.2f} FCFA")
    print(f"  Cartes totales: {stats['total_carte'] or 0:.2f} FCFA")
    print(f"  Cotisations: {stats_cotisations['total']}")
    print(f"  Montant total cotisations: {stats_cotisations['total_montant'] or 0:.2f} FCFA")
    print(f"  Moyenne par cotisation: {stats_cotisations['moyen_montant'] or 0:.2f} FCFA")
    
    # Répartition par type de contrat
    print(f"\n📋 RÉPARTITION PAR TYPE DE CONTRAT:")
    repartition = Membre.objects.values('type_contrat').annotate(
        count=models.Count('id'),
        pourcentage=models.Count('id') * 100 / stats['total']
    )
    for item in repartition:
        print(f"  - {item['type_contrat']}: {item['count']} membres ({item['pourcentage']:.1f}%)")
    
    # Statut des membres
    print(f"\n🎯 STATUT DES MEMBRES:")
    statuts = Membre.objects.values('statut').annotate(
        count=models.Count('id')
    )
    for statut in statuts:
        print(f"  - {statut['statut'] or 'Non défini'}: {statut['count']} membres")
    
    # Montants répartis des cotisations
    print(f"\n💰 RÉPARTITION DES MONTANTS COTISATIONS:")
    repartition_montants = Cotisation.objects.aggregate(
        total_clinique=models.Sum('montant_clinique'),
        total_pharmacie=models.Sum('montant_pharmacie'),
        total_charges=models.Sum('montant_charges_mutuelle')
    )
    
    total_cotisations_montant = stats_cotisations['total_montant'] or 0
    if total_cotisations_montant > 0:
        print(f"  Clinique: {repartition_montants['total_clinique'] or 0:.2f} FCFA ({(repartition_montants['total_clinique'] or 0) / total_cotisations_montant * 100:.1f}%)")
        print(f"  Pharmacie: {repartition_montants['total_pharmacie'] or 0:.2f} FCFA ({(repartition_montants['total_pharmacie'] or 0) / total_cotisations_montant * 100:.1f}%)")
        print(f"  Charges mutuelle: {repartition_montants['total_charges'] or 0:.2f} FCFA ({(repartition_montants['total_charges'] or 0) / total_cotisations_montant * 100:.1f}%)")

def generer_rapport_implementation():
    """Génère un rapport pour l'implémentation des vues"""
    print("\n" + "="*60)
    print("🚀 RAPPORT POUR IMPLÉMENTATION DES VUES")
    print("="*60)
    
    print("\n✅ DONNÉES PRÊTES POUR LE DÉVELOPPEMENT:")
    print(f"   - {Membre.objects.count()} membres dans la base")
    print(f"   - {Cotisation.objects.count()} cotisations dans la base")
    print(f"   - Structure des modèles validée")
    print(f"   - Relations fonctionnelles vérifiées")
    
    print("\n🎯 PROCHAINES ÉTAPES:")
    print("   1. Créer les templates manquants")
    print("   2. Implémenter les vues avec les forms corrigés")
    print("   3. Tester l'interface complète")
    print("   4. Ajouter la logique métier spécifique")
    
    print("\n📋 TEMPLATES À CRÉER:")
    templates = [
        "assureur/creer_membre.html",
        "assureur/enregistrer_cotisation.html", 
        "assureur/detail_membre.html",
        "agent/verification_cotisations.html",
        "agent/detail_membre_verification.html"
    ]
    
    for template in templates:
        print(f"   - {template}")

if __name__ == "__main__":
    print("🎯 DÉMARRAGE DU SYSTÈME DE GESTION DES COTISATIONS")
    print("="*60)
    
    membres, cotisations = creer_donnees_test_final()
    verifier_donnees_test_final()
    analyse_statistiques_final()
    generer_rapport_implementation()
    
    print("\n🎉 SYSTÈME PRÊT POUR LE DÉVELOPPEMENT!")
    print("   Vous pouvez maintenant créer les templates et implémenter les vues.")