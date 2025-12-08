# analyser_structure_agent.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import Agent

def analyser_structure_agent():
    print("🔍 ANALYSE DE LA STRUCTURE DU MODÈLE AGENT...")
    
    # 1. Vérifier les champs disponibles
    print("\n📋 CHAMPS DU MODÈLE AGENT:")
    for field in Agent._meta.get_fields():
        print(f"  - {field.name} ({field.get_internal_type()})")
    
    # 2. Vérifier s'il y a des agents existants
    print(f"\n👨‍💼 AGENTS EXISTANTS: {Agent.objects.count()}")
    
    # 3. Analyser VerificationCotisation
    from agents.models import VerificationCotisation
    print("\n📋 CHAMPS DU MODÈLE VERIFICATIONCOTISATION:")
    for field in VerificationCotisation._meta.get_fields():
        print(f"  - {field.name} ({field.get_internal_type()})")
    
    # 4. Vérifier la relation entre Agent et User
    try:
        from django.contrib.auth.models import User
        print("\n🔗 RELATION AVEC USER:")
        # Vérifier si Agent a un champ user
        for field in Agent._meta.get_fields():
            if hasattr(field, 'related_model') and field.related_model == User:
                print(f"  - Relation User trouvée: {field.name}")
    except:
        pass

if __name__ == "__main__":
    analyser_structure_agent()