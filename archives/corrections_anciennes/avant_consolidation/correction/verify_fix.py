#!/usr/bin/env python3
import os
import sys
import django

project_path = "/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30"
sys.path.insert(0, project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("=== VÉRIFICATION COMPLÈTE DE LA CORRECTION ===")

# 1. Vérifier la vue corrigée
print("\n1. VÉRIFICATION DE LA VUE historique_validation:")
try:
    from pharmacien.views import historique_validation
    print("   ✓ Vue importée avec succès")
    
    # Vérifier les décorateurs
    import inspect
    source = inspect.getsource(historique_validation)
    if '@login_required' in source and '@pharmacien_required' in source and '@gerer_erreurs' in source:
        print("   ✓ Tous les décorateurs présents")
    else:
        print("   ✗ Décorateurs manquants")
        
except Exception as e:
    print(f"   ✗ Erreur: {e}")

# 2. Vérifier le modèle OrdonnancePharmacien
print("\n2. VÉRIFICATION DU MODÈLE OrdonnancePharmacien:")
try:
    from pharmacien.models import OrdonnancePharmacien
    print(f"   ✓ Modèle importé")
    print(f"   - Nombre d'objets: {OrdonnancePharmacien.objects.count()}")
    
    # Afficher les champs importants
    date_fields = [f.name for f in OrdonnancePharmacien._meta.fields if 'date' in f.name]
    print(f"   - Champs de date: {date_fields}")
    
    # Vérifier la relation avec l'utilisateur
    for field in OrdonnancePharmacien._meta.get_fields():
        if field.name == 'pharmacien':
            print(f"   - Relation pharmacien: {field.related_model}")
            break
            
except Exception as e:
    print(f"   ✗ Erreur: {e}")

# 3. Vérifier les URLs
print("\n3. VÉRIFICATION DES URLs:")
try:
    from django.urls import reverse, NoReverseMatch
    
    urls_to_test = [
        'pharmacien:dashboard',
        'pharmacien:historique_validation',
        'pharmacien:liste_ordonnances_attente',
    ]
    
    for url_name in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"   ✓ {url_name} -> {url}")
        except NoReverseMatch as e:
            print(f"   ✗ {url_name}: {e}")
            
except Exception as e:
    print(f"   ✗ Erreur: {e}")

# 4. Vérifier les données de test
print("\n4. DONNÉES DE TEST:")
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Chercher un utilisateur pharmacien
    pharmacien_users = User.objects.filter(groups__name='Pharmacien')[:5]
    if pharmacien_users.exists():
        print(f"   ✓ {pharmacien_users.count()} utilisateur(s) pharmacien trouvé(s)")
        
        # Créer quelques données de test si nécessaire
        from pharmacien.models import OrdonnancePharmacien
        
        for user in pharmacien_users:
            count = OrdonnancePharmacien.objects.filter(pharmacien__user=user).count()
            print(f"   - {user.username}: {count} OrdonnancePharmacien")
            
    else:
        print("   ℹ Aucun utilisateur pharmacien trouvé")
        
except Exception as e:
    print(f"   ✗ Erreur: {e}")

print("\n=== VÉRIFICATION TERMINÉE ===")
print("\nInstructions:")
print("1. Démarrez le serveur: python manage.py runserver")
print("2. Accédez à: http://127.0.0.1:8000/pharmacien/historique/")
print("3. Connectez-vous avec un compte pharmacien")
print("4. Si la page s'affiche sans erreur, la correction est réussie")
