# diagnostic_cotisations_assureur_agent.py
import os
import sys
import django
import json
from datetime import datetime, timedelta
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from django.db import connection
from django.db.models import Q, Count, F
from django.contrib.auth.models import User

print("🔍 DIAGNOSTIC COTISATIONS ASSUREUR → AGENT")
print("=" * 60)

class DiagnosticCotisations:
    def __init__(self):
        self.rapport = {
            'timestamp': datetime.now().isoformat(),
            'analyse': {},
            'problemes': [],
            'recommandations': [],
            'trace_cotisations': []
        }
    
    def executer_diagnostic_complet(self):
        """Exécute le diagnostic complet du flux cotisations"""
        print("🎯 DIAGNOSTIC FLUX COTISATIONS ASSUREUR-AGENT...")
        
        try:
            # 1. Analyse des modèles et relations
            self.analyser_structure_cotisations()
            
            # 2. Diagnostic du flux de données
            self.diagnostiquer_flux_cotisations()
            
            # 3. Vérification de la synchronisation
            self.verifier_synchronisation_assureur_agent()
            
            # 4. Analyse des problèmes courants
            self.analyser_problemes_courants()
            
            # 5. Générer le rapport
            self.generer_rapport_detaille()
            
            print("✅ DIAGNOSTIC TERMINÉ AVEC SUCCÈS")
            
        except Exception as e:
            print(f"❌ Erreur lors du diagnostic: {str(e)}")
            self.rapport['erreur'] = str(e)
    
    def analyser_structure_cotisations(self):
        """Analyse la structure des modèles de cotisations"""
        print("\n1. 🏗️  ANALYSE STRUCTURE COTISATIONS...")
        
        try:
            # Import des modèles avec gestion d'erreur
            try:
                from membres.models import Membre, Cotisation
                self.rapport['analyse']['modeles'] = {
                    'Membre': '✅ Disponible',
                    'Cotisation': '✅ Disponible'
                }
                print("   ✅ Modèles Membre et Cotisation importés")
            except ImportError as e:
                self.rapport['analyse']['modeles'] = {'erreur': str(e)}
                print(f"   ❌ Erreur import modèles: {e}")
                return
            
            try:
                from assureur.models import Assureur, PaiementAssureur
                self.rapport['analyse']['modeles']['Assureur'] = '✅ Disponible'
                self.rapport['analyse']['modeles']['PaiementAssureur'] = '✅ Disponible'
                print("   ✅ Modèles Assureur importés")
            except ImportError as e:
                self.rapport['analyse']['modeles']['Assureur'] = f'❌ {e}'
                print(f"   ⚠️  Modèles Assureur: {e}")
            
            try:
                from agents.models import Agent, VerificationCotisation
                self.rapport['analyse']['modeles']['Agent'] = '✅ Disponible'
                self.rapport['analyse']['modeles']['VerificationCotisation'] = '✅ Disponible'
                print("   ✅ Modèles Agent importés")
            except ImportError as e:
                self.rapport['analyse']['modeles']['Agent'] = f'❌ {e}'
                print(f"   ⚠️  Modèles Agent: {e}")
            
            # Analyser les relations
            self.analyser_relations_modeles()
            
        except Exception as e:
            print(f"   ❌ Erreur analyse structure: {e}")
    
    def analyser_relations_modeles(self):
        """Analyse les relations entre les modèles"""
        print("   🔗 Analyse des relations...")
        
        relations = {}
        
        try:
            from membres.models import Membre
            from django.db import models
            
            # Analyser les champs du modèle Membre
            membre_fields = []
            for field in Membre._meta.get_fields():
                if hasattr(field, 'name'):
                    relation_info = {
                        'name': field.name,
                        'type': field.get_internal_type(),
                        'related_model': getattr(field, 'related_model', None)
                    }
                    membre_fields.append(relation_info)
                    
                    if 'cotisation' in field.name.lower():
                        relations['membre_cotisation'] = field.name
            
            self.rapport['analyse']['champs_membre'] = membre_fields
            
            # Chercher spécifiquement les relations de cotisation
            for field in membre_fields:
                if 'cotisation' in field['name'].lower():
                    print(f"   ✅ Relation cotisation trouvée: {field['name']}")
            
        except Exception as e:
            print(f"   ⚠️  Analyse relations: {e}")
    
    def diagnostiquer_flux_cotisations(self):
        """Diagnostique le flux complet des cotisations"""
        print("\n2. 🔄 DIAGNOSTIC FLUX COTISATIONS...")
        
        try:
            # Compter les entités
            stats = {}
            
            from membres.models import Membre
            stats['membres'] = Membre.objects.count()
            print(f"   👤 Membres: {stats['membres']}")
            
            # Chercher les cotisations
            try:
                from membres.models import Cotisation
                stats['cotisations'] = Cotisation.objects.count()
                print(f"   💰 Cotisations: {stats['cotisations']}")
                
                # Analyser les statuts des cotisations
                if stats['cotisations'] > 0:
                    statuts = Cotisation.objects.values('statut').annotate(
                        count=Count('id')
                    )
                    print(f"   📊 Statuts cotisations:")
                    for statut in statuts:
                        print(f"      • {statut['statut']}: {statut['count']}")
                    
                    self.rapport['analyse']['statuts_cotisations'] = list(statuts)
            except Exception as e:
                print(f"   ⚠️  Analyse cotisations: {e}")
                stats['cotisations'] = 0
            
            # Chercher les assureurs
            try:
                from assureur.models import Assureur
                stats['assureurs'] = Assureur.objects.count()
                print(f"   🏢 Assureurs: {stats['assureurs']}")
            except Exception as e:
                print(f"   ⚠️  Analyse assureurs: {e}")
                stats['assureurs'] = 0
            
            # Chercher les vérifications
            try:
                from agents.models import VerificationCotisation
                stats['verifications'] = VerificationCotisation.objects.count()
                print(f"   🔍 Vérifications: {stats['verifications']}")
                
                if stats['verifications'] > 0:
                    verif_statuts = VerificationCotisation.objects.values('statut').annotate(
                        count=Count('id')
                    )
                    print(f"   📊 Statuts vérifications:")
                    for statut in verif_statuts:
                        print(f"      • {statut['statut']}: {statut['count']}")
                    
                    self.rapport['analyse']['statuts_verifications'] = list(verif_statuts)
            except Exception as e:
                print(f"   ⚠️  Analyse vérifications: {e}")
                stats['verifications'] = 0
            
            self.rapport['analyse']['statistiques'] = stats
            
            # Tracer le flux
            self.tracer_flux_cotisations()
            
        except Exception as e:
            print(f"   ❌ Erreur diagnostic flux: {e}")
    
    def tracer_flux_cotisations(self):
        """Trace le flux complet des cotisations"""
        print("   📈 Tracé du flux cotisations...")
        
        try:
            # Essayer de trouver des données de test
            from membres.models import Membre
            
            # Prendre quelques membres pour tracer
            membres_echantillon = Membre.objects.all()[:3]
            
            for membre in membres_echantillon:
                trace = {
                    'membre_id': membre.id,
                    'membre_numero': getattr(membre, 'numero_unique', 'N/A'),
                    'cotisations': [],
                    'verifications': []
                }
                
                # Chercher les cotisations du membre
                try:
                    from membres.models import Cotisation
                    cotisations = Cotisation.objects.filter(membre=membre)
                    for cotisation in cotisations:
                        trace['cotisations'].append({
                            'id': cotisation.id,
                            'montant': getattr(cotisation, 'montant', 'N/A'),
                            'statut': getattr(cotisation, 'statut', 'N/A'),
                            'date': getattr(cotisation, 'date_paiement', 'N/A')
                        })
                except Exception as e:
                    trace['cotisations'] = f'Erreur: {e}'
                
                # Chercher les vérifications
                try:
                    from agents.models import VerificationCotisation
                    verifications = VerificationCotisation.objects.filter(membre=membre)
                    for verification in verifications:
                        trace['verifications'].append({
                            'id': verification.id,
                            'statut': getattr(verification, 'statut', 'N/A'),
                            'date': getattr(verification, 'date_verification', 'N/A'),
                            'agent': getattr(verification, 'agent_id', 'N/A')
                        })
                except Exception as e:
                    trace['verifications'] = f'Erreur: {e}'
                
                self.rapport['trace_cotisations'].append(trace)
            
            print(f"   ✅ Flux tracé pour {len(self.rapport['trace_cotisations'])} membres")
            
        except Exception as e:
            print(f"   ⚠️  Tracé flux: {e}")
    
    def verifier_synchronisation_assureur_agent(self):
        """Vérifie la synchronisation entre assureurs et agents"""
        print("\n3. 🔄 VÉRIFICATION SYNCHRONISATION ASSUREUR-AGENT...")
        
        try:
            # Vérifier la cohérence des données
            problemes = []
            
            # 1. Vérifier si les membres ont des cotisations mais pas de vérifications
            try:
                from membres.models import Membre, Cotisation
                from agents.models import VerificationCotisation
                
                membres_avec_cotisations = Membre.objects.filter(
                    cotisation__isnull=False
                ).distinct()
                
                membres_sans_verification = membres_avec_cotisations.exclude(
                    verificationcotisation__isnull=False
                )
                
                if membres_sans_verification.exists():
                    probleme = {
                        'type': 'SYNCHRONISATION',
                        'description': f'{membres_sans_verification.count()} membres avec cotisations mais sans vérification agent',
                        'severite': 'MOYENNE'
                    }
                    problemes.append(probleme)
                    print(f"   ⚠️  {probleme['description']}")
                else:
                    print("   ✅ Tous les membres avec cotisations ont des vérifications")
                    
            except Exception as e:
                print(f"   ⚠️  Vérification synchronisation: {e}")
            
            # 2. Vérifier les incohérences de statuts
            try:
                from membres.models import Cotisation
                from agents.models import VerificationCotisation
                
                # Cotisations payées mais non vérifiées
                cotisations_payees_non_verifiees = Cotisation.objects.filter(
                    statut='PAYEE'
                ).exclude(
                    membre__verificationcotisation__statut='VALIDE'
                )
                
                if cotisations_payees_non_verifiees.exists():
                    probleme = {
                        'type': 'STATUT_INCOHERENT',
                        'description': f'{cotisations_payees_non_verifiees.count()} cotisations payées mais non vérifiées valides',
                        'severite': 'MOYENNE'
                    }
                    problemes.append(probleme)
                    print(f"   ⚠️  {probleme['description']}")
                    
            except Exception as e:
                print(f"   ⚠️  Vérification statuts: {e}")
            
            # 3. Vérifier les délais de synchronisation
            try:
                from membres.models import Cotisation
                from agents.models import VerificationCotisation
                
                # Cotisations récentes sans vérification
                date_limite = datetime.now() - timedelta(days=2)
                cotisations_recentes_sans_verif = Cotisation.objects.filter(
                    date_paiement__gte=date_limite
                ).exclude(
                    membre__verificationcotisation__isnull=False
                )
                
                if cotisations_recentes_sans_verif.exists():
                    probleme = {
                        'type': 'DELAI_SYNCHRO',
                        'description': f'{cotisations_recentes_sans_verif.count()} cotisations récentes sans vérification (>48h)',
                        'severite': 'BASSE'
                    }
                    problemes.append(probleme)
                    print(f"   ⚠️  {probleme['description']}")
                    
            except Exception as e:
                print(f"   ⚠️  Vérification délais: {e}")
            
            self.rapport['problemes'].extend(problemes)
            
        except Exception as e:
            print(f"   ❌ Erreur vérification synchronisation: {e}")
    
    def analyser_problemes_courants(self):
        """Analyse les problèmes courants dans le flux cotisations"""
        print("\n4. 🚨 ANALYSE PROBLÈMES COURANTS...")
        
        problemes = []
        
        try:
            # Vérifier l'accès aux modèles
            from django.apps import apps
            
            # Vérifier si les modèles nécessaires existent
            modeles_requis = ['membres.Membre', 'membres.Cotisation', 'agents.VerificationCotisation']
            modeles_manquants = []
            
            for modele in modeles_requis:
                try:
                    apps.get_model(modele)
                except LookupError:
                    modeles_manquants.append(modele)
            
            if modeles_manquants:
                probleme = {
                    'type': 'MODELE_MANQUANT',
                    'description': f'Modèles non trouvés: {", ".join(modeles_manquants)}',
                    'severite': 'HAUTE'
                }
                problemes.append(probleme)
                print(f"   ❌ {probleme['description']}")
            
            # Vérifier la configuration des URLs
            try:
                from django.urls import get_resolver
                urls = get_resolver()
                patterns_cotisation = []
                
                # Chercher les URLs liées aux cotisations
                for pattern in urls.url_patterns:
                    if hasattr(pattern, 'pattern'):
                        pattern_str = str(pattern.pattern)
                        if any(keyword in pattern_str for keyword in ['cotisation', 'paiement', 'verification']):
                            patterns_cotisation.append(pattern_str)
                
                if not patterns_cotisation:
                    probleme = {
                        'type': 'URLS_MANQUANTES',
                        'description': 'Aucune URL trouvée pour la gestion des cotisations',
                        'severite': 'MOYENNE'
                    }
                    problemes.append(probleme)
                    print(f"   ⚠️  {probleme['description']}")
                else:
                    print(f"   ✅ URLs cotisations trouvées: {len(patterns_cotisation)}")
                    
            except Exception as e:
                print(f"   ⚠️  Vérification URLs: {e}")
            
            self.rapport['problemes'].extend(problemes)
            
        except Exception as e:
            print(f"   ❌ Erreur analyse problèmes: {e}")
    
    def generer_rapport_detaille(self):
        """Génère un rapport détaillé du diagnostic"""
        print("\n5. 📄 GÉNÉRATION RAPPORT DÉTAILLÉ...")
        
        # Résumé des problèmes
        total_problemes = len(self.rapport['problemes'])
        problemes_haute = len([p for p in self.rapport['problemes'] if p.get('severite') == 'HAUTE'])
        problemes_moyenne = len([p for p in self.rapport['problemes'] if p.get('severite') == 'MOYENNE'])
        
        # État général
        if total_problemes == 0:
            etat = 'EXCELLENT'
        elif problemes_haute == 0:
            etat = 'BON'
        else:
            etat = 'ATTENTION REQUISE'
        
        resume = {
            'date_execution': self.rapport['timestamp'],
            'total_problemes': total_problemes,
            'problemes_haute_priorite': problemes_haute,
            'problemes_moyenne_priorite': problemes_moyenne,
            'etat_general': etat
        }
        
        self.rapport['resume_executif'] = resume
        
        # Générer les recommandations
        self._generer_recommandations()
        
        # Sauvegarder le rapport
        self._sauvegarder_rapport()
        
        # Afficher le résumé
        self._afficher_resume()
    
    def _generer_recommandations(self):
        """Génère des recommandations basées sur l'analyse"""
        recommandations = []
        
        # Basé sur les problèmes identifiés
        problemes_types = [p['type'] for p in self.rapport['problemes']]
        
        if 'SYNCHRONISATION' in problemes_types:
            recommandations.append({
                'priorite': 'HAUTE',
                'action': 'Automatiser la synchronisation',
                'description': 'Implémenter un système de notification automatique entre assureurs et agents'
            })
        
        if 'STATUT_INCOHERENT' in problemes_types:
            recommandations.append({
                'priorite': 'MOYENNE',
                'action': 'Uniformiser les statuts',
                'description': 'Créer une table de correspondance des statuts entre assureurs et agents'
            })
        
        if 'MODELE_MANQUANT' in problemes_types:
            recommandations.append({
                'priorite': 'HAUTE',
                'action': 'Créer les modèles manquants',
                'description': 'Développer les modèles Cotisation et VerificationCotisation si absents'
            })
        
        # Recommandations générales
        if self.rapport['analyse'].get('statistiques', {}).get('cotisations', 0) > 0:
            recommandations.append({
                'priorite': 'MOYENNE',
                'action': 'Monitorer le flux en temps réel',
                'description': 'Implémenter un dashboard de suivi des cotisations'
            })
        
        self.rapport['recommandations'] = recommandations
    
    def _sauvegarder_rapport(self):
        """Sauvegarde le rapport dans un fichier JSON"""
        nom_fichier = f"diagnostic_cotisations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(nom_fichier, 'w', encoding='utf-8') as f:
                json.dump(self.rapport, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Rapport sauvegardé: {nom_fichier}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
    
    def _afficher_resume(self):
        """Affiche un résumé du diagnostic"""
        resume = self.rapport['resume_executif']
        
        print("\n" + "="*60)
        print("📋 RAPPORT DIAGNOSTIC COTISATIONS ASSUREUR-AGENT")
        print("="*60)
        print(f"📅 Date: {resume['date_execution']}")
        print(f"🎯 État: {resume['etat_general']}")
        print(f"❌ Problèmes: {resume['total_problemes']} (🔴{resume['problemes_haute_priorite']} 🟡{resume['problemes_moyenne_priorite']})")
        
        # Afficher les statistiques
        if 'statistiques' in self.rapport['analyse']:
            print(f"\n📊 STATISTIQUES:")
            stats = self.rapport['analyse']['statistiques']
            for key, value in stats.items():
                print(f"   {key}: {value}")
        
        # Afficher les problèmes
        if self.rapport['problemes']:
            print(f"\n🚨 PROBLÈMES IDENTIFIÉS:")
            for probleme in self.rapport['problemes']:
                severite_icon = '🔴' if probleme['severite'] == 'HAUTE' else '🟡' if probleme['severite'] == 'MOYENNE' else '🟢'
                print(f"   {severite_icon} {probleme['description']}")
        
        # Afficher les recommandations
        if self.rapport['recommandations']:
            print(f"\n💡 RECOMMANDATIONS:")
            for reco in self.rapport['recommandations']:
                priorite_icon = '🔴' if reco['priorite'] == 'HAUTE' else '🟡' if reco['priorite'] == 'MOYENNE' else '🟢'
                print(f"   {priorite_icon} {reco['action']}: {reco['description']}")
        
        print("="*60)

# Exécution
if __name__ == "__main__":
    diagnostic = DiagnosticCotisations()
    diagnostic.executer_diagnostic_complet()