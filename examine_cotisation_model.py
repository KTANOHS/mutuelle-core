# examine_cotisation_model.py
import os
import sys
import django

sys.path.append('/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

# Trouver où se trouve le modèle Cotisation
try:
    from assureur.models import Cotisation
    print("✅ Modèle Cotisation trouvé dans assureur.models")
    
    # Afficher les champs du modèle
    print("\n📊 Champs du modèle Cotisation :")
    for field in Cotisation._meta.fields:
        print(f"  - {field.name} : {field.get_internal_type()}")
    
    print("\n📋 Méthode create du modèle :")
    print("  Les champs attendus sont :")
    for field in Cotisation._meta.fields:
        if not field.auto_created:
            print(f"  • {field.name}")
    
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    
    # Chercher le modèle ailleurs
    print("\n🔍 Recherche du modèle dans d'autres apps...")
    try:
        from cotisations.models import Cotisation
        print("✅ Modèle Cotisation trouvé dans cotisations.models")
    except ImportError:
        print("❌ Modèle Cotisation non trouvé dans cotisations.models")
    
    try:
        from membres.models import Cotisation
        print("✅ Modèle Cotisation trouvé dans membres.models")
    except ImportError:
        print("❌ Modèle Cotisation non trouvé dans membres.models")

# Vérifier la migration actuelle
print("\n📁 Migration actuelle pour assureur_cotisation :")
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("PRAGMA table_info(assureur_cotisation)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")