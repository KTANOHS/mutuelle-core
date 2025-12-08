# check_bon_model.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("="*70)
print("🔍 VÉRIFICATION DU MODÈLE BON (BonDeSoin)")
print("="*70)

try:
    # Essayer d'importer le modèle Bon (BonDeSoin)
    from agents.models import Bon  # ou assureur.models selon votre structure
    
    print("✅ Modèle Bon importé avec succès")
    
    # Afficher les champs
    print("\n📋 CHAMPS DU MODÈLE BON:")
    for field in Bon._meta.fields:
        field_type = field.get_internal_type()
        print(f"  • {field.name}: {field_type}")
    
    # Vérifier les champs de date
    print("\n🔍 CHAMPS DE DATE:")
    date_fields = [f for f in Bon._meta.fields if f.get_internal_type() in ['DateTimeField', 'DateField']]
    for field in date_fields:
        print(f"  • {field.name}: {field.get_internal_type()}")
    
    # Vérifier spécifiquement date_creation
    if hasattr(Bon, 'date_creation'):
        print(f"\n✅ Le modèle Bon a un champ 'date_creation'")
        # Vérifier un exemple
        if Bon.objects.exists():
            bon = Bon.objects.first()
            print(f"  Exemple: {bon.date_creation}")
    else:
        print(f"\n❌ Le modèle Bon n'a pas de champ 'date_creation'")
        
    if hasattr(Bon, 'created_at'):
        print(f"✅ Le modèle Bon a un champ 'created_at'")
    else:
        print(f"❌ Le modèle Bon n'a pas de champ 'created_at'")
        
except ImportError as e:
    print(f"❌ Impossible d'importer le modèle Bon: {e}")
    
    # Essayer avec un autre nom
    try:
        from agents.models import BonSoin
        print("✅ Modèle BonSoin importé avec succès")
        bon_model = BonSoin
    except ImportError:
        try:
            from agents.models import BonDeSoin
            print("✅ Modèle BonDeSoin importé avec succès")
            bon_model = BonDeSoin
        except ImportError as e2:
            print(f"❌ Impossible d'importer aucun modèle Bon: {e2}")
            exit()

print("\n" + "="*70)