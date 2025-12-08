# demarrage_rapide.py
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Membre, Cotisation
from datetime import date

def creer_donnees_test():
    """Crée des données de test pour le développement"""
    print("🎯 CRÉATION DE DONNÉES DE TEST...")
    
    # Vérifier si des données existent déjà
    if Membre.objects.count() > 1:
        print("ℹ️  Des données existent déjà, passage à la configuration des vues...")
        return
    
    # Créer quelques membres de test
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
            'statut': 'actif',
            'avance_payee': 5000.00,
            'carte_adhesion_payee': 2000.00
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
            'statut': 'actif',
            'avance_payee': 10000.00,
            'carte_adhesion_payee': 5000.00
        }
    ]
    
    membres_crees = []
    for data in membres_data:
        membre, created = Membre.objects.get_or_create(
            numero_membre=data['numero_membre'],
            defaults=data
        )
        if created:
            membres_crees.append(membre)
            print(f"✅ Membre créé: {membre.nom} {membre.prenom}")
    
    # Créer des cotisations de test
    if membres_crees:
        for membre in membres_crees:
            cotisation = Cotisation.objects.create(
                membre=membre,
                periode=f"{date.today().month}/{date.today().year}",
                type_cotisation='mensuelle',
                montant=15000.00,
                montant_clinique=8000.00,
                montant_pharmacie=5000.00,
                montant_charges_mutuelle=2000.00,
                date_emission=date.today(),
                date_echeance=date.today().replace(day=28),
                date_paiement=date.today(),
                statut='payee',
                reference=f"COT-{membre.numero_membre}-{date.today().strftime('%Y%m')}",
                notes="Cotisation test pour développement"
            )
            print(f"✅ Cotisation créée pour {membre.nom}: {cotisation.montant} FCFA")
    
    print(f"🎉 Données de test créées: {len(membres_crees)} membres avec cotisations")

if __name__ == "__main__":
    creer_donnees_test()
    
    # Lancer l'analyse complète
    print("\n" + "="*50)
    exec(open('analyse_existant_complet.py').read())