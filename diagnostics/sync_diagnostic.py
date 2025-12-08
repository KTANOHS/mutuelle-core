# diagnostics/sync_diagnostic.py
import os
import sys
import django
import json
from datetime import datetime, timedelta
from collections import defaultdict, Counter

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db import models, connection
from django.db.models import Count, Q, F, ExpressionWrapper, DurationField
from django.contrib.auth.models import User
from membres.models import Membre, Paiement, Cotisation
from agents.models import Agent
from medecin.models import BonSoin, Ordonnance, Consultation
from communication.models import Notification
import logging

logger = logging.getLogger(__name__)

class DiagnosticSynchronisation:
    """
    Script complet de diagnostic des problèmes de synchronisation des données
    """
    
    def __init__(self):
        self.resultats = {
            'timestamp': datetime.now().isoformat(),
            'statistiques': {},
            'problemes': [],
            'recommandations': [],
            'performance': {}
        }
    
    def executer_diagnostic_complet(self):
        """Exécute tous les diagnostics"""
        print("🔍 LANCEMENT DU DIAGNOSTIC DE SYNCHRONISATION...")
        
        try:
            # 1. Diagnostic de base de données
            self.diagnostic_base_donnees()
            
            # 2. Diagnostic d'intégrité des données
            self.diagnostic_integrite_donnees()
            
            # 3. Diagnostic de performance
            self.diagnostic_performance()
            
            # 4. Diagnostic de cohérence métier
            self.diagnostic_coherence_metier()
            
            # 5. Diagnostic des relations
            self.diagnostic_relations()
            
            # 6. Génération du rapport
            self.generer_rapport()
            
            print("✅ DIAGNOSTIC TERMINÉ AVEC SUCCÈS")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du diagnostic: {str(e)}")
            self.resultats['erreur'] = str(e)
    
    def diagnostic_base_donnees(self):
        """Diagnostic de l'état de la base de données"""
        print("📊 Analyse de la base de données...")
        
        with connection.cursor() as cursor:
            # Taille de la base de données
            cursor.execute("""
                SELECT pg_size_pretty(pg_database_size(current_database()))
            """)
            taille_bdd = cursor.fetchone()[0]
            
            # Nombre de tables
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            nb_tables = cursor.fetchone()[0]
        
        # Statistiques par modèle
        model_stats = {}
        models_apps = [
            (Membre, 'membres'),
            (User, 'auth'),
            (Paiement, 'membres'), 
            (Cotisation, 'membres'),
            (Agent, 'agents'),
            (BonSoin, 'medecin'),
            (Ordonnance, 'medecin'),
            (Consultation, 'medecin'),
            (Notification, 'communication')
        ]
        
        for modele, app in models_apps:
            try:
                count = modele.objects.count()
                model_stats[f"{modele.__name__} ({app})"] = count
            except Exception as e:
                model_stats[f"{modele.__name__} ({app})"] = f"ERREUR: {str(e)}"
        
        self.resultats['statistiques'].update({
            'taille_base_donnees': taille_bdd,
            'nombre_tables': nb_tables,
            'nombre_par_modele': model_stats
        })
    
    def diagnostic_integrite_donnees(self):
        """Vérification de l'intégrité des données"""
        print("🔎 Vérification de l'intégrité des données...")
        
        problemes = []
        
        # 1. Membres sans utilisateur associé
        try:
            membres_sans_user = Membre.objects.filter(user__isnull=True)
            if membres_sans_user.exists():
                problemes.append({
                    'type': 'INTÉGRITÉ RELATIONNELLE',
                    'description': f'{membres_sans_user.count()} membres sans utilisateur associé',
                    'severite': 'HAUTE',
                    'correction': 'Supprimer ou associer ces membres à un utilisateur'
                })
        except Exception as e:
            problemes.append({
                'type': 'ERREUR VÉRIFICATION',
                'description': f'Erreur vérification membres sans user: {str(e)}',
                'severite': 'MOYENNE'
            })
        
        # 2. Doublons potentiels
        try:
            # Membres avec même numéro
            doublons_numero = Membre.objects.values('numero_membre').annotate(
                count=Count('id')
            ).filter(count__gt=1)
            
            if doublons_numero.exists():
                problemes.append({
                    'type': 'DOUBLONS',
                    'description': f'{doublons_numero.count()} numéros de membre en double',
                    'severite': 'HAUTE',
                    'correction': 'Fusionner ou corriger les doublons'
                })
        except Exception as e:
            problemes.append({
                'type': 'ERREUR VÉRIFICATION',
                'description': f'Erreur vérification doublons: {str(e)}',
                'severite': 'MOYENNE'
            })
        
        # 3. Données obligatoires manquantes
        try:
            membres_sans_numero = Membre.objects.filter(
                Q(numero_membre__isnull=True) | Q(numero_membre='')
            )
            if membres_sans_numero.exists():
                problemes.append({
                    'type': 'DONNÉES MANQUANTES',
                    'description': f'{membres_sans_numero.count()} membres sans numéro',
                    'severite': 'HAUTE',
                    'correction': 'Générer des numéros pour ces membres'
                })
        except Exception as e:
            problemes.append({
                'type': 'ERREUR VÉRIFICATION', 
                'description': f'Erreur vérification données manquantes: {str(e)}',
                'severite': 'MOYENNE'
            })
        
        self.resultats['problemes'].extend(problemes)
    
    def diagnostic_performance(self):
        """Diagnostic des performances et indexation"""
        print("⚡ Analyse des performances...")
        
        with connection.cursor() as cursor:
            # Index manquants
            cursor.execute("""
                SELECT schemaname, tablename, indexname, indexdef
                FROM pg_indexes 
                WHERE schemaname = 'public'
                ORDER BY tablename, indexname
            """)
            indexes = cursor.fetchall()
            
            # Tables sans index (potentiellement problématiques)
            cursor.execute("""
                SELECT schemaname, tablename
                FROM pg_tables 
                WHERE schemaname = 'public'
                AND tablename NOT IN (
                    SELECT DISTINCT tablename 
                    FROM pg_indexes 
                    WHERE schemaname = 'public'
                )
            """)
            tables_sans_index = cursor.fetchall()
        
        performance_data = {
            'nombre_index_total': len(indexes),
            'tables_sans_index': [f"{table[0]}.{table[1]}" for table in tables_sans_index],
            'indexes_existants': [f"{idx[1]}.{idx[2]}" for idx in indexes[:10]]  # Premiers 10
        }
        
        # Vérification des requêtes lentes potentielles
        if tables_sans_index:
            self.resultats['problemes'].append({
                'type': 'PERFORMANCE',
                'description': f'{len(tables_sans_index)} tables sans index',
                'severite': 'MOYENNE',
                'correction': 'Ajouter des indexes sur les colonnes fréquemment interrogées'
            })
        
        self.resultats['performance'] = performance_data
    
    def diagnostic_coherence_metier(self):
        """Vérification de la cohérence métier"""
        print("🏥 Vérification de la cohérence métier...")
        
        problemes = []
        
        # 1. Cotisations en retard
        try:
            aujourd_hui = datetime.now().date()
            cotisations_en_retard = Cotisation.objects.filter(
                date_echeance__lt=aujourd_hui,
                statut__in=['EN_ATTENTE', 'IMPAYEE']
            )
            
            if cotisations_en_retard.exists():
                problemes.append({
                    'type': 'COHÉRENCE MÉTIER',
                    'description': f'{cotisations_en_retard.count()} cotisations en retard',
                    'severite': 'MOYENNE',
                    'correction': 'Relancer les membres concernés'
                })
        except Exception as e:
            problemes.append({
                'type': 'ERREUR VÉRIFICATION',
                'description': f'Erreur vérification cotisations: {str(e)}',
                'severite': 'MOYENNE'
            })
        
        # 2. Bons de soin sans ordonnance
        try:
            bons_sans_ordonnance = BonSoin.objects.filter(ordonnance__isnull=True)
            if bons_sans_ordonnance.exists():
                problemes.append({
                    'type': 'COHÉRENCE MÉTIER',
                    'description': f'{bons_sans_ordonnance.count()} bons de soin sans ordonnance',
                    'severite': 'HAUTE',
                    'correction': 'Associer ces bons à des ordonnances ou les archiver'
                })
        except Exception as e:
            problemes.append({
                'type': 'ERREUR VÉRIFICATION',
                'description': f'Erreur vérification bons de soin: {str(e)}',
                'severite': 'MOYENNE'
            })
        
        # 3. Incohérences de dates
        try:
            # Membres créés après leur dernière cotisation
            incoh_dates = Membre.objects.filter(
                date_inscription__gt=models.Subquery(
                    Cotisation.objects.filter(
                        membre=models.OuterRef('pk')
                    ).order_by('-date_paiement').values('date_paiement')[:1]
                )
            )
            
            if incoh_dates.exists():
                problemes.append({
                    'type': 'INCOHÉRENCE TEMPORELLE', 
                    'description': f'{incoh_dates.count()} membres avec dates incohérentes',
                    'severite': 'MOYENNE',
                    'correction': 'Vérifier les dates d\'inscription et de paiement'
                })
        except Exception as e:
            # Cette vérification peut échouer selon la structure
            pass
        
        self.resultats['problemes'].extend(problemes)
    
    def diagnostic_relations(self):
        """Diagnostic des relations entre modèles"""
        print("🔗 Analyse des relations entre modèles...")
        
        problemes = []
        
        # 1. Relations circulaires potentielles
        try:
            # Membres sans région
            membres_sans_region = Membre.objects.filter(region__isnull=True)
            if membres_sans_region.exists():
                problemes.append({
                    'type': 'RELATION MANQUANTE',
                    'description': f'{membres_sans_region.count()} membres sans région assignée',
                    'severite': 'MOYENNE',
                    'correction': 'Assigner une région à ces membres'
                })
        except Exception as e:
            problemes.append({
                'type': 'ERREUR VÉRIFICATION',
                'description': f'Erreur vérification relations: {str(e)}',
                'severite': 'MOYENNE'
            })
        
        # 2. Ordonnances sans médecin
        try:
            ordonnances_sans_medecin = Ordonnance.objects.filter(medecin__isnull=True)
            if ordonnances_sans_medecin.exists():
                problemes.append({
                    'type': 'RELATION MANQUANTE',
                    'description': f'{ordonnances_sans_medecin.count()} ordonnances sans médecin',
                    'severite': 'HAUTE', 
                    'correction': 'Associer ces ordonnances à un médecin'
                })
        except Exception as e:
            problemes.append({
                'type': 'ERREUR VÉRIFICATION',
                'description': f'Erreur vérification ordonnances: {str(e)}',
                'severite': 'MOYENNE'
            })
        
        self.resultats['problemes'].extend(problemes)
    
    def generer_rapport(self):
        """Génère un rapport complet du diagnostic"""
        print("📄 Génération du rapport...")
        
        # Statistiques résumées
        total_problemes = len(self.resultats['problemes'])
        problemes_haute = len([p for p in self.resultats['problemes'] if p['severite'] == 'HAUTE'])
        problemes_moyenne = len([p for p in self.resultats['problemes'] if p['severite'] == 'MOYENNE'])
        
        # Résumé exécutif
        resume = {
            'date_execution': self.resultats['timestamp'],
            'total_problemes': total_problemes,
            'problemes_haute_priorite': problemes_haute,
            'problemes_moyenne_priorite': problemes_moyenne,
            'etat_general': 'BON' if total_problemes == 0 else 'ATTENTION REQUISE'
        }
        
        self.resultats['resume_executif'] = resume
        
        # Génération des recommandations
        self._generer_recommandations()
        
        # Sauvegarde du rapport
        self._sauvegarder_rapport()
        
        # Affichage du résumé
        self._afficher_resume()
    
    def _generer_recommandations(self):
        """Génère des recommandations basées sur les problèmes identifiés"""
        recommandations = []
        
        problemes_par_type = defaultdict(list)
        for probleme in self.resultats['problemes']:
            problemes_par_type[probleme['type']].append(probleme)
        
        # Recommandations spécifiques par type de problème
        if 'INTÉGRITÉ RELATIONNELLE' in problemes_par_type:
            recommandations.append({
                'priorite': 'HAUTE',
                'action': 'Nettoyer les relations brisées',
                'description': 'Supprimer ou corriger les enregistrements sans relations valides'
            })
        
        if 'DOUBLONS' in problemes_par_type:
            recommandations.append({
                'priorite': 'HAUTE', 
                'action': 'Éliminer les doublons',
                'description': 'Exécuter un script de déduplication des membres'
            })
        
        if 'PERFORMANCE' in problemes_par_type:
            recommandations.append({
                'priorite': 'MOYENNE',
                'action': 'Optimiser les indexes',
                'description': 'Ajouter des indexes sur les tables sans index et colonnes fréquemment interrogées'
            })
        
        # Recommandations générales
        if self.resultats['statistiques']['nombre_par_modele'].get('Membre (membres)', 0) > 1000:
            recommandations.append({
                'priorite': 'MOYENNE',
                'action': 'Implémenter la pagination',
                'description': 'Ajouter la pagination sur les listes de membres pour améliorer les performances'
            })
        
        self.resultats['recommandations'] = recommandations
    
    def _sauvegarder_rapport(self):
        """Sauvegarde le rapport dans un fichier JSON"""
        nom_fichier = f"diagnostic_sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(nom_fichier, 'w', encoding='utf-8') as f:
            json.dump(self.resultats, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Rapport sauvegardé: {nom_fichier}")
    
    def _afficher_resume(self):
        """Affiche un résumé du diagnostic dans la console"""
        resume = self.resultats['resume_executif']
        problemes_haute = [p for p in self.resultats['problemes'] if p['severite'] == 'HAUTE']
        
        print("\n" + "="*60)
        print("📋 RAPPORT DE DIAGNOSTIC - SYNCHRONISATION DONNÉES")
        print("="*60)
        print(f"📅 Date d'exécution: {resume['date_execution']}")
        print(f"🏷️  État général: {resume['etat_general']}")
        print(f"❌ Problèmes totaux: {resume['total_problemes']}")
        print(f"🔴 Problèmes haute priorité: {resume['problemes_haute_priorite']}")
        print(f"🟡 Problèmes moyenne priorité: {resume['problemes_moyenne_priorite']}")
        
        if problemes_haute:
            print("\n🔴 PROBLÈMES HAUTE PRIORITÉ:")
            for probleme in problemes_haute:
                print(f"   • {probleme['description']}")
        
        if self.resultats['recommandations']:
            print("\n💡 RECOMMANDATIONS:")
            for reco in sorted(self.resultats['recommandations'], key=lambda x: x['priorite'], reverse=True):
                print(f"   [{reco['priorite']}] {reco['action']}: {reco['description']}")
        
        print("="*60)

# Script d'exécution
if __name__ == "__main__":
    diagnostic = DiagnosticSynchronisation()
    diagnostic.executer_diagnostic_complet()