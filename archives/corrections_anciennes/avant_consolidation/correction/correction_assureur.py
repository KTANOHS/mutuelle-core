# correction_assureur.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User
from assureur.models import Assureur

def corriger_relations():
    """Corrige les relations entre User et Assureur"""
    print("🔧 Correction des relations User-Assureur")
    
    # Vérifier tous les users
    users = User.objects.all()
    for user in users:
        # Vérifier si l'user a un profil assureur
        if hasattr(user, 'assureur_profile'):
            print(f"✅ User {user.username} a déjà assureur_profile")
        else:
            # Chercher un assureur lié à cet user via un autre champ
            try:
                assureur = Assureur.objects.get(user=user)
                print(f"⚠️  User {user.username} a un Assureur mais pas de relation 'assureur_profile'")
                print(f"   Assureur: {assureur.numero_employe}")
            except Assureur.DoesNotExist:
                pass
    
    print("\n✅ Vérification terminée")

def tester_vue_dashboard():
    """Teste la vue dashboard avec un user"""
    print("\n🧪 Test de la vue dashboard")
    
    # Trouver un user avec assureur_profile
    user = User.objects.filter(assureur_profile__isnull=False).first()
    
    if user:
        print(f"User test: {user.username}")
        print(f"Assureur profile: {user.assureur_profile}")
        print(f"Nom via propriété: {getattr(user.assureur_profile, 'nom', 'Non disponible')}")
    else:
        print("❌ Aucun user avec assureur_profile trouvé")
        
        # Créer un user de test si nécessaire
        user, created = User.objects.get_or_create(
            username='admin_test',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        if created:
            user.set_password('admin123')
            user.save()
            print("✅ User admin_test créé")

if __name__ == "__main__":
    corriger_relations()
    tester_vue_dashboard()