# analyse_existant_complet.py
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Membre, Cotisation
from django.db import models

def analyser_modeles_complet():
    """Analyse complète des modèles"""
    print("=== ANALYSE COMPLÈTE DES MODÈLES ===")
    
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

def analyser_donnees_complet():
    """Analyse complète des données existantes"""
    print("\n=== ANALYSE DES DONNÉES EXISTANTES ===")
    
    total_membres = Membre.objects.count()
    total_cotisations = Cotisation.objects.count()
    
    print(f"Nombre total de membres: {total_membres}")
    print(f"Nombre total de cotisations: {total_cotisations}")
    
    # Statistiques détaillées sur les membres
    if total_membres > 0:
        membres_avec_avance = Membre.objects.filter(avance_payee__gt=0).count()
        membres_avec_carte = Membre.objects.filter(carte_adhesion_payee__gt=0).count()
        femmes_enceintes = Membre.objects.filter(est_femme_enceinte=True).count()
        
        print(f"\n📈 Statistiques détaillées:")
        print(f"  - Membres avec avance payée: {membres_avec_avance}")
        print(f"  - Membres avec carte payée: {membres_avec_carte}")
        print(f"  - Femmes enceintes: {femmes_enceintes}")
        
        # Types de contrat
        types_contrat = Membre.objects.values('type_contrat').annotate(
            count=models.Count('id')
        )
        print(f"\n📋 Répartition par type de contrat:")
        for type_contrat in types_contrat:
            print(f"  - {type_contrat['type_contrat']}: {type_contrat['count']} membres")
        
        # Aperçu des membres
        print("\n👥 Aperçu des membres:")
        for membre in Membre.objects.all()[:10]:
            cotisations_count = membre.cotisations_assureur.count()
            statut_enceinte = "👶" if membre.est_femme_enceinte else ""
            print(f"  - {membre.nom} {membre.prenom} ({membre.numero_membre}) {statut_enceinte}")
            print(f"    Cotisations: {cotisations_count}, Type: {membre.type_contrat}")

def analyser_relations_complet():
    """Analyse complète des relations"""
    print("\n=== ANALYSE DES RELATIONS ===")
    
    try:
        # Relation Cotisation -> Membre
        champ_membre = Cotisation._meta.get_field('membre')
        print(f"Relation Cotisation -> Membre: {champ_membre.related_model.__name__}")
        
        # Tester le related_name
        membre = Membre.objects.first()
        if membre:
            cotisations = membre.cotisations_assureur.all()
            print(f"Related name 'cotisations_assureur' fonctionnel: {cotisations.count()} cotisations")
            
            # Vérifier les champs de la première cotisation (si elle existe)
            if cotisations.exists():
                cotisation = cotisations.first()
                print(f"\nExemple de cotisation:")
                print(f"  - Montant: {cotisation.montant}")
                print(f"  - Période: {cotisation.periode}")
                print(f"  - Statut: {cotisation.statut}")
        
        # Relation Cotisation -> User (enregistre_par)
        champ_enregistre_par = Cotisation._meta.get_field('enregistre_par')
        print(f"\nRelation Cotisation -> User: {champ_enregistre_par.related_model.__name__}")
        
    except Exception as e:
        print(f"Erreur dans l'analyse des relations: {e}")

def analyser_structure_cotisation():
    """Analyse spécifique de la structure des cotisations"""
    print("\n=== STRUCTURE DES COTISATIONS ===")
    
    # Vérifier les valeurs possibles pour certains champs
    if Cotisation.objects.exists():
        cotisation = Cotisation.objects.first()
        print("Exemple de structure de cotisation:")
        print(f"  - Période: {getattr(cotisation, 'periode', 'Non défini')}")
        print(f"  - Type: {getattr(cotisation, 'type_cotisation', 'Non défini')}")
        print(f"  - Montant total: {getattr(cotisation, 'montant', 'Non défini')}")
        print(f"  - Montant clinique: {getattr(cotisation, 'montant_clinique', 'Non défini')}")
        print(f"  - Montant pharmacie: {getattr(cotisation, 'montant_pharmacie', 'Non défini')}")
        print(f"  - Montant charges: {getattr(cotisation, 'montant_charges_mutuelle', 'Non défini')}")

def suggestions_implementation():
    """Suggestions pour l'implémentation"""
    print("\n=== SUGGESTIONS D'IMPLÉMENTATION ===")
    
    print("1. ✅ CHAMPS IDENTIFIÉS:")
    print("   - Structure Membre complète avec gestion grossesse")
    print("   - Structure Cotisation détaillée avec répartition des montants")
    print("   - Relations fonctionnelles vérifiées")
    
    print("\n2. 🎯 PRIORITÉS DE DÉVELOPPEMENT:")
    print("   - Interface enregistrement cotisations avec calculs automatiques")
    print("   - Gestion des femmes enceintes (dates importantes)")
    print("   - Tableau de bord avec statistiques par type de contrat")
    print("   - Système de vérification pour les agents")
    
    print("\n3. 🔧 ADAPTATIONS NÉCESSAIRES:")
    print("   - Ajouter mois_couvert et annee_couverte dans les forms Cotisation")
    print("   - Prévoir logique métier pour femmes enceintes")
    print("   - Génération automatique des références de cotisation")
    print("   - Calcul des échéances basé sur le type de contrat")

if __name__ == "__main__":
    analyser_modeles_complet()
    analyser_donnees_complet()
    analyser_relations_complet()
    analyser_structure_cotisation()
    suggestions_implementation()