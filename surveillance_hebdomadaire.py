#!/usr/bin/env python3
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
    print(f"\n📋 RAPPORT HEBDOMADAIRE - {datetime.now().strftime('%d/%m/%Y')}")
    print(f"📊 Synchronisation: {rapport['statistiques']['taux_synchronisation']:.1f}%")
    print(f"🚨 Alertes: {len(rapport['alertes'])}")
    print(f"💡 Recommandations: {len(rapport['recommandations'])}")
