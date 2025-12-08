# creation_agent_test.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

print("👤 CRÉATION UTILISATEUR AGENT TEST")
print("=" * 40)

def creer_agent_test():
    """Crée un utilisateur agent de test"""
    
    try:
        # 1. Créer l'utilisateur
        user, created = User.objects.get_or_create(
            username='test_agent',
            defaults={
                'email': 'agent@test.com',
                'first_name': 'Agent',
                'last_name': 'Test',
                'is_active': True,
                'is_staff': True
            }
        )
        
        if created:
            user.set_password('testpass123')
            user.save()
            print("✅ Utilisateur test_agent créé")
        else:
            print("✅ Utilisateur test_agent existe déjà")
        
        # 2. Créer/assigner le groupe Agents
        groupe, groupe_created = Group.objects.get_or_create(name='Agents')
        if groupe_created:
            print("✅ Groupe Agents créé")
        else:
            print("✅ Groupe Agents existe déjà")
        
        user.groups.add(groupe)
        print("✅ Utilisateur ajouté au groupe Agents")
        
        # 3. Vérification
        print(f"\n📋 INFORMATIONS UTILISATEUR:")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Nom complet: {user.get_full_name()}")
        print(f"   Groupes: {[g.name for g in user.groups.all()]}")
        print(f"   Mot de passe: testpass123")
        
        return user
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

if creuer_agent_test():
    print("\n🎉 UTILISATEUR AGENT PRÊT !")
    print("💡 Connectez-vous avec: test_agent / testpass123")