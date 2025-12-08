#!/usr/bin/env python
"""
CORRECTION DES CONTENTTYPES EN DOUBLE
Résout l'erreur: get() returned more than one ContentType
"""

import os
import sys
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.db import transaction

def corriger_contenttypes_doubles():
    """Corrige les ContentTypes en double"""
    print("🔧 CORRECTION DES CONTENTTYPES EN DOUBLE")
    print("=" * 60)
    
    # Trouve les ContentTypes avec le même app_label et model
    from django.db.models import Count
    duplicates = ContentType.objects.values('app_label', 'model').annotate(
        count=Count('id')
    ).filter(count__gt=1)
    
    print(f"ContentTypes en double trouvés: {duplicates.count()}")
    
    fixed_count = 0
    for dup in duplicates:
        app_label = dup['app_label']
        model = dup['model']
        
        ctypes = ContentType.objects.filter(app_label=app_label, model=model)
        print(f"\n📋 {app_label}.{model}: {ctypes.count()} instances")
        
        # Garde le premier, supprime les autres
        if ctypes.count() > 1:
            keep_ct = ctypes.first()
            delete_cts = ctypes.exclude(id=keep_ct.id)
            
            print(f"  ✅ Garde: ID {keep_ct.id}")
            print(f"  🗑️  Supprime: {delete_cts.count()} instances")
            
            # Pour chaque ContentType à supprimer, déplace les permissions
            for delete_ct in delete_cts:
                # Trouve toutes les permissions liées à ce ContentType
                permissions = Permission.objects.filter(content_type=delete_ct)
                
                for perm in permissions:
                    # Essaie de trouver une permission équivalente dans le ContentType gardé
                    existing = Permission.objects.filter(
                        content_type=keep_ct,
                        codename=perm.codename
                    ).exists()
                    
                    if not existing:
                        # Déplace la permission vers le ContentType gardé
                        perm.content_type = keep_ct
                        perm.save()
                        print(f"    → Permission '{perm.codename}' déplacée")
                    else:
                        # Supprime la permission en double
                        perm.delete()
                        print(f"    🗑️ Permission '{perm.codename}' supprimée (double)")
                
                # Supprime le ContentType
                delete_ct.delete()
                fixed_count += 1
    
    print(f"\n✅ {fixed_count} ContentTypes en double corrigés")
    return fixed_count

def verifier_contenttypes_pharmacien():
    """Vérifie spécifiquement les ContentTypes pour 'pharmacien'"""
    print("\n" + "=" * 60)
    print("💊 VÉRIFICATION CONTENTTYPES PHARMACIEN")
    print("=" * 60)
    
    # Regarde tous les ContentTypes pour 'pharmacien'
    ctypes = ContentType.objects.filter(app_label='pharmacien')
    
    if ctypes.exists():
        print(f"ContentTypes trouvés pour 'pharmacien': {ctypes.count()}")
        
        for ct in ctypes:
            print(f"\n📦 ContentType ID {ct.id}:")
            print(f"   Model: {ct.model}")
            print(f"   App label: {ct.app_label}")
            
            # Compte les permissions associées
            perm_count = Permission.objects.filter(content_type=ct).count()
            print(f"   Permissions associées: {perm_count}")
            
            # Liste les permissions
            permissions = Permission.objects.filter(content_type=ct)
            for perm in permissions[:5]:  # Limite à 5 pour la lisibilité
                print(f"      - {perm.codename}")
            
            if perm_count > 5:
                print(f"      ... et {perm_count - 5} autres")
    else:
        print("❌ Aucun ContentType trouvé pour 'pharmacien'")
    
    return ctypes

def creer_contenttypes_necessaires():
    """Crée les ContentTypes nécessaires s'ils n'existent pas"""
    print("\n" + "=" * 60)
    print("🏗️ CRÉATION CONTENTTYPES NÉCESSAIRES")
    print("=" * 60)
    
    # Liste des ContentTypes qui devraient exister
    contenttypes_needed = [
        ('pharmacien', 'pharmacien'),
        ('pharmacien', 'stockpharmacie'),
        ('ordonnances', 'ordonnance'),
        ('medicaments', 'medicament'),
        ('soins', 'bondesoin'),
    ]
    
    created_count = 0
    for app_label, model in contenttypes_needed:
        # Vérifie s'il existe déjà
        exists = ContentType.objects.filter(app_label=app_label, model=model).exists()
        
        if not exists:
            try:
                # Essaie de créer le ContentType
                ct, created = ContentType.objects.get_or_create(
                    app_label=app_label,
                    model=model
                )
                
                if created:
                    created_count += 1
                    print(f"✅ Créé: {app_label}.{model}")
                else:
                    print(f"✅ Existe déjà: {app_label}.{model}")
                    
            except Exception as e:
                print(f"❌ Erreur création {app_label}.{model}: {str(e)}")
        else:
            print(f"✅ Existe déjà: {app_label}.{model}")
    
    print(f"\n✅ {created_count} nouveaux ContentTypes créés")
    return created_count

def reinitialiser_permissions_pharmacien():
    """Réinitialise complètement les permissions du groupe Pharmacien"""
    print("\n" + "=" * 60)
    print("🔄 RÉINITIALISATION PERMISSIONS PHARMACIEN")
    print("=" * 60)
    
    from django.contrib.auth.models import Group
    
    try:
        # Récupère le groupe Pharmacien
        group = Group.objects.get(name='Pharmacien')
        
        # Supprime toutes les permissions actuelles
        old_count = group.permissions.count()
        group.permissions.clear()
        print(f"🗑️  {old_count} anciennes permissions supprimées")
        
        # Liste des permissions nécessaires avec leur app_label
        permissions_needed = [
            ('pharmacien', 'view_pharmacien'),
            ('pharmacien', 'change_pharmacien'),
            ('pharmacien', 'view_stockpharmacie'),
            ('pharmacien', 'change_stockpharmacie'),
            ('ordonnances', 'view_ordonnance'),
            ('ordonnances', 'change_ordonnance'),
            ('medicaments', 'view_medicament'),
            ('medicaments', 'change_medicament'),
            ('soins', 'view_bondesoin'),
            ('communication', 'view_message'),
            ('communication', 'add_message'),
        ]
        
        added_count = 0
        for app_label, codename in permissions_needed:
            try:
                # Trouve la permission
                # D'abord, essaie de trouver par app_label et codename
                content_types = ContentType.objects.filter(app_label=app_label)
                
                for ct in content_types:
                    try:
                        perm = Permission.objects.get(content_type=ct, codename=codename)
                        group.permissions.add(perm)
                        added_count += 1
                        print(f"✅ Ajouté: {app_label}.{codename}")
                        break
                    except Permission.DoesNotExist:
                        continue
                else:
                    # Si pas trouvé avec app_label, essaie juste avec codename
                    try:
                        perm = Permission.objects.get(codename=codename)
                        group.permissions.add(perm)
                        added_count += 1
                        print(f"✅ Ajouté: {codename} (sans app_label)")
                    except Permission.DoesNotExist:
                        print(f"⚠ Permission non trouvée: {app_label}.{codename}")
                    except Permission.MultipleObjectsReturned:
                        # Prend la première
                        perm = Permission.objects.filter(codename=codename).first()
                        group.permissions.add(perm)
                        added_count += 1
                        print(f"✅ Ajouté: {codename} (première trouvée)")
                        
            except Exception as e:
                print(f"❌ Erreur avec {app_label}.{codename}: {str(e)}")
        
        print(f"\n✅ {added_count} nouvelles permissions ajoutées au groupe Pharmacien")
        
        # Mise à jour des utilisateurs
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Réinitialise les permissions pour GLORIA1
        try:
            gloria1 = User.objects.get(username='GLORIA1')
            
            # S'assure que GLORIA1 est dans le groupe Pharmacien
            if not gloria1.groups.filter(name='Pharmacien').exists():
                gloria1.groups.add(group)
                print("✅ GLORIA1 ajouté au groupe Pharmacien")
            
            # Rafraîchit les permissions
            gloria1 = User.objects.get(pk=gloria1.pk)
            
            print(f"\n🔍 TEST GLORIA1:")
            print(f"   Groupes: {[g.name for g in gloria1.groups.all()]}")
            
            # Test des permissions
            test_permissions = [
                ('view_ordonnance', 'Voir ordonnances'),
                ('change_ordonnance', 'Modifier ordonnances'),
                ('view_stockpharmacie', 'Voir stock'),
                ('change_stockpharmacie', 'Modifier stock'),
            ]
            
            for codename, description in test_permissions:
                has_perm = False
                
                # Essaie avec différents app_labels
                for app_label in ['pharmacien', 'ordonnances']:
                    if gloria1.has_perm(f'{app_label}.{codename}'):
                        has_perm = True
                        print(f"   ✅ {description}: OUI ({app_label}.{codename})")
                        break
                
                if not has_perm and gloria1.has_perm(codename):
                    has_perm = True
                    print(f"   ✅ {description}: OUI ({codename})")
                
                if not has_perm:
                    print(f"   ❌ {description}: NON")
                    
        except User.DoesNotExist:
            print("⚠ GLORIA1 non trouvé")
        
        return group
        
    except Group.DoesNotExist:
        print("❌ Groupe Pharmacien non trouvé")
        return None

def main():
    """Fonction principale"""
    print("🚀 CORRECTION DÉFINITIVE DES CONTENTTYPES ET PERMISSIONS")
    print("=" * 60)
    
    # Applique toutes les corrections dans une transaction
    with transaction.atomic():
        print("\n1. Correction des ContentTypes en double...")
        corriger_contenttypes_doubles()
        
        print("\n2. Vérification des ContentTypes 'pharmacien'...")
        verifier_contenttypes_pharmacien()
        
        print("\n3. Création des ContentTypes nécessaires...")
        creer_contenttypes_necessaires()
        
        print("\n4. Réinitialisation des permissions Pharmacien...")
        reinitialiser_permissions_pharmacien()
    
    print("\n" + "=" * 60)
    print("✅ CORRECTIONS APPLIQUÉES !")
    print("=" * 60)
    
    print("\n📋 POUR TESTER:")
    print("1. Redémarrez le serveur: python manage.py runserver")
    print("2. Connectez-vous avec GLORIA1 (Pharmacien123!)")
    print("3. Testez l'accès aux pages:")
    print("   - http://127.0.0.1:8000/pharmacien/dashboard/")
    print("   - http://127.0.0.1:8000/pharmacien/ordonnances/")
    print("   - http://127.0.0.1:8000/pharmacien/stock/")
    print("\n🔧 Si problème persiste, utilisez la commande Django:")
    print("   python manage.py remove_stale_contenttypes")

if __name__ == "__main__":
    main()