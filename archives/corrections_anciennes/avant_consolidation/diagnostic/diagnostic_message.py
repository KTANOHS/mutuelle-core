# diagnostic_message.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostic_message():
    print("=== DIAGNOSTIC MODÈLE MESSAGE ===")
    
    try:
        from communication.models import Message
        
        # Vérifier si le modèle existe
        messages = Message.objects.all()
        print(f"Nombre de messages: {messages.count()}")
        
        if messages.exists():
            first_msg = messages.first()
            print(f"\nStructure du premier message (ID: {first_msg.id}):")
            
            # Lister tous les champs disponibles
            fields = [f.name for f in first_msg._meta.fields]
            print(f"Champs disponibles: {fields}")
            
            # Afficher les valeurs de chaque champ
            for field in first_msg._meta.fields:
                try:
                    value = getattr(first_msg, field.name)
                    print(f"  - {field.name}: {value}")
                except Exception as e:
                    print(f"  - {field.name}: ERREUR - {e}")
                    
        else:
            print("Aucun message dans la base de données")
            
    except Exception as e:
        print(f"❌ Erreur avec le modèle Message: {e}")
        
        # Essayer d'importer quand même pour voir la structure
        try:
            from communication.models import Message
            print("✓ Modèle Message importé avec succès")
            print(f"Champs définis: {[f.name for f in Message._meta.fields]}")
        except Exception as import_error:
            print(f"❌ Impossible d'importer le modèle Message: {import_error}")

if __name__ == "__main__":
    diagnostic_message()