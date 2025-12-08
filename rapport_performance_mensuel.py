#!/usr/bin/env python3
# rapport_performance_mensuel.py
import os
import sys
import django
import json
from datetime import datetime, timedelta
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from django.contrib.auth.models import User
from membres.models import Membre
from django.db import connection

print("📈 RAPPORT DE PERFORMANCE MENSUEL")
print("=" * 50)

class RapportPerformanceMensuel:
    def __init__(self):
        self.mois_courant = datetime.now().month
        self.annee_courante = datetime.now().year
        
    def generer_rapport(self):
        """Génère le rapport de performance mensuel"""
        rapport = {
            'periode': f"{self.mois_courant}/{self.annee_courante}",
            'timestamp': datetime.now().isoformat(),
            'performances': {},
            'evolution': {},
            'recommandations': []
        }
        
        # Analyse des performances
        rapport['performances'] = self.analyser_performances()
        
        # Évolution mensuelle
        rapport['evolution'] = self.analyser_evolution()
        
        # Recommandations
        rapport['recommandations'] = self.generer_recommandations(rapport)
        
        # Sauvegarder
        self.sauvegarder_rapport(rapport)
        
        return rapport
    
    def analyser_performances(self):
        """Analyse les performances du système"""
        performances = {}
        
        # Temps de réponse des requêtes
        start_time = datetime.now()
        User.objects.count()
        performances['temps_requete_users'] = (datetime.now() - start_time).total_seconds()
        
        start_time = datetime.now()
        Membre.objects.count()
        performances['temps_requete_membres'] = (datetime.now() - start_time).total_seconds()
        
        # Statistiques de base de données
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            performances['nombre_tables'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='index'")
            performances['nombre_indexes'] = cursor.fetchone()[0]
        
        return performances
    
    def analyser_evolution(self):
        """Analyse l'évolution sur le mois"""
        evolution = {}
        
        # Données du mois précédent pour comparaison
        mois_precedent = self.mois_courant - 1 if self.mois_courant > 1 else 12
        annee_precedente = self.annee_courante if self.mois_courant > 1 else self.annee_courante - 1
        
        # Calcul de l'évolution (simplifié)
        membres_actuels = Membre.objects.count()
        users_actuels = User.objects.count()
        
        evolution['membres'] = {
            'actuel': membres_actuels,
            'croissance': 'N/A'  # À compléter avec données historiques
        }
        
        evolution['utilisateurs'] = {
            'actuel': users_actuels,
            'croissance': 'N/A'
        }
        
        return evolution
    
    def generer_recommandations(self, rapport):
        """Génère des recommandations basées sur l'analyse"""
        recommandations = []
        perf = rapport['performances']
        
        if perf['temps_requete_membres'] > 0.5:
            recommandations.append("Optimiser les requêtes sur la table membres")
        
        if perf['temps_requete_users'] > 0.5:
            recommandations.append("Vérifier les indexes sur la table users")
        
        # Recommandations générales
        recommandations.extend([
            "Réviser la stratégie de sauvegarde",
            "Vérifier l'espace disque et la mémoire",
            "Planifier les mises à jour de sécurité"
        ])
        
        return recommandations
    
    def sauvegarder_rapport(self, rapport):
        """Sauvegarde le rapport mensuel"""
        nom_fichier = f"rapport_performance_{self.mois_courant:02d}_{self.annee_courante}.json"
        dossier = Path("rapports_performance")
        dossier.mkdir(exist_ok=True)
        
        with open(dossier / nom_fichier, 'w') as f:
            json.dump(rapport, f, indent=2)
        
        print(f"💾 Rapport sauvegardé: {dossier}/{nom_fichier}")

if __name__ == "__main__":
    rapporteur = RapportPerformanceMensuel()
    rapport = rapporteur.generer_rapport()
    
    print(f"📊 Performances du mois {rapport['periode']}:")
    print(f"   ⏱️  Temps requête membres: {rapport['performances']['temps_requete_membres']:.3f}s")
    print(f"   ⏱️  Temps requête users: {rapport['performances']['temps_requete_users']:.3f}s")
    print(f"   📊 Nombre de tables: {rapport['performances']['nombre_tables']}")
    print(f"   📈 Nombre d'indexes: {rapport['performances']['nombre_indexes']}")
    print(f"   💡 Recommandations: {len(rapport['recommandations'])}")
