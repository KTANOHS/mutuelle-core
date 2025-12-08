# correct_imports.py
import os
import sys
import django
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

print("🔧 CORRECTION DES IMPORTATIONS DE MODÈLES")
print("=" * 50)

# Analyser les modèles disponibles
def analyser_modeles_disponibles():
    """Analyse quels modèles sont réellement disponibles"""
    print("🔍 Analyse des modèles disponibles...")
    
    modeles_analyse = {}
    
    # Membres
    try:
        from membres.models import Membre
        modeles_analyse['Membre'] = True
        print("✅ Membre importé")
        
        # Vérifier les autres modèles dans membres
        try:
            from membres.models import Paiement
            modeles_analyse['Paiement'] = True
            print("✅ Paiement importé")
        except ImportError:
            print("⚠️  Paiement non disponible")
            
        try:
            from membres.models import Cotisation
            modeles_analyse['Cotisation'] = True
            print("✅ Cotisation importé")
        except ImportError:
            print("⚠️  Cotisation non disponible")
            
    except ImportError as e:
        print(f"❌ Membre: {e}")
        modeles_analyse['Membre'] = False
    
    # Médecins
    try:
        from medecin.models import Ordonnance
        modeles_analyse['Ordonnance'] = True
        print("✅ Ordonnance importé")
        
        try:
            from medecin.models import Consultation
            modeles_analyse['Consultation'] = True
            print("✅ Consultation importé")
        except ImportError:
            print("⚠️  Consultation non disponible")
            
        try:
            from medecin.models import BonSoin
            modeles_analyse['BonSoin'] = True
            print("✅ BonSoin importé")
        except ImportError:
            print("⚠️  BonSoin non disponible - chercher variantes...")
            # Chercher des noms alternatifs
            try:
                from medecin.models import BonDeSoin
                modeles_analyse['BonDeSoin'] = True
                print("✅ BonDeSoin importé (nom alternatif)")
            except ImportError:
                print("❌ Aucun modèle BonSoin trouvé")
                
    except ImportError as e:
        print(f"❌ Modèles medecin: {e}")
    
    # Agents
    try:
        from agents.models import Agent
        modeles_analyse['Agent'] = True
        print("✅ Agent importé")
    except ImportError as e:
        print(f"❌ Agent: {e}")
    
    # Communication
    try:
        from communication.models import Notification
        modeles_analyse['Notification'] = True
        print("✅ Notification importé")
    except ImportError as e:
        print(f"❌ Notification: {e}")
    
    return modeles_analyse

# Exécuter l'analyse
modeles = analyser_modeles_disponibles()

print("\n" + "=" * 50)
print("📋 RAPPORT DES MODÈLES DISPONIBLES")
print("=" * 50)

for modele, disponible in modeles.items():
    status = "✅" if disponible else "❌"
    print(f"{status} {modele}")

print("\n💡 RECOMMANDATIONS:")
if not modeles.get('Membre'):
    print("🔴 Vérifier le modèle Membre dans membres/models.py")
if not any(['BonSoin' in k or 'BonDeSoin' in k for k in modeles.keys()]):
    print("🔴 Vérifier le modèle BonSoin/BonDeSoin dans medecin/models.py")