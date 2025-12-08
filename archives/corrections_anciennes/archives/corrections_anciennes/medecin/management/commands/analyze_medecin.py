# medecin/management/commands/analyze_medecin.py
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import models
from django.urls import get_resolver, URLPattern, URLResolver
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.contrib.auth.models import User
import inspect
from collections import defaultdict

class MedecinAnalyzer:
    def __init__(self, stdout=None):
        self.stdout = stdout
        self.results = {
            'errors': [],
            'warnings': [],
            'infos': [],
            'conformity_score': 0
        }
        
    def log(self, message):
        """Utilise stdout si disponible, sinon print"""
        if self.stdout:
            self.stdout.write(message)
        else:
            print(message)
        
    def analyze_all(self):
        """Exécute toutes les analyses"""
        self.log("🔍 ANALYSE DE L'APPLICATION MEDECIN")
        self.log("=" * 60)
        
        self.analyze_models()
        self.analyze_views()
        self.analyze_urls()
        self.analyze_forms()
        self.analyze_templates()
        self.check_data_consistency()
        
        self.calculate_conformity_score()
        self.generate_report()
    
    def analyze_models(self):
        """Analyse la cohérence des modèles"""
        self.log("\n📊 ANALYSE DES MODÈLES")
        self.log("-" * 40)
        
        try:
            # Vérifier l'existence des modèles critiques
            critical_models = ['Medecin', 'Consultation', 'Ordonnance']
            
            for model_name in critical_models:
                try:
                    model = apps.get_model('medecin', model_name)
                    self.results['infos'].append(f"✅ Modèle {model_name} trouvé")
                    
                    # Analyser les champs du modèle
                    self.analyze_model_fields(model, model_name)
                    
                except LookupError:
                    self.results['errors'].append(f"❌ Modèle {model_name} non trouvé")
            
            # Vérifications spécifiques
            self.check_medecin_model()
            self.check_consultation_model()
            
        except Exception as e:
            self.results['errors'].append(f"❌ Erreur lors de l'analyse des modèles: {str(e)}")
    
    def analyze_model_fields(self, model, model_name):
        """Analyse les champs d'un modèle spécifique"""
        fields = model._meta.get_fields()
        
        field_info = []
        for field in fields:
            if hasattr(field, 'name'):
                field_type = type(field).__name__
                field_info.append(f"{field.name} ({field_type})")
        
        self.results['infos'].append(f"  Champs de {model_name}: {', '.join(field_info[:5])}...")  # Limiter l'affichage
    
    def check_medecin_model(self):
        """Vérifications spécifiques pour le modèle Medecin"""
        try:
            medecin_model = apps.get_model('medecin', 'Medecin')
            fields = [f.name for f in medecin_model._meta.get_fields()]
            
            # Vérifier les champs critiques
            critical_fields = ['user', 'specialite', 'telephone_pro']
            for field in critical_fields:
                if field not in fields:
                    self.results['warnings'].append(f"⚠️  Champ {field} manquant dans Medecin")
                else:
                    self.results['infos'].append(f"✅ Champ {field} présent dans Medecin")
                    
        except Exception as e:
            self.results['errors'].append(f"❌ Erreur dans check_medecin_model: {str(e)}")
    
    def check_consultation_model(self):
        """Vérifications spécifiques pour le modèle Consultation"""
        try:
            consultation_model = apps.get_model('medecin', 'Consultation')
            fields = [f.name for f in consultation_model._meta.get_fields()]
            
            # Vérifier le type de date_consultation
            date_field = consultation_model._meta.get_field('date_consultation')
            field_type = type(date_field).__name__
            self.results['infos'].append(f"📅 Consultation.date_consultation: {field_type}")
            
            # Vérifier les relations
            if 'medecin' not in fields:
                self.results['errors'].append("❌ Champ 'medecin' manquant dans Consultation")
            
        except Exception as e:
            self.results['errors'].append(f"❌ Erreur dans check_consultation_model: {str(e)}")
    
    def analyze_views(self):
        """Analyse la cohérence des vues"""
        self.log("\n👁️ ANALYSE DES VUES")
        self.log("-" * 40)
        
        try:
            from medecin import views
            
            # Liste des vues critiques à vérifier
            critical_views = [
                'dashboard_medecin', 'mes_rendez_vous', 'liste_bons_soin',
                'detail_consultation', 'creer_ordonnance', 'profil_medecin'
            ]
            
            for view_name in critical_views:
                if hasattr(views, view_name):
                    view_func = getattr(views, view_name)
                    
                    # Vérifier si c'est une fonction
                    if callable(view_func):
                        self.results['infos'].append(f"✅ Vue {view_name} trouvée")
                    else:
                        self.results['warnings'].append(f"⚠️  {view_name} n'est pas callable")
                else:
                    self.results['errors'].append(f"❌ Vue {view_name} non trouvée")
            
            # Vérifications spécifiques des vues
            self.check_view_consistency(views)
            
        except Exception as e:
            self.results['errors'].append(f"❌ Erreur lors de l'analyse des vues: {str(e)}")
    
    def check_view_consistency(self, views_module):
        """Vérifie la cohérence des vues avec les modèles"""
        try:
            # Vérifier que les vues utilisent les bons modèles
            view_methods = [method for method in dir(views_module) 
                          if not method.startswith('_') and callable(getattr(views_module, method))]
            
            self.results['infos'].append(f"📋 Vues disponibles: {', '.join(view_methods[:5])}...")
            
        except Exception as e:
            self.results['errors'].append(f"❌ Erreur dans check_view_consistency: {str(e)}")
    
    def analyze_urls(self):
        """Analyse la configuration des URLs"""
        self.log("\n🔗 ANALYSE DES URLs")
        self.log("-" * 40)
        
        try:
            from medecin import urls as medecin_urls
            
            # Analyser les URLs spécifiques de l'app medecin
            if hasattr(medecin_urls, 'urlpatterns'):
                url_count = len(medecin_urls.urlpatterns)
                self.results['infos'].append(f"🌐 URLs Medecin trouvées: {url_count}")
                
                for pattern in medecin_urls.urlpatterns[:3]:  # Afficher seulement les 3 premiers
                    self.analyze_url_pattern(pattern)
            
        except Exception as e:
            self.results['errors'].append(f"❌ Erreur lors de l'analyse des URLs: {str(e)}")
    
    def analyze_url_pattern(self, pattern):
        """Analyse un pattern URL spécifique"""
        try:
            if hasattr(pattern, 'name') and pattern.name:
                self.results['infos'].append(f"  ✅ URL: {pattern.name}")
            else:
                self.results['warnings'].append("⚠️  URL sans nom")
                
        except Exception as e:
            self.results['warnings'].append(f"⚠️  Impossible d'analyser le pattern URL: {str(e)}")
    
    def analyze_forms(self):
        """Analyse l'existence et la cohérence des formulaires"""
        self.log("\n📝 ANALYSE DES FORMULAIRES")
        self.log("-" * 40)
        
        try:
            # Essayer d'importer les formulaires
            try:
                from medecin import forms
                form_classes = [cls for cls in dir(forms) 
                              if not cls.startswith('_') and isinstance(getattr(forms, cls), type)]
                
                self.results['infos'].append(f"📋 Formulaires trouvés: {', '.join(form_classes)}")
                
            except ImportError:
                self.results['warnings'].append("⚠️  Module forms.py non trouvé")
                
        except Exception as e:
            self.results['errors'].append(f"❌ Erreur lors de l'analyse des formulaires: {str(e)}")
    
    def analyze_templates(self):
        """Vérifie l'existence des templates critiques"""
        self.log("\n🎨 ANALYSE DES TEMPLATES")
        self.log("-" * 40)
        
        try:
            critical_templates = [
                'medecin/dashboard.html',
                'medecin/mes_rendez_vous.html',
                'medecin/liste_bons.html',
                'medecin/detail_consultation.html'
            ]
            
            for template_path in critical_templates:
                try:
                    get_template(template_path)
                    self.results['infos'].append(f"✅ Template {template_path} trouvé")
                except TemplateDoesNotExist:
                    self.results['warnings'].append(f"⚠️  Template {template_path} manquant")
                    
        except Exception as e:
            self.results['errors'].append(f"❌ Erreur lors de l'analyse des templates: {str(e)}")
    
    def check_data_consistency(self):
        """Vérifie la cohérence des données entre modèles et vues"""
        self.log("\n🔄 VÉRIFICATION DE COHÉRENCE DES DONNÉES")
        self.log("-" * 40)
        
        try:
            # Vérifier la cohérence Medecin ↔ User
            from medecin.models import Medecin
            
            user_count = User.objects.count()
            medecin_count = Medecin.objects.count()
            
            self.results['infos'].append(f"👥 Utilisateurs: {user_count}, Médecins: {medecin_count}")
            
            if user_count > 0 and medecin_count == 0:
                self.results['warnings'].append("⚠️  Aucun médecin lié aux utilisateurs")
            
            # Vérifier les consultations
            try:
                from medecin.models import Consultation
                consultation_count = Consultation.objects.count()
                self.results['infos'].append(f"📅 Consultations en base: {consultation_count}")
            except:
                self.results['warnings'].append("⚠️  Impossible de compter les consultations")
            
        except Exception as e:
            self.results['warnings'].append(f"⚠️  Impossible de vérifier la cohérence des données: {str(e)}")
    
    def calculate_conformity_score(self):
        """Calcule un score de conformité global"""
        total_checks = len(self.results['errors']) + len(self.results['warnings']) + len(self.results['infos'])
        
        if total_checks == 0:
            self.results['conformity_score'] = 0
            return
            
        error_weight = 3
        warning_weight = 1
        
        penalty = (len(self.results['errors']) * error_weight + 
                  len(self.results['warnings']) * warning_weight)
        
        max_penalty = total_checks * error_weight
        self.results['conformity_score'] = max(0, 100 - (penalty / max_penalty * 100))
    
    def generate_report(self):
        """Génère un rapport complet"""
        self.log("\n" + "=" * 60)
        self.log("📊 RAPPORT D'ANALYSE - APPLICATION MEDECIN")
        self.log("=" * 60)
        
        # Score de conformité
        score = self.results['conformity_score']
        score_emoji = "🔴"
        if score >= 80:
            score_emoji = "🟢"
        elif score >= 60:
            score_emoji = "🟡"
        
        self.log(f"\n{score_emoji} SCORE DE CONFORMITÉ: {score:.1f}%")
        
        # Erreurs critiques
        if self.results['errors']:
            self.log(f"\n❌ ERREURS CRITIQUES ({len(self.results['errors'])}):")
            for error in self.results['errors']:
                self.log(f"  • {error}")
        
        # Avertissements
        if self.results['warnings']:
            self.log(f"\n⚠️  AVERTISSEMENTS ({len(self.results['warnings'])}):")
            for warning in self.results['warnings']:
                self.log(f"  • {warning}")
        
        # Informations
        if self.results['infos']:
            self.log(f"\nℹ️  INFORMATIONS ({len(self.results['infos'])}):")
            for info in self.results['infos'][:15]:  # Afficher seulement les 15 premières
                self.log(f"  • {info}")
        
        # Recommandations
        self.generate_recommendations()
    
    def generate_recommendations(self):
        """Génère des recommandations basées sur l'analyse"""
        self.log(f"\n💡 RECOMMANDATIONS:")
        
        recommendations = []
        
        # Basé sur les erreurs trouvées
        if any("Modèle" in error for error in self.results['errors']):
            recommendations.append("• Vérifier la définition des modèles dans models.py")
        
        if any("Vue" in error for error in self.results['errors']):
            recommendations.append("• Vérifier l'importation et la définition des vues")
        
        if any("URL" in error for error in self.results['errors']):
            recommendations.append("• Vérifier la configuration des URLs dans urls.py")
        
        # Recommandations générales
        recommendations.extend([
            "• Vérifier que tous les modèles critiques existent (Medecin, Consultation, Ordonnance)",
            "• S'assurer que les vues utilisent les bons modèles dans les querysets",
            "• Tester les URLs avec des données réelles",
            "• Vérifier les relations entre Medecin.user et le modèle User",
            "• Confirmer le type de champ pour date_consultation (DateField vs DateTimeField)"
        ])
        
        for rec in recommendations:
            self.log(f"  {rec}")

class Command(BaseCommand):
    help = 'Analyse la conformité de l\'application medecin'
    
    def handle(self, *args, **options):
        analyzer = MedecinAnalyzer(stdout=self.stdout)
        analyzer.analyze_all()