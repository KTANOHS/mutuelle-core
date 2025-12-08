# verification_finale.py
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

django.setup()

from django.contrib.auth import get_user_model
from django.apps import apps

def verification_complete():
    """Vérification complète après redémarrage"""
    print("🎯 VÉRIFICATION COMPLÈTE APRÈS REDÉMARRAGE")
    print("=" * 60)
    
    User = get_user_model()
    
    # Test de tous les utilisateurs problématiques
    test_cases = [
        ('test_medecin', 'Medecin', 'medecin'),
        ('docteur_kouame', 'Medecin', 'medecin'),
        ('test_membre', 'Membre', 'membre'),
        ('test_assureur', 'Assureur', 'assureur')
    ]
    
    print("📊 ÉTAT DES RELATIONS:")
    
    for username, model_name, relation_name in test_cases:
        try:
            user = User.objects.get(username=username)
            
            # Test 1: Relation Django
            has_django_relation = hasattr(user, relation_name)
            
            # Test 2: Existence en base
            model_class = apps.get_model(relation_name, model_name)
            exists_in_db = model_class.objects.filter(user=user).exists()
            
            status = "✅" if has_django_relation else "❌"
            db_status = "✅" if exists_in_db else "❌"
            
            print(f"\n{status} {username}:")
            print(f"   Relation Django: {has_django_relation}")
            print(f"   Existe en base: {exists_in_db}")
            
            if has_django_relation:
                obj = getattr(user, relation_name)
                print(f"   📋 Objet: {obj}")
                print(f"   🎯 Redirection: /{relation_name}/dashboard/")
            elif exists_in_db:
                obj = model_class.objects.get(user=user)
                print(f"   ⚠️  Objet en base mais relation inaccessible: {obj}")
                print(f"   💡 Redirection par groupe vers: /{relation_name}/dashboard/")
            else:
                print(f"   🚨 AUCUN OBJET TROUVÉ")
                
        except Exception as e:
            print(f"❌ {username}: Erreur - {e}")
    
    print("\n" + "=" * 60)
    print("💡 RAPPEL: Même si les relations Django ne sont pas accessibles,")
    print("   la redirection devrait fonctionner par DÉTECTION DE GROUPE")
    print("   dans la vue redirect_after_login")

if __name__ == "__main__":
    verification_complete()