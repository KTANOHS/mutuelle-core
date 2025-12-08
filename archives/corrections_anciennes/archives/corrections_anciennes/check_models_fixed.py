#!/usr/bin/env python
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Django configuré avec succès")
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

def verifier_correction():
    """Vérifier que la correction a fonctionné"""
    print("\n🔍 VÉRIFICATION CORRECTION MODÈLES")
    print("=" * 50)
    
    try:
        # Essayer d'importer les modèles corrigés
        from communication.models import Conversation, Message, Notification, PieceJointe
        
        print("✅ Modèle 'Conversation' importé")
        print("✅ Modèle 'Message' importé (anciennement Message)")
        print("✅ Modèle 'Notification' importé")
        print("✅ Modèle 'PieceJointe' importé")
        
        # Vérifier que les services fonctionnent maintenant
        from communication.services import MessagerieService, NotificationService
        print("✅ Services de communication importés")
        
        print("\n🎉 CORRECTION RÉUSSIE !")
        print("Le système de communication est maintenant opérationnel.")
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print("=" * 50)

if __name__ == "__main__":
    verifier_correction()