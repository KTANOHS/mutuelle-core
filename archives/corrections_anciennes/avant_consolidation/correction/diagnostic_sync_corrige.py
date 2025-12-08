# diagnostic_sync_corrige.py
import os
import sys
import django
import json
from datetime import datetime
from pathlib import Path

# 🔧 CORRECTION : Configuration Django correcte
try:
    # Votre projet utilise probablement 'core' comme module principal
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    print("✅ Configuration Django: core.settings")
    
    # Ajouter le chemin du projet
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    django.setup()
    print("✅ Django configuré avec succès")
    
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    print("🔍 Tentative avec mutuelle_core...")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        django.setup()
        print("✅ Django configuré avec mutuelle_core.settings")
    except Exception as e2:
        print(f"❌ Échec configuration: {e2}")
        sys.exit(1)

# Maintenant importer les modèles Django
from django.db import connection
from django.db.models import Count, Q
from django.contrib.auth.models import User

# Importer vos modèles avec gestion d'erreur
try:
    from membres.models import Membre, Paiement, Cotisation
    print("✅ Modèles membres importés")
except ImportError as e:
    print(f"⚠️  Impossible d'importer membres: {e}")
    # Créer des placeholders pour le diagnostic
    class Membre: 
        objects = None
    class Paiement: 
        objects = None
    class Cotisation: 
        objects = None

try:
    from agents.models import Agent
    print("✅ Modèles agents importés")
except ImportError as e:
    print(f"⚠️  Impossible d'importer agents: {e}")
    class Agent: 
        objects = None

try:
    from medecin.models import BonSoin, Ordonnance, Consultation
    print("✅ Modèles medecin importés")
except ImportError as e:
    print(f"⚠️  Impossible d'importer medecin: {e}")
    class BonSoin: 
        objects = None
    class Ordonnance: 
        objects = None
    class Consultation: 
        objects = None

try:
    from communication.models import Notification
    print("✅ Modèles communication importés")
except ImportError as e:
    print(f"⚠️  Impossible d'importer communication: {e}")
    class Notification: 
        objects = None

class DiagnosticSynchronisation:
    def __init__(self):
        self.resultats = {
            'timestamp': datetime.now().isoformat(),
            'statistiques': {},
            'problemes': [],
            'recommandations': [],
            'performance': {},
            'erreurs_import': []
        }
    
    def executer_diagnostic_complet(self):
        print("🔍 LANCEMENT DU DIAGNOSTIC DE SYNCHRONISATION...")
        print("=" * 60)
        
        try:
            self.diagnostic_base_donnees()
            self.diagnostic_integrite_donnees()
            self.diagnostic_performance()
            self.diagnostic_coherence_metier()
            self.diagnostic_relations()
            self.generer_rapport()
            
            print("✅ DIAGNOSTIC TERMINÉ AVEC SUCCÈS")
            
        except Exception as e:
            print(f"❌ Erreur lors du diagnostic: {str(e)}")
            self.resultats['erreur'] = str(e)
    
    def diagnostic_base_donnees(self):
        print("📊 Analyse de la base de données...")
        
        try:
            with connection.cursor() as cursor:
                # Taille de la base (si PostgreSQL)
                try:
                    cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database()))")
                    taille_bdd = cursor.fetchone()[0]
                except:
                    taille_bdd = "SQLite - taille non disponible"
                
                # Nombre de tables
                try:
                    cursor.execute("""
                        SELECT name FROM sqlite_master WHERE type='table'
                    """)
                    tables = cursor.fetchall()
                    nb_tables = len(tables)
                except:
                    try:
                        cursor.execute("""
                            SELECT COUNT(*) FROM information_schema.tables 
                            WHERE table_schema = 'public'
                        """)
                        nb_tables = cursor.fetchone()[0]
                    except:
                        nb_tables = "Indisponible"
                
                self.resultats['statistiques'].update({
                    'taille_base_donnees': taille_bdd,
                    'nombre_tables': nb_tables,
                })
                print(f"   📁 Taille BDD: {taille_bdd}")
                print(f"   📊 Nombre tables: {nb_tables}")
                
        except Exception as e:
            print(f"   ❌ Erreur analyse BDD: {e}")
            self.resultats['problemes'].append({
                'type': 'CONNEXION BDD',
                'description': f'Erreur connexion base de données: {str(e)}',
                'severite': 'HAUTE'
            })
    
    def diagnostic_integrite_donnees(self):
        print("🔎 Vérification de l'intégrité des données...")
        
        # Vérifier les utilisateurs
        try:
            user_count = User.objects.count()
            self.resultats['statistiques']['utilisateurs'] = user_count
            print(f"   👥 Utilisateurs: {user_count}")
        except Exception as e:
            print(f"   ⚠️  Impossible de compter les utilisateurs: {e}")
        
        # Vérifier les membres
        try:
            if hasattr(Membre, 'objects') and Membre.objects is not None:
                membre_count = Membre.objects.count()
                self.resultats['statistiques']['membres'] = membre_count
                print(f"   👤 Membres: {membre_count}")
                
                # Vérifier membres sans user
                try:
                    membres_sans_user = Membre.objects.filter(user__isnull=True)
                    if membres_sans_user.exists():
                        self.resultats['problemes'].append({
                            'type': 'INTÉGRITÉ RELATIONNELLE',
                            'description': f'{membres_sans_user.count()} membres sans utilisateur associé',
                            'severite': 'HAUTE'
                        })
                        print(f"   ❌ {membres_sans_user.count()} membres sans user")
                except Exception as e:
                    print(f"   ⚠️  Impossible de vérifier membres sans user: {e}")
                    
        except Exception as e:
            print(f"   ⚠️  Impossible d'analyser les membres: {e}")
    
    def diagnostic_performance(self):
        print("⚡ Analyse des performances...")
        
        try:
            with connection.cursor() as cursor:
                # Pour SQLite
                try:
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
                    indexes = cursor.fetchall()
                    self.resultats['performance']['indexes'] = len(indexes)
                    print(f"   📈 Indexes SQLite trouvés: {len(indexes)}")
                except:
                    # Pour PostgreSQL
                    try:
                        cursor.execute("""
                            SELECT schemaname, tablename, indexname
                            FROM pg_indexes WHERE schemaname = 'public'
                        """)
                        indexes = cursor.fetchall()
                        self.resultats['performance']['indexes'] = len(indexes)
                        print(f"   📈 Indexes PostgreSQL trouvés: {len(indexes)}")
                    except Exception as e:
                        print(f"   ⚠️  Impossible d'analyser les indexes: {e}")
                
        except Exception as e:
            print(f"   ⚠️  Impossible d'analyser les performances: {e}")
    
    def diagnostic_coherence_metier(self):
        print("🏥 Vérification de la cohérence métier...")
        
        # Vérifications basiques de cohérence
        try:
            # Vérifier si la base répond
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                print("   ✅ Base de données responsive")
                
        except Exception as e:
            self.resultats['problemes'].append({
                'type': 'PERFORMANCE BDD',
                'description': f'Base de données non responsive: {str(e)}',
                'severite': 'HAUTE'
            })
        
        # Vérifier les cotisations si le modèle existe
        try:
            if hasattr(Cotisation, 'objects') and Cotisation.objects is not None:
                cotisations_count = Cotisation.objects.count()
                self.resultats['statistiques']['cotisations'] = cotisations_count
                print(f"   💰 Cotisations: {cotisations_count}")
        except Exception as e:
            print(f"   ⚠️  Impossible de compter les cotisations: {e}")
    
    def diagnostic_relations(self):
        print("🔗 Analyse des relations entre modèles...")
        
        # Vérifier les relations clés
        try:
            if hasattr(Membre, 'objects') and Membre.objects is not None:
                # Membres avec des relations brisées
                try:
                    membres_problemes = Membre.objects.filter(
                        Q(user__isnull=True) | 
                        Q(numero_membre__isnull=True) |
                        Q(numero_membre='')
                    )
                    if membres_problemes.exists():
                        self.resultats['problemes'].append({
                            'type': 'RELATIONS BROYÉES',
                            'description': f'{membres_problemes.count()} membres avec relations problématiques',
                            'severite': 'MOYENNE'
                        })
                        print(f"   ⚠️  {membres_problemes.count()} membres avec problèmes de relations")
                except Exception as e:
                    print(f"   ⚠️  Impossible de vérifier relations membres: {e}")
                    
        except Exception as e:
            print(f"   ⚠️  Impossible d'analyser les relations: {e}")
    
    def generer_rapport(self):
        print("📄 Génération du rapport...")
        
        # Calculer les statistiques résumées
        total_problemes = len(self.resultats['problemes'])
        problemes_haute = len([p for p in self.resultats['problemes'] if p.get('severite') == 'HAUTE'])
        problemes_moyenne = len([p for p in self.resultats['problemes'] if p.get('severite') == 'MOYENNE'])
        
        # Résumé exécutif
        resume = {
            'date_execution': self.resultats['timestamp'],
            'total_problemes': total_problemes,
            'problemes_haute_priorite': problemes_haute,
            'problemes_moyenne_priorite': problemes_moyenne,
            'etat_general': 'EXCELLENT' if total_problemes == 0 else 'BON' if problemes_haute == 0 else 'ATTENTION REQUISE'
        }
        
        self.resultats['resume_executif'] = resume
        
        # Générer des recommandations
        self._generer_recommandations()
        
        # Sauvegarde du rapport
        self._sauvegarder_rapport()
        
        # Affichage du résumé
        self._afficher_resume()
    
    def _generer_recommandations(self):
        """Génère des recommandations basées sur les problèmes identifiés"""
        recommandations = []
        
        # Recommandations basées sur les problèmes
        problemes_par_type = {}
        for probleme in self.resultats['problemes']:
            probleme_type = probleme.get('type', 'AUTRE')
            if probleme_type not in problemes_par_type:
                problemes_par_type[probleme_type] = 0
            problemes_par_type[probleme_type] += 1
        
        if 'INTÉGRITÉ RELATIONNELLE' in problemes_par_type:
            recommandations.append({
                'priorite': 'HAUTE',
                'action': 'Nettoyer les relations brisées',
                'description': 'Corriger les membres sans utilisateur associé'
            })
        
        if self.resultats['statistiques'].get('membres', 0) > 100:
            recommandations.append({
                'priorite': 'MOYENNE',
                'action': 'Implémenter la pagination',
                'description': 'Ajouter la pagination sur les listes de membres pour améliorer les performances'
            })
        
        # Recommandation générale de maintenance
        recommandations.append({
            'priorite': 'BASSE',
            'action': 'Maintenance préventive',
            'description': 'Exécuter ce diagnostic régulièrement pour surveiller la santé des données'
        })
        
        self.resultats['recommandations'] = recommandations
    
    def _sauvegarder_rapport(self):
        """Sauvegarde le rapport dans un fichier JSON"""
        nom_fichier = f"diagnostic_sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(nom_fichier, 'w', encoding='utf-8') as f:
                json.dump(self.resultats, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Rapport sauvegardé: {nom_fichier}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde rapport: {e}")
    
    def _afficher_resume(self):
        """Affiche un résumé du diagnostic dans la console"""
        resume = self.resultats['resume_executif']
        problemes_haute = [p for p in self.resultats['problemes'] if p.get('severite') == 'HAUTE']
        
        print("\n" + "="*60)
        print("📋 RAPPORT DE DIAGNOSTIC - SYNCHRONISATION DONNÉES")
        print("="*60)
        print(f"📅 Date d'exécution: {resume['date_execution']}")
        print(f"🏷️  État général: {resume['etat_general']}")
        print(f"❌ Problèmes totaux: {resume['total_problemes']}")
        print(f"🔴 Problèmes haute priorité: {resume['problemes_haute_priorite']}")
        print(f"🟡 Problèmes moyenne priorité: {resume['problemes_moyenne_priorite']}")
        
        # Afficher les statistiques
        print(f"\n📊 STATISTIQUES:")
        for key, value in self.resultats['statistiques'].items():
            print(f"   {key}: {value}")
        
        if problemes_haute:
            print(f"\n🔴 PROBLÈMES HAUTE PRIORITÉ:")
            for probleme in problemes_haute:
                print(f"   • {probleme['description']}")
        
        if self.resultats['recommandations']:
            print(f"\n💡 RECOMMANDATIONS:")
            for reco in sorted(self.resultats['recommandations'], key=lambda x: x['priorite'], reverse=True):
                print(f"   [{reco['priorite']}] {reco['action']}: {reco['description']}")
        
        print("="*60)

# Script d'exécution
if __name__ == "__main__":
    diagnostic = DiagnosticSynchronisation()
    diagnostic.executer_diagnostic_complet()