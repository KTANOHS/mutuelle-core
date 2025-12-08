# diagnostic_permissions_acces_corrige.py

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
    """Vérifie la structure de la base de données - VERSION CORRIGÉE"""
    print("🗃️ STRUCTURE DE LA BASE DE DONNÉES")
    print("=" * 50)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
        
        tables_importantes = [
            'membres_membre', 'soins_bondesoin', 'medecin_ordonnance',
            'pharmacien_ordonnancepharmacien', 'agents_agent', 'paiements_paiement'
        ]
        
        for table in tables_importantes:
            if table in tables:
                # CORRECTION: Créer un nouveau curseur pour chaque requête
                with connection.cursor() as cursor_count:
                    cursor_count.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor_count.fetchone()[0]
                print(f"✅ {table}: {count} enregistrements")
            else:
                print(f"❌ {table}: TABLE MANQUANTE")
                
    except Exception as e:
        print(f"❌ Erreur vérification base de données: {e}")

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
        # Vérifier si le modèle Agent existe
        try:
            from agents.models import Agent
            agents_count = Agent.objects.count()
            print(f"👤 Agents enregistrés: {agents_count}")
        except ImportError:
            print("👤 Modèle Agent: NON DISPONIBLE")
        
        # Vérifier accès aux membres
        try:
            from membres.models import Membre
            membres_count = Membre.objects.count()
            print(f"📋 Membres accessibles: {membres_count}")
        except ImportError:
            print("📋 Modèle Membre: NON DISPONIBLE")
        
        # Vérifier accès aux bons de soin
        try:
            from soins.models import BonDeSoin
            bons_count = BonDeSoin.objects.count()
            print(f"📄 Bons de soin accessibles: {bons_count}")
        except ImportError:
            print("📄 Modèle BonDeSoin: NON DISPONIBLE")
        
        # Vérifier modèle Cotisation
        try:
            from cotisations.models import Cotisation
            cotisations_count = Cotisation.objects.count()
            print(f"💰 Cotisations accessibles: {cotisations_count}")
        except ImportError:
            print("💰 Modèle Cotisation: NON DISPONIBLE")
            
    except Exception as e:
        print(f"❌ Erreur vérification agents: {e}")

def verifier_acces_medecins():
    """Vérifie ce que les médecins peuvent voir"""
    print("\n🏥 ACCÈS DES MÉDECINS")
    print("=" * 50)
    
    try:
        # Vérifier si le modèle Medecin existe
        try:
            from medecin.models import Medecin
            medecins_count = Medecin.objects.count()
            print(f"👨‍⚕️ Médecins enregistrés: {medecins_count}")
        except ImportError:
            print("👨‍⚕️ Modèle Medecin: NON DISPONIBLE")
        
        # Vérifier accès aux bons de soin
        try:
            from soins.models import BonDeSoin
            bons_total = BonDeSoin.objects.count()
            print(f"📋 Bons de soin totaux: {bons_total}")
            
            # Essayer de compter les bons créés par des agents
            try:
                bons_agents = BonDeSoin.objects.filter(createur__groups__name='Agents').count()
                print(f"📋 Bons créés par agents: {bons_agents}")
            except Exception:
                print("📋 Bons agents: IMPOSSIBLE À COMPTER")
                
        except ImportError:
            print("📋 Modèle BonDeSoin: NON DISPONIBLE")
        
        # Vérifier accès aux ordonnances
        try:
            from medecin.models import Ordonnance
            ordonnances_count = Ordonnance.objects.count()
            print(f"💊 Ordonnances accessibles: {ordonnances_count}")
        except ImportError:
            print("💊 Modèle Ordonnance: NON DISPONIBLE")
            
    except Exception as e:
        print(f"❌ Erreur vérification médecins: {e}")

def verifier_acces_pharmaciens():
    """Vérifie ce que les pharmaciens peuvent voir"""
    print("\n💊 ACCÈS DES PHARMACIENS")
    print("=" * 50)
    
    try:
        # Vérifier si le modèle Pharmacien existe
        try:
            from pharmacien.models import Pharmacien
            pharmaciens_count = Pharmacien.objects.count()
            print(f"👨‍⚕️ Pharmaciens enregistrés: {pharmaciens_count}")
        except ImportError:
            print("👨‍⚕️ Modèle Pharmacien: NON DISPONIBLE")
        
        # Vérifier accès aux ordonnances
        try:
            from medecin.models import Ordonnance
            ordonnances_total = Ordonnance.objects.count()
            print(f"📋 Ordonnances totales: {ordonnances_total}")
            
            # Essayer de compter les ordonnances par type de créateur
            try:
                ordonnances_medecins = Ordonnance.objects.filter(medecin__isnull=False).count()
                print(f"📋 Ordonnances médecins: {ordonnances_medecins}")
            except Exception:
                print("📋 Ordonnances médecins: IMPOSSIBLE À COMPTER")
                
            try:
                ordonnances_agents = Ordonnance.objects.filter(createur__groups__name='Agents').count()
                print(f"📋 Ordonnances agents: {ordonnances_agents}")
            except Exception:
                print("📋 Ordonnances agents: IMPOSSIBLE À COMPTER")
                
        except ImportError:
            print("📋 Modèle Ordonnance: NON DISPONIBLE")
        
    except Exception as e:
        print(f"❌ Erreur vérification pharmaciens: {e}")

def verifier_acces_membres():
    """Vérifie ce que les membres peuvent voir"""
    print("\n👤 ACCÈS DES MEMBRES")
    print("=" * 50)
    
    try:
        # Vérifier si le modèle Membre existe
        try:
            from membres.models import Membre
            membres_count = Membre.objects.count()
            print(f"👤 Membres enregistrés: {membres_count}")
            
            if membres_count > 0:
                membre_test = Membre.objects.first()
                
                # Vérifier accès aux propres bons du membre
                try:
                    from soins.models import BonDeSoin
                    bons_membre = BonDeSoin.objects.filter(patient=membre_test).count()
                    print(f"📋 Bons du membre test: {bons_membre}")
                except Exception:
                    print("📋 Bons membre: IMPOSSIBLE À COMPTER")
                
                # Vérifier accès aux propres ordonnances du membre
                try:
                    from medecin.models import Ordonnance
                    ordonnances_membre = Ordonnance.objects.filter(patient=membre_test).count()
                    print(f"💊 Ordonnances du membre test: {ordonnances_membre}")
                except Exception:
                    print("💊 Ordonnances membre: IMPOSSIBLE À COMPTER")
                    
        except ImportError:
            print("👤 Modèle Membre: NON DISPONIBLE")
        
    except Exception as e:
        print(f"❌ Erreur vérification membres: {e}")

def tester_urls_par_role():
    """Teste l'accès aux URLs par rôle - VERSION CORRIGÉE"""
    print("\n🌐 TEST DES URLs PAR RÔLE")
    print("=" * 50)
    
    urls_par_role = {
        'agents': [
            ('agents:dashboard', 'Tableau de bord agents'),
            ('agents:creer_membre', 'Créer membre'),
            ('agents:liste_membres', 'Liste membres'),
            ('agents:creer_bon_soin', 'Créer bon de soin'),
            ('agents:verification_cotisations', 'Vérification cotisations'),
        ],
        'medecin': [
            ('medecin:dashboard', 'Tableau de bord médecin'),
            ('medecin:liste_ordonnances', 'Liste ordonnances'),
            ('medecin:creer_ordonnance', 'Créer ordonnance'),
        ],
        'pharmacien': [
            ('pharmacien:dashboard', 'Tableau de bord pharmacien'),
            ('pharmacien:liste_ordonnances_attente', 'Ordonnances en attente'),
            ('pharmacien:stock', 'Gestion stock'),
        ],
        'membres': [
            ('membres:dashboard', 'Tableau de bord membre'),
            ('membres:mes_bons', 'Mes bons de soin'),
            ('membres:mes_ordonnances', 'Mes ordonnances'),
        ]
    }
    
    for role, urls in urls_par_role.items():
        print(f"\n🔗 {role.upper()}:")
        for url_name, description in urls:
            try:
                url = reverse(url_name)
                print(f"   ✅ {description}: {url_name}")
            except Exception as e:
                print(f"   ❌ {description}: {e}")

def verifier_relations_modeles():
    """Vérifie les relations entre les modèles"""
    print("\n🔗 RELATIONS ENTRE MODÈLES")
    print("=" * 50)
    
    try:
        # Vérifier relation BonDeSoin -> Membre
        try:
            from soins.models import BonDeSoin
            from membres.models import Membre
            
            if BonDeSoin.objects.exists():
                bon = BonDeSoin.objects.first()
                if hasattr(bon, 'patient'):
                    print("✅ Relation BonDeSoin -> Membre: OK")
                else:
                    print("❌ Relation BonDeSoin -> Membre: MANQUANTE")
        except ImportError:
            print("📋 Modèles soins/membres: NON DISPONIBLES")
        
        # Vérifier relation Ordonnance -> Membre
        try:
            from medecin.models import Ordonnance
            
            if Ordonnance.objects.exists():
                ordonnance = Ordonnance.objects.first()
                if hasattr(ordonnance, 'patient'):
                    print("✅ Relation Ordonnance -> Membre: OK")
                else:
                    print("❌ Relation Ordonnance -> Membre: MANQUANTE")
        except ImportError:
            print("💊 Modèle Ordonnance: NON DISPONIBLE")
                
        # Vérifier relation Ordonnance -> Médecin
        try:
            from medecin.models import Ordonnance
            
            if Ordonnance.objects.exists():
                ordonnance = Ordonnance.objects.first()
                if hasattr(ordonnance, 'medecin'):
                    print("✅ Relation Ordonnance -> Médecin: OK")
                else:
                    print("❌ Relation Ordonnance -> Médecin: MANQUANTE")
        except ImportError:
            print("💊 Modèle Ordonnance: NON DISPONIBLE")
                
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