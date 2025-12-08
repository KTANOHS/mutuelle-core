# analysis_medecin.py
import os
import sys
import django
from django.apps import apps
from django.core.management import execute_from_command_line
from django.conf import settings

# Configuration Django
if __name__ == "__main__":
    # Ajouter le chemin de votre projet
    project_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(project_path)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    django.setup()

from django.db import models
from django.urls import get_resolver, URLPattern, URLResolver
import inspect
from collections import defaultdict

class MedecinAnalyzer:
    def __init__(self):
        self.results = {
            'errors': [],
            'warnings': [],
            'infos': [],
            'conformity_score': 0
        }
        
    def analyze_all(self):
        """Exécute toutes les analyses"""
        print("🔍 ANALYSE DE L'APPLICATION MEDECIN")
        print("=" * 60)
        
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
        print("\n📊 ANALYSE DES MODÈLES")
        print("-" * 40)
        
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
        
        self.results['infos'].append(f"  Champs de {model_name}: {', '.join(field_info)}")
    
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
        print("\n👁️ ANALYSE DES VUES")
        print("-" * 40)
        
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
                        
                        # Analyser les paramètres et le code source
                        self.analyze_view_source(view_name, view_func)
                    else:
                        self.results['warnings'].append(f"⚠️  {view_name} n'est pas callable")
                else:
                    self.results['errors'].append(f"❌ Vue {view_name} non trouvée")
            
            # Vérifications spécifiques des vues
            self.check_view_consistency(views)
            
        except Exception as e:
            self.results['errors'].append(f"❌ Erreur lors de l'analyse des vues: {str(e)}")
    
    def analyze_view_source(self, view_name, view_func):
        """Analyse le code source d'une vue"""
        try:
            source = inspect.getsource(view_func)
            
            # Vérifications basiques
            if '@login_required' not in source:
                self.results['warnings'].append(f"⚠️  Vue {view_name} sans @login_required")
            
            if 'request' not in source:
                self.results['warnings'].append(f"⚠️  Vue {view_name} n'utilise pas request")
                
            # Vérifier les modèles utilisés
            models_used = []
            for model_name in ['Medecin', 'Consultation', 'Ordonnance']:
                if model_name in source:
                    models_used.append(model_name)
            
            if models_used:
                self.results['infos'].append(f"  Modèles utilisés dans {view_name}: {', '.join(models_used)}")
                
        except Exception as e:
            self.results['warnings'].append(f"⚠️  Impossible d'analyser le code de {view_name}: {str(e)}")
    
    def check_view_consistency(self, views_module):
        """Vérifie la cohérence des vues avec les modèles"""
        try:
            # Vérifier que les vues utilisent les bons modèles
            view_methods = [method for method in dir(views_module) 
                          if not method.startswith('_') and callable(getattr(views_module, method))]
            
            self.results['infos'].append(f"📋 Vues disponibles: {', '.join(view_methods)}")
            
        except Exception as e:
            self.results['errors'].append(f"❌ Erreur dans check_view_consistency: {str(e)}")
    
    def analyze_urls(self):
        """Analyse la configuration des URLs"""
        print("\n🔗 ANALYSE DES URLs")
        print("-" * 40)
        
        try:
            from django.urls import get_resolver
            from medecin import urls as medecin_urls
            
            resolver = get_resolver()
            url_patterns = self.get_all_urls(resolver)
            
            medecin_urls_found = []
            for pattern in url_patterns:
                if 'medecin' in str(pattern):
                    medecin_urls_found.append(str(pattern))
            
            self.results['infos'].append(f"🌐 URLs Medecin trouvées: {len(medecin_urls_found)}")
            
            # Analyser les URLs spécifiques de l'app medecin
            if hasattr(medecin_urls, 'urlpatterns'):
                for pattern in medecin_urls.urlpatterns:
                    self.analyze_url_pattern(pattern)
            
        except Exception as e:
            self.results['errors'].append(f"❌ Erreur lors de l'analyse des URLs: {str(e)}")
    
    def get_all_urls(self, resolver, namespace=None):
        """Récupère toutes les URLs"""
        patterns = []
        for pattern in resolver.url_patterns:
            if isinstance(pattern, URLResolver):
                patterns.extend(self.get_all_urls(pattern, pattern.namespace))
            elif isinstance(pattern, URLPattern):
                patterns.append({
                    'pattern': pattern.pattern,
                    'callback': pattern.callback,
                    'name': pattern.name,
                    'namespace': namespace
                })
        return patterns
    
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
        print("\n📝 ANALYSE DES FORMULAIRES")
        print("-" * 40)
        
        try:
            # Essayer d'importer les formulaires
            try:
                from medecin import forms
                form_classes = [cls for cls in dir(forms) 
                              if not cls.startswith('_') and isinstance(getattr(forms, cls), type)]
                
                self.results['infos'].append(f"📋 Formulaires trouvés: {', '.join(form_classes)}")
                
                # Vérifier les formulaires critiques
                critical_forms = ['ConsultationFilterForm', 'OrdonnanceForm']
                for form_name in critical_forms:
                    if form_name in form_classes:
                        self.results['infos'].append(f"✅ Formulaire {form_name} trouvé")
                    else:
                        self.results['warnings'].append(f"⚠️  Formulaire {form_name} manquant")
                        
            except ImportError:
                self.results['warnings'].append("⚠️  Module forms.py non trouvé")
                
        except Exception as e:
            self.results['errors'].append(f"❌ Erreur lors de l'analyse des formulaires: {str(e)}")
    
    def analyze_templates(self):
        """Vérifie l'existence des templates critiques"""
        print("\n🎨 ANALYSE DES TEMPLATES")
        print("-" * 40)
        
        try:
            from django.template.loader import get_template
            from django.template import TemplateDoesNotExist
            
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
        print("\n🔄 VÉRIFICATION DE COHÉRENCE DES DONNÉES")
        print("-" * 40)
        
        try:
            # Vérifier la cohérence Medecin ↔ User
            from django.contrib.auth.models import User
            from medecin.models import Medecin
            
            user_count = User.objects.count()
            medecin_count = Medecin.objects.count()
            
            self.results['infos'].append(f"👥 Utilisateurs: {user_count}, Médecins: {medecin_count}")
            
            if user_count > 0 and medecin_count == 0:
                self.results['warnings'].append("⚠️  Aucun médecin lié aux utilisateurs")
            
            # Vérifier les consultations
            from medecin.models import Consultation
            consultation_count = Consultation.objects.count()
            self.results['infos'].append(f"📅 Consultations en base: {consultation_count}")
            
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
        info_weight = 0
        
        penalty = (len(self.results['errors']) * error_weight + 
                  len(self.results['warnings']) * warning_weight)
        
        max_penalty = total_checks * error_weight
        self.results['conformity_score'] = max(0, 100 - (penalty / max_penalty * 100))
    
    def generate_report(self):
        """Génère un rapport complet"""
        print("\n" + "=" * 60)
        print("📊 RAPPORT D'ANALYSE - APPLICATION MEDECIN")
        print("=" * 60)
        
        # Score de conformité
        score = self.results['conformity_score']
        score_emoji = "🔴"
        if score >= 80:
            score_emoji = "🟢"
        elif score >= 60:
            score_emoji = "🟡"
        
        print(f"\n{score_emoji} SCORE DE CONFORMITÉ: {score:.1f}%")
        
        # Erreurs critiques
        if self.results['errors']:
            print(f"\n❌ ERREURS CRITIQUES ({len(self.results['errors'])}):")
            for error in self.results['errors']:
                print(f"  • {error}")
        
        # Avertissements
        if self.results['warnings']:
            print(f"\n⚠️  AVERTISSEMENTS ({len(self.results['warnings'])}):")
            for warning in self.results['warnings']:
                print(f"  • {warning}")
        
        # Informations
        if self.results['infos']:
            print(f"\nℹ️  INFORMATIONS ({len(self.results['infos'])}):")
            for info in self.results['infos'][:10]:  # Afficher seulement les 10 premières
                print(f"  • {info}")
        
        # Recommandations
        self.generate_recommendations()
    
    def generate_recommendations(self):
        """Génère des recommandations basées sur l'analyse"""
        print(f"\n💡 RECOMMANDATIONS:")
        
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
            print(f"  {rec}")

def main():
    """Fonction principale"""
    analyzer = MedecinAnalyzer()
    analyzer.analyze_all()

if __name__ == "__main__":
    main()