# correction_utilisateurs.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def corriger_utilisateurs_assureur():
    from django.contrib.auth.models import User, Group
    
    print("=== CORRECTION UTILISATEURS ASSUREUR ===")
    
    # 1. Créer le groupe ASSUREUR s'il n'existe pas
    group, created = Group.objects.get_or_create(name='ASSUREUR')
    if created:
        print("✅ Groupe ASSUREUR créé")
    else:
        print("✅ Groupe ASSUREUR existe déjà")
    
    # 2. Vérifier/Créer l'utilisateur assureur_test
    try:
        user = User.objects.get(username='assureur_test')
        print("✅ Utilisateur assureur_test existe déjà")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='assureur_test',
            email='assureur@test.com', 
            password='test123',
            first_name='Assureur',
            last_name='Test'
        )
        print("✅ Utilisateur assureur_test créé")
    
    # 3. Ajouter au groupe ASSUREUR
    if group not in user.groups.all():
        user.groups.add(group)
        print("✅ Utilisateur ajouté au groupe ASSUREUR")
    else:
        print("✅ Utilisateur déjà dans le groupe ASSUREUR")
    
    # 4. Vérification finale
    print(f"\n📊 VÉRIFICATION FINALE:")
    print(f"   - Utilisateur: {user.username}")
    print(f"   - Groupes: {[g.name for g in user.groups.all()]}")
    print(f"   - Total dans groupe ASSUREUR: {group.user_set.count()}")

if __name__ == "__main__":
    corriger_utilisateurs_assureur()