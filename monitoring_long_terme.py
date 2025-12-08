# monitoring_long_terme.py
import os
import sys
import django
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from django.contrib.auth.models import User
from membres.models import Membre
from django.db import connection

print("📊 MONITORING LONG TERME - ANALYSE HISTORIQUE")
print("=" * 60)

class MonitoringLongTerme:
    def __init__(self):
        self.dossier_donnees = Path("donnees_monitoring")
        self.dossier_donnees.mkdir(exist_ok=True)
    
    def collecter_metriques_quotidiennes(self):
        """Collecte les métriques quotidiennes pour l'historique"""
        print("📈 Collecte des métriques quotidiennes...")
        
        metriques = {
            'date': datetime.now().isoformat(),
            'utilisateurs': User.objects.count(),
            'membres': Membre.objects.count(),
            'membres_avec_user': Membre.objects.filter(user__isnull=False).count(),
            'taux_synchronisation': 0
        }
        
        if metriques['membres'] > 0:
            metriques['taux_synchronisation'] = (
                metriques['membres_avec_user'] / metriques['membres'] * 100
            )
        
        # Performance
        start_time = datetime.now()
        Membre.objects.first()
        metriques['temps_requete'] = (datetime.now() - start_time).total_seconds()
        
        # Sauvegarder
        self._sauvegarder_metriques(metriques)
        
        return metriques
    
    def _sauvegarder_metriques(self, metriques):
        """Sauvegarde les métriques dans un fichier JSON"""
        date_str = datetime.now().strftime('%Y%m%d')
        fichier_metriques = self.dossier_donnees / f"metriques_{date_str}.json"
        
        # Charger les métriques existantes
        metriques_existantes = []
        if fichier_metriques.exists():
            with open(fichier_metriques, 'r') as f:
                metriques_existantes = json.load(f)
        
        # Ajouter la nouvelle métrique
        metriques_existantes.append(metriques)
        
        # Sauvegarder
        with open(fichier_metriques, 'w') as f:
            json.dump(metriques_existantes, f, indent=2)
    
    def analyser_tendances_historiques(self, jours=30):
        """Analyse les tendances sur une période donnée"""
        print(f"📊 Analyse des tendances sur {jours} jours...")
        
        date_debut = datetime.now() - timedelta(days=jours)
        tendances = {
            'periode': f"{jours} jours",
            'date_debut': date_debut.isoformat(),
            'date_fin': datetime.now().isoformat(),
            'analyse': {}
        }
        
        # Collecter toutes les métriques de la période
        toutes_metriques = []
        for i in range(jours):
            date = datetime.now() - timedelta(days=i)
            fichier = self.dossier_donnees / f"metriques_{date.strftime('%Y%m%d')}.json"
            if fichier.exists():
                with open(fichier, 'r') as f:
                    toutes_metriques.extend(json.load(f))
        
        if not toutes_metriques:
            print("⚠️ Aucune donnée historique trouvée")
            return tendances
        
        # Analyser les tendances
        tendances['analyse'] = {
            'moyenne_synchronisation': self._calculer_moyenne(toutes_metriques, 'taux_synchronisation'),
            'croissance_membres': self._calculer_croissance(toutes_metriques, 'membres'),
            'performance_moyenne': self._calculer_moyenne(toutes_metriques, 'temps_requete'),
            'nombre_points_donnees': len(toutes_metriques)
        }
        
        # Détecter les anomalies
        tendances['anomalies'] = self._detecter_anomalies(toutes_metriques)
        
        return tendances
    
    def _calculer_moyenne(self, metriques, champ):
        """Calcule la moyenne d'un champ dans les métriques"""
        valeurs = [m.get(champ, 0) for m in metriques if m.get(champ) is not None]
        return sum(valeurs) / len(valeurs) if valeurs else 0
    
    def _calculer_croissance(self, metriques, champ):
        """Calcule la croissance sur la période"""
        if len(metriques) < 2:
            return 0
        
        valeur_initiale = metriques[-1].get(champ, 0)
        valeur_finale = metriques[0].get(champ, 0)
        
        if valeur_initiale == 0:
            return 0
        
        return ((valeur_finale - valeur_initiale) / valeur_initiale) * 100
    
    def _detecter_anomalies(self, metriques):
        """Détecte les anomalies dans les métriques"""
        anomalies = []
        
        # Détecter les baisses de synchronisation
        for i, metrique in enumerate(metriques):
            if metrique.get('taux_synchronisation', 100) < 95:
                anomalies.append({
                    'date': metrique['date'],
                    'type': 'SYNCHRONISATION',
                    'valeur': metrique['taux_synchronisation'],
                    'seuil': 95
                })
        
        return anomalies
    
    def generer_rapport_long_terme(self):
        """Génère un rapport complet de monitoring long terme"""
        print("📋 Génération rapport long terme...")
        
        # Collecter métriques actuelles
        metriques_actuelles = self.collecter_metriques_quotidiennes()
        
        # Analyser tendances
        tendances_30j = self.analyser_tendances_historiques(30)
        tendances_90j = self.analyser_tendances_historiques(90)
        
        rapport = {
            'timestamp': datetime.now().isoformat(),
            'metriques_actuelles': metriques_actuelles,
            'tendances_30_jours': tendances_30j,
            'tendances_90_jours': tendances_90j,
            'recommandations_strategiques': self._generer_recommandations_strategiques(
                metriques_actuelles, tendances_30j, tendances_90j
            )
        }
        
        # Sauvegarder le rapport
        nom_fichier = f"rapport_long_terme_{datetime.now().strftime('%Y%m')}.json"
        with open(self.dossier_donnees / nom_fichier, 'w') as f:
            json.dump(rapport, f, indent=2)
        
        print(f"💾 Rapport long terme sauvegardé: {nom_fichier}")
        return rapport
    
    def _generer_recommandations_strategiques(self, metriques, tendances_30j, tendances_90j):
        """Génère des recommandations stratégiques basées sur l'analyse long terme"""
        recommandations = []
        
        # Analyse de la croissance
        croissance_30j = tendances_30j['analyse'].get('croissance_membres', 0)
        croissance_90j = tendances_90j['analyse'].get('croissance_membres', 0)
        
        if croissance_30j > 20:
            recommandations.append(
                "Forte croissance détectée - Prévoir l'augmentation des ressources"
            )
        
        if croissance_90j < 5:
            recommandations.append(
                "Croissance ralentie - Évaluer la stratégie d'acquisition"
            )
        
        # Analyse des performances
        perf_moyenne = tendances_30j['analyse'].get('performance_moyenne', 0)
        if perf_moyenne > 1.0:
            recommandations.append(
                "Performances dégradées - Audit complet des requêtes et indexes requis"
            )
        
        # Recommandations générales
        recommandations.extend([
            "Maintenir la surveillance quotidienne",
            "Réviser trimestriellement la stratégie de données",
            "Planifier les évolutions d'infrastructure annuellement"
        ])
        
        return recommandations

# Interface utilisateur
def menu_monitoring():
    print("\\n📊 MENU MONITORING LONG TERME")
    print("1. Collecter métriques quotidiennes")
    print("2. Analyser tendances 30 jours")
    print("3. Analyser tendances 90 jours") 
    print("4. Rapport long terme complet")
    print("5. Quitter")
    
    moniteur = MonitoringLongTerme()
    
    while True:
        choix = input("\\nChoisir une option (1-5): ").strip()
        
        if choix == '1':
            metriques = moniteur.collecter_metriques_quotidiennes()
            print(f"✅ Métriques collectées: {metriques['date']}")
            
        elif choix == '2':
            tendances = moniteur.analyser_tendances_historiques(30)
            print(f"📈 Tendances 30j: {tendances['analyse']}")
            
        elif choix == '3':
            tendances = moniteur.analyser_tendances_historiques(90)
            print(f"📈 Tendances 90j: {tendances['analyse']}")
            
        elif choix == '4':
            rapport = moniteur.generer_rapport_long_terme()
            print("✅ Rapport long terme généré")
            
        elif choix == '5':
            print("👋 Au revoir!")
            break
            
        else:
            print("❌ Option invalide")

if __name__ == "__main__":
    menu_monitoring()