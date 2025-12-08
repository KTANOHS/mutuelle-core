# creation_relations_reelles.py
import os
import sys
import django
from pathlib import Path
from datetime import date, datetime

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur setup Django: {e}")
    sys.exit(1)

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.apps import apps
from django.utils import timezone

def print_section(title):
    print(f"\n{'='*80}")
    print(f"🔧 {title}")
    print(f"{'='*80}")

def create_medecin_relations():
    """Crée les relations Medecin avec les champs obligatoires"""
    print_section("CRÉATION DES RELATIONS MÉDECIN")
    
    User = get_user_model()
    medecin_users = User.objects.filter(groups__name='Medecin')
    
    try:
        from medecin.models import Medecin, SpecialiteMedicale, EtablissementMedical
        
        # Créer ou récupérer les dépendances nécessaires
        specialite_default, _ = SpecialiteMedicale.objects.get_or_create(
            nom="Médecine Générale",
            defaults={'description': "Spécialité par défaut"}
        )
        
        etablissement_default, _ = EtablissementMedical.objects.get_or_create(
            nom="Centre Médical Principal",
            defaults={
                'adresse': "Adresse par défaut",
                'telephone': "0102030405",
                'type_etablissement': "CENTRE"
            }
        )
        
        users_created = 0
        
        for user in medecin_users:
            if not hasattr(user, 'medecin'):
                print(f"🔧 Création Medecin pour {user.username}")
                
                medecin = Medecin.objects.create(
                    user=user,
                    numero_ordre=f"ORD{user.id:04d}",
                    specialite=specialite_default,
                    etablissement=etablissement_default,
                    telephone_pro="0102030405",
                    email_pro=user.email or f"medecin{user.id}@example.com",
                    annees_experience=5,
                    tarif_consultation=5000.00,
                    actif=True,
                    disponible=True,
                    date_inscription=timezone.now(),
                    date_derniere_modif=timezone.now(),
                    horaires_travail={},
                    diplome_verifie=False
                )
                print(f"   ✅ Médecin créé: {medecin}")
                users_created += 1
            else:
                print(f"   ✅ {user.username} a déjà un Medecin: {user.medecin}")
        
        return users_created
        
    except Exception as e:
        print(f"❌ Erreur création Medecin: {e}")
        return 0

def create_agent_relations():
    """Crée les relations Agent avec les champs obligatoires"""
    print_section("CRÉATION DES RELATIONS AGENT")
    
    User = get_user_model()
    agent_users = User.objects.filter(groups__name='Agents')
    
    try:
        from agents.models import Agent, RoleAgent
        
        # Créer ou récupérer le rôle par défaut
        role_default, _ = RoleAgent.objects.get_or_create(
            nom="Agent Standard",
            defaults={'description': "Rôle par défaut pour les agents"}
        )
        
        users_created = 0
        
        for user in agent_users:
            if not hasattr(user, 'agent'):
                print(f"🔧 Création Agent pour {user.username}")
                
                agent = Agent.objects.create(
                    user=user,
                    matricule=f"AGT{user.id:03d}",
                    poste="Agent de saisie",
                    role=role_default,
                    date_embauche=date.today(),
                    est_actif=True,
                    limite_bons_quotidienne=20,
                    telephone="0102030405",
                    email_professionnel=user.email or f"agent{user.id}@example.com"
                )
                print(f"   ✅ Agent créé: {agent}")
                users_created += 1
            else:
                print(f"   ✅ {user.username} a déjà un Agent: {user.agent}")
        
        return users_created
        
    except Exception as e:
        print(f"❌ Erreur création Agent: {e}")
        return 0

def create_membre_relations():
    """Crée les relations Membre avec les champs obligatoires"""
    print_section("CRÉATION DES RELATIONS MEMBRE")
    
    User = get_user_model()
    membre_users = User.objects.filter(groups__name='Membre')
    
    try:
        from membres.models import Membre
        
        users_created = 0
        
        for user in membre_users:
            if not hasattr(user, 'membre'):
                print(f"🔧 Création Membre pour {user.username}")
                
                membre = Membre.objects.create(
                    user=user,
                    numero_unique=f"MEM{user.id:04d}",
                    nom=user.last_name or user.username,
                    prenom=user.first_name or user.username,
                    telephone="0102030405",
                    numero_urgence="0102030406",
                    date_inscription=timezone.now(),
                    statut="AC",  # Actif
                    categorie="ST",  # Standard
                    cmu_option=False,
                    adresse="Adresse par défaut",
                    email=user.email or f"membre{user.id}@example.com",
                    profession="Non spécifié",
                    type_piece_identite="CNI",
                    statut_documents="EN_ATTENTE"
                )
                print(f"   ✅ Membre créé: {membre}")
                users_created += 1
            else:
                print(f"   ✅ {user.username} a déjà un Membre: {user.membre}")
        
        return users_created
        
    except Exception as e:
        print(f"❌ Erreur création Membre: {e}")
        return 0

def create_pharmacien_relations():
    """Crée les relations Pharmacien avec les champs obligatoires"""
    print_section("CRÉATION DES RELATIONS PHARMACIEN")
    
    User = get_user_model()
    pharmacien_users = User.objects.filter(groups__name='Pharmacien')
    
    try:
        from pharmacien.models import Pharmacien
        
        users_created = 0
        
        for user in pharmacien_users:
            if not hasattr(user, 'pharmacien'):
                print(f"🔧 Création Pharmacien pour {user.username}")
                
                pharmacien = Pharmacien.objects.create(
                    user=user,
                    numero_pharmacien=f"PHARM{user.id:04d}",
                    nom_pharmacie=f"Pharmacie {user.username}",
                    adresse_pharmacie="Adresse par défaut",
                    telephone="0102030405",
                    actif=True,
                    date_inscription=timezone.now()
                )
                print(f"   ✅ Pharmacien créé: {pharmacien}")
                users_created += 1
            else:
                print(f"   ✅ {user.username} a déjà un Pharmacien: {user.pharmacien}")
        
        return users_created
        
    except Exception as e:
        print(f"❌ Erreur création Pharmacien: {e}")
        return 0

def create_assureur_relations():
    """Crée les relations Assureur avec les champs obligatoires"""
    print_section("CRÉATION DES RELATIONS ASSUREUR")
    
    User = get_user_model()
    assureur_users = User.objects.filter(groups__name='Assureur')
    
    try:
        from assureur.models import Assureur
        
        users_created = 0
        
        for user in assureur_users:
            if not hasattr(user, 'assureur'):
                print(f"🔧 Création Assureur pour {user.username}")
                
                assureur = Assureur.objects.create(
                    user=user,
                    numero_employe=f"ASS{user.id:03d}",
                    departement="Gestion des sinistres",
                    date_embauche=date.today(),
                    est_actif=True,
                    created_at=timezone.now(),
                    updated_at=timezone.now()
                )
                print(f"   ✅ Assureur créé: {assureur}")
                users_created += 1
            else:
                print(f"   ✅ {user.username} a déjà un Assureur: {user.assureur}")
        
        return users_created
        
    except Exception as e:
        print(f"❌ Erreur création Assureur: {e}")
        return 0

def verify_all_relations():
    """Vérifie que toutes les relations ont été créées"""
    print_section("VÉRIFICATION FINALE DES RELATIONS")
    
    User = get_user_model()
    
    groups_to_check = [
        ('Medecin', 'medecin'),
        ('Membre', 'membre'),
        ('Agents', 'agent'),
        ('Pharmacien', 'pharmacien'),
        ('Assureur', 'assureur')
    ]
    
    total_with_relations = 0
    total_without_relations = 0
    
    for group_name, relation_name in groups_to_check:
        users_in_group = User.objects.filter(groups__name=group_name)
        with_relation = 0
        without_relation = 0
        
        for user in users_in_group:
            if hasattr(user, relation_name):
                with_relation += 1
            else:
                without_relation += 1
        
        total_with_relations += with_relation
        total_without_relations += without_relation
        
        status = "✅" if with_relation == len(users_in_group) else "⚠️"
        print(f"{status} {group_name}: {with_relation}/{len(users_in_group)} avec relation")
        
        if without_relation > 0:
            print(f"   ❌ Sans relation: {without_relation} utilisateur(s)")
    
    print(f"\n📊 TOTAL: {total_with_relations} avec relations, {total_without_relations} sans relations")
    
    if total_without_relations == 0:
        print("🎉 TOUTES LES RELATIONS SONT CRÉÉES !")
    else:
        print("⚠️  Certaines relations manquent encore")

def test_redirection_logic():
    """Teste la logique de redirection avec les relations créées"""
    print_section("TEST DE LA LOGIQUE DE REDIRECTION")
    
    User = get_user_model()
    
    # Tester chaque type d'utilisateur
    test_cases = [
        ('Medecin', 'medecin', '/medecin/dashboard/'),
        ('Membre', 'membre', '/membres/dashboard/'),
        ('Agents', 'agent', '/agents/dashboard/'),
        ('Pharmacien', 'pharmacien', '/pharmacien/dashboard/'),
        ('Assureur', 'assureur', '/assureur/dashboard/')
    ]
    
    print("🧪 Simulation de redirection:")
    
    for group_name, relation, expected_url in test_cases:
        users = User.objects.filter(groups__name=group_name)
        
        print(f"\n📋 {group_name}:")
        for user in users[:2]:  # Tester les 2 premiers
            has_relation = hasattr(user, relation)
            status = "✅" if has_relation else "❌"
            
            if has_relation:
                obj = getattr(user, relation)
                print(f"   {status} {user.username}: {obj}")
                print(f"      🎯 Serait redirigé vers: {expected_url}")
            else:
                print(f"   {status} {user.username}: Aucune relation")
                print(f"      ⚠️  Redirection par défaut ou par groupe")

def main():
    """Fonction principale"""
    print("🚀 CRÉATION DES RELATIONS AVEC STRUCTURE RÉELLE")
    print("📋 Utilisation des champs obligatoires réels")
    
    try:
        # Créer les relations pour chaque type d'utilisateur
        total_created = 0
        total_created += create_medecin_relations()
        total_created += create_agent_relations()
        total_created += create_membre_relations()
        total_created += create_pharmacien_relations()
        total_created += create_assureur_relations()
        
        # Vérifier les résultats
        verify_all_relations()
        
        # Tester la redirection
        test_redirection_logic()
        
        print_section("RÉSULTAT FINAL")
        print(f"✅ {total_created} nouvelles relations créées")
        
        if total_created > 0:
            print("🎯 Maintenant vous pouvez:")
            print("   1. Redémarrer le serveur Django")
            print("   2. Tester la connexion avec test_medecin")
            print("   3. Vérifier la redirection vers /medecin/dashboard/")
        else:
            print("ℹ️  Aucune nouvelle relation créée - vérifiez les logs ci-dessus")
            
    except Exception as e:
        print(f"💥 Erreur critique: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()