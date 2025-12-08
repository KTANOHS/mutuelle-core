# analyse_existant_corrige.py
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Membre, Cotisation
from django.db import models

def analyser_modeles_corrige():
    """Analyse corrigée des modèles"""
    print("=== ANALYSE CORRIGÉE DES MODÈLES ===")
    
    # Modèle Membre
    print("\n📊 MODÈLE MEMBRE:")
    for field in Membre._meta.get_fields():
        if field.is_relation:
            print(f"  - {field.name}: {field.get_internal_type()} -> {field.related_model.__name__}")
        else:
            print(f"  - {field.name}: {field.get_internal_type()}")
    
    # Modèle Cotisation
    print("\n📊 MODÈLE COTISATION:")
    for field in Cotisation._meta.get_fields():
        if field.is_relation:
            print(f"  - {field.name}: {field.get_internal_type()} -> {field.related_model.__name__}")
        else:
            print(f"  - {field.name}: {field.get_internal_type()}")

def analyser_relations_corrigee():
    """Analyse corrigée des relations"""
    print("\n=== ANALYSE DES RELATIONS CORRIGÉE ===")
    
    try:
        # Relation Cotisation -> Membre
        champ_membre = Cotisation._meta.get_field('membre')
        print(f"Relation Cotisation -> Membre: {champ_membre.related_model.__name__}")
        print(f"Related name: {champ_membre.related_query_name()}")
        
        # Vérifier si le related_name existe
        membre = Membre.objects.first()
        if membre:
            cotisations = membre.cotisations_assureur.all()
            print(f"Related name fonctionnel: {cotisations.count()} cotisations pour le premier membre")
            
    except Exception as e:
        print(f"Erreur relation: {e}")

if __name__ == "__main__":
    analyser_modeles_corrige()
    analyser_donnees()  # Garder l'ancienne fonction pour les données
    analyser_relations_corrigee()