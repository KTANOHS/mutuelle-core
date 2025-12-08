# diagnostic_auto.py
import os
import sys
import django
import json
from datetime import datetime
from pathlib import Path

def detecter_module_django():
    """Détecte le module Django automatiquement"""
    current_dir = Path(__file__).parent
    
    # Méthode 1: Via manage.py
    manage_py = current_dir / "manage.py"
    if manage_py.exists():
        with open(manage_py, 'r') as f:
            content = f.read()
            if 'os.environ.setdefault' in content:
                import re
                match = re.search(r"os\.environ\.setdefault\('DJANGO_SETTINGS_MODULE', '([^']+)'", content)
                if match:
                    full_module = match.group(1)
                    return full_module.split('.')[0]
    
    # Méthode 2: Recherche de settings.py
    for item in current_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            settings_file = item / "settings.py"
            if settings_file.exists():
                return item.name
    
    # Méthode 3: settings.py à la racine
    if (current_dir / "settings.py").exists():
        return current_dir.name
    
    return None

# Détection automatique
print("🔍 Détection du module Django...")
module_django = detecter_module_django()

if not module_django:
    print("❌ Impossible de détecter le module Django")
    print("📁 Contenu du dossier:")
    for item in Path('.').iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            print(f"   📂 {item.name}")
    sys.exit(1)

print(f"✅ Module détecté: {module_django}")

# Configuration Django
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{module_django}.settings')
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    django.setup()
    print("✅ Django configuré avec succès")
    
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

# Import des modèles Django
from django.db import connection
from django.db.models import Count, Q
from django.contrib.auth.models import User

# Import des modèles avec gestion d'erreur
modeles_importes = {}
try:
    from membres.models import Membre, Paiement, Cotisation
    modeles_importes['membres'] = True
    print("✅ Modèles membres importés")
except ImportError as e:
    print(f"⚠️  Modèles membres: {e}")
    modeles_importes['membres'] = False

try:
    from agents.models import Agent
    modeles_importes['agents'] = True
    print("✅ Modèles agents importés")
except ImportError as e:
    print(f"⚠️  Modèles agents: {e}")
    modeles_importes['agents'] = False

try:
    from medecin.models import BonSoin, Ordonnance, Consultation
    modeles_importes['medecin'] = True
    print("✅ Modèles medecin importés")
except ImportError as e:
    print(f"⚠️  Modèles medecin: {e}")
    modeles_importes['medecin'] = False

try:
    from communication.models import Notification
    modeles_importes['communication'] = True
    print("✅ Modèles communication importés")
except ImportError as e:
    print(f"⚠️  Modèles communication: {e}")
    modeles_importes['communication'] = False

class DiagnosticSynchronisation:
    def __init__(self):
        self.resultats = {
            'timestamp': datetime.now().isoformat(),
            'module_django': module_django,
            'statistiques': {},
            'problemes': [],
            'recommandations': [],
            'performance': {},
            'modeles_disponibles': modeles_importes
        }
    
    def executer_diagnostic_complet(self):
        print("\n🔍 LANCEMENT DU DIAGNOSTIC DE SYNCHRONISATION...")
        print("=" * 60)
        
        try:
            self.diagnostic_base_donnees()
            self.diagnostic_integrite_donnees()
            self.diagnostic_performance()
            self.diagnostic_coherence_metier()
            self.generer_rapport()
            
            print("✅ DIAGNOSTIC TERMINÉ AVEC SUCCÈS")
            
        except Exception as e:
            print(f"❌ Erreur lors du diagnostic: {str(e)}")
            self.resultats['erreur'] = str(e)
    
    def diagnostic_base_donnees(self):
        print("📊 Analyse de la base de données...")
        
        try:
            with connection.cursor() as cursor:
                # Test de connexion
                cursor.execute("SELECT 1")
                print("   ✅ Base de données connectée")
                
                # Détection du type de BDD
                try:
                    cursor.execute("SELECT sqlite_version()")
                    bdd_type = "SQLite"
                    print("   🗃️  Type: SQLite")
                except:
                    bdd_type = "PostgreSQL"
                    print("   🗃️  Type: PostgreSQL")
                
                # Statistiques de base
                user_count = User.objects.count()
                self.resultats['statistiques']['utilisateurs'] = user_count
                print(f"   👥 Utilisateurs: {user_count}")
                
        except Exception as e:
            print(f"   ❌ Erreur connexion BDD: {e}")
            self.resultats['problemes'].append({
                'type': 'CONNEXION BDD',
                'description': f'Erreur connexion base de données: {str(e)}',
                'severite': 'HAUTE'
            })
    
    def diagnostic_integrite_donnees(self):
        print("🔎 Vérification de l'intégrité des données...")
        
        # Vérifier les membres si disponible
        if modeles_importes.get('membres'):
            try:
                membre_count = Membre.objects.count()
                self.resultats['statistiques']['membres'] = membre_count
                print(f"   👤 Membres: {membre_count}")
                
                # Vérifications d'intégrité
                try:
                    membres_sans_user = Membre.objects.filter(user__isnull=True)
                    if membres_sans_user.exists():
                        self.resultats['problemes'].append({
                            'type': 'INTÉGRITÉ RELATIONNELLE',
                            'description': f'{membres_sans_user.count()} membres sans utilisateur associé',
                            'severite': 'HAUTE'
                        })
                        print(f"   ❌ {membres_sans_user.count()} membres sans user")
                    
                    # Vérifier les numéros uniques
                    from django.db.models import Count
                    doublons = Membre.objects.values('numero_membre').annotate(
                        count=Count('id')
                    ).filter(count__gt=1, numero_membre__isnull=False)
                    
                    if doublons.exists():
                        self.resultats['problemes'].append({
                            'type': 'DOUBLONS',
                            'description': f'{doublons.count()} numéros de membre en double',
                            'severite': 'MOYENNE'
                        })
                        print(f"   ⚠️  {doublons.count()} numéros en double")
                        
                except Exception as e:
                    print(f"   ⚠️  Vérifications avancées échouées: {e}")
                    
            except Exception as e:
                print(f"   ⚠️  Impossible d'analyser les membres: {e}")
        
        # Vérifier autres modèles
        if modeles_importes.get('agents'):
            try:
                agent_count = Agent.objects.count()
                self.resultats['statistiques']['agents'] = agent_count
                print(f"   🏢 Agents: {agent_count}")
            except Exception as e:
                print(f"   ⚠️  Impossible de compter les agents: {e}")
        
        if modeles_importes.get('medecin'):
            try:
                bonsoin_count = BonSoin.objects.count()
                self.resultats['statistiques']['bons_soin'] = bonsoin_count
                print(f"   🏥 Bons de soin: {bonsoin_count}")
            except Exception as e:
                print(f"   ⚠️  Impossible de compter les bons de soin: {e}")
    
    def diagnostic_performance(self):
        print("⚡ Analyse des performances...")
        
        try:
            with connection.cursor() as cursor:
                # Compter les indexes
                try:
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
                    indexes = cursor.fetchall()
                    index_count = len([idx for idx in indexes if not idx[0].startswith('sqlite_')])
                    self.resultats['performance']['indexes'] = index_count
                    print(f"   📈 Indexes: {index_count}")
                except:
                    print("   ⚠️  Analyse indexes non disponible")
                
        except Exception as e:
            print(f"   ⚠️  Analyse performance: {e}")
    
    def diagnostic_coherence_metier(self):
        print("🏥 Vérification de la cohérence métier...")
        
        # Vérifications métier de base
        try:
            # Vérifier si des données existent
            total_membres = self.resultats['statistiques'].get('membres', 0)
            total_agents = self.resultats['statistiques'].get('agents', 0)
            
            if total_membres == 0:
                self.resultats['problemes'].append({
                    'type': 'DONNÉES MANQUANTES',
                    'description': 'Aucun membre dans la base de données',
                    'severite': 'MOYENNE'
                })
                print("   ⚠️  Aucun membre trouvé")
            
            if total_agents == 0:
                self.resultats['problemes'].append({
                    'type': 'DONNÉES MANQUANTES', 
                    'description': 'Aucun agent dans la base de données',
                    'severite': 'MOYENNE'
                })
                print("   ⚠️  Aucun agent trouvé")
                
            print("   ✅ Vérifications métier de base terminées")
                
        except Exception as e:
            print(f"   ⚠️  Vérifications métier: {e}")
    
    def generer_rapport(self):
        print("📄 Génération du rapport...")
        
        # Statistiques résumées
        total_problemes = len(self.resultats['problemes'])
        problemes_haute = len([p for p in self.resultats['problemes'] if p.get('severite') == 'HAUTE'])
        problemes_moyenne = len([p for p in self.resultats['problemes'] if p.get('severite') == 'MOYENNE'])
        
        # Déterminer l'état général
        if total_problemes == 0:
            etat = 'EXCELLENT'
        elif problemes_haute == 0:
            etat = 'BON' 
        else:
            etat = 'ATTENTION REQUISE'
        
        resume = {
            'date_execution': self.resultats['timestamp'],
            'module_django': self.resultats['module_django'],
            'total_problemes': total_problemes,
            'problemes_haute_priorite': problemes_haute,
            'problemes_moyenne_priorite': problemes_moyenne,
            'etat_general': etat
        }
        
        self.resultats['resume_executif'] = resume
        
        # Générer recommandations
        self._generer_recommandations()
        
        # Sauvegarder
        self._sauvegarder_rapport()
        
        # Afficher résumé
        self._afficher_resume()
    
    def _generer_recommandations(self):
        recommandations = []
        
        # Basé sur les problèmes
        if any(p['type'] == 'INTÉGRITÉ RELATIONNELLE' for p in self.resultats['problemes']):
            recommandations.append({
                'priorite': 'HAUTE',
                'action': 'Corriger relations brisées',
                'description': 'Nettoyer les membres sans utilisateur associé'
            })
        
        if any(p['type'] == 'DOUBLONS' for p in self.resultats['problemes']):
            recommandations.append({
                'priorite': 'MOYENNE', 
                'action': 'Éliminer les doublons',
                'description': 'Corriger les numéros de membre en double'
            })
        
        # Recommandations générales
        if self.resultats['statistiques'].get('membres', 0) > 50:
            recommandations.append({
                'priorite': 'MOYENNE',
                'action': 'Implémenter pagination',
                'description': 'Ajouter pagination pour améliorer performances'
            })
        
        self.resultats['recommandations'] = recommandations
    
    def _sauvegarder_rapport(self):
        nom_fichier = f"diagnostic_{self.resultats['module_django']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(nom_fichier, 'w', encoding='utf-8') as f:
                json.dump(self.resultats, f, indent=2, ensure_ascii=False)
            print(f"💾 Rapport sauvegardé: {nom_fichier}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
    
    def _afficher_resume(self):
        resume = self.resultats['resume_executif']
        
        print("\n" + "="*60)
        print("📋 RAPPORT DE DIAGNOSTIC - SYNCHRONISATION")
        print("="*60)
        print(f"🏷️  Module: {resume['module_django']}")
        print(f"📅 Date: {resume['date_execution']}")
        print(f"🎯 État: {resume['etat_general']}")
        print(f"❌ Problèmes: {resume['total_problemes']} (🔴{resume['problemes_haute_priorite']} 🟡{resume['problemes_moyenne_priorite']})")
        
        print(f"\n📊 STATISTIQUES:")
        for key, value in self.resultats['statistiques'].items():
            print(f"   {key}: {value}")
        
        if self.resultats['problemes']:
            print(f"\n🚨 PROBLÈMES IDENTIFIÉS:")
            for probleme in self.resultats['problemes']:
                severite_icon = '🔴' if probleme['severite'] == 'HAUTE' else '🟡'
                print(f"   {severite_icon} {probleme['description']}")
        
        if self.resultats['recommandations']:
            print(f"\n💡 RECOMMANDATIONS:")
            for reco in self.resultats['recommandations']:
                priorite_icon = '🔴' if reco['priorite'] == 'HAUTE' else '🟡' if reco['priorite'] == 'MOYENNE' else '🟢'
                print(f"   {priorite_icon} {reco['action']}: {reco['description']}")
        
        print("="*60)

# Exécution
if __name__ == "__main__":
    diagnostic = DiagnosticSynchronisation()
    diagnostic.executer_diagnostic_complet()