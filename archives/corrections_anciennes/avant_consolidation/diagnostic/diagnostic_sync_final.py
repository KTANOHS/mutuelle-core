# diagnostic_sync_final.py
import os
import sys
import django
import json
from datetime import datetime
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from django.db import connection
from django.db.models import Count, Q
from django.contrib.auth.models import User

print("🔍 DIAGNOSTIC COMPLET DE SYNCHRONISATION - VERSION CORRIGÉE")
print("=" * 60)

# Import des modèles avec les noms corrects
try:
    from membres.models import Membre
    print("✅ Membre importé")
except ImportError as e:
    print(f"❌ Membre: {e}")
    sys.exit(1)

try:
    from medecin.models import Ordonnance, Consultation, BonDeSoin
    print("✅ Modèles medecin importés (BonDeSoin au lieu de BonSoin)")
except ImportError as e:
    print(f"❌ Modèles medecin: {e}")

try:
    from agents.models import Agent
    print("✅ Agent importé")
except ImportError as e:
    print(f"❌ Agent: {e}")

try:
    from communication.models import Notification
    print("✅ Notification importé")
except ImportError as e:
    print(f"❌ Notification: {e}")

class DiagnosticSynchronisationFinal:
    def __init__(self):
        self.resultats = {
            'timestamp': datetime.now().isoformat(),
            'module_django': 'mutuelle_core',
            'statistiques': {},
            'problemes': [],
            'recommandations': [],
            'performance': {},
            'synchronisation': {}
        }
    
    def executer_diagnostic_complet(self):
        print("\n🎯 LANCEMENT DU DIAGNOSTIC COMPLET...")
        print("=" * 60)
        
        try:
            self.diagnostic_base_donnees()
            self.diagnostic_synchronisation_metier()
            self.diagnostic_integrite_relations()
            self.diagnostic_performance()
            self.diagnostic_coherence_donnees()
            self.generer_rapport()
            
            print("✅ DIAGNOSTIC TERMINÉ AVEC SUCCÈS")
            
        except Exception as e:
            print(f"❌ Erreur lors du diagnostic: {str(e)}")
            self.resultats['erreur'] = str(e)
    
    def diagnostic_base_donnees(self):
        print("📊 ANALYSE DE LA BASE DE DONNÉES...")
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                print("   ✅ Base de données connectée")
                
            # Statistiques de base
            user_count = User.objects.count()
            self.resultats['statistiques']['utilisateurs'] = user_count
            print(f"   👥 Utilisateurs: {user_count}")
            
            membre_count = Membre.objects.count()
            self.resultats['statistiques']['membres'] = membre_count
            print(f"   👤 Membres: {membre_count}")
            
            agent_count = Agent.objects.count()
            self.resultats['statistiques']['agents'] = agent_count
            print(f"   🏢 Agents: {agent_count}")
            
            # Modèles medecin
            try:
                ordonnance_count = Ordonnance.objects.count()
                self.resultats['statistiques']['ordonnances'] = ordonnance_count
                print(f"   💊 Ordonnances: {ordonnance_count}")
            except:
                print("   ⚠️  Ordonnances: Non disponible")
                
            try:
                consultation_count = Consultation.objects.count()
                self.resultats['statistiques']['consultations'] = consultation_count
                print(f"   🏥 Consultations: {consultation_count}")
            except:
                print("   ⚠️  Consultations: Non disponible")
                
            try:
                bondesoin_count = BonDeSoin.objects.count()
                self.resultats['statistiques']['bons_de_soin'] = bondesoin_count
                print(f"   📋 Bons de soin: {bondesoin_count}")
            except:
                print("   ⚠️  Bons de soin: Non disponible")
                
        except Exception as e:
            print(f"   ❌ Erreur analyse BDD: {e}")
    
    def diagnostic_synchronisation_metier(self):
        print("\n🔄 SYNCHRONISATION MÉTIER...")
        
        # Ratio membres/utilisateurs
        total_users = self.resultats['statistiques']['utilisateurs']
        total_membres = self.resultats['statistiques']['membres']
        
        if total_users > 0:
            ratio = (total_membres / total_users) * 100
            self.resultats['synchronisation']['ratio_membres_utilisateurs'] = f"{ratio:.1f}%"
            print(f"   📈 Ratio membres/utilisateurs: {ratio:.1f}%")
            
            if ratio < 50:
                self.resultats['problemes'].append({
                    'type': 'SYNCHRONISATION',
                    'description': f'Faible ratio membres/utilisateurs ({ratio:.1f}%) - synchronisation incomplète',
                    'severite': 'MOYENNE'
                })
        
        # Membres avec user associé
        try:
            membres_avec_user = Membre.objects.filter(user__isnull=False).count()
            pourcentage_avec_user = (membres_avec_user / total_membres * 100) if total_membres > 0 else 0
            self.resultats['synchronisation']['membres_avec_user'] = f"{membres_avec_user}/{total_membres} ({pourcentage_avec_user:.1f}%)"
            print(f"   🔗 Membres avec user: {membres_avec_user}/{total_membres} ({pourcentage_avec_user:.1f}%)")
            
            if pourcentage_avec_user < 80 and total_membres > 0:
                self.resultats['problemes'].append({
                    'type': 'SYNCHRONISATION',
                    'description': f'Seulement {pourcentage_avec_user:.1f}% des membres ont un user associé',
                    'severite': 'MOYENNE'
                })
                
        except Exception as e:
            print(f"   ⚠️  Impossible de vérifier associations: {e}")
    
    def diagnostic_integrite_relations(self):
        print("\n🔗 INTÉGRITÉ DES RELATIONS...")
        
        # Vérifier les membres sans user
        try:
            membres_sans_user = Membre.objects.filter(user__isnull=True)
            if membres_sans_user.exists():
                self.resultats['problemes'].append({
                    'type': 'RELATIONS BROYÉES',
                    'description': f'{membres_sans_user.count()} membres sans utilisateur associé',
                    'severite': 'HAUTE'
                })
                print(f"   ❌ Membres sans user: {membres_sans_user.count()}")
            else:
                print("   ✅ Tous les membres ont un user associé")
                
        except Exception as e:
            print(f"   ⚠️  Vérification membres sans user: {e}")
        
        # Vérifier les doublons de numéros
        try:
            doublons = Membre.objects.values('numero_membre').annotate(
                count=Count('id')
            ).filter(count__gt=1, numero_membre__isnull=False)
            
            if doublons.exists():
                self.resultats['problemes'].append({
                    'type': 'DOUBLONS',
                    'description': f'{doublons.count()} numéros de membre en double',
                    'severite': 'MOYENNE'
                })
                print(f"   ⚠️  Numéros en double: {doublons.count()}")
            else:
                print("   ✅ Aucun numéro de membre en double")
                
        except Exception as e:
            print(f"   ⚠️  Vérification doublons: {e}")
        
        # Vérifier les données manquantes
        try:
            membres_sans_numero = Membre.objects.filter(
                Q(numero_membre__isnull=True) | Q(numero_membre='')
            )
            if membres_sans_numero.exists():
                self.resultats['problemes'].append({
                    'type': 'DONNÉES MANQUANTES',
                    'description': f'{membres_sans_numero.count()} membres sans numéro',
                    'severite': 'MOYENNE'
                })
                print(f"   ⚠️  Membres sans numéro: {membres_sans_numero.count()}")
            else:
                print("   ✅ Tous les membres ont un numéro")
                
        except Exception as e:
            print(f"   ⚠️  Vérification données manquantes: {e}")
    
    def diagnostic_performance(self):
        print("\n⚡ PERFORMANCE...")
        
        try:
            with connection.cursor() as cursor:
                # Indexes
                cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
                indexes = cursor.fetchall()
                index_count = len([idx for idx in indexes if not idx[0].startswith('sqlite_')])
                self.resultats['performance']['indexes'] = index_count
                print(f"   📈 Indexes: {index_count}")
                
                # Taille approximative
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name NOT LIKE 'sqlite_%'
                """)
                tables = cursor.fetchall()
                
                total_size = 0
                for table in tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                        count = cursor.fetchone()[0]
                        total_size += count
                    except:
                        pass
                
                self.resultats['performance']['enregistrements_totaux'] = total_size
                print(f"   💾 Enregistrements totaux: {total_size}")
                
        except Exception as e:
            print(f"   ⚠️  Analyse performance: {e}")
    
    def diagnostic_coherence_donnees(self):
        print("\n🎯 COHÉRENCE DES DONNÉES...")
        
        total_membres = self.resultats['statistiques']['membres']
        total_agents = self.resultats['statistiques']['agents']
        
        # Vérifications métier
        if total_membres == 0:
            self.resultats['problemes'].append({
                'type': 'DONNÉES MANQUANTES',
                'description': 'Aucun membre dans la base de données',
                'severite': 'MOYENNE'
            })
        elif total_membres < 5:
            print(f"   ℹ️  Base de données petite: {total_membres} membres")
        
        if total_agents == 0:
            self.resultats['problemes'].append({
                'type': 'DONNÉES MANQUANTES',
                'description': 'Aucun agent dans la base de données',
                'severite': 'MOYENNE'
            })
        
        # Cohérence globale
        if total_membres > 0 and total_agents > 0:
            ratio_agent_membre = total_agents / total_membres
            self.resultats['synchronisation']['ratio_agent_membre'] = f"1:{total_membres/total_agents:.1f}"
            print(f"   📊 Ratio agent/membre: 1:{total_membres/total_agents:.1f}")
            
            if ratio_agent_membre < 0.1:  # Moins de 10% d'agents
                self.resultats['problemes'].append({
                    'type': 'RESSOURCES',
                    'description': f'Peu d\'agents ({total_agents}) pour gérer les membres ({total_membres})',
                    'severite': 'BASSE'
                })
    
    def generer_rapport(self):
        print("\n📄 GÉNÉRATION DU RAPPORT...")
        
        # Statistiques résumées
        total_problemes = len(self.resultats['problemes'])
        problemes_haute = len([p for p in self.resultats['problemes'] if p.get('severite') == 'HAUTE'])
        problemes_moyenne = len([p for p in self.resultats['problemes'] if p.get('severite') == 'MOYENNE'])
        problemes_basse = len([p for p in self.resultats['problemes'] if p.get('severite') == 'BASSE'])
        
        # État général
        if total_problemes == 0:
            etat = 'EXCELLENT'
        elif problemes_haute == 0:
            etat = 'BON'
        else:
            etat = 'ATTENTION REQUISE'
        
        resume = {
            'date_execution': self.resultats['timestamp'],
            'total_problemes': total_problemes,
            'problemes_haute_priorite': problemes_haute,
            'problemes_moyenne_priorite': problemes_moyenne,
            'problemes_basse_priorite': problemes_basse,
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
        
        # Basé sur les problèmes identifiés
        problemes_types = [p['type'] for p in self.resultats['problemes']]
        
        if 'RELATIONS BROYÉES' in problemes_types:
            recommandations.append({
                'priorite': 'HAUTE',
                'action': 'Corriger relations membres-user',
                'description': 'Associer tous les membres à un utilisateur ou les archiver'
            })
        
        if 'DOUBLONS' in problemes_types:
            recommandations.append({
                'priorite': 'MOYENNE',
                'action': 'Nettoyer les doublons',
                'description': 'Fusionner ou corriger les numéros de membre en double'
            })
        
        if 'SYNCHRONISATION' in problemes_types:
            recommandations.append({
                'priorite': 'MOYENNE',
                'action': 'Améliorer synchronisation',
                'description': 'Automatiser la création des membres pour les nouveaux utilisateurs'
            })
        
        # Recommandations de performance
        if self.resultats['statistiques'].get('membres', 0) > 100:
            recommandations.append({
                'priorite': 'MOYENNE',
                'action': 'Optimiser performances',
                'description': 'Implémenter la pagination et les indexes sur les recherches fréquentes'
            })
        
        # Maintenance préventive
        recommandations.append({
            'priorite': 'BASSE',
            'action': 'Maintenance régulière',
            'description': 'Exécuter ce diagnostic mensuellement pour surveiller la santé des données'
        })
        
        self.resultats['recommandations'] = recommandations
    
    def _sauvegarder_rapport(self):
        nom_fichier = f"diagnostic_sync_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(nom_fichier, 'w', encoding='utf-8') as f:
                json.dump(self.resultats, f, indent=2, ensure_ascii=False)
            print(f"💾 Rapport sauvegardé: {nom_fichier}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
    
    def _afficher_resume(self):
        resume = self.resultats['resume_executif']
        
        print("\n" + "="*60)
        print("📋 RAPPORT FINAL - SYNCHRONISATION DONNÉES")
        print("="*60)
        print(f"📅 Date: {resume['date_execution']}")
        print(f"🎯 État: {resume['etat_general']}")
        print(f"❌ Problèmes: {resume['total_problemes']} (🔴{resume['problemes_haute_priorite']} 🟡{resume['problemes_moyenne_priorite']} 🟢{resume['problemes_basse_priorite']})")
        
        print(f"\n📊 STATISTIQUES:")
        for key, value in self.resultats['statistiques'].items():
            print(f"   {key}: {value}")
        
        print(f"\n🔄 SYNCHRONISATION:")
        for key, value in self.resultats['synchronisation'].items():
            print(f"   {key}: {value}")
        
        if self.resultats['problemes']:
            print(f"\n🚨 PROBLÈMES IDENTIFIÉS:")
            for probleme in self.resultats['problemes']:
                severite_icon = '🔴' if probleme['severite'] == 'HAUTE' else '🟡' if probleme['severite'] == 'MOYENNE' else '🟢'
                print(f"   {severite_icon} {probleme['description']}")
        
        if self.resultats['recommandations']:
            print(f"\n💡 RECOMMANDATIONS:")
            for reco in self.resultats['recommandations']:
                priorite_icon = '🔴' if reco['priorite'] == 'HAUTE' else '🟡' if reco['priorite'] == 'MOYENNE' else '🟢'
                print(f"   {priorite_icon} {reco['action']}: {reco['description']}")
        
        print("="*60)

# Exécution
if __name__ == "__main__":
    diagnostic = DiagnosticSynchronisationFinal()
    diagnostic.executer_diagnostic_complet()