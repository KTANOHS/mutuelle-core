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

def create_custom_permission_check():
    """Crée une vérification personnalisée des permissions"""
    print("\n" + "=" * 60)
    print("🎯 VÉRIFICATION PERSONNALISÉE")
    print("=" * 60)
    
    User = get_user_model()
    
    try:
        user = User.objects.get(username='GLORIA1')
        
        # Fonction de vérification étendue
        def check_perm_extended(user, perm_codename, app_labels):
            """Vérifie une permission avec plusieurs app_labels possibles"""
            for app_label in app_labels:
                if user.has_perm(f'{app_label}.{perm_codename}'):
                    return True, f'{app_label}.{perm_codename}'
            
            if user.has_perm(perm_codename):
                return True, perm_codename
            
            return False, None
        
        # Liste des permissions et leurs app_labels possibles
        permissions_map = {
            'view_ordonnance': ['ordonnances', 'pharmacien', 'soins', 'ordonnance', 'ordonnancepharmacien'],
            'change_ordonnance': ['ordonnances', 'pharmacien', 'soins', 'ordonnance', 'ordonnancepharmacien'],
            'view_stockpharmacie': ['pharmacien'],
            'change_stockpharmacie': ['pharmacien'],
            'view_pharmacien': ['pharmacien'],
            'view_medicament': ['medicaments', 'pharmacien'],
            'change_medicament': ['medicaments', 'pharmacien'],
        }
        
        print("📊 RÉSULTATS DES PERMISSIONS:")
        for perm_codename, app_labels in permissions_map.items():
            has_perm, location = check_perm_extended(user, perm_codename, app_labels)
            
            if has_perm:
                print(f"✅ {perm_codename}: OUI ({location})")
            else:
                print(f"❌ {perm_codename}: NON")
                
                # Cherche les permissions dans la DB
                perms = Permission.objects.filter(codename=perm_codename)
                if perms.exists():
                    print(f"   ℹ️  Disponible dans DB:")
                    for p in perms:
                        groups = Group.objects.filter(permissions=p)
                        group_names = [g.name for g in groups] if groups.exists() else ['Aucun']
                        print(f"      - {p.content_type.app_label}.{p.codename} (Groupes: {', '.join(group_names)})")
        
    except User.DoesNotExist:
        print("❌ GLORIA1 non trouvé")

def force_add_permissions():
    """Force l'ajout des permissions nécessaires"""
    print("\n" + "=" * 60)
    print("⚡ AJOUT FORCÉ DES PERMISSIONS")
    print("=" * 60)
    
    with transaction.atomic():
        # 1. Trouve le groupe Pharmacien
        group = Group.objects.get(name='Pharmacien')
        
        # 2. Trouve toutes les permissions avec 'ordonnance' dans le codename
        ordonnance_perms = Permission.objects.filter(codename__contains='ordonnance')
        print(f"Permissions 'ordonnance' trouvées: {ordonnance_perms.count()}")
        
        added = 0
        for perm in ordonnance_perms:
            if not group.permissions.filter(id=perm.id).exists():
                group.permissions.add(perm)
                added += 1
                print(f"✅ Ajoutée: {perm.codename} ({perm.content_type.app_label})")
        
        print(f"\n✅ {added} permissions ajoutées au groupe")
        
        # 3. Met à jour GLORIA1
        User = get_user_model()
        gloria1 = User.objects.get(username='GLORIA1')
        
        # Force la récupération
        gloria1 = User.objects.get(pk=gloria1.pk)
        
        # Test
        print(f"\n🧪 TEST FINAL:")
        
        # Liste des permissions à vérifier
        test_perms = [
            'view_ordonnance',
            'change_ordonnance',
            'view_stockpharmacie',
            'change_stockpharmacie',
            'view_pharmacien',
        ]
        
        for perm_codename in test_perms:
            # Essaie tous les app_labels possibles
            app_labels = ['ordonnances', 'pharmacien', 'soins', 'ordonnancepharmacien', 'medicaments']
            found = False
            
            for app_label in app_labels:
                if gloria1.has_perm(f'{app_label}.{perm_codename}'):
                    print(f"✅ {perm_codename}: OUI ({app_label}.{perm_codename})")
                    found = True
                    break
            
            if not found and gloria1.has_perm(perm_codename):
                print(f"✅ {perm_codename}: OUI ({perm_codename})")
                found = True
            
            if not found:
                print(f"❌ {perm_codename}: NON")
    
    return added

def create_test_script():
    """Crée un script de test pour vérifier les permissions"""
    print("\n" + "=" * 60)
    print("📝 CRÉATION SCRIPT DE TEST")
    print("=" * 60)
    
    script_content = """#!/usr/bin/env python
"""
TEST MANUEL DES PERMISSIONS
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Permission, Group

def test_gloria1_permissions():
    \"\"\"Teste toutes les permissions de GLORIA1\"\"\"
    print("🧪 TEST COMPLET DES PERMISSIONS GLORIA1")
    print("=" * 60)
    
    # Authentification
    user = authenticate(username='GLORIA1', password='Pharmacien123!')
    
    if not user:
        print("❌ Échec d'authentification")
        return
    
    print(f"✅ Authentifié: {user.username}")
    
    # 1. Vérifie les groupes
    groups = user.groups.all()
    print(f"\\n👥 GROUPES ({len(groups)}):")
    for group in groups:
        print(f"   - {group.name}")
    
    # 2. Liste toutes les permissions via les groupes
    all_perms = set()
    for group in groups:
        for perm in group.permissions.all():
            all_perms.add(f"{perm.content_type.app_label}.{perm.codename}")
    
    print(f"\\n🔑 PERMISSIONS ({len(all_perms)}):")
    for perm in sorted(all_perms):
        print(f"   - {perm}")
    
    # 3. Test spécifique des permissions importantes
    print(f"\\n🎯 TEST DES PERMISSIONS IMPORTANTES:")
    
    test_permissions = [
        # Ordonnances
        ('view_ordonnance', 'Voir les ordonnances'),
        ('change_ordonnance', 'Modifier les ordonnances'),
        ('delete_ordonnance', 'Supprimer les ordonnances'),
        ('add_ordonnance', 'Créer des ordonnances'),
        
        # Pharmacien
        ('view_pharmacien', 'Voir le profil pharmacien'),
        ('change_pharmacien', 'Modifier le profil pharmacien'),
        
        # Stock
        ('view_stockpharmacie', 'Voir le stock'),
        ('change_stockpharmacie', 'Modifier le stock'),
        ('add_stockpharmacie', 'Ajouter au stock'),
        ('delete_stockpharmacie', 'Supprimer du stock'),
        
        # Médicaments
        ('view_medicament', 'Voir les médicaments'),
        ('change_medicament', 'Modifier les médicaments'),
        
        # Communication
        ('view_message', 'Voir les messages'),
        ('add_message', 'Envoyer des messages'),
    ]
    
    for perm_codename, description in test_permissions:
        # Essaie avec différents app_labels
        app_labels = ['ordonnances', 'pharmacien', 'soins', 'medicaments', 'communication', 'ordonnancepharmacien']
        
        found = False
        for app_label in app_labels:
            if user.has_perm(f'{app_label}.{perm_codename}'):
                print(f"   ✅ {description}: OUI ({app_label}.{perm_codename})")
                found = True
                break
        
        if not found and user.has_perm(perm_codename):
            print(f"   ✅ {description}: OUI ({perm_codename})")
            found = True
        
        if not found:
            print(f"   ❌ {description}: NON")
    
    # 4. Vérifie si l'utilisateur peut accéder aux URLs
    print(f"\\n🌐 SIMULATION D'ACCÈS AUX URLs:")
    
    urls_to_test = [
        ('/pharmacien/dashboard/', 'Dashboard pharmacien'),
        ('/pharmacien/ordonnances/', 'Liste des ordonnances'),
        ('/pharmacien/ordonnances/1/', 'Détail ordonnance'),
        ('/pharmacien/stock/', 'Gestion du stock'),
        ('/pharmacien/historique/', 'Historique'),
        ('/communication/messagerie/', 'Messagerie'),
    ]
    
    for url, description in urls_to_test:
        # Permissions nécessaires pour chaque URL
        required_perms = {
            '/pharmacien/dashboard/': ['view_pharmacien'],
            '/pharmacien/ordonnances/': ['view_ordonnance'],
            '/pharmacien/ordonnances/1/': ['view_ordonnance', 'change_ordonnance'],
            '/pharmacien/stock/': ['view_stockpharmacie'],
            '/pharmacien/historique/': ['view_pharmacien'],
            '/communication/messagerie/': ['view_message'],
        }
        
        if url in required_perms:
            perms_needed = required_perms[url]
            has_all = True
            
            for perm_needed in perms_needed:
                has_perm = False
                for app_label in ['pharmacien', 'ordonnances', 'communication']:
                    if user.has_perm(f'{app_label}.{perm_needed}'):
                        has_perm = True
                        break
                
                if not has_perm and user.has_perm(perm_needed):
                    has_perm = True
                
                if not has_perm:
                    has_all = False
                    break
            
            if has_all:
                print(f"   ✅ {description}: Accès AUTORISÉ")
            else:
                print(f"   ❌ {description}: Accès REFUSÉ (permissions manquantes)")
        else:
            print(f"   ⚠ {description}: Permissions inconnues")

if __name__ == "__main__":
    test_gloria1_permissions()
"""
    
    # Écrit le script
    with open('test_permissions_final.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ Script créé: test_permissions_final.py")
    print("\n📋 POUR L'EXÉCUTER:")
    print("   python test_permissions_final.py")

def main():
    """Fonction principale"""
    print("🚀 RÉSOLUTION DÉFINITIVE DES PERMISSIONS")
    print("=" * 60)
    
    # 1. Debug initial
    debug_permissions()
    
    # 2. Corrige les permissions d'ordonnance
    print("\n" + "=" * 60)
    input("Appuyez sur Entrée pour corriger les permissions d'ordonnance...")
    fix_ordonnance_permissions()
    
    # 3. Vérification personnalisée
    print("\n" + "=" * 60)
    input("Appuyez sur Entrée pour vérification personnalisée...")
    create_custom_permission_check()
    
    # 4. Ajout forcé des permissions
    print("\n" + "=" * 60)
    response = input("Voulez-vous forcer l'ajout de toutes les permissions 'ordonnance'? (o/N): ").lower()
    if response == 'o':
        force_add_permissions()
    
    # 5. Crée un script de test
    print("\n" + "=" * 60)
    create_test_script()
    
    print("\n" + "=" * 60)
    print("✅ CORRECTIONS TERMINÉES")
    print("=" * 60)
    print("\n📋 PROCHAINES ÉTAPES:")
    print("1. Exécutez le script de test: python test_permissions_final.py")
    print("2. Si les permissions ne fonctionnent toujours pas, redémarrez Django:")
    print("   - Arrêtez le serveur (Ctrl+C)")
    print("   - python manage.py runserver")
    print("3. Testez l'interface web: http://127.0.0.1:8000/pharmacien/ordonnances/")
    print("\n⚠ Si problème persiste, vérifiez dans l'admin Django que:")
    print("   - Le groupe 'Pharmacien' a les permissions view_ordonnance et change_ordonnance")
    print("   - GLORIA1 est bien dans le groupe 'Pharmacien'")

if __name__ == "__main__":
    main()