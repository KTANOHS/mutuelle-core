#!/usr/bin/env python
"""
RÉSOLUTION DÉFINITIVE DES PERMISSIONS POUR GLORIA1
"""

import os
import sys
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import Permission, Group, ContentType
from django.contrib.auth import get_user_model
from django.db import transaction

def debug_permissions():
    """Debug complet des permissions"""
    print("🔍 DEBUG COMPLET DES PERMISSIONS")
    print("=" * 60)
    
    # 1. Cherche toutes les permissions avec 'ordonnance' dans le nom
    ordonnance_perms = Permission.objects.filter(codename__contains='ordonnance')
    print(f"Permissions avec 'ordonnance': {ordonnance_perms.count()}")
    
    for perm in ordonnance_perms:
        print(f"\n📋 {perm.codename}:")
        print(f"   ID: {perm.id}")
        print(f"   ContentType: {perm.content_type.app_label}.{perm.content_type.model}")
        print(f"   Nom: {perm.name}")
        
        # Cherche quels groupes ont cette permission
        groups = Group.objects.filter(permissions=perm)
        if groups.exists():
            print(f"   Groupes: {', '.join([g.name for g in groups])}")
        else:
            print(f"   ⚠ Aucun groupe")
    
    # 2. Vérifie le groupe Pharmacien
    print("\n" + "=" * 60)
    print("💊 GROUPE PHARMACIEN")
    print("=" * 60)
    
    try:
        group = Group.objects.get(name='Pharmacien')
        print(f"✅ Groupe Pharmacien trouvé")
        print(f"   ID: {group.id}")
        print(f"   Permissions: {group.permissions.count()}")
        
        # Liste toutes les permissions du groupe
        for perm in group.permissions.all():
            print(f"   - {perm.content_type.app_label}.{perm.codename}")
        
    except Group.DoesNotExist:
        print("❌ Groupe Pharmacien non trouvé")
    
    # 3. Vérifie GLORIA1
    print("\n" + "=" * 60)
    print("👤 UTILISATEUR GLORIA1")
    print("=" * 60)
    
    User = get_user_model()
    try:
        user = User.objects.get(username='GLORIA1')
        print(f"✅ GLORIA1 trouvé")
        print(f"   Groupes: {[g.name for g in user.groups.all()]}")
        
        # Test détaillé des permissions
        print(f"\n🧪 TEST DÉTAILLÉ DES PERMISSIONS:")
        
        # Liste des permissions à tester avec leurs ContentTypes possibles
        permissions_tests = [
            ('view_ordonnance', ['ordonnances', 'pharmacien', 'soins', 'ordonnance']),
            ('change_ordonnance', ['ordonnances', 'pharmacien', 'soins', 'ordonnance']),
            ('view_stockpharmacie', ['pharmacien']),
            ('change_stockpharmacie', ['pharmacien']),
            ('view_pharmacien', ['pharmacien']),
        ]
        
        for perm_codename, app_labels in permissions_tests:
            print(f"\n🔍 {perm_codename}:")
            found = False
            
            # Test 1: Avec app_label
            for app_label in app_labels:
                if user.has_perm(f'{app_label}.{perm_codename}'):
                    print(f"   ✅ {app_label}.{perm_codename}: OUI")
                    found = True
                    break
            
            # Test 2: Sans app_label
            if not found and user.has_perm(perm_codename):
                print(f"   ✅ {perm_codename} (sans app_label): OUI")
                found = True
            
            if not found:
                print(f"   ❌ {perm_codename}: NON")
                
                # Cherche pourquoi
                perms = Permission.objects.filter(codename=perm_codename)
                if perms.exists():
                    print(f"   ℹ️  Permissions existent dans DB ({perms.count()}):")
                    for p in perms:
                        print(f"      - {p.content_type.app_label}.{p.codename}")
                else:
                    print(f"   ℹ️  Aucune permission avec ce codename dans DB")
        
    except User.DoesNotExist:
        print("❌ GLORIA1 non trouvé")

def fix_ordonnance_permissions():
    """Corrige spécifiquement les permissions d'ordonnance"""
    print("\n" + "=" * 60)
    print("📄 CORRECTION DES PERMISSIONS D'ORDONNANCE")
    print("=" * 60)
    
    with transaction.atomic():
        # 1. Trouve ou crée le ContentType pour ordonnances
        ct, created = ContentType.objects.get_or_create(
            app_label='ordonnances',
            model='ordonnance'
        )
        
        if created:
            print(f"✅ ContentType créé: ordonnances.ordonnance")
        else:
            print(f"✅ ContentType existant: ordonnances.ordonnance (ID: {ct.id})")
        
        # 2. Trouve ou crée les permissions
        permissions_to_create = [
            ('view_ordonnance', 'Can view ordonnance'),
            ('change_ordonnance', 'Can change ordonnance'),
            ('add_ordonnance', 'Can add ordonnance'),
            ('delete_ordonnance', 'Can delete ordonnance'),
        ]
        
        created_perms = []
        for codename, name in permissions_to_create:
            perm, created = Permission.objects.get_or_create(
                codename=codename,
                content_type=ct,
                defaults={'name': name}
            )
            
            if created:
                created_perms.append(perm)
                print(f"✅ Permission créée: {codename}")
            else:
                print(f"✅ Permission existante: {codename}")
        
        # 3. Ajoute ces permissions au groupe Pharmacien
        try:
            group = Group.objects.get(name='Pharmacien')
            
            for perm in [Permission.objects.get(codename='view_ordonnance', content_type=ct),
                        Permission.objects.get(codename='change_ordonnance', content_type=ct)]:
                if not group.permissions.filter(id=perm.id).exists():
                    group.permissions.add(perm)
                    print(f"✅ Permission ajoutée au groupe: {perm.codename}")
                else:
                    print(f"✅ Permission déjà dans le groupe: {perm.codename}")
            
            # 4. Met à jour GLORIA1
            User = get_user_model()
            gloria1 = User.objects.get(username='GLORIA1')
            
            # S'assure que GLORIA1 est dans le groupe
            if not gloria1.groups.filter(name='Pharmacien').exists():
                gloria1.groups.add(group)
                print(f"✅ GLORIA1 ajouté au groupe Pharmacien")
            
            # Force la récupération des permissions
            gloria1 = User.objects.get(pk=gloria1.pk)
            
            # Test
            print(f"\n🧪 TEST APRÈS CORRECTION:")
            if gloria1.has_perm('ordonnances.view_ordonnance'):
                print(f"✅ GLORIA1 peut voir les ordonnances")
            else:
                print(f"❌ GLORIA1 ne peut pas voir les ordonnances")
            
            if gloria1.has_perm('ordonnances.change_ordonnance'):
                print(f"✅ GLORIA1 peut modifier les ordonnances")
            else:
                print(f"❌ GLORIA1 ne peut pas modifier les ordonnances")
                
        except Group.DoesNotExist:
            print("❌ Groupe Pharmacien non trouvé")
        except User.DoesNotExist:
            print("❌ GLORIA1 non trouvé")
    
    return created_perms

def force_add_all_ordonnance_permissions():
    """Force l'ajout de TOUTES les permissions d'ordonnance"""
    print("\n" + "=" * 60)
    print("⚡ AJOUT FORCÉ DE TOUTES LES PERMISSIONS ORDONNANCE")
    print("=" * 60)
    
    User = get_user_model()
    
    with transaction.atomic():
        # 1. Récupère le groupe Pharmacien
        group = Group.objects.get(name='Pharmacien')
        
        # 2. Trouve TOUTES les permissions qui contiennent "ordonnance"
        all_ordonnance_perms = Permission.objects.filter(codename__contains='ordonnance')
        print(f"Permissions trouvées avec 'ordonnance': {all_ordonnance_perms.count()}")
        
        # 3. Ajoute toutes ces permissions au groupe
        added_count = 0
        for perm in all_ordonnance_perms:
            if not group.permissions.filter(id=perm.id).exists():
                group.permissions.add(perm)
                added_count += 1
                print(f"✅ Ajoutée: {perm.codename} ({perm.content_type.app_label})")
        
        print(f"\n✅ {added_count} permissions ajoutées au groupe Pharmacien")
        
        # 4. Met à jour GLORIA1
        gloria1 = User.objects.get(username='GLORIA1')
        
        # Force le rafraîchissement
        gloria1 = User.objects.get(pk=gloria1.pk)
        
        # 5. Test complet
        print(f"\n🧪 TEST COMPLET APRÈS AJOUT:")
        
        # Test toutes les permissions d'ordonnance possibles
        ordonnance_permissions = [
            'view_ordonnance',
            'change_ordonnance', 
            'add_ordonnance',
            'delete_ordonnance',
            'view_ordonnancepharmacien',
            'change_ordonnancepharmacien',
            'add_ordonnancepharmacien',
            'delete_ordonnancepharmacien',
        ]
        
        for perm_name in ordonnance_permissions:
            # Essaie toutes les combinaisons possibles d'app_labels
            found = False
            app_labels = ['ordonnances', 'pharmacien', 'soins', 'ordonnance']
            
            for app_label in app_labels:
                if gloria1.has_perm(f'{app_label}.{perm_name}'):
                    print(f"✅ {perm_name}: OUI ({app_label}.{perm_name})")
                    found = True
                    break
            
            if not found and gloria1.has_perm(perm_name):
                print(f"✅ {perm_name}: OUI ({perm_name})")
                found = True
            
            if not found:
                print(f"❌ {perm_name}: NON")
    
    return added_count

def create_simple_test_script():
    """Crée un script de test simple"""
    print("\n" + "=" * 60)
    print("📝 CRÉATION SCRIPT DE TEST SIMPLE")
    print("=" * 60)
    
    script_content = '''#!/usr/bin/env python
"""
TEST SIMPLE DES PERMISSIONS
"""
import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mutuelle_core.settings")
django.setup()

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Permission, Group

def test_permissions():
    print("🧪 TEST DES PERMISSIONS DE GLORIA1")
    print("=" * 50)
    
    # Authentification
    user = authenticate(username="GLORIA1", password="Pharmacien123!")
    
    if not user:
        print("❌ Échec d'authentification")
        return
    
    print(f"✅ Authentifié: {user.username}")
    print(f"Groupes: {[g.name for g in user.groups.all()]}")
    
    # Test des permissions spécifiques
    print("\\n🔍 TEST DES PERMISSIONS:")
    
    permissions_to_test = [
        ("view_ordonnance", "Voir les ordonnances"),
        ("change_ordonnance", "Modifier les ordonnances"),
        ("view_stockpharmacie", "Voir le stock"),
        ("change_stockpharmacie", "Modifier le stock"),
        ("view_pharmacien", "Voir le profil pharmacien"),
    ]
    
    for perm_codename, description in permissions_to_test:
        # Essaie avec différents app_labels
        found = False
        app_labels = ["ordonnances", "pharmacien", "soins", "ordonnance"]
        
        for app_label in app_labels:
            if user.has_perm(f"{app_label}.{perm_codename}"):
                print(f"✅ {description}: OUI ({app_label}.{perm_codename})")
                found = True
                break
        
        if not found and user.has_perm(perm_codename):
            print(f"✅ {description}: OUI ({perm_codename})")
            found = True
        
        if not found:
            print(f"❌ {description}: NON")

if __name__ == "__main__":
    test_permissions()
'''
    
    # Écrit le script
    with open('test_simple_permissions.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ Script créé: test_simple_permissions.py")
    print("📋 Exécutez-le avec: python test_simple_permissions.py")

def main():
    """Fonction principale"""
    print("🚀 RÉSOLUTION DÉFINITIVE DES PERMISSIONS")
    print("=" * 60)
    
    # Option 1: Debug
    print("\n1. Debug des permissions actuelles...")
    debug_permissions()
    
    # Option 2: Ajout forcé de toutes les permissions
    print("\n" + "=" * 60)
    response = input("Voulez-vous forcer l'ajout de TOUTES les permissions 'ordonnance'? (Oui/Non): ").strip().lower()
    
    if response in ['oui', 'o', 'yes', 'y']:
        print("\n2. Ajout forcé des permissions...")
        force_add_all_ordonnance_permissions()
    
    # Option 3: Créer un script de test
    print("\n3. Création d'un script de test...")
    create_simple_test_script()
    
    print("\n" + "=" * 60)
    print("✅ CORRECTIONS TERMINÉES")
    print("=" * 60)
    print("\n📋 PROCHAINES ÉTAPES:")
    print("1. Testez les permissions: python test_simple_permissions.py")
    print("2. Redémarrez le serveur Django (si en cours)")
    print("3. Testez l'accès web: http://127.0.0.1:8000/pharmacien/ordonnances/")
    print("\n🔧 Si problème persiste:")
    print("   - Vérifiez dans l'admin Django que GLORIA1 a les permissions")
    print("   - Utilisez la vue d'admin: http://127.0.0.1:8000/admin/")

if __name__ == "__main__":
    main()