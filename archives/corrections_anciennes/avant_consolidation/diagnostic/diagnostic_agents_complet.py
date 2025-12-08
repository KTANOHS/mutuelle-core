# diagnostic_agents_complet.py

import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db import connection
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.urls import reverse, NoReverseMatch
from django.test import Client

# Import des modèles agents
try:
    from agents.models import Agent, PerformanceAgent
    MODELS_AGENTS_DISPONIBLES = True
except ImportError as e:
    MODELS_AGENTS_DISPONIBLES = False
    print(f"❌ Erreur import modèles agents: {e}")

# Import des autres modèles
try:
    from membres.models import Membre, DossierMedical
    from soins.models import BonDeSoin, Ordonnance
    from communication.models import Notification
    MODELS_AUTRES_DISPONIBLES = True
except ImportError as e:
    MODELS_AUTRES_DISPONIBLES = False
    print(f"⚠️  Erreur import autres modèles: {e}")

def verifier_structure_fichiers():
    """Vérifie la structure des fichiers de l'application agents"""
    print("=" * 80)
    print("🔍 DIAGNOSTIC COMPLET - APPLICATION AGENTS")
    print("=" * 80)
    
    repertoire_agents = BASE_DIR / "agents"
    templates_agents = BASE_DIR / "templates" / "agents"
    
    print("\n📁 STRUCTURE DES FICHIERS AGENTS")
    print("-" * 40)
    
    # Vérification des fichiers essentiels
    fichiers_essentiels = [
        ("models.py", repertoire_agents / "models.py"),
        ("views.py", repertoire_agents / "views.py"),
        ("urls.py", repertoire_agents / "urls.py"),
        ("forms.py", repertoire_agents / "forms.py"),
        ("admin.py", repertoire_agents / "admin.py"),
    ]
    
    for nom_fichier, chemin in fichiers_essentiels:
        if chemin.exists():
            taille = chemin.stat().st_size
            print(f"✅ {nom_fichier} - {taille} octets")
        else:
            print(f"❌ {nom_fichier} - MANQUANT")
    
    # Vérification des templates
    print(f"\n🎨 TEMPLATES AGENTS:")
    if templates_agents.exists():
        templates = list(templates_agents.rglob("*.html"))
        for template in templates:
            rel_path = template.relative_to(templates_agents.parent)
            print(f"   📄 {rel_path} - {template.stat().st_size} octets")
    else:
        print("❌ Répertoire templates/agents non trouvé")

def analyser_modeles_agents():
    """Analyse les modèles de l'application agents"""
    print(f"\n📊 ANALYSE DES MODÈLES AGENTS")
    print("-" * 40)
    
    if not MODELS_AGENTS_DISPONIBLES:
        print("❌ Modèles agents non disponibles")
        return
    
    try:
        # Vérifier les tables en base de données
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name LIKE '%agent%'
            """)
            tables_agents = cursor.fetchall()
            
        print(f"🗃️ Tables agents en base: {[t[0] for t in tables_agents]}")
        
        # Analyser le modèle Agent
        agent_fields = Agent._meta.get_fields()
        print(f"\n📋 Champs du modèle Agent:")
        for field in agent_fields:
            if hasattr(field, 'name'):
                null_info = "NULL" if field.null else "NOT NULL"
                blank_info = "BLANK" if field.blank else ""
                print(f"   • {field.name}: {field.get_internal_type()} [{null_info}] [{blank_info}]")
        
        # Compter les agents
        total_agents = Agent.objects.count()
        agents_actifs = Agent.objects.filter(actif=True).count()
        print(f"\n👥 Statistiques agents:")
        print(f"   • Total agents: {total_agents}")
        print(f"   • Agents actifs: {agents_actifs}")
        
    except Exception as e:
        print(f"❌ Erreur analyse modèles: {e}")

def verifier_vues_agents():
    """Vérifie les vues de l'application agents"""
    print(f"\n👁️ ANALYSE DES VUES AGENTS")
    print("-" * 40)
    
    try:
        # Importer les vues
        from agents import views
        
        # Lister les fonctions de vue
        fonctions_vues = [attr for attr in dir(views) 
                         if not attr.startswith('_') and callable(getattr(views, attr))]
        
        print("Vues disponibles dans agents/views.py:")
        for vue in sorted(fonctions_vues):
            if not vue.startswith('__'):
                func = getattr(views, vue)
                if hasattr(func, '__name__'):
                    print(f"   🎯 {vue}")
        
        # Vérifier les décorateurs sur les vues principales
        vues_principales = ['tableau_de_bord', 'creer_membre', 'creer_bon_soin']
        for vue_name in vues_principales:
            if hasattr(views, vue_name):
                func = getattr(views, vue_name)
                print(f"   ✅ {vue_name} - Présente")
            else:
                print(f"   ❌ {vue_name} - Manquante")
                
    except Exception as e:
        print(f"❌ Erreur analyse vues: {e}")

def verifier_urls_agents():
    """Vérifie les URLs configurées"""
    print(f"\n🌐 ANALYSE DES URLs AGENTS")
    print("-" * 40)
    
    try:
        from agents.urls import urlpatterns
        
        print("URLs définies dans agents/urls.py:")
        for pattern in urlpatterns:
            if hasattr(pattern, 'pattern'):
                print(f"   • {pattern.pattern.describe()} -> {pattern.name}")
        
        # Tester l'accès aux URLs principales
        urls_a_tester = [
            'agents:tableau_de_bord',
            'agents:creer_membre',
            'agents:creer_bon_soin',
            'agents:liste_membres',
        ]
        
        print(f"\n🔗 Test des URLs:")
        client = Client()
        for url_name in urls_a_tester:
            try:
                url = reverse(url_name)
                print(f"   ✅ {url_name} -> {url}")
            except NoReverseMatch:
                print(f"   ❌ {url_name} -> URL NON CONFIGURÉE")
                
    except Exception as e:
        print(f"❌ Erreur analyse URLs: {e}")

def verifier_permissions_agents():
    """Vérifie les permissions et groupes"""
    print(f"\n🔐 ANALYSE DES PERMISSIONS")
    print("-" * 40)
    
    try:
        # Vérifier le groupe Agents
        groupe_agents, created = Group.objects.get_or_create(name='Agents')
        if created:
            print("✅ Groupe 'Agents' créé")
        else:
            print("✅ Groupe 'Agents' existe déjà")
        
        # Compter les permissions
        total_permissions = Permission.objects.count()
        content_types_agents = ContentType.objects.filter(app_label='agents')
        permissions_agents = Permission.objects.filter(content_type__in=content_types_agents)
        
        print(f"📊 Permissions système:")
        print(f"   • Permissions totales: {total_permissions}")
        print(f"   • Permissions agents: {permissions_agents.count()}")
        
        # Vérifier les utilisateurs dans le groupe Agents
        users_agents = User.objects.filter(groups__name='Agents')
        print(f"   • Utilisateurs dans groupe Agents: {users_agents.count()}")
        
    except Exception as e:
        print(f"❌ Erreur analyse permissions: {e}")

def verifier_relations_base_donnees():
    """Vérifie les relations avec autres applications"""
    print(f"\n🗃️ RELATIONS BASE DE DONNÉES")
    print("-" * 40)
    
    try:
        # Vérifier les tables liées
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            all_tables = [row[0] for row in cursor.fetchall()]
        
        tables_importantes = [
            'agents_agent',
            'membres_membre', 
            'soins_bondesoin',
            'communication_notification'
        ]
        
        print("Tables disponibles:")
        for table in tables_importantes:
            if table in all_tables:
                # Compter les enregistrements
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   ✅ {table}: {count} enregistrements")
            else:
                print(f"   ❌ {table}: TABLE MANQUANTE")
                
    except Exception as e:
        print(f"❌ Erreur analyse base de données: {e}")

def tester_fonctionnalites_principales():
    """Test des fonctionnalités principales"""
    print(f"\n🧪 TEST DES FONCTIONNALITÉS")
    print("-" * 40)
    
    try:
        # Test création d'agent de test
        user, created = User.objects.get_or_create(
            username='agent_test',
            defaults={'email': 'agent@test.com', 'first_name': 'Test', 'last_name': 'Agent'}
        )
        if created:
            user.set_password('password123')
            user.save()
            print("✅ Utilisateur agent_test créé")
        
        # Associer au groupe Agents
        groupe_agents = Group.objects.get(name='Agents')
        user.groups.add(groupe_agents)
        
        # Créer le profil Agent
        agent, created = Agent.objects.get_or_create(
            user=user,
            defaults={
                'numero_agent': 'AGT001',
                'telephone': '+33123456789',
                'actif': True
            }
        )
        if created:
            print("✅ Profil Agent créé")
        
        # Test des modèles membres
        if MODELS_AUTRES_DISPONIBLES:
            total_membres = Membre.objects.count()
            total_bons_soins = BonDeSoin.objects.count()
            print(f"📊 Données existantes:")
            print(f"   • Membres: {total_membres}")
            print(f"   • Bons de soin: {total_bons_soins}")
        
        print("🔑 Identifiants de test:")
        print(f"   👤 Utilisateur: agent_test")
        print(f"   🔑 Mot de passe: password123")
        
    except Exception as e:
        print(f"❌ Erreur tests fonctionnalités: {e}")

def verifier_templates_agents():
    """Vérifie les templates agents"""
    print(f"\n🎨 VÉRIFICATION DES TEMPLATES")
    print("-" * 40)
    
    templates_agents = BASE_DIR / "templates" / "agents"
    templates_essentiels = [
        'dashboard.html',
        'tableau_bord.html', 
        'creer_membre.html',
        'creer_bon_soin.html',
        'liste_membres.html'
    ]
    
    if templates_agents.exists():
        for template in templates_essentiels:
            template_path = templates_agents / template
            if template_path.exists():
                print(f"✅ {template} - Présent")
            else:
                print(f"❌ {template} - Manquant")
    else:
        print("❌ Répertoire templates/agents introuvable")

def diagnostic_complet():
    """Exécute le diagnostic complet"""
    print("🚀 LANCEMENT DU DIAGNOSTIC COMPLET AGENTS")
    print("=" * 80)
    
    verifier_structure_fichiers()
    analyser_modeles_agents()
    verifier_vues_agents()
    verifier_urls_agents()
    verifier_permissions_agents()
    verifier_relations_base_donnees()
    verifier_templates_agents()
    tester_fonctionnalites_principales()
    
    print("\n" + "=" * 80)
    print("✅ DIAGNOSTIC TERMINÉ")
    print("=" * 80)

if __name__ == "__main__":
    diagnostic_complet()