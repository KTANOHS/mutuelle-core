#!/usr/bin/env python
import os
import sys
import django

# Modifier cette ligne avec le bon chemin de settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

# Ajouter le chemin du projet
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur de configuration Django: {e}")
    print("💡 Vérifiez le chemin de settings dans le script")
    sys.exit(1)

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate

def final_check():
    print("🔍 VÉRIFICATION FINALE DES PERMISSIONS")
    print("=" * 50)
    
    # Test d'authentification
    user = authenticate(username='GLORIA1', password='NouveauMotDePasse123')
    
    if not user:
        print("❌ Échec d'authentification")
        print("💡 Essayez avec le mot de passe original ou réinitialisez-le:")
        print("   python manage.py shell")
        print("   from django.contrib.auth.models import User")
        print("   user = User.objects.get(username='GLORIA1')")
        print("   user.set_password('VotreMotDePasse')")
        print("   user.save()")
        return
    
    print(f"✅ Authentifié: {user.username}")
    print(f"📋 Groupes: {[g.name for g in user.groups.all()]}")
    
    # Permissions critiques
    permissions = [
        ('medecin.view_ordonnance', 'Voir ordonnances médecin'),
        ('medecin.change_ordonnance', 'Modifier ordonnances médecin'),
        ('medecin.add_ordonnance', 'Ajouter ordonnances médecin'),
        ('medecin.delete_ordonnance', 'Supprimer ordonnances médecin'),
        ('pharmacien.view_ordonnancepharmacien', 'Voir ordonnances pharmacien'),
        ('pharmacien.change_ordonnancepharmacien', 'Modifier ordonnances pharmacien'),
        ('pharmacien.add_ordonnancepharmacien', 'Ajouter ordonnances pharmacien'),
        ('pharmacien.delete_ordonnancepharmacien', 'Supprimer ordonnances pharmacien'),
        ('pharmacien.view_stockpharmacie', 'Voir stock pharmacie'),
        ('pharmacien.change_stockpharmacie', 'Modifier stock pharmacie'),
    ]
    
    print("\n🔐 PERMISSIONS CRITIQUES:")
    print("-" * 40)
    
    for perm_code, perm_name in permissions:
        if user.has_perm(perm_code):
            print(f"✅ {perm_name}")
        else:
            print(f"❌ {perm_name}")
    
    # Résumé
    print("\n📊 RÉSUMÉ:")
    print(f"   • Total permissions: {len(user.get_all_permissions())}")
    print(f"   • Est actif: {user.is_active}")
    print(f"   • Superutilisateur: {user.is_superuser}")
    
    print("\n" + "=" * 50)
    print("✅ VÉRIFICATION TERMINÉE")
    print("\n📋 ÉTAPES FINALES:")
    print("1. Redémarrez le serveur Django")
    print("2. Connectez-vous avec GLORIA1")
    print("3. Testez l'interface web")

if __name__ == "__main__":
    final_check()