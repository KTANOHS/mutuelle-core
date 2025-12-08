#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC STATISTIQUE - VERSION CORRIGÉE
Usage: python diagnostic_statistique.py
"""

import os
import sys
import django
from datetime import datetime
from django.apps import apps
from django.db.models import Count, Sum, Avg, Max, Min, Q

# Configuration Django
def setup_django():
    """Configuration de l'environnement Django"""
    try:
        # Trouver le répertoire du projet
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.abspath(os.path.join(current_dir, '..'))
        
        # Ajouter au chemin Python
        sys.path.append(project_dir)
        
        # Configurer Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        django.setup()
        
        print("✅ Django configuré avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur de configuration Django: {e}")
        return False

class DiagnosticStatistiqueCorrige:
    """Classe corrigée pour le diagnostic statistique"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.models_info = {}
        self.detecter_applications()
    
    def detecter_applications(self):
        """Détecter automatiquement les applications et modèles"""
        print("\n" + "="*80)
        print("🔍 DÉTECTION AUTOMATIQUE DES APPLICATIONS")
        print("="*80)
        
        for app_config in apps.get_app_configs():
            app_name = app_config.name
            models_list = app_config.get_models()
            
            for model in models_list:
                model_name = model.__name__
                app_label = model._meta.app_label
                
                # Stocker les informations du modèle
                key = f"{app_label}.{model_name}"
                self.models_info[model_name] = {
                    'model': model,
                    'app_label': app_label,
                    'app_name': app_name,
                    'verbose_name': model._meta.verbose_name,
                    'verbose_name_plural': model._meta.verbose_name_plural
                }
        
        print(f"📊 Modèles détectés: {len(self.models_info)}")
    
    def get_model(self, model_name):
        """Obtenir un modèle par son nom"""
        if model_name in self.models_info:
            return self.models_info[model_name]['model']
        
        # Chercher avec différentes variantes
        for name, info in self.models_info.items():
            if model_name.lower() in name.lower():
                return info['model']
        
        return None
    
    def run_diagnostic(self):
        """Exécuter le diagnostic corrigé"""
        print("\n" + "="*80)
        print("📊 DIAGNOSTIC STATISTIQUE CORRIGÉ")
        print("="*80)
        
        # 1. Analyse de base
        self.analyze_base()
        
        # 2. Chercher et analyser les modèles principaux
        self.analyze_membres_corrige()
        self.analyze_cotisations_corrige()
        self.analyze_paiements_corrige()
        
        # 3. Résumé
        self.generer_resume()
    
    def analyze_base(self):
        """Analyse de base des données"""
        print("\n" + "="*80)
        print("📦 ANALYSE GÉNÉRALE DE LA BASE DE DONNÉES")
        print("="*80)
        
        total_records = 0
        models_avec_donnees = []
        models_sans_donnees = []
        
        for model_name, info in self.models_info.items():
            model = info['model']
            count = model.objects.count()
            total_records += count
            
            if count > 0:
                models_avec_donnees.append({
                    'nom': model_name,
                    'verbose': info['verbose_name_plural'],
                    'count': count,
                    'app': info['app_label']
                })
            else:
                models_sans_donnees.append({
                    'nom': model_name,
                    'verbose': info['verbose_name_plural'],
                    'app': info['app_label']
                })
        
        print(f"\n📊 STATISTIQUES GLOBALES:")
        print(f"   • Total modèles: {len(self.models_info)}")
        print(f"   • Total enregistrements: {total_records}")
        print(f"   • Modèles avec données: {len(models_avec_donnees)}")
        print(f"   • Modèles sans données: {len(models_sans_donnees)}")
        
        # Afficher les modèles avec données
        if models_avec_donnees:
            print(f"\n✅ MODÈLES AVEC DONNÉES:")
            models_tries = sorted(models_avec_donnees, key=lambda x: x['count'], reverse=True)
            for i, m in enumerate(models_tries[:15], 1):
                print(f"   {i:2}. {m['verbose']:30} ({m['nom']:20}): {m['count']:6,} (app: {m['app']})")
        
        # Afficher quelques modèles sans données importants
        if models_sans_donnees:
            models_importants = [m for m in models_sans_donnees if any(
                keyword in m['nom'].lower() for keyword in 
                ['cotisation', 'paiement', 'bon', 'soin', 'consultation', 'medicament']
            )]
            
            if models_importants:
                print(f"\n⚠️  MODÈLES IMPORTANTS SANS DONNÉES:")
                for i, m in enumerate(models_importants[:10], 1):
                    print(f"   {i:2}. {m['verbose']:30} ({m['nom']:20})")
    
    def analyze_membres_corrige(self):
        """Analyser les membres avec détection automatique"""
        print("\n" + "="*80)
        print("👥 ANALYSE DES MEMBRES (CORRIGÉ)")
        print("="*80)
        
        # Chercher le modèle Membre
        membre_model = self.get_model('Membre')
        
        if not membre_model:
            print("❌ Modèle Membre non trouvé")
            print("\n🔍 Recherche de modèles similaires...")
            # Chercher des modèles avec des noms similaires
            for name, info in self.models_info.items():
                if any(keyword in name.lower() for keyword in ['membre', 'member', 'user', 'client', 'patient']):
                    print(f"   • {name} ({info['verbose_name_plural']}) - App: {info['app_label']}")
            return
        
        print(f"✅ Modèle trouvé: {membre_model.__name__} (app: {membre_model._meta.app_label})")
        
        try:
            total = membre_model.objects.count()
            print(f"\n📊 TOTAL MEMBRES: {total:,}")
            
            if total == 0:
                print("⚠️  Aucun membre trouvé")
                return
            
            # Analyser les champs disponibles
            fields = membre_model._meta.fields
            field_names = [f.name for f in fields]
            
            print(f"\n📋 CHAMPS DISPONIBLES ({len(fields)}):")
            # Afficher les champs intéressants
            interesting_fields = ['nom', 'prenom', 'genre', 'statut', 'date_naissance', 'date_inscription']
            for field in interesting_fields:
                if field in field_names:
                    print(f"   • {field}: OUI")
                else:
                    print(f"   • {field}: NON")
            
            # Essayer d'analyser par genre si le champ existe
            if 'genre' in field_names:
                try:
                    stats_genre = membre_model.objects.values('genre').annotate(
                        count=Count('id')
                    ).order_by('-count')
                    
                    if stats_genre:
                        print(f"\n👫 RÉPARTITION PAR GENRE:")
                        for stat in stats_genre:
                            pourcentage = (stat['count'] / total * 100) if total > 0 else 0
                            print(f"   • {stat['genre']}: {stat['count']:,} ({pourcentage:.1f}%)")
                except:
                    pass
            
            # Essayer d'analyser par statut si le champ existe
            if 'statut' in field_names:
                try:
                    stats_statut = membre_model.objects.values('statut').annotate(
                        count=Count('id')
                    ).order_by('-count')
                    
                    if stats_statut:
                        print(f"\n📋 RÉPARTITION PAR STATUT:")
                        for stat in stats_statut:
                            pourcentage = (stat['count'] / total * 100) if total > 0 else 0
                            print(f"   • {stat['statut']}: {stat['count']:,} ({pourcentage:.1f}%)")
                except:
                    pass
            
            # Afficher quelques membres
            print(f"\n👤 EXEMPLE DE MEMBRES (premiers 5):")
            membres = membre_model.objects.all()[:5]
            for i, membre in enumerate(membres, 1):
                # Essayer d'afficher nom et prénom
                nom = getattr(membre, 'nom', 'N/A')
                prenom = getattr(membre, 'prenom', 'N/A')
                print(f"   {i}. {prenom} {nom}")
            
            # Informations supplémentaires si disponibles
            if 'date_inscription' in field_names:
                try:
                    dates = membre_model.objects.filter(date_inscription__isnull=False)
                    if dates.exists():
                        premier = dates.earliest('date_inscription')
                        dernier = dates.latest('date_inscription')
                        print(f"\n📅 PREMIÈRE INSCRIPTION: {getattr(premier, 'date_inscription', 'N/A')}")
                        print(f"📅 DERNIÈRE INSCRIPTION: {getattr(dernier, 'date_inscription', 'N/A')}")
                except:
                    pass
            
        except Exception as e:
            print(f"⚠️  Erreur d'analyse des membres: {e}")
    
    def analyze_cotisations_corrige(self):
        """Analyser les cotisations avec détection automatique"""
        print("\n" + "="*80)
        print("💰 ANALYSE DES COTISATIONS (CORRIGÉ)")
        print("="*80)
        
        # Chercher le modèle Cotisation
        cotisation_model = self.get_model('Cotisation')
        
        if not cotisation_model:
            print("❌ Modèle Cotisation non trouvé")
            print("\n🔍 Recherche de modèles similaires...")
            for name, info in self.models_info.items():
                if any(keyword in name.lower() for keyword in ['cotisation', 'contribution', 'payment', 'fee', 'subscription']):
                    print(f"   • {name} ({info['verbose_name_plural']}) - App: {info['app_label']}")
            return
        
        print(f"✅ Modèle trouvé: {cotisation_model.__name__} (app: {cotisation_model._meta.app_label})")
        
        try:
            total = cotisation_model.objects.count()
            print(f"\n📊 TOTAL COTISATIONS: {total:,}")
            
            if total == 0:
                print("⚠️  Aucune cotisation trouvé")
                print("💡 Conseil: Exécutez le script de génération de cotisations")
                return
            
            # Analyser les champs disponibles
            fields = cotisation_model._meta.fields
            field_names = [f.name for f in fields]
            
            print(f"\n📋 CHAMPS DISPONIBLES ({len(fields)}):")
            interesting_fields = ['montant', 'periode', 'date_cotisation', 'membre', 'statut']
            for field in interesting_fields:
                if field in field_names:
                    print(f"   • {field}: OUI")
                else:
                    print(f"   • {field}: NON")
            
            # Statistiques financières si le champ montant existe
            if 'montant' in field_names:
                try:
                    stats = cotisation_model.objects.aggregate(
                        total=Sum('montant'),
                        moyenne=Avg('montant'),
                        max=Max('montant'),
                        min=Min('montant')
                    )
                    
                    print(f"\n💰 STATISTIQUES FINANCIÈRES:")
                    if stats['total']:
                        print(f"   • Total: {stats['total']:,.0f} FCFA")
                        print(f"   • Moyenne: {stats['moyenne']:,.0f} FCFA")
                        print(f"   • Maximum: {stats['max']:,.0f} FCFA")
                        print(f"   • Minimum: {stats['min']:,.0f} FCFA")
                except:
                    pass
            
            # Par période si le champ existe
            if 'periode' in field_names:
                try:
                    stats_periode = cotisation_model.objects.values('periode').annotate(
                        count=Count('id'),
                        total=Sum('montant')
                    ).order_by('-periode')[:12]
                    
                    if stats_periode:
                        print(f"\n📅 COTISATIONS PAR PÉRIODE (12 dernières):")
                        for periode in stats_periode:
                            print(f"   • {periode['periode']}: {periode['count']:,} = {periode['total'] or 0:,.0f} FCFA")
                except:
                    pass
            
            # Afficher quelques cotisations
            print(f"\n💰 EXEMPLE DE COTISATIONS (5 dernières):")
            cotisations = cotisation_model.objects.all().order_by('-id')[:5]
            for i, cot in enumerate(cotisations, 1):
                # Essayer d'afficher les informations
                periode = getattr(cot, 'periode', 'N/A')
                montant = getattr(cot, 'montant', 'N/A')
                date = getattr(cot, 'date_cotisation', 'N/A')
                
                # Essayer d'afficher le membre
                membre_info = "N/A"
                if hasattr(cot, 'membre'):
                    membre = cot.membre
                    if hasattr(membre, 'nom') and hasattr(membre, 'prenom'):
                        membre_info = f"{membre.prenom} {membre.nom}"
                
                print(f"   {i}. {membre_info} - {periode}: {montant} FCFA ({date})")
            
        except Exception as e:
            print(f"⚠️  Erreur d'analyse des cotisations: {e}")
    
    def analyze_paiements_corrige(self):
        """Analyser les paiements avec détection automatique"""
        print("\n" + "="*80)
        print("💳 ANALYSE DES PAIEMENTS (CORRIGÉ)")
        print("="*80)
        
        # Chercher le modèle Paiement
        paiement_model = self.get_model('Paiement')
        
        if not paiement_model:
            print("❌ Modèle Paiement non trouvé")
            print("\n🔍 Recherche de modèles similaires...")
            for name, info in self.models_info.items():
                if any(keyword in name.lower() for keyword in ['paiement', 'payment', 'transaction', 'facture', 'invoice']):
                    print(f"   • {name} ({info['verbose_name_plural']}) - App: {info['app_label']}")
            return
        
        print(f"✅ Modèle trouvé: {paiement_model.__name__} (app: {paiement_model._meta.app_label})")
        
        try:
            total = paiement_model.objects.count()
            print(f"\n📊 TOTAL PAIEMENTS: {total:,}")
            
            if total == 0:
                print("⚠️  Aucun paiement trouvé")
                return
            
            # Analyser les champs disponibles
            fields = paiement_model._meta.fields
            field_names = [f.name for f in fields]
            
            print(f"\n📋 CHAMPS DISPONIBLES ({len(fields)}):")
            interesting_fields = ['montant', 'date_paiement', 'mode_paiement', 'statut', 'membre']
            for field in interesting_fields:
                if field in field_names:
                    print(f"   • {field}: OUI")
                else:
                    print(f"   • {field}: NON")
            
            # Statistiques financières
            if 'montant' in field_names:
                try:
                    stats = paiement_model.objects.aggregate(
                        total=Sum('montant'),
                        moyenne=Avg('montant'),
                        max=Max('montant'),
                        min=Min('montant')
                    )
                    
                    print(f"\n💰 STATISTIQUES FINANCIÈRES:")
                    if stats['total']:
                        print(f"   • Total: {stats['total']:,.0f} FCFA")
                        print(f"   • Moyenne: {stats['moyenne']:,.0f} FCFA")
                        print(f"   • Maximum: {stats['max']:,.0f} FCFA")
                        print(f"   • Minimum: {stats['min']:,.0f} FCFA")
                except:
                    pass
            
            # Par mode de paiement
            if 'mode_paiement' in field_names:
                try:
                    stats_mode = paiement_model.objects.values('mode_paiement').annotate(
                        count=Count('id'),
                        total=Sum('montant')
                    ).order_by('-total')
                    
                    if stats_mode:
                        print(f"\n💳 RÉPARTITION PAR MODE DE PAIEMENT:")
                        for mode in stats_mode:
                            pourcentage = (mode['total'] / stats['total'] * 100) if stats.get('total') else 0
                            print(f"   • {mode['mode_paiement']}: {mode['count']:,} = {mode['total']:,.0f} FCFA ({pourcentage:.1f}%)")
                except:
                    pass
            
            # Par statut
            if 'statut' in field_names:
                try:
                    stats_statut = paiement_model.objects.values('statut').annotate(
                        count=Count('id'),
                        total=Sum('montant')
                    ).order_by('-total')
                    
                    if stats_statut:
                        print(f"\n📋 RÉPARTITION PAR STATUT:")
                        for statut in stats_statut:
                            print(f"   • {statut['statut']}: {statut['count']:,} = {statut['total']:,.0f} FCFA")
                except:
                    pass
            
            # Afficher quelques paiements
            print(f"\n💳 EXEMPLE DE PAIEMENTS (5 derniers):")
            paiements = paiement_model.objects.all().order_by('-id')[:5]
            for i, paiement in enumerate(paiements, 1):
                montant = getattr(paiement, 'montant', 'N/A')
                date = getattr(paiement, 'date_paiement', 'N/A')
                mode = getattr(paiement, 'mode_paiement', 'N/A')
                
                # Essayer d'afficher le membre
                membre_info = "N/A"
                if hasattr(paiement, 'membre'):
                    membre = paiement.membre
                    if hasattr(membre, 'nom') and hasattr(membre, 'prenom'):
                        membre_info = f"{membre.prenom} {membre.nom}"
                
                print(f"   {i}. {membre_info} - {montant} FCFA ({mode}) le {date}")
            
        except Exception as e:
            print(f"⚠️  Erreur d'analyse des paiements: {e}")
    
    def generer_resume(self):
        """Générer un résumé des analyses"""
        print("\n" + "="*80)
        print("📋 RÉSUMÉ DU DIAGNOSTIC")
        print("="*80)
        
        # Obtenir les comptes
        membre_model = self.get_model('Membre')
        cotisation_model = self.get_model('Cotisation')
        paiement_model = self.get_model('Paiement')
        
        total_membres = membre_model.objects.count() if membre_model else 0
        total_cotisations = cotisation_model.objects.count() if cotisation_model else 0
        total_paiements = paiement_model.objects.count() if paiement_model else 0
        
        print(f"\n📊 SYNTHÈSE:")
        print(f"   👥 Membres: {total_membres:,}")
        print(f"   💰 Cotisations: {total_cotisations:,}")
        print(f"   💳 Paiements: {total_paiements:,}")
        
        # Calculer les totaux financiers
        total_financier = 0
        
        if cotisation_model and hasattr(cotisation_model, 'montant'):
            total_cot = cotisation_model.objects.aggregate(total=Sum('montant'))['total'] or 0
            total_financier += total_cot
            print(f"   📈 Total cotisations: {total_cot:,.0f} FCFA")
        
        if paiement_model and hasattr(paiement_model, 'montant'):
            total_pai = paiement_model.objects.aggregate(total=Sum('montant'))['total'] or 0
            total_financier += total_pai
            print(f"   📈 Total paiements: {total_pai:,.0f} FCFA")
        
        print(f"\n💰 TOTAL FINANCIER: {total_financier:,.0f} FCFA")
        
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS:")
        
        if total_membres == 0:
            print("   • Ajouter des membres dans l'application")
        
        if total_cotisations == 0:
            print("   • Générer des cotisations avec le script approprié")
        
        if total_paiements == 0:
            print("   • Enregistrer des paiements pour les membres")
        
        # Vérifier les modèles sans données importants
        models_importants_vides = []
        for name, info in self.models_info.items():
            if any(keyword in name.lower() for keyword in ['cotisation', 'paiement', 'bon', 'soin']):
                count = info['model'].objects.count()
                if count == 0:
                    models_importants_vides.append(name)
        
        if models_importants_vides:
            print(f"\n⚠️  MODÈLES IMPORTANTS VIDES:")
            for model in models_importants_vides[:5]:
                print(f"   • {model}")
        
        # Temps d'exécution
        duration = datetime.now() - self.start_time
        print(f"\n⏱️  TEMPS D'EXÉCUTION: {duration.total_seconds():.2f} secondes")

def main():
    """Fonction principale"""
    print("\n" + "="*80)
    print("🚀 DIAGNOSTIC STATISTIQUE - VERSION CORRIGÉE")
    print("="*80)
    
    # Configuration Django
    if not setup_django():
        return
    
    # Exécuter le diagnostic
    diagnostic = DiagnosticStatistiqueCorrige()
    diagnostic.run_diagnostic()
    
    print("\n" + "="*80)
    print("✅ DIAGNOSTIC TERMINÉ")
    print("="*80)

if __name__ == "__main__":
    main()