#!/usr/bin/env python3
"""
DÉBOGAGE DES MODÈLES - Vérifie la structure exacte des modèles problématiques
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps

def debug_specific_models():
    """Débogue les modèles spécifiques qui posent problème"""
    
    print("🔍 DÉBOGAGE DES MODÈLES PROBLÉMATIQUES")
    print("=" * 60)
    
    models_to_debug = [
        'medecin.Medecin',
        'medecin.EtablissementMedical',
        'assureur.Assureur',
        'pharmacien.Pharmacien',
        'agents.Agent'
    ]
    
    for model_path in models_to_debug:
        try:
            model = apps.get_model(model_path)
            print(f"\n📦 {model_path}")
            print("-" * 40)
            print(f"   🏷️  Nom du modèle: {model.__name__}")
            print(f"   📁 App: {model._meta.app_label}")
            
            # Afficher tous les attributs et méthodes
            print(f"   🔍 Attributs disponibles:")
            for attr in dir(model):
                if not attr.startswith('_'):
                    try:
                        value = getattr(model, attr)
                        if not callable(value):
                            print(f"     • {attr}: {type(value)}")
                    except:
                        print(f"     • {attr}: <erreur>")
            
            # Champs du modèle
            print(f"   📝 Champs du modèle:")
            for field in model._meta.get_fields():
                if field.is_relation:
                    if field.many_to_one:
                        print(f"     🔗 {field.name} (ForeignKey -> {field.related_model.__name__})")
                    elif field.one_to_one:
                        print(f"     🔗 {field.name} (OneToOne -> {field.related_model.__name__})")
                    elif field.many_to_many:
                        print(f"     🔗 {field.name} (ManyToMany -> {field.related_model.__name__})")
                else:
                    print(f"     📝 {field.name} ({field.get_internal_type()})")
                    
        except LookupError as e:
            print(f"\n❌ Modèle non trouvé: {model_path}")
            print(f"   Erreur: {e}")

def test_model_creation():
    """Teste la création d'instances des modèles problématiques"""
    
    print("\n🧪 TEST DE CRÉATION DES MODÈLES")
    print("=" * 60)
    
    from django.contrib.auth.models import User
    
    # Créer un user test
    user, created = User.objects.get_or_create(
        username='debug_user',
        defaults={'email': 'debug@test.com', 'is_active': True}
    )
    
    # Test Medecin
    try:
        from medecin.models import Medecin, SpecialiteMedicale, EtablissementMedical
        
        # Créer les dépendances
        specialite, _ = SpecialiteMedicale.objects.get_or_create(
            nom='Debug Specialite',
            defaults={'description': 'Spécialité de test'}
        )
        
        etablissement, _ = EtablissementMedical.objects.get_or_create(
            nom='Debug Etablissement',
            defaults={'adresse': 'Adresse test'}
        )
        
        # Essayer de créer un médecin
        medecin_data = {
            'user': user,
            'numero_ordre': 'DEBUG001',
            'specialite': specialite,
            'etablissement': etablissement,
            'telephone_pro': '+22500000000',
            'actif': True,
        }
        
        # Filtrer les champs existants
        existing_fields = [f.name for f in Medecin._meta.get_fields()]
        filtered_data = {k: v for k, v in medecin_data.items() if k in existing_fields}
        
        medecin = Medecin.objects.create(**filtered_data)
        print(f"✅ Médecin créé avec succès!")
        print(f"   Champs utilisés: {list(filtered_data.keys())}")
        print(f"   Attributs de l'instance: {[attr for attr in dir(medecin) if not attr.startswith('_')]}")
        
        # Nettoyer
        medecin.delete()
        
    except Exception as e:
        print(f"❌ Erreur création Medecin: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_specific_models()
    test_model_creation()