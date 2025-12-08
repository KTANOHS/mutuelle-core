import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

try:
    from medecin.models import EtablissementMedical
    print("✅ Modèle EtablissementMedical existe")
    
    # Afficher les établissements existants
    etablissements = EtablissementMedical.objects.all()
    print(f"Établissements existants: {etablissements.count()}")
    for etab in etablissements:
        print(f"  - {etab.nom} ({etab.type_etablissement})")
        
except ImportError as e:
    print(f"❌ Modèle EtablissementMedical non trouvé: {e}")