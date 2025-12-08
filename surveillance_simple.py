# surveillance_simple.py
import os
import sys
import django
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from django.contrib.auth.models import User
from membres.models import Membre
from django.db.models import Count, Q

class SurveillantSimple:
    def __init__(self):
        self.dernier_rapport = None
    
    def verifier_etat_systeme(self):
        """Vérification complète de l'état du système"""
        print(f"\n🔍 Vérification à {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 50)
        
        rapport = {
            'timestamp': datetime.now().isoformat(),
            'statistiques': {},
            'alertes': [],
            'etat': 'OPTIMAL'
        }
        
        # Statistiques de base
        try:
            total_users = User.objects.count()
            total_membres = Membre.objects.count()
            membres_avec_user = Membre.objects.filter(user__isnull=False).count()
            
            rapport['statistiques'] = {
                'utilisateurs': total_users,
                'membres': total_membres,
                'membres_avec_user': membres_avec_user,
                'taux_synchronisation': (membres_avec_user / total_membres * 100) if total_membres > 0 else 0
            }
            
            print(f"📊 Utilisateurs: {total_users}")
            print(f"📊 Membres: {total_membres}")
            print(f"📊 Synchronisation: {rapport['statistiques']['taux_synchronisation']:.1f}%")
            
            # Vérifications critiques
            if membres_avec_user < total_membres:
                rapport['alertes'].append("Membres non synchronisés détectés")
                rapport['etat'] = 'CRITIQUE'
            
            # Vérifier l'intégrité des données
            try:
                doublons = Membre.objects.values('numero_unique').annotate(
                    count=Count('id')
                ).filter(count__gt=1, numero_unique__isnull=False)
                
                if doublons.exists():
                    rapport['alertes'].append(f"Doublons numéros: {doublons.count()}")
                    rapport['etat'] = 'ATTENTION'
            except Exception as e:
                print(f"⚠️  Vérification doublons: {e}")
            
            # Évaluation globale
            if not rapport['alertes']:
                print("✅ État: OPTIMAL")
            else:
                print(f"🚨 Alertes: {len(rapport['alertes'])}")
                for alerte in rapport['alertes']:
                    print(f"   ⚠️  {alerte}")
            
        except Exception as e:
            print(f"❌ Erreur vérification: {e}")
            rapport['etat'] = 'ERREUR'
        
        self.dernier_rapport = rapport
        return rapport
    
    def surveiller_en_continu(self, intervalle_minutes=5):
        """Surveillance continue simple"""
        print("🚀 Démarrage surveillance continue...")
        print(f"⏰ Vérification toutes les {intervalle_minutes} minutes")
        print("🛑 Ctrl+C pour arrêter")
        
        try:
            while True:
                rapport = self.verifier_etat_systeme()
                
                # Sauvegarder si état dégradé
                if rapport['etat'] != 'OPTIMAL':
                    self.sauvegarder_rapport_alerte(rapport)
                
                # Attendre avant prochaine vérification
                print(f"⏳ Prochaine vérification dans {intervalle_minutes} minutes...")
                time.sleep(intervalle_minutes * 60)
                
        except KeyboardInterrupt:
            print("\n🛑 Surveillance arrêtée")
    
    def sauvegarder_rapport_alerte(self, rapport):
        """Sauvegarde les rapports d'alerte"""
        nom_fichier = f"alerte_sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(nom_fichier, 'w', encoding='utf-8') as f:
                json.dump(rapport, f, indent=2, ensure_ascii=False)
            print(f"💾 Alerte sauvegardée: {nom_fichier}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde alerte: {e}")
    
    def generer_rapport_quotidien(self):
        """Génère un rapport quotidien"""
        print("\n📊 RAPPORT QUOTIDIEN DE SYNCHRONISATION")
        print("=" * 50)
        
        rapport = self.verifier_etat_systeme()
        
        # Statistiques détaillées
        print("\n📈 STATISTIQUES DÉTAILLÉES:")
        for key, value in rapport['statistiques'].items():
            print(f"   {key}: {value}")
        
        # Recommandations
        print("\n💡 RECOMMANDATIONS:")
        if rapport['statistiques']['taux_synchronisation'] == 100:
            print("   ✅ Synchronisation optimale - Maintenir la surveillance")
        else:
            print("   🔧 Exécuter le correcteur de synchronisation")
        
        print("   📅 Vérifier régulièrement l'intégrité des données")
        
        print("=" * 50)

# Interface utilisateur
def menu_principal():
    print("🎯 SYSTÈME DE SURVEILLANCE - SYNCHRONISATION")
    print("=" * 50)
    print("1. Vérification immédiate")
    print("2. Surveillance continue (5 min)")
    print("3. Rapport quotidien")
    print("4. Quitter")
    print("=" * 50)
    
    while True:
        choix = input("Choisir une option (1-4): ").strip()
        
        surveillant = SurveillantSimple()
        
        if choix == '1':
            surveillant.verifier_etat_systeme()
        elif choix == '2':
            surveillant.surveiller_en_continu(intervalle_minutes=5)
        elif choix == '3':
            surveillant.generer_rapport_quotidien()
        elif choix == '4':
            print("👋 Au revoir!")
            break
        else:
            print("❌ Option invalide")

if __name__ == "__main__":
    menu_principal()