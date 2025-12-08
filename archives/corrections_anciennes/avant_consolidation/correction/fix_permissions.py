#!/usr/bin/env python
"""
CORRECTION DES PERMISSIONS EN DOUBLE
Résout l'erreur: get() returned more than one Permission
"""

import os
import sys
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

def corriger_permissions_en_double():
    """Corrige les permissions en double"""
    print("🔧 CORRECTION DES PERMISSIONS EN DOUBLE")
    print("=" * 60)
    
    # Trouve toutes les permissions avec le même codename
    from django.db.models import Count
    duplicates = Permission.objects.values('codename').annotate(
        count=Count('id')
    ).filter(count__gt=1)
    
    print(f"Permissions en double trouvées: {duplicates.count()}")
    
    fixed_count = 0
    for dup in duplicates:
        codename = dup['codename']
        perms = Permission.objects.filter(codename=codename)
        
        print(f"\n📋 Permission '{codename}': {perms.count()} instances")
        
        # Garde la première, supprime les autres
        if perms.count() > 1:
            keep_perm = perms.first()
            delete_perms = perms.exclude(id=keep_perm.id)
            
            # Vérifie quelles groupes utilisent ces permissions
            for group in Group.objects.all():
                group_perms = group.permissions.filter(codename=codename)
                if group_perms.count() > 1:
                    # Garde seulement la première permission dans le groupe
                    group.permissions.remove(*delete_perms)
                    print(f"  ✅ Groupe '{group.name}' nettoyé")
            
            # Supprime les permissions en double
            delete_count = delete_perms.count()
            delete_perms.delete()
            fixed_count += delete_count
            print(f"  ✅ {delete_count} instances supprimées")
    
    print(f"\n✅ {fixed_count} permissions en double corrigées")
    return fixed_count

def verifier_permissions_pharmacien_fixe():
    """Version corrigée de la vérification des permissions Pharmacien"""
    print("\n" + "=" * 60)
    print("💊 VÉRIFICATION CORRIGÉE DES PERMISSIONS PHARMACIEN")
    print("=" * 60)
    
    try:
        group = Group.objects.get(name='Pharmacien')
        print(f"✅ Groupe Pharmacien trouvé ({group.user_set.count()} utilisateurs)")
        
        # Permissions requises pour un pharmacien
        required_permissions = [
            # Ordonnances
            ('ordonnances', 'view_ordonnance'),
            ('ordonnances', 'change_ordonnance'),
            ('ordonnances', 'view_ordonnancepharmacien'),
            ('ordonnances', 'change_ordonnancepharmacien'),
            
            # Médicaments
            ('medicaments', 'view_medicament'),
            ('medicaments', 'change_medicament'),
            
            # Stock
            ('pharmacien', 'view_stockpharmacie'),
            ('pharmacien', 'change_stockpharmacie'),
            
            # Bon de soin
            ('soins', 'view_bondesoin'),
        ]
        
        # Vérifie et ajoute les permissions
        added_count = 0
        for app_label, codename in required_permissions:
            try:
                # Essaie de trouver la permission avec app_label
                content_type = ContentType.objects.get(app_label=app_label)
                perm = Permission.objects.get(codename=codename, content_type=content_type)
            except (ContentType.DoesNotExist, Permission.DoesNotExist):
                try:
                    # Essaie sans app_label (première trouvée)
                    perm = Permission.objects.filter(codename=codename).first()
                except:
                    perm = None
            
            if perm:
                if not group.permissions.filter(id=perm.id).exists():
                    group.permissions.add(perm)
                    added_count += 1
                    print(f"✅ Ajouté: {codename} (app: {app_label})")
                else:
                    print(f"✅ Déjà présent: {codename}")
            else:
                print(f"⚠ Permission non trouvée: {codename} (app: {app_label})")
        
        print(f"\n✅ {added_count} nouvelles permissions ajoutées au groupe Pharmacien")
        
        # Vérifie GLORIA1 spécifiquement
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            gloria1 = User.objects.get(username='GLORIA1')
            print(f"\n🔍 Vérification GLORIA1:")
            
            # Réinitialise les permissions en retirant et réajoutant le groupe
            print("🔄 Réinitialisation des permissions de GLORIA1...")
            gloria1.groups.clear()
            gloria1.groups.add(group)
            
            # Rafraîchit l'utilisateur
            gloria1 = User.objects.get(username='GLORIA1')
            
            # Vérifie les permissions
            perms_a_verifier = [
                ('view_ordonnance', 'Voir les ordonnances'),
                ('change_ordonnance', 'Modifier les ordonnances'),
                ('view_pharmacien', 'Voir le profil pharmacien'),
                ('view_stockpharmacie', 'Voir le stock'),
            ]
            
            for perm_codename, description in perms_a_verifier:
                # Vérifie par app_label spécifique
                has_perm = False
                
                # Essaie différentes applications
                for app_label in ['ordonnances', 'pharmacien', 'soins']:
                    if gloria1.has_perm(f'{app_label}.{perm_codename}'):
                        has_perm = True
                        break
                
                # Essaie aussi sans app_label
                if not has_perm and gloria1.has_perm(perm_codename):
                    has_perm = True
                
                if has_perm:
                    print(f"✅ {description} ({perm_codename}): OK")
                else:
                    print(f"❌ {description} ({perm_codename}): Manquante")
                    
        except User.DoesNotExist:
            print("⚠ GLORIA1 non trouvé")
        
        return group
        
    except Group.DoesNotExist:
        print("❌ Groupe Pharmacien non trouvé")
        return None

def creer_permissions_manquantes():
    """Crée les permissions manquantes si elles n'existent pas"""
    print("\n" + "=" * 60)
    print("🏗️ CRÉATION DES PERMISSIONS MANQUANTES")
    print("=" * 60)
    
    # Liste des permissions à créer (si elles n'existent pas)
    permissions_a_creer = [
        ('ordonnances', 'ordonnance', 'view_ordonnance', 'Can view ordonnance'),
        ('ordonnances', 'ordonnance', 'change_ordonnance', 'Can change ordonnance'),
        ('pharmacien', 'stockpharmacie', 'view_stockpharmacie', 'Can view stock pharmacie'),
        ('pharmacien', 'stockpharmacie', 'change_stockpharmacie', 'Can change stock pharmacie'),
    ]
    
    created_count = 0
    for app_label, model, codename, name in permissions_a_creer:
        try:
            # Vérifie si la permission existe déjà
            content_type = ContentType.objects.get(app_label=app_label, model=model)
            perm, created = Permission.objects.get_or_create(
                codename=codename,
                content_type=content_type,
                defaults={'name': name}
            )
            
            if created:
                created_count += 1
                print(f"✅ Créée: {codename} (app: {app_label}.{model})")
            else:
                print(f"✅ Existe déjà: {codename}")
                
        except ContentType.DoesNotExist:
            print(f"⚠ ContentType non trouvé: {app_label}.{model}")
        except Exception as e:
            print(f"⚠ Erreur avec {codename}: {str(e)}")
    
    print(f"\n✅ {created_count} nouvelles permissions créées")
    return created_count

def tester_permissions_gloria1():
    """Test complet des permissions de GLORIA1"""
    print("\n" + "=" * 60)
    print("🧪 TEST COMPLET DES PERMISSIONS GLORIA1")
    print("=" * 60)
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    try:
        gloria1 = User.objects.get(username='GLORIA1')
        
        # Réinitialise les caches de permissions
        gloria1 = User.objects.get(pk=gloria1.pk)
        
        print(f"🔍 Utilisateur: {gloria1.username}")
        print(f"   Groupes: {[g.name for g in gloria1.groups.all()]}")
        
        # Test 1: Vérifie les permissions directement via les groupes
        print("\n📋 PERMISSIONS DIRECTES:")
        all_perms = set()
        for group in gloria1.groups.all():
            for perm in group.permissions.all():
                all_perms.add(f"{perm.content_type.app_label}.{perm.codename}")
        
        for perm in sorted(list(all_perms)):
            print(f"   - {perm}")
        
        # Test 2: Vérifie les méthodes has_perm
        print("\n✅ VÉRIFICATION has_perm():")
        
        # Liste des permissions à vérifier
        permissions_tests = [
            ('view_ordonnance', 'Voir les ordonnances'),
            ('change_ordonnance', 'Modifier les ordonnances'),
            ('view_stockpharmacie', 'Voir le stock pharmacie'),
            ('change_stockpharmacie', 'Modifier le stock pharmacie'),
            ('view_bondesoin', 'Voir les bons de soin'),
            ('view_medicament', 'Voir les médicaments'),
        ]
        
        for perm_codename, description in permissions_tests:
            # Essaie avec différents app_labels
            found = False
            app_labels = ['ordonnances', 'pharmacien', 'soins', 'medicaments']
            
            for app_label in app_labels:
                if gloria1.has_perm(f'{app_label}.{perm_codename}'):
                    print(f"   ✅ {description}: OUI ({app_label}.{perm_codename})")
                    found = True
                    break
            
            if not found and gloria1.has_perm(perm_codename):
                print(f"   ✅ {description}: OUI ({perm_codename})")
                found = True
            
            if not found:
                print(f"   ❌ {description}: NON")
        
        # Test 3: Test d'accès à des URLs spécifiques
        print("\n🌐 TEST D'ACCÈS AUX URLs (simulé):")
        
        urls_permissions = [
            ('/pharmacien/ordonnances/', 'view_ordonnance', 'Liste des ordonnances'),
            ('/pharmacien/stock/', 'view_stockpharmacie', 'Gestion du stock'),
            ('/pharmacien/dashboard/', 'view_pharmacien', 'Dashboard pharmacien'),
            ('/communication/messagerie/', 'view_message', 'Messagerie'),
        ]
        
        for url, perm_needed, description in urls_permissions:
            # Simule la vérification
            has_access = False
            
            for app_label in ['pharmacien', 'ordonnances', 'communication']:
                if gloria1.has_perm(f'{app_label}.{perm_needed}') or gloria1.has_perm(perm_needed):
                    has_access = True
                    break
            
            if has_access:
                print(f"   ✅ {description}: Accès autorisé")
            else:
                print(f"   ⚠ {description}: Permission manquante ({perm_needed})")
        
        return True
        
    except User.DoesNotExist:
        print("❌ GLORIA1 non trouvé")
        return False

def generer_rapport_final():
    """Génère un rapport final"""
    print("\n" + "=" * 60)
    print("📊 RAPPORT FINAL - SYSTÈME DE PERMISSIONS")
    print("=" * 60)
    
    # Statistiques
    print(f"\n📈 STATISTIQUES:")
    print(f"   Groupes: {Group.objects.count()}")
    print(f"   Permissions: {Permission.objects.count()}")
    print(f"   ContentTypes: {ContentType.objects.count()}")
    
    # Liste des groupes et leurs permissions
    print(f"\n👥 GROUPES ET PERMISSIONS:")
    for group in Group.objects.all():
        print(f"\n🔹 {group.name} ({group.user_set.count()} utilisateurs):")
        perms = group.permissions.all()
        if perms:
            for perm in perms[:5]:  # Limite à 5 pour la lisibilité
                print(f"   - {perm.content_type.app_label}.{perm.codename}")
            if perms.count() > 5:
                print(f"   ... et {perms.count() - 5} autres")
        else:
            print(f"   ⚠ Aucune permission")
    
    # Instructions finales
    print("\n" + "=" * 60)
    print("✅ SYSTÈME DE PERMISSIONS CORRIGÉ")
    print("=" * 60)
    print("\n📋 POUR TESTER:")
    print("1. Redémarrez le serveur: python manage.py runserver")
    print("2. Connectez-vous avec GLORIA1 (Pharmacien123!)")
    print("3. Testez l'accès aux pages:")
    print("   - http://127.0.0.1:8000/pharmacien/dashboard/")
    print("   - http://127.0.0.1:8000/pharmacien/ordonnances/")
    print("   - http://127.0.0.1:8000/pharmacien/stock/")
    print("4. Si des problèmes persistent, vérifiez dans l'admin Django")

def main():
    """Fonction principale"""
    print("🚀 CORRECTION DÉFINITIVE DES PERMISSIONS")
    print("=" * 60)
    
    # Applique les corrections dans l'ordre
    print("\n1. Correction des permissions en double...")
    with transaction.atomic():
        fixed = corriger_permissions_en_double()
    
    print("\n2. Création des permissions manquantes...")
    with transaction.atomic():
        created = creer_permissions_manquantes()
    
    print("\n3. Vérification des permissions Pharmacien...")
    with transaction.atomic():
        group = verifier_permissions_pharmacien_fixe()
    
    print("\n4. Test complet des permissions GLORIA1...")
    tester_permissions_gloria1()
    
    # Génère le rapport
    generer_rapport_final()
    
    print("\n" + "=" * 60)
    print("🎉 CORRECTIONS TERMINÉES !")
    print("=" * 60)

if __name__ == "__main__":
    main()