#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC AGENTS
Analyse et corrige les problèmes du modèle Agent
"""

import os
import sys
import django
import inspect

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from django.db import models
from django.apps import apps
from django.db.models import Q

def print_header(title):
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)

def diagnostic_complet():
    """Diagnostic complet du système Agents"""
    
    print_header("DIAGNOSTIC COMPLET DU SYSTÈME AGENTS")
    
    # 1. Vérifier le modèle Agent
    diagnostic_modele_agent()
    
    # 2. Vérifier les utilisateurs et groupes
    diagnostic_utilisateurs()
    
    # 3. Vérifier les données existantes
    diagnostic_donnees()
    
    # 4. Vérifier la vue tableau_de_bord
    diagnostic_vues()
    
    # 5. Solutions et corrections
    proposer_corrections()

def diagnostic_modele_agent():
    """Analyse le modèle Agent"""
    print_header("1. ANALYSE DU MODÈLE AGENT")
    
    try:
        # Import dynamique pour éviter les erreurs d'import
        from agents.models import Agent
        
        print("✅ Module agents.models importé avec succès")
        print(f"📊 Modèle Agent trouvé: {Agent}")
        
        # Analyser les champs
        print("\n🔍 CHAMPS DU MODÈLE AGENT:")
        for field in Agent._meta.fields:
            print(f"  - {field.name} ({field.__class__.__name__})")
        
        # Vérifier les champs problématiques
        champs_problematiques = ['actif', 'email', 'nom', 'prenom']
        champs_existants = [f.name for f in Agent._meta.fields]
        
        print("\n⚠️ CHAMPS PROBLÉMATIQUES DÉTECTÉS:")
        for champ in champs_problematiques:
            if champ in champs_existants:
                print(f"  ✅ {champ} existe dans le modèle")
            else:
                print(f"  ❌ {champ} N'EXISTE PAS dans le modèle")
        
        # Vérifier la relation avec User
        print("\n🔗 RELATION AVEC USER:")
        for field in Agent._meta.fields:
            if field.name == 'user':
                print(f"  - Relation {field.__class__.__name__}")
                print(f"    Vers: {field.related_model}")
                print(f"    Primary key: {field.primary_key}")
        
        # Vérifier la méthode __str__
        print(f"\n📝 Méthode __str__: {Agent.__str__}")
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("Le module agents/models.py n'existe pas ou est corrompu")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()

def diagnostic_utilisateurs():
    """Analyse les utilisateurs et groupes"""
    print_header("2. ANALYSE DES UTILISATEURS ET GROUPES")
    
    # Vérifier l'utilisateur ORNELLA
    try:
        user = User.objects.get(username='ORNELLA')
        print(f"✅ Utilisateur ORNELLA trouvé (ID: {user.id})")
        print(f"   Nom complet: {user.get_full_name()}")
        print(f"   Email: {user.email}")
        print(f"   Actif: {user.is_active}")
        print(f"   Staff: {user.is_staff}")
        print(f"   Superuser: {user.is_superuser}")
        
        # Vérifier les groupes
        groupes = user.groups.all()
        if groupes:
            print(f"   Groupes: {', '.join([g.name for g in groupes])}")
        else:
            print("   ❌ Aucun groupe assigné")
            
    except User.DoesNotExist:
        print("❌ Utilisateur ORNELLA non trouvé")
        return
    
    # Vérifier le groupe AGENT
    try:
        groupe_agent = Group.objects.get(name='AGENT')
        print(f"\n✅ Groupe AGENT trouvé (ID: {groupe_agent.id})")
        
        # Vérifier les permissions
        permissions = groupe_agent.permissions.all()
        print(f"   Permissions: {permissions.count()}")
        
    except Group.DoesNotExist:
        print("❌ Groupe AGENT non trouvé")
        
    # Vérifier si l'utilisateur est dans le groupe AGENT
    if 'groupe_agent' in locals() and groupe_agent in user.groups.all():
        print("✅ ORNELLA est bien dans le groupe AGENT")
    else:
        print("❌ ORNELLA n'est pas dans le groupe AGENT")

def diagnostic_donnees():
    """Analyse les données Agent existantes"""
    print_header("3. ANALYSE DES DONNÉES AGENTS")
    
    try:
        from agents.models import Agent
        
        # Compter les agents
        total_agents = Agent.objects.count()
        print(f"📊 Total agents dans la base: {total_agents}")
        
        if total_agents > 0:
            print("\n📋 LISTE DES AGENTS:")
            for agent in Agent.objects.all():
                user_info = f"{agent.user.username}" if agent.user else "Sans utilisateur"
                print(f"  - {user_info} (ID: {agent.pk})")
                
                # Afficher tous les attributs
                for field in Agent._meta.fields:
                    try:
                        value = getattr(agent, field.name)
                        print(f"    {field.name}: {value}")
                    except:
                        pass
        
        # Vérifier l'agent pour ORNELLA
        try:
            user_ornella = User.objects.get(username='ORNELLA')
            agent_ornella = Agent.objects.get(user=user_ornella)
            print(f"\n✅ Agent trouvé pour ORNELLA (ID: {agent_ornella.pk})")
            
            # Vérifier tous les champs
            print("🔍 VÉRIFICATION DES CHAMPS:")
            for field in Agent._meta.fields:
                try:
                    value = getattr(agent_ornella, field.name)
                    print(f"  - {field.name}: {value}")
                except AttributeError:
                    print(f"  - {field.name}: CHAMP INEXISTANT")
                except Exception as e:
                    print(f"  - {field.name}: ERREUR - {e}")
                    
        except Agent.DoesNotExist:
            print("❌ Aucun agent trouvé pour ORNELLA")
        except User.DoesNotExist:
            print("❌ Utilisateur ORNELLA non trouvé")
            
    except ImportError:
        print("❌ Impossible d'importer le modèle Agent")
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")

def diagnostic_vues():
    """Analyse les vues agents"""
    print_header("4. ANALYSE DES VUES AGENTS")
    
    # Vérifier le fichier views.py
    views_path = 'agents/views.py'
    if os.path.exists(views_path):
        print(f"✅ Fichier {views_path} existe")
        
        # Lire et analyser la vue tableau_de_bord
        try:
            with open(views_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Rechercher la vue tableau_de_bord
            if 'def tableau_de_bord' in content:
                print("✅ Vue tableau_de_bord trouvée")
                
                # Extraire la fonction
                import re
                pattern = r'def tableau_de_bord\(request\):.*?(?=\n\n|\Z)'
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    print("\n📄 CODE DE LA VUE tableau_de_bord:")
                    print("-" * 40)
                    print(match.group(0)[:500] + "..." if len(match.group(0)) > 500 else match.group(0))
                    print("-" * 40)
                    
                    # Vérifier les problèmes courants
                    problèmes = []
                    if 'agent = Agent.objects.get(user=user)' in content:
                        print("✅ Utilisation correcte de Agent.objects.get(user=user)")
                    else:
                        problèmes.append("Mauvaise récupération de l'agent")
                        
                    if 'except Agent.DoesNotExist' in content:
                        print("✅ Gestion de l'exception Agent.DoesNotExist")
                    else:
                        problèmes.append("Exception non gérée")
                        
                    if problèmes:
                        print(f"\n⚠️ PROBLÈMES DÉTECTÉS:")
                        for pb in problèmes:
                            print(f"  - {pb}")
                            
            else:
                print("❌ Vue tableau_de_bord non trouvée")
                
        except Exception as e:
            print(f"❌ Erreur lors de la lecture: {e}")
    else:
        print(f"❌ Fichier {views_path} non trouvé")

def proposer_corrections():
    """Propose des corrections basées sur le diagnostic"""
    print_header("5. SOLUTIONS ET CORRECTIONS PROPOSÉES")
    
    print("\n🎯 CORRECTIONS PRIORITAIRES:")
    
    # 1. Vérifier le modèle Agent
    print("\n1. CORRIGER LE MODÈLE AGENT:")
    print("""
    # Dans agents/models.py, assurez-vous que le modèle Agent a:
    class Agent(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
        code_agent = models.CharField(max_length=20, unique=True)
        telephone = models.CharField(max_length=20, blank=True)
        agence = models.ForeignKey('Agence', on_delete=models.SET_NULL, null=True, blank=True)
        date_creation = models.DateTimeField(auto_now_add=True)
        est_actif = models.BooleanField(default=True)  # Utiliser 'est_actif' au lieu de 'actif'
        
        # Les champs email, nom, prenom sont déjà dans User
        # Utilisez agent.user.email, agent.user.first_name, agent.user.last_name
        
        def __str__(self):
            return f"{self.user.get_full_name()} ({self.code_agent})"
    """)
    
    # 2. Créer un agent pour ORNELLA
    print("\n2. CRÉER UN AGENT POUR ORNELLA:")
    print("""
    # Exécutez ce code dans le shell Django:
    from django.contrib.auth.models import User
    from agents.models import Agent
    
    # Récupérer l'utilisateur
    user = User.objects.get(username='ORNELLA')
    
    # Créer l'agent (si non existant)
    agent, created = Agent.objects.get_or_create(
        user=user,
        defaults={
            'code_agent': 'AG001',
            'telephone': '',
            'est_actif': True
        }
    )
    
    print(f"Agent créé: {created}, ID: {agent.pk}")
    """)
    
    # 3. Corriger la vue tableau_de_bord
    print("\n3. CORRIGER LA VUE tableau_de_bord:")
    print("""
    # Dans agents/views.py, modifiez la vue:
    from django.contrib.auth.decorators import login_required
    from agents.models import Agent
    from core.utils import gerer_erreurs
    
    @login_required
    @gerer_erreurs
    def tableau_de_bord(request):
        user = request.user
        
        try:
            # Récupérer l'agent correctement
            agent = Agent.objects.get(user=user)
            
            # Préparer le contexte avec les bonnes données
            context = {
                'agent': agent,
                'nom_agent': agent.user.get_full_name() or agent.user.username,
                'email_agent': agent.user.email,
                'code_agent': agent.code_agent,
                'telephone': agent.telephone,
                'est_actif': agent.est_actif,
            }
            
            return render(request, 'agents/tableau_de_bord.html', context)
            
        except Agent.DoesNotExist:
            messages.error(request, "Votre profil agent n'est pas configuré.")
            return redirect('login')
    """)
    
    # 4. Script de migration
    print("\n4. SCRIPT DE MIGRATION:")
    print("""
    # Créez un fichier correct_agents.py et exécutez-le:
    
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    django.setup()
    
    from django.contrib.auth.models import User
    from agents.models import Agent
    from django.db import connection
    
    def corriger_agents():
        print("Début de la correction des agents...")
        
        # Vérifier si la table agents_agent existe
        tables = connection.introspection.table_names()
        if 'agents_agent' not in tables:
            print("❌ La table agents_agent n'existe pas!")
            print("Exécutez: python manage.py makemigrations agents")
            print("         python manage.py migrate agents")
            return
        
        # Vérifier la structure de la table
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info(agents_agent)")
            columns = [col[1] for col in cursor.fetchall()]
            print(f"Colonnes de agents_agent: {columns}")
        
        # Créer les agents manquants pour les utilisateurs du groupe AGENT
        groupe_agent, _ = Group.objects.get_or_create(name='AGENT')
        users_agent = User.objects.filter(groups__name='AGENT')
        
        for user in users_agent:
            try:
                Agent.objects.get(user=user)
                print(f"✅ Agent existe déjà pour {user.username}")
            except Agent.DoesNotExist:
                agent = Agent.objects.create(
                    user=user,
                    code_agent=f"AG{user.id:03d}",
                    telephone="",
                    est_actif=True
                )
                print(f"✅ Agent créé pour {user.username} (ID: {agent.pk})")
        
        print("Correction terminée!")
    
    if __name__ == "__main__":
        corriger_agents()
    """)

def executer_corrections():
    """Exécute automatiquement les corrections"""
    print_header("EXÉCUTION DES CORRECTIONS")
    
    try:
        from django.contrib.auth.models import User, Group
        from agents.models import Agent
        
        print("1. Vérification de l'utilisateur ORNELLA...")
        try:
            user = User.objects.get(username='ORNELLA')
            print(f"✅ Utilisateur trouvé: {user.username}")
        except User.DoesNotExist:
            print("❌ Utilisateur ORNELLA non trouvé")
            return
        
        print("\n2. Vérification/création de l'agent...")
        try:
            # Vérifier si l'agent existe
            agent = Agent.objects.get(user=user)
            print(f"✅ Agent existant trouvé (ID: {agent.pk})")
            
            # Mettre à jour les champs si nécessaire
            if not hasattr(agent, 'code_agent'):
                agent.code_agent = f"AG{user.id:03d}"
                agent.save()
                print("✅ Code agent ajouté")
                
            if not hasattr(agent, 'est_actif'):
                agent.est_actif = True
                agent.save()
                print("✅ Champ est_actif ajouté")
                
        except Agent.DoesNotExist:
            print("❌ Agent non trouvé, création en cours...")
            
            # Créer l'agent avec les champs disponibles
            try:
                # Essayer avec code_agent
                agent = Agent.objects.create(
                    user=user,
                    code_agent=f"AG{user.id:03d}",
                    est_actif=True
                )
                print(f"✅ Agent créé avec succès (ID: {agent.pk})")
            except Exception as e:
                print(f"⚠️ Erreur création standard: {e}")
                
                # Essayer avec les champs minimaux
                try:
                    agent = Agent.objects.create(user=user)
                    print(f"✅ Agent créé avec uniquement user (ID: {agent.pk})")
                except Exception as e2:
                    print(f"❌ Impossible de créer l'agent: {e2}")
                    print("Le modèle Agent a besoin d'être corrigé d'abord.")
                    return
        
        print("\n3. Vérification des champs de l'agent...")
        agent = Agent.objects.get(user=user)
        print("📋 CHAMPS DISPONIBLES:")
        for field in Agent._meta.fields:
            try:
                value = getattr(agent, field.name)
                print(f"  - {field.name}: {value}")
            except:
                print(f"  - {field.name}: NON DISPONIBLE")
        
        print("\n✅ Correction terminée avec succès!")
        print(f"Agent ID: {agent.pk}")
        print(f"Code agent: {getattr(agent, 'code_agent', 'NON DÉFINI')}")
        print(f"Est actif: {getattr(agent, 'est_actif', 'NON DÉFINI')}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        import traceback
        traceback.print_exc()

def menu_principal():
    """Menu principal du script de diagnostic"""
    while True:
        print_header("MENU PRINCIPAL - DIAGNOSTIC AGENTS")
        print("1. 🔍 Diagnostic complet")
        print("2. 📊 Analyser le modèle Agent")
        print("3. 👤 Analyser les utilisateurs")
        print("4. 💾 Analyser les données")
        print("5. 🖥️ Analyser les vues")
        print("6. 🔧 Proposer des corrections")
        print("7. ⚡ Exécuter les corrections")
        print("8. 📝 Générer un rapport")
        print("9. 🚪 Quitter")
        
        choix = input("\nVotre choix (1-9): ").strip()
        
        if choix == '1':
            diagnostic_complet()
        elif choix == '2':
            diagnostic_modele_agent()
        elif choix == '3':
            diagnostic_utilisateurs()
        elif choix == '4':
            diagnostic_donnees()
        elif choix == '5':
            diagnostic_vues()
        elif choix == '6':
            proposer_corrections()
        elif choix == '7':
            executer_corrections()
        elif choix == '8':
            generer_rapport()
        elif choix == '9':
            print("Au revoir!")
            break
        else:
            print("Choix invalide!")
        
        input("\nAppuyez sur Entrée pour continuer...")

def generer_rapport():
    """Génère un rapport complet"""
    import datetime
    
    rapport = f"""
    RAPPORT DE DIAGNOSTIC AGENTS
    Date: {datetime.datetime.now()}
    """
    
    print_header("GÉNÉRATION DU RAPPORT")
    
    try:
        # Collecter les informations
        from django.contrib.auth.models import User
        from agents.models import Agent
        
        rapport += f"\n\n1. INFORMATIONS SYSTÈME:"
        rapport += f"\n- Django version: {django.get_version()}"
        rapport += f"\n- Python version: {sys.version}"
        
        rapport += f"\n\n2. UTILISATEURS AGENTS:"
        try:
            groupe_agent = Group.objects.get(name='AGENT')
            users_agent = User.objects.filter(groups=groupe_agent)
            rapport += f"\n- Nombre d'utilisateurs dans le groupe AGENT: {users_agent.count()}"
            
            for user in users_agent:
                rapport += f"\n  - {user.username} ({user.email})"
                try:
                    agent = Agent.objects.get(user=user)
                    rapport += f" -> Agent ID: {agent.pk}"
                except Agent.DoesNotExist:
                    rapport += " -> ❌ PAS D'AGENT"
        except Group.DoesNotExist:
            rapport += "\n- ❌ Groupe AGENT non trouvé"
        
        rapport += f"\n\n3. STATISTIQUES AGENTS:"
        try:
            total_agents = Agent.objects.count()
            rapport += f"\n- Total agents: {total_agents}"
            
            if total_agents > 0:
                agents_sans_user = Agent.objects.filter(user__isnull=True).count()
                rapport += f"\n- Agents sans utilisateur: {agents_sans_user}"
                
                # Vérifier les champs
                sample_agent = Agent.objects.first()
                champs = [f.name for f in Agent._meta.fields]
                rapport += f"\n- Champs du modèle: {', '.join(champs)}"
        except:
            rapport += "\n- ❌ Impossible d'accéder au modèle Agent"
        
        # Sauvegarder le rapport
        nom_fichier = f"rapport_agents_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(nom_fichier, 'w', encoding='utf-8') as f:
            f.write(rapport)
        
        print(f"✅ Rapport généré: {nom_fichier}")
        print("\n" + "="*80)
        print(rapport)
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération du rapport: {e}")

if __name__ == "__main__":
    print_header("SCRIPT DE DIAGNOSTIC AGENTS - MUTUELLE CORE")
    print("Version 1.0 - Analyse et correction des problèmes Agents")
    
    # Vérifier les arguments de ligne de commande
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == '--diagnostic':
            diagnostic_complet()
        elif arg == '--corriger':
            executer_corrections()
        elif arg == '--rapport':
            generer_rapport()
        elif arg == '--menu':
            menu_principal()
        else:
            print(f"Argument inconnu: {arg}")
            print("Options disponibles: --diagnostic, --corriger, --rapport, --menu")
    else:
        # Mode interactif par défaut
        menu_principal()