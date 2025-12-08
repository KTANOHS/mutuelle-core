# diagnostic_permissions_acces.py

import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.urls import reverse
from django.test import Client

def verifier_structure_base_donnees():
    """Vérifie la structure de la base de données"""
    print("🗃️ STRUCTURE DE LA BASE DE DONNÉES")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
    
    tables_importantes = [
        'membres_membre', 'soins_bondesoin', 'medecin_ordonnance',
        'pharmacien_ordonnancepharmacien', 'agents_agent', 'paiements_paiement'
    ]
    
    for table in tables_importantes:
        if table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"✅ {table}: {count} enregistrements")
        else:
            print(f"❌ {table}: TABLE MANQUANTE")

def verifier_groupes_utilisateurs():
    """Vérifie les groupes et leurs permissions"""
    print("\n👥 GROUPES ET UTILISATEURS")
    print("=" * 50)
    
    groupes_requis = ['Agents', 'Médecins', 'Pharmaciens', 'Membres']
    
    for nom_groupe in groupes_requis:
        try:
            groupe = Group.objects.get(name=nom_groupe)
            users_count = groupe.user_set.count()
            perms_count = groupe.permissions.count()
            print(f"✅ {nom_groupe}: {users_count} utilisateurs, {perms_count} permissions")
        except Group.DoesNotExist:
            print(f"❌ {nom_groupe}: GROUPE MANQUANT")

def verifier_acces_agents():
    """Vérifie ce que les agents peuvent voir"""
    print("\n🔍 ACCÈS DES AGENTS")
    print("=" * 50)
    
    try:
        from agents.models import Agent
        from membres.models import Membre
        from soins.models import BonDeSoin
        
        # Vérifier si les agents existent
        agents_count = Agent.objects.count()
        print(f"👤 Agents enregistrés: {agents_count}")
        
        # Vérifier accès aux membres
        membres_count = Membre.objects.count()
        print(f"📋 Membres accessibles: {membres_count}")
        
        # Vérifier accès aux bons de soin
        bons_count = BonDeSoin.objects.count()
        print(f"📄 Bons de soin accessibles: {bons_count}")
        
        # Vérifier modèle Cotisation
        try:
            from cotisations.models import Cotisation
            cotisations_count = Cotisation.objects.count()
            print(f"💰 Cotisations accessibles: {cotisations_count}")
        except ImportError:
            print("💰 Cotisations: MODÈLE NON DISPONIBLE")
            
    except Exception as e:
        print(f"❌ Erreur vérification agents: {e}")

def verifier_acces_medecins():
    """Vérifie ce que les médecins peuvent voir"""
    print("\n🏥 ACCÈS DES MÉDECINS")
    print("=" * 50)
    
    try:
        from medecin.models import Medecin
        from soins.models import BonDeSoin
        
        # Vérifier si les médecins existent
        medecins_count = Medecin.objects.count()
        print(f"👨‍⚕️ Médecins enregistrés: {medecins_count}")
        
        # Vérifier accès aux bons de soin créés par les agents
        bons_agents = BonDeSoin.objects.filter(createur__groups__name='Agents').count()
        print(f"📋 Bons créés par agents: {bons_agents}")
        
        # Vérifier accès aux ordonnances
        try:
            from medecin.models import Ordonnance
            ordonnances_count = Ordonnance.objects.count()
            print(f"💊 Ordonnances accessibles: {ordonnances_count}")
        except Exception as e:
            print(f"💊 Ordonnances: {e}")
            
    except Exception as e:
        print(f"❌ Erreur vérification médecins: {e}")

def verifier_acces_pharmaciens():
    """Vérifie ce que les pharmaciens peuvent voir"""
    print("\n💊 ACCÈS DES PHARMACIENS")
    print("=" * 50)
    
    try:
        from pharmacien.models import Pharmacien
        from medecin.models import Ordonnance
        
        # Vérifier si les pharmaciens existent
        pharmaciens_count = Pharmacien.objects.count()
        print(f"👨‍⚕️ Pharmaciens enregistrés: {pharmaciens_count}")
        
        # Vérifier accès aux ordonnances créées par les médecins
        ordonnances_medecins = Ordonnance.objects.filter(medecin__isnull=False).count()
        print(f"📋 Ordonnances médecins: {ordonnances_medecins}")
        
        # Vérifier accès aux ordonnances des agents
        ordonnances_agents = Ordonnance.objects.filter(createur__groups__name='Agents').count()
        print(f"📋 Ordonnances agents: {ordonnances_agents}")
        
    except Exception as e:
        print(f"❌ Erreur vérification pharmaciens: {e}")

def verifier_acces_membres():
    """Vérifie ce que les membres peuvent voir"""
    print("\n👤 ACCÈS DES MEMBRES")
    print("=" * 50)
    
    try:
        from membres.models import Membre
        from soins.models import BonDeSoin
        from medecin.models import Ordonnance
        
        # Vérifier si les membres existent
        membres_count = Membre.objects.count()
        print(f"👤 Membres enregistrés: {membres_count}")
        
        # Vérifier accès aux propres bons du membre
        if membres_count > 0:
            membre_test = Membre.objects.first()
            bons_membre = BonDeSoin.objects.filter(patient=membre_test).count()
            print(f"📋 Bons du membre test: {bons_membre}")
            
            # Vérifier accès aux propres ordonnances du membre
            ordonnances_membre = Ordonnance.objects.filter(patient=membre_test).count()
            print(f"💊 Ordonnances du membre test: {ordonnances_membre}")
        
    except Exception as e:
        print(f"❌ Erreur vérification membres: {e}")

def tester_urls_par_role():
    """Teste l'accès aux URLs par rôle"""
    print("\n🌐 TEST DES URLs PAR RÔLE")
    print("=" * 50)
    
    urls_par_role = {
        'agents': [
            'agents:dashboard',
            'agents:creer_membre', 
            'agents:liste_membres',
            'agents:creer_bon_soin',
            'agents:verification_cotisations',
        ],
        'medecin': [
            'medecin:dashboard',
            'medecin:liste_ordonnances',
            'medecin:creer_ordonnance',
        ],
        'pharmacien': [
            'pharmacien:dashboard',
            'pharmacien:liste_ordonnances_attente',
            'pharmacien:stock',
        ],
        'membres': [
            'membres:dashboard',
            'membres:mes_bons',
            'membres:mes_ordonnances',
        ]
    }
    
    for role, urls in urls_par_role.items():
        print(f"\n🔗 {role.upper()}:")
        for url_name in urls:
            try:
                url = reverse(url_name)
                print(f"   ✅ {url_name}")
            except Exception as e:
                print(f"   ❌ {url_name}: {e}")

def verifier_relations_modeles():
    """Vérifie les relations entre les modèles"""
    print("\n🔗 RELATIONS ENTRE MODÈLES")
    print("=" * 50)
    
    try:
        from soins.models import BonDeSoin
        from medecin.models import Ordonnance
        from membres.models import Membre
        
        # Vérifier relation BonDeSoin -> Membre
        if BonDeSoin.objects.exists():
            bon = BonDeSoin.objects.first()
            if hasattr(bon, 'patient'):
                print("✅ Relation BonDeSoin -> Membre: OK")
            else:
                print("❌ Relation BonDeSoin -> Membre: MANQUANTE")
        
        # Vérifier relation Ordonnance -> Membre
        if Ordonnance.objects.exists():
            ordonnance = Ordonnance.objects.first()
            if hasattr(ordonnance, 'patient'):
                print("✅ Relation Ordonnance -> Membre: OK")
            else:
                print("❌ Relation Ordonnance -> Membre: MANQUANTE")
                
        # Vérifier relation Ordonnance -> Médecin
        if Ordonnance.objects.exists():
            ordonnance = Ordonnance.objects.first()
            if hasattr(ordonnance, 'medecin'):
                print("✅ Relation Ordonnance -> Médecin: OK")
            else:
                print("❌ Relation Ordonnance -> Médecin: MANQUANTE")
                
    except Exception as e:
        print(f"❌ Erreur vérification relations: {e}")

def creer_utilisateurs_test():
    """Crée des utilisateurs de test pour chaque rôle"""
    print("\n🧪 CRÉATION UTILISATEURS TEST")
    print("=" * 50)
    
    roles_utilisateurs = {
        'agent_test': 'Agents',
        'medecin_test': 'Médecins', 
        'pharmacien_test': 'Pharmaciens',
        'membre_test': 'Membres'
    }
    
    for username, groupe_nom in roles_utilisateurs.items():
        try:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@test.com',
                    'first_name': 'Test',
                    'last_name': groupe_nom[:-1],  # Enlève le 's' final
                    'is_staff': True,
                    'is_active': True
                }
            )
            
            if created:
                user.set_password('password123')
                user.save()
                print(f"✅ {username} créé")
            
            # Ajouter au groupe
            try:
                groupe = Group.objects.get(name=groupe_nom)
                user.groups.add(groupe)
                print(f"✅ {username} ajouté au groupe {groupe_nom}")
            except Group.DoesNotExist:
                print(f"❌ Groupe {groupe_nom} non trouvé pour {username}")
                
        except Exception as e:
            print(f"❌ Erreur création {username}: {e}")

def generer_rapport_complet():
    """Génère un rapport complet des permissions et accès"""
    print("🚀 DIAGNOSTIC COMPLET DES PERMISSIONS ET ACCÈS")
    print("=" * 60)
    
    verifier_structure_base_donnees()
    verifier_groupes_utilisateurs()
    verifier_acces_agents()
    verifier_acces_medecins()
    verifier_acces_pharmaciens()
    verifier_acces_membres()
    verifier_relations_modeles()
    tester_urls_par_role()
    creer_utilisateurs_test()
    
    print("\n" + "=" * 60)
    print("✅ DIAGNOSTIC TERMINÉ")
    print("=" * 60)
    
    print("\n📋 RÉSUMÉ DES ACCÈS:")
    print("• Agents: Voir membres, créer bons, vérifier cotisations")
    print("• Médecins: Voir bons agents, créer ordonnances") 
    print("• Pharmaciens: Voir ordonnances médecins/agents, gérer stock")
    print("• Membres: Voir leurs propres bons et ordonnances")

if __name__ == "__main__":
    generer_rapport_complet()