import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import transaction

def refresh_all_user_profiles():
    print("🔄 RAFRAÎCHISSEMENT DES RELATIONS UTILISATEUR-PROFIL...")
    print("=" * 50)
    
    refreshed_count = 0
    
    with transaction.atomic():
        for user in User.objects.all():
            # Forcer le rafraîchissement de l'objet user depuis la base de données
            user_refreshed = User.objects.get(pk=user.pk)
            
            # Vérifier les profils avec l'objet rafraîchi
            profiles_before = []
            profiles_after = []
            
            if hasattr(user, 'membre'): profiles_before.append('Membre')
            if hasattr(user, 'medecin'): profiles_before.append('Medecin')
            if hasattr(user, 'pharmacien'): profiles_before.append('Pharmacien')
            if hasattr(user, 'assureur'): profiles_before.append('Assureur')
            
            if hasattr(user_refreshed, 'membre'): profiles_after.append('Membre')
            if hasattr(user_refreshed, 'medecin'): profiles_after.append('Medecin')
            if hasattr(user_refreshed, 'pharmacien'): profiles_after.append('Pharmacien')
            if hasattr(user_refreshed, 'assureur'): profiles_after.append('Assureur')
            
            if profiles_before != profiles_after:
                print(f"👤 {user.username}:")
                print(f"   AVANT: {profiles_before}")
                print(f"   APRÈS: {profiles_after}")
                refreshed_count += 1
            else:
                print(f"👤 {user.username}: ✅ Profils cohérents: {profiles_after}")
    
    return refreshed_count

def verify_final_state():
    print("\n🔍 VÉRIFICATION FINALE AVEC OBJETS FRAIS:")
    print("=" * 40)
    
    from membres.models import Membre
    from medecin.models import Medecin
    from pharmacien.models import Pharmacien
    from assureur.models import Assureur
    
    stats = {
        'Utilisateurs': User.objects.count(),
        'Membres': Membre.objects.count(),
        'Médecins': Medecin.objects.count(),
        'Pharmaciens': Pharmacien.objects.count(),
        'Assureurs': Assureur.objects.count()
    }
    
    print("📊 STATISTIQUES:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n👥 DÉTAIL DES RELATIONS:")
    for user in User.objects.all():
        groups = [g.name for g in user.groups.all()]
        profiles = []
        
        # Utiliser des objets frais
        user_fresh = User.objects.get(pk=user.pk)
        
        if hasattr(user_fresh, 'membre'): profiles.append('Membre')
        if hasattr(user_fresh, 'medecin'): profiles.append('Medecin')
        if hasattr(user_fresh, 'pharmacien'): profiles.append('Pharmacien')
        if hasattr(user_fresh, 'assureur'): profiles.append('Assureur')
        
        status = "✅" if (groups and profiles) or (not groups and not profiles) else "⚠️"
        print(f"  {status} {user.username}: Groupes={groups} | Profils={profiles}")

def fix_remaining_inconsistencies():
    """Corrige les dernières incohérences de groupes"""
    print("\n🔧 CORRECTION DES DERNIÈRES INCOHÉRENCES...")
    
    from django.contrib.auth.models import Group
    
    for user in User.objects.all():
        user_fresh = User.objects.get(pk=user.pk)
        groups = [g.name for g in user_fresh.groups.all()]
        
        # Ajouter le groupe manquant si le profil existe
        if hasattr(user_fresh, 'assureur') and 'assureur' not in groups:
            assureur_group = Group.objects.get(name='assureur')
            user_fresh.groups.add(assureur_group)
            print(f"   ✅ {user.username}: groupe 'assureur' ajouté")
        
        if hasattr(user_fresh, 'pharmacien') and 'pharmacien' not in groups:
            pharmacien_group = Group.objects.get(name='pharmacien')
            user_fresh.groups.add(pharmacien_group)
            print(f"   ✅ {user.username}: groupe 'pharmacien' ajouté")

if __name__ == "__main__":
    print("🎯 DÉMARRAGE DU RAFRAÎCHISSEMENT FINAL")
    
    refreshed = refresh_all_user_profiles()
    fix_remaining_inconsistencies()
    verify_final_state()
    
    print(f"\n🎉 RAFRAÎCHISSEMENT TERMINÉ: {refreshed} utilisateurs mis à jour!")
    print("\n📋 ÉTAPE SUIVANTE:")
    print("   Exécutez: python diagnostic_access.py")