#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC COMPLET - SYSTÈME ASSUREUR
Vérifie tous les aspects du système Assureur et corrige les problèmes.
"""

import os
import sys
import django
from datetime import date, datetime
import logging

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

# Imports Django
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from assureur.models import Assureur
from membres.models import Membre
from soins.models import Bon
from paiements.models import Paiement

# Configuration logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def print_section(title):
    """Affiche une section de diagnostic"""
    print("\n" + "="*80)
    print(f"🔍 {title}")
    print("="*80)

def diagnostic_complet_assureur():
    """
    Diagnostic complet du système Assureur
    """
    print("🎯 DIAGNOSTIC COMPLET DU SYSTÈME ASSUREUR")
    print("="*80)
    
    # 1. VÉRIFICATION DES GROUPES
    print_section("1. GROUPES D'UTILISATEURS")
    
    # Liste tous les groupes
    groupes = Group.objects.all().order_by('name')
    print(f"Groupes existants ({groupes.count()}):")
    for groupe in groupes:
        users_count = groupe.user_set.count()
        print(f"  - {groupe.name}: {users_count} utilisateur(s)")
    
    # Vérifier spécifiquement le groupe Assureur
    groupes_assureur = Group.objects.filter(name__icontains='assureur')
    if groupes_assureur.exists():
        print(f"\n✅ Groupe(s) Assureur trouvé(s):")
        for groupe in groupes_assureur:
            users = groupe.user_set.all()
            print(f"\n  Groupe: {groupe.name}")
            print(f"  Nombre d'utilisateurs: {users.count()}")
            for user in users:
                print(f"    • {user.username} ({user.get_full_name()})")
    else:
        print("\n❌ AUCUN groupe Assureur trouvé!")
    
    # 2. VÉRIFICATION DES UTILISATEURS ASSUREUR
    print_section("2. UTILISATEURS ASSUREUR")
    
    # Chercher tous les utilisateurs qui devraient être assureurs
    users_assureur = []
    for username in ['DOUA', 'ktanos', 'DOUA1', 'matrix']:
        try:
            user = User.objects.get(username=username)
            groups = [g.name for g in user.groups.all()]
            is_in_assureur = any('assureur' in g.lower() for g in groups)
            
            status = "✅" if is_in_assureur else "❌"
            print(f"{status} {username}: {user.get_full_name()}")
            print(f"     Groupes: {', '.join(groups) if groups else 'Aucun'}")
            print(f"     Email: {user.email}")
            print(f"     Dernière connexion: {user.last_login}")
            print(f"     Date inscription: {user.date_joined}")
            
            users_assureur.append(user)
        except User.DoesNotExist:
            print(f"❌ {username}: Utilisateur non trouvé")
    
    # 3. VÉRIFICATION DES PROFILS ASSUREUR
    print_section("3. PROFILS ASSUREUR")
    
    assureurs = Assureur.objects.all().select_related('user')
    print(f"Profils Assureur dans la base: {assureurs.count()}")
    
    for assureur in assureurs:
        print(f"\n  👤 {assureur.user.username}")
        print(f"     ID: {assureur.id}")
        print(f"     Numéro employé: {assureur.numero_employe}")
        print(f"     Département: {assureur.departement}")
        print(f"     Date embauche: {assureur.date_embauche}")
        print(f"     Actif: {'✅' if assureur.est_actif else '❌'}")
        print(f"     Créé le: {assureur.created_at}")
        
        # Vérifier si l'utilisateur est dans le bon groupe
        user_groups = [g.name for g in assureur.user.groups.all()]
        has_assureur_group = any('assureur' in g.lower() for g in user_groups)
        
        if has_assureur_group:
            print(f"     ✅ Dans groupe assureur")
        else:
            print(f"     ❌ PAS dans groupe assureur! Groupes: {user_groups}")
    
    # 4. VÉRIFICATION DES DONNÉES MÉTIER
    print_section("4. DONNÉES MÉTIER")
    
    # Membres
    total_membres = Membre.objects.count()
    membres_actifs = Membre.objects.filter(est_actif=True).count()
    print(f"📊 Membres:")
    print(f"  • Total: {total_membres}")
    print(f"  • Actifs: {membres_actifs}")
    print(f"  • Inactifs: {total_membres - membres_actifs}")
    
    # Bons de soin
    total_bons = Bon.objects.count()
    print(f"\n🏥 Bons de soin:")
    print(f"  • Total: {total_bons}")
    
    # Paiements
    total_paiements = Paiement.objects.count()
    montant_total = sum(p.montant for p in Paiement.objects.all() if p.montant)
    print(f"\n💰 Paiements:")
    print(f"  • Total: {total_paiements}")
    print(f"  • Montant total: {montant_total:,} FCFA")
    
    # 5. VÉRIFICATION DES PERMISSIONS
    print_section("5. PERMISSIONS")
    
    # Vérifier les permissions du modèle Assureur
    try:
        ct = ContentType.objects.get(app_label='assureur', model='assureur')
        permissions = Permission.objects.filter(content_type=ct)
        print(f"Permissions pour le modèle Assureur: {permissions.count()}")
        for perm in permissions:
            print(f"  • {perm.codename}: {perm.name}")
    except ContentType.DoesNotExist:
        print("❌ ContentType pour Assureur non trouvé")
    
    # 6. CORRECTIONS RECOMMANDÉES
    print_section("6. RECOMMANDATIONS")
    
    # Vérifier les incohérences
    problems_found = False
    
    # a. Utilisateurs sans profil Assureur mais dans le groupe
    for user in users_assureur:
        user_groups = [g.name.lower() for g in user.groups.all()]
        is_in_assureur_group = any('assureur' in g for g in user_groups)
        
        try:
            Assureur.objects.get(user=user)
            has_profile = True
        except Assureur.DoesNotExist:
            has_profile = False
        
        if is_in_assureur_group and not has_profile:
            print(f"❌ {user.username}: Dans groupe assureur mais pas de profil!")
            problems_found = True
        elif not is_in_assureur_group and has_profile:
            print(f"❌ {user.username}: Profil assureur mais pas dans le groupe!")
            problems_found = True
    
    # b. Groupes multiples "Assureur"
    assureur_groups = Group.objects.filter(name__icontains='assureur')
    if assureur_groups.count() > 1:
        print(f"❌ {assureur_groups.count()} groupes 'Assureur' trouvés!")
        print("   Recommandation: Fusionner en un seul groupe 'Assureur'")
        problems_found = True
    
    if not problems_found:
        print("✅ Aucun problème critique détecté!")
    
    # 7. RÉCAPITULATIF
    print_section("7. RÉCAPITULATIF")
    
    print("📋 ÉTAT DU SYSTÈME ASSUREUR:")
    print(f"  • Groupes Assureur: {groupes_assureur.count()}")
    print(f"  • Profils Assureur: {assureurs.count()}")
    print(f"  • Membres actifs: {membres_actifs}")
    print(f"  • Bons de soin: {total_bons}")
    
    print("\n🎯 RECOMMANDATIONS:")
    print("  1. Standardiser sur un seul groupe: 'Assureur' (avec A majuscule)")
    print("  2. Vérifier que tous les utilisateurs du groupe ont un profil")
    print("  3. Vérifier les permissions d'accès aux vues")
    
    print("\n✅ Diagnostic terminé!")

def corriger_problemes_assureur():
    """
    Corrige les problèmes identifiés
    """
    print("\n🔧 CORRECTION AUTOMATIQUE DES PROBLÈMES")
    print("="*80)
    
    # 1. Standardiser le groupe Assureur
    print("\n1. Standardisation du groupe 'Assureur'...")
    
    # Trouver tous les groupes assureur
    assureur_groups = Group.objects.filter(name__icontains='assureur')
    
    if assureur_groups.exists():
        # Prendre le premier groupe comme référence
        groupe_principal = assureur_groups.first()
        print(f"   Groupe principal: {groupe_principal.name}")
        
        # Renommer en 'Assureur' si nécessaire
        if groupe_principal.name != 'Assureur':
            ancien_nom = groupe_principal.name
            groupe_principal.name = 'Assureur'
            groupe_principal.save()
            print(f"   ✅ Renommé '{ancien_nom}' en 'Assureur'")
        
        # Fusionner les autres groupes
        autres_groupes = assureur_groups.exclude(id=groupe_principal.id)
        if autres_groupes.exists():
            for groupe in autres_groupes:
                users = groupe.user_set.all()
                for user in users:
                    user.groups.add(groupe_principal)
                groupe.delete()
                print(f"   ✅ Fusionné le groupe '{groupe.name}' dans 'Assureur'")
    else:
        # Créer le groupe Assureur
        groupe_principal = Group.objects.create(name='Assureur')
        print(f"   ✅ Groupe 'Assureur' créé")
    
    # 2. Vérifier/créer les profils Assureur
    print("\n2. Vérification des profils Assureur...")
    
    # Liste des utilisateurs à vérifier
    usernames = ['DOUA', 'ktanos', 'DOUA1', 'matrix']
    
    for username in usernames:
        try:
            user = User.objects.get(username=username)
            
            # Ajouter au groupe Assureur
            if not user.groups.filter(name='Assureur').exists():
                user.groups.add(groupe_principal)
                print(f"   ✅ {username}: Ajouté au groupe Assureur")
            
            # Vérifier/créer le profil Assureur
            try:
                assureur = Assureur.objects.get(user=user)
                print(f"   ✅ {username}: Profil existant (ID: {assureur.id})")
            except Assureur.DoesNotExist:
                assureur = Assureur.objects.create(
                    user=user,
                    numero_employe=user.username,
                    departement="Service Client",
                    date_embauche=date.today(),
                    est_actif=True
                )
                print(f"   ✅ {username}: Profil créé (ID: {assureur.id})")
                
        except User.DoesNotExist:
            print(f"   ⚠️  {username}: Utilisateur non trouvé")
    
    # 3. Vérifier la cohérence
    print("\n3. Vérification de la cohérence...")
    
    # Compter les utilisateurs dans le groupe
    users_in_group = groupe_principal.user_set.count()
    print(f"   • Utilisateurs dans le groupe 'Assureur': {users_in_group}")
    
    # Compter les profils
    profiles_count = Assureur.objects.count()
    print(f"   • Profils Assureur: {profiles_count}")
    
    # Vérifier les incohérences
    for assureur in Assureur.objects.all():
        if not assureur.user.groups.filter(name='Assureur').exists():
            assureur.user.groups.add(groupe_principal)
            print(f"   ✅ {assureur.user.username}: Ajouté au groupe Assureur")
    
    print("\n✅ Correction terminée!")

def generer_rapport():
    """
    Génère un rapport détaillé
    """
    print("\n📊 RAPPORT DU SYSTÈME ASSUREUR")
    print("="*80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Statistiques
    total_users = User.objects.count()
    total_assureurs = Assureur.objects.count()
    total_membres = Membre.objects.count()
    
    print(f"\n📈 STATISTIQUES:")
    print(f"  • Utilisateurs totaux: {total_users}")
    print(f"  • Assureurs: {total_assureurs}")
    print(f"  • Membres: {total_membres}")
    
    # Liste détaillée
    print(f"\n👥 ASSUREURS:")
    for assureur in Assureur.objects.select_related('user').all():
        groupes = [g.name for g in assureur.user.groups.all()]
        print(f"  • {assureur.user.username}: {assureur.departement} (Groupes: {', '.join(groupes)})")

if __name__ == "__main__":
    print("🛠️  OUTIL DE DIAGNOSTIC ET CORRECTION - SYSTÈME ASSUREUR")
    print("="*80)
    
    while True:
        print("\nMENU:")
        print("1. Diagnostic complet")
        print("2. Corriger les problèmes")
        print("3. Générer rapport")
        print("4. Quitter")
        
        choix = input("\nVotre choix (1-4): ").strip()
        
        if choix == "1":
            diagnostic_complet_assureur()
        elif choix == "2":
            corriger_problemes_assureur()
        elif choix == "3":
            generer_rapport()
        elif choix == "4":
            print("Au revoir!")
            break
        else:
            print("Choix invalide!")