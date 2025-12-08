# planificateur_surveillance.py
import os
import sys
import django
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

print("📅 PLANIFICATEUR DE SURVEILLANCE HEBDOMADAIRE")
print("=" * 60)

class PlanificateurSurveillance:
    def __init__(self):
        self.scripts = {
            'quotidien': 'surveillance_simple.py',
            'hebdomadaire': 'diagnostic_sync_final.py', 
            'mensuel': 'rapport_performance_mensuel.py',
            'correcteur': 'correcteur_sync_urgence.py'
        }
    
    def generer_planification_cron(self):
        """Génère les entrées cron pour la surveillance automatique"""
        print("🕐 Génération planification cron...")
        
        cron_entries = [
            "# ===========================================",
            "# SURVEILLANCE SYNCHRONISATION - MUTUELLE CORE",
            "# ===========================================",
            "",
            "# Surveillance quotidienne à 8h00",
            "0 8 * * * cd /Users/koffitanohsoualiho/Documents/P\ FINALE\ AVANT\ SYNCHRO/projet\ 21.49.30 && /Users/koffitanohsoualiho/Documents/P\ FINALE\ AVANT\ SYNCHRO/projet\ 21.49.30/venv/bin/python surveillance_simple.py --mode auto >> /tmp/surveillance_sync.log 2>&1",
            "",
            "# Diagnostic hebdomadaire le lundi à 9h00", 
            "0 9 * * 1 cd /Users/koffitanohsoualiho/Documents/P\ FINALE\ AVANT\ SYNCHRO/projet\ 21.49.30 && /Users/koffitanohsoualiho/Documents/P\ FINALE\ AVANT\ SYNCHRO/projet\ 21.49.30/venv/bin/python diagnostic_sync_final.py >> /tmp/diagnostic_hebdo.log 2>&1",
            "",
            "# Nettoyage des logs mensuel",
            "0 6 1 * * find /tmp -name \"*surveillance*\" -mtime +30 -delete",
            "",
            "# ==========================================="
        ]
        
        # Sauvegarder le fichier cron
        cron_file = "planification_surveillance.cron"
        with open(cron_file, 'w') as f:
            f.write('\n'.join(cron_entries))
        
        print(f"✅ Planification générée: {cron_file}")
        print("\n💡 Pour activer, exécutez:")
        print(f"   crontab {cron_file}")
        
        return cron_entries
    
    def creer_script_hebdomadaire(self):
        """Crée un script de surveillance hebdomadaire avancé"""
        script_content = '''#!/usr/bin/env python3
# surveillance_hebdomadaire.py
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
from django.db.models import Count, Q
from django.core.mail import send_mail
import smtplib

class SurveillanceHebdomadaire:
    def __init__(self):
        self.rapport = {
            'timestamp': datetime.now().isoformat(),
            'periode': 'hebdomadaire',
            'statistiques': {},
            'alertes': [],
            'tendances': [],
            'recommandations': []
        }
    
    def executer_surveillance_complete(self):
        """Exécute la surveillance hebdomadaire complète"""
        print("🔍 SURVEILLANCE HEBDOMADAIRE - LANCEMENT...")
        
        # 1. Statistiques de base
        self.collecter_statistiques()
        
        # 2. Vérifications critiques
        self.verifier_synchronisation()
        self.verifier_performances()
        self.analyser_tendances()
        
        # 3. Générer recommandations
        self.generer_recommandations()
        
        # 4. Sauvegarder et notifier
        self.sauvegarder_rapport()
        self.notifier_alertes()
        
        return self.rapport
    
    def collecter_statistiques(self):
        """Collecte les statistiques hebdomadaires"""
        print("📊 Collecte des statistiques...")
        
        total_users = User.objects.count()
        total_membres = Membre.objects.count()
        membres_avec_user = Membre.objects.filter(user__isnull=False).count()
        
        # Statistiques de la semaine
        date_debut_semaine = datetime.now() - timedelta(days=7)
        nouveaux_membres = Membre.objects.filter(
            date_inscription__gte=date_debut_semaine
        ).count()
        
        self.rapport['statistiques'] = {
            'utilisateurs_totaux': total_users,
            'membres_totaux': total_membres,
            'taux_synchronisation': (membres_avec_user / total_membres * 100) if total_membres > 0 else 0,
            'nouveaux_membres_semaine': nouveaux_membres,
            'date_debut_periode': date_debut_semaine.isoformat(),
            'date_fin_periode': datetime.now().isoformat()
        }
    
    def verifier_synchronisation(self):
        """Vérifie l'état de la synchronisation"""
        stats = self.rapport['statistiques']
        
        if stats['taux_synchronisation'] < 100:
            self.rapport['alertes'].append({
                'niveau': 'CRITIQUE',
                'message': f"Synchronisation à {stats['taux_synchronisation']:.1f}%",
                'action': 'Exécuter le correcteur de synchronisation'
            })
        
        # Vérifier l'intégrité des données
        try:
            doublons = Membre.objects.values('numero_unique').annotate(
                count=Count('id')
            ).filter(count__gt=1, numero_unique__isnull=False)
            
            if doublons.exists():
                self.rapport['alertes'].append({
                    'niveau': 'MOYEN',
                    'message': f"{doublons.count()} numéros uniques en double",
                    'action': 'Nettoyer les doublons'
                })
        except Exception as e:
            print(f"⚠️ Vérification doublons: {e}")
    
    def verifier_performances(self):
        """Vérifie les performances du système"""
        from django.db import connection
        
        try:
            with connection.cursor() as cursor:
                # Temps de réponse moyen
                start_time = datetime.now()
                Membre.objects.count()
                temps_reponse = (datetime.now() - start_time).total_seconds()
                
                if temps_reponse > 1.0:
                    self.rapport['alertes'].append({
                        'niveau': 'MOYEN', 
                        'message': f"Temps de réponse élevé: {temps_reponse:.2f}s",
                        'action': 'Optimiser les requêtes et indexes'
                    })
                
                self.rapport['statistiques']['temps_reponse_moyen'] = temps_reponse
                
        except Exception as e:
            print(f"⚠️ Vérification performances: {e}")
    
    def analyser_tendances(self):
        """Analyse les tendances sur la période"""
        date_debut = datetime.now() - timedelta(days=30)
        
        try:
            # Évolution du nombre de membres
            membres_par_semaine = []
            for i in range(4):
                date_fin = datetime.now() - timedelta(weeks=i)
                date_debut_periode = date_fin - timedelta(weeks=1)
                count = Membre.objects.filter(
                    date_inscription__range=[date_debut_periode, date_fin]
                ).count()
                membres_par_semaine.append(count)
            
            self.rapport['tendances'] = {
                'membres_4_dernieres_semaines': membres_par_semaine,
                'croissance_membres': sum(membres_par_semaine[1:]) - sum(membres_par_semaine[:-1])
            }
            
        except Exception as e:
            print(f"⚠️ Analyse tendances: {e}")
    
    def generer_recommandations(self):
        """Génère des recommandations basées sur l'analyse"""
        stats = self.rapport['statistiques']
        tendances = self.rapport['tendances']
        
        # Recommandations basées sur la croissance
        if stats['nouveaux_membres_semaine'] > 10:
            self.rapport['recommandations'].append(
                "Forte croissance détectée - Vérifier la capacité du système"
            )
        
        # Recommandations de performance
        if stats.get('temps_reponse_moyen', 0) > 0.5:
            self.rapport['recommandations'].append(
                "Optimiser les performances de la base de données"
            )
        
        # Maintenance préventive
        self.rapport['recommandations'].extend([
            "Sauvegarder la base de données",
            "Vérifier l'espace disque disponible",
            "Mettre à jour les dépendances si nécessaire"
        ])
    
    def sauvegarder_rapport(self):
        """Sauvegarde le rapport hebdomadaire"""
        nom_fichier = f"rapport_hebdomadaire_{datetime.now().strftime('%Y%m%d')}.json"
        
        try:
            with open(nom_fichier, 'w', encoding='utf-8') as f:
                json.dump(self.rapport, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Rapport sauvegardé: {nom_fichier}")
            
            # Sauvegarde dans un dossier dédié
            dossier_rapports = Path("rapports_surveillance")
            dossier_rapports.mkdir(exist_ok=True)
            Path(nom_fichier).rename(dossier_rapports / nom_fichier)
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
    
    def notifier_alertes(self):
        """Envoie des notifications pour les alertes critiques"""
        alertes_critiques = [a for a in self.rapport['alertes'] if a['niveau'] == 'CRITIQUE']
        
        if alertes_critiques:
            print("🚨 Alertes critiques détectées - Envoi de notification...")
            # Ici vous pouvez intégrer l'envoi d'email, Slack, etc.
            for alerte in alertes_critiques:
                print(f"   ⚠️ {alerte['message']}")
        
        print("✅ Surveillance hebdomadaire terminée")

if __name__ == "__main__":
    surveillant = SurveillanceHebdomadaire()
    rapport = surveillant.executer_surveillance_complete()
    
    # Afficher le résumé
    print(f"\\n📋 RAPPORT HEBDOMADAIRE - {datetime.now().strftime('%d/%m/%Y')}")
    print(f"📊 Synchronisation: {rapport['statistiques']['taux_synchronisation']:.1f}%")
    print(f"🚨 Alertes: {len(rapport['alertes'])}")
    print(f"💡 Recommandations: {len(rapport['recommandations'])}")
'''
        
        with open('surveillance_hebdomadaire.py', 'w') as f:
            f.write(script_content)
        
        print("✅ Script hebdomadaire créé: surveillance_hebdomadaire.py")
    
    def creer_script_performance_mensuel(self):
        """Crée un script de rapport de performance mensuel"""
        script_content = '''#!/usr/bin/env python3
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
'''
        
        with open('rapport_performance_mensuel.py', 'w') as f:
            f.write(script_content)
        
        print("✅ Script mensuel créé: rapport_performance_mensuel.py")
    
    def installer_planification(self):
        """Installe la planification automatique"""
        print("\n📅 INSTALLATION PLANIFICATION...")
        
        # Générer les fichiers
        self.generer_planification_cron()
        self.creer_script_hebdomadaire()
        self.creer_script_performance_mensuel()
        
        print("\n🎯 PLANIFICATION PRÊTE!")
        print("💡 Commandes d'installation:")
        print("   1. crontab planification_surveillance.cron")
        print("   2. chmod +x surveillance_hebdomadaire.py")
        print("   3. chmod +x rapport_performance_mensuel.py")
        
        return True

# Exécution
if __name__ == "__main__":
    planificateur = PlanificateurSurveillance()
    planificateur.installer_planification()