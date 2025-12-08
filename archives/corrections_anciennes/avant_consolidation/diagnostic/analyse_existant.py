# analyse_existant.py
import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Membre, Cotisation
from django.db import models

def analyser_modeles():
    """Analyse les modèles existants"""
    print("=== ANALYSE DES MODÈLES ===")
    
    # Analyse du modèle Membre
    membre_fields = Membre._meta.get_fields()
    print("\n📊 Champs du modèle Membre:")
    for field in membre_fields:
        print(f"  - {field.name}: {field.get_internal_type()}")

    # Analyse du modèle Cotisation
    cotisation_fields = Cotisation._meta.get_fields()
    print("\n📊 Champs du modèle Cotisation:")
    for field in cotisation_fields:
        print(f"  - {field.name}: {field.get_internal_type()}")

def analyser_donnees():
    """Analyse les données existantes"""
    print("\n=== ANALYSE DES DONNÉES ===")
    
    total_membres = Membre.objects.count()
    total_cotisations = Cotisation.objects.count()
    
    print(f"Nombre total de membres: {total_membres}")
    print(f"Nombre total de cotisations: {total_cotisations}")
    
    # Statistiques sur les membres
    if total_membres > 0:
        membres_avec_avance = Membre.objects.filter(avance_payee__gt=0).count()
        membres_avec_carte = Membre.objects.filter(carte_adhesion_payee__gt=0).count()
        
        print(f"Membres avec avance payée: {membres_avec_avance}")
        print(f"Membres avec carte payée: {membres_avec_carte}")
        
        # Aperçu des 5 premiers membres
        print("\n👥 Aperçu des membres:")
        for membre in Membre.objects.all()[:5]:
            cotisations_count = membre.cotisations_assureur.count()
            print(f"  - {membre.nom}: {cotisations_count} cotisations")

def analyser_relations():
    """Analyse les relations entre modèles"""
    print("\n=== ANALYSE DES RELATIONS ===")
    
    # Vérifier la relation Membre -> Cotisation
    try:
        membre = Membre.objects.first()
        if membre:
            related_name = Membre._meta.get_field('cotisations_assureur').related_query_name()
            print(f"Relation Membre -> Cotisations: {related_name}")
    except Exception as e:
        print(f"Erreur dans l'analyse des relations: {e}")

if __name__ == "__main__":
    analyser_modeles()
    analyser_donnees()
    analyser_relations()