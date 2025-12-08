#!/usr/bin/env python3
"""
SCRIPT D'ASSIGNATION DES GROUPES ET PERMISSIONS
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

def creer_groupes_et_permissions():
    """Crée les groupes et assigne les permissions"""
    
    print("👥 CRÉATION DES GROUPES ET PERMISSIONS")
    print("=" * 50)
    
    # Liste des groupes à créer
    groupes_data = {
        'Membres': {
            'description': 'Utilisateurs membres de la mutuelle',
            'permissions': [
                'view_own_profile', 'update_own_profile', 'view_own_bons', 
                'create_consultation_request', 'view_own_paiements'
            ]
        },
        'Medecins': {
            'description': 'Médecins partenaires',
            'permissions': [
                'view_patient_profile', 'create_consultation', 'create_ordonnance',
                'view_own_schedule', 'update_own_availability'
            ]
        },
        'Assureurs': {
            'description': 'Personnel assureur',
            'permissions': [
                'view_all_membres', 'validate_bons', 'process_paiements',
                'view_statistics', 'manage_configuration'
            ]
        },
        'Pharmaciens': {
            'description': 'Pharmaciens partenaires',
            'permissions': [
                'view_ordonnances', 'process_medicaments', 'update_stock',
                'validate_delivery', 'view_patient_history'
            ]
        },
        'Agents': {
            'description': 'Agents de terrain',
            'permissions': [
                'create_bons_soin', 'verify_cotisations', 'validate_documents',
                'view_member_info', 'create_activity_report'
            ]
        },
        'Administrateurs': {
            'description': 'Administrateurs système',
            'permissions': [
                'all'  # Toutes les permissions
            ]
        }
    }
    
    groupes_crees = {}
    
    for nom_groupe, infos in groupes_data.items():
        groupe, created = Group.objects.get_or_create(
            name=nom_groupe
        )
        
        if created:
            print(f"✅ Groupe créé: {nom_groupe}")
        else:
            print(f"⚠️  Groupe existant: {nom_groupe}")
        
        groupes_crees[nom_groupe] = groupe
    
    print(f"\n📊 {len(groupes_crees)} groupes configurés")
    return groupes_crees

def assigner_utilisateurs_aux_groupes():
    """Assigner les utilisateurs de test aux groupes appropriés"""
    
    print("\n👤 ASSIGNATION DES UTILISATEURS AUX GROUPES")
    print("=" * 50)
    
    # Récupérer tous les utilisateurs de test
    utilisateurs_test = User.objects.filter(username__startswith='test_')
    
    if not utilisateurs_test.exists():
        print("❌ Aucun utilisateur de test trouvé")
        print("💡 Exécutez d'abord le script de test: python test_acteurs_perfection.py")
        return
    
    # Mapping des rôles vers les groupes
    mapping_roles_groupes = {
        'membre': 'Membres',
        'medecin': 'Medecins', 
        'assureur': 'Assureurs',
        'pharmacien': 'Pharmaciens',
        'agent': 'Agents'
    }
    
    compteur_assignations = 0
    
    for user in utilisateurs_test:
        # Déterminer le rôle basé sur le username
        role_trouve = None
        for role, groupe_nom in mapping_roles_groupes.items():
            if role in user.username:
                role_trouve = role
                break
        
        if role_trouve:
            groupe_nom = mapping_roles_groupes[role_trouve]
            try:
                groupe = Group.objects.get(name=groupe_nom)
                user.groups.add(groupe)
                compteur_assignations += 1
                print(f"✅ {user.username} → Groupe {groupe_nom}")
            except Group.DoesNotExist:
                print(f"❌ Groupe {groupe_nom} non trouvé pour {user.username}")
        else:
            print(f"⚠️  Rôle non déterminé pour {user.username}")
    
    print(f"\n📊 {compteur_assignations} utilisateurs assignés à des groupes")

def verifier_assignations():
    """Vérifie les assignations de groupes"""
    
    print("\n🔍 VÉRIFICATION DES ASSIGNATIONS")
    print("=" * 50)
    
    # Compter par groupe
    for groupe in Group.objects.all():
        membres_count = groupe.user_set.count()
        if membres_count > 0:
            print(f"👥 {groupe.name}: {membres_count} membres")
            
            # Afficher les membres de ce groupe
            membres = groupe.user_set.all()[:5]  # Limiter à 5 pour éviter trop d'affichage
            for user in membres:
                print(f"   👤 {user.username} ({user.get_full_name()})")

def creer_permissions_personnalisees():
    """Crée des permissions personnalisées si nécessaire"""
    
    print("\n🔐 CRÉATION DE PERMISSIONS PERSONNALISÉES")
    print("=" * 50)
    
    permissions_personnalisees = [
        # Permissions Membres
        ('view_own_profile', 'Peut voir son propre profil'),
        ('update_own_profile', 'Peut modifier son propre profil'),
        ('view_own_bons', 'Peut voir ses propres bons'),
        ('create_consultation_request', 'Peut créer une demande de consultation'),
        ('view_own_paiements', 'Peut voir ses propres paiements'),
        
        # Permissions Médecins
        ('view_patient_profile', 'Peut voir le profil des patients'),
        ('create_consultation', 'Peut créer des consultations'),
        ('create_ordonnance', 'Peut créer des ordonnances'),
        ('view_own_schedule', 'Peut voir son propre emploi du temps'),
        ('update_own_availability', 'Peut modifier sa disponibilité'),
        
        # Permissions Assureurs
        ('view_all_membres', 'Peut voir tous les membres'),
        ('validate_bons', 'Peut valider les bons'),
        ('process_paiements', 'Peut traiter les paiements'),
        ('view_statistics', 'Peut voir les statistiques'),
        ('manage_configuration', 'Peut gérer la configuration'),
        
        # Permissions Pharmaciens
        ('view_ordonnances', 'Peut voir les ordonnances'),
        ('process_medicaments', 'Peut traiter les médicaments'),
        ('update_stock', 'Peut mettre à jour le stock'),
        ('validate_delivery', 'Peut valider les livraisons'),
        ('view_patient_history', 'Peut voir l\'historique patient'),
        
        # Permissions Agents
        ('create_bons_soin', 'Peut créer des bons de soin'),
        ('verify_cotisations', 'Peut vérifier les cotisations'),
        ('validate_documents', 'Peut valider les documents'),
        ('view_member_info', 'Peut voir les informations membres'),
        ('create_activity_report', 'Peut créer des rapports d\'activité'),
    ]
    
    # Ces permissions seraient normalement créées via les modèles Django
    # Ici on se contente de les lister pour information
    print("📋 Permissions personnalisées nécessaires:")
    for perm_code, perm_desc in permissions_personnalisees:
        print(f"   🔐 {perm_code}: {perm_desc}")
    
    print("\n💡 Ces permissions doivent être implémentées dans les modèles Django")

def assigner_permissions_avancees():
    """Assigner des permissions Django standard aux groupes"""
    
    print("\n🎯 ASSIGNATION DES PERMISSIONS DJANGO STANDARD")
    print("=" * 50)
    
    # Permissions par groupe (modèles Django standards)
    permissions_par_groupe = {
        'Membres': [
            ('membres', 'membre', 'view_membre'),  # Peut voir son propre membre
            ('membres', 'bon', 'view_bon'),        # Peut voir ses bons
        ],
        'Medecins': [
            ('medecin', 'medecin', 'change_medecin'),      # Peut modifier son profil médecin
            ('medecin', 'consultation', 'add_consultation'), # Peut ajouter des consultations
            ('medecin', 'ordonnance', 'add_ordonnance'),    # Peut ajouter des ordonnances
            ('membres', 'membre', 'view_membre'),          # Peut voir les membres (patients)
        ],
        'Assureurs': [
            ('membres', 'membre', 'view_membre'),          # Peut voir tous les membres
            ('membres', 'bon', 'view_bon'),                # Peut voir tous les bons
            ('membres', 'bon', 'change_bon'),              # Peut modifier les bons
            ('assureur', 'paiement', 'view_paiement'),     # Peut voir les paiements
            ('assureur', 'paiement', 'change_paiement'),   # Peut modifier les paiements
        ],
        'Pharmaciens': [
            ('pharmacien', 'pharmacien', 'change_pharmacien'), # Peut modifier son profil
            ('pharmacien', 'ordonnancepharmacien', 'add_ordonnancepharmacien'), # Peut traiter ordonnances
            ('pharmacien', 'stockpharmacie', 'change_stockpharmacie'), # Peut gérer stock
        ],
        'Agents': [
            ('agents', 'agent', 'change_agent'),           # Peut modifier son profil agent
            ('agents', 'bonsoin', 'add_bonsoin'),          # Peut créer des bons de soin
            ('agents', 'verificationcotisation', 'add_verificationcotisation'), # Peut vérifier cotisations
            ('membres', 'membre', 'view_membre'),          # Peut voir les membres
        ],
        'Administrateurs': [
            # Toutes les permissions (sera géré via is_staff)
        ]
    }
    
    for groupe_nom, permissions in permissions_par_groupe.items():
        try:
            groupe = Group.objects.get(name=groupe_nom)
            permissions_assignees = 0
            
            for app_label, model, perm_codename in permissions:
                try:
                    perm = Permission.objects.get(
                        content_type__app_label=app_label,
                        codename=perm_codename
                    )
                    groupe.permissions.add(perm)
                    permissions_assignees += 1
                except Permission.DoesNotExist:
                    print(f"   ⚠️  Permission non trouvée: {app_label}.{perm_codename}")
            
            if permissions_assignees > 0:
                print(f"✅ {groupe_nom}: {permissions_assignees} permissions assignées")
            else:
                print(f"ℹ️  {groupe_nom}: Aucune permission spécifique assignée")
                
        except Group.DoesNotExist:
            print(f"❌ Groupe non trouvé: {groupe_nom}")

def main():
    """Fonction principale"""
    
    print("🚀 CONFIGURATION COMPLÈTE DES GROUPES ET PERMISSIONS")
    print("=" * 60)
    
    # 1. Créer les groupes
    groupes = creer_groupes_et_permissions()
    
    # 2. Assigner les utilisateurs aux groupes
    assigner_utilisateurs_aux_groupes()
    
    # 3. Assigner les permissions Django standard
    assigner_permissions_avancees()
    
    # 4. Vérifier les assignations
    verifier_assignations()
    
    # 5. Lister les permissions personnalisées nécessaires
    creer_permissions_personnalisees()
    
    print("\n🎉 CONFIGURATION TERMINÉE !")
    print("=" * 60)
    print("\n📋 RÉSUMÉ:")
    print("• Groupes créés/verifiés")
    print("• Utilisateurs assignés aux groupes") 
    print("• Permissions de base configurées")
    print("• Liste des permissions personnalisées fournie")
    
    print("\n💡 PROCHAINES ÉTAPES:")
    print("1. Implémenter les permissions personnalisées dans vos vues")
    print("2. Utiliser les décorateurs @permission_required dans vos vues")
    print("3. Tester l'accès aux différentes fonctionnalités par groupe")

if __name__ == "__main__":
    main()