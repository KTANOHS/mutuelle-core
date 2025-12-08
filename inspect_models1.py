#!/usr/bin/env python3
"""
INSPECTION DES MODÈLES - Découvre la structure des modèles
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps

def inspect_all_models():
    """Inspecte tous les modèles et leurs champs"""
    
    print("🔍 INSPECTION DES MODÈLES")
    print("=" * 60)
    
    models_to_inspect = [
        'membres.Membre',
        'membres.Bon',
        'membres.LigneBon',
        'medecin.Medecin',
        'medecin.SpecialiteMedicale',
        'medecin.Consultation',
        'medecin.Ordonnance',
        'medecin.Medicament',
        'assureur.Assureur',
        'assureur.ConfigurationAssurance',
        'assureur.Paiement',
        'pharmacien.Pharmacien',
        'pharmacien.OrdonnancePharmacien',
        'pharmacien.StockPharmacie',
        'agents.Agent',
        'agents.RoleAgent',
        'agents.BonSoin',
        'agents.VerificationCotisation',
        'soins.TypeSoin',
        'soins.Soin',
        'soins.BonDeSoin',
        'paiements.Paiement'
    ]
    
    for model_path in models_to_inspect:
        try:
            model = apps.get_model(model_path)
            print(f"\n📦 {model_path}")
            print("-" * 40)
            
            # Champs du modèle
            for field in model._meta.get_fields():
                if field.is_relation:
                    if field.many_to_one:
                        print(f"  🔗 {field.name} (ForeignKey -> {field.related_model.__name__})")
                    elif field.one_to_one:
                        print(f"  🔗 {field.name} (OneToOne -> {field.related_model.__name__})")
                    elif field.many_to_many:
                        print(f"  🔗 {field.name} (ManyToMany -> {field.related_model.__name__})")
                else:
                    print(f"  📝 {field.name} ({field.get_internal_type()})")
                    
        except LookupError:
            print(f"\n❌ Modèle non trouvé: {model_path}")

if __name__ == "__main__":
    inspect_all_models()