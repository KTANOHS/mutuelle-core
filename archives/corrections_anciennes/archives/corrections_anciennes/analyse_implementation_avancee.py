# analyse_implementation_avancee.py
import os
import django
import sys
from pathlib import Path

# Configuration Django
sys.path.append('/Users/koffitanohsoualiho/Documents/VERIFICATION/projet')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps
from django.conf import settings
from django.db import models
from django.core.serializers import serialize
import json
from collections import defaultdict

class AnalyseurImplementation:
    def __init__(self):
        self.rapport = {
            'notifications': {'status': 'À implémenter', 'details': []},
            'api_mobile': {'status': 'À implémenter', 'details': []},
            'analytics': {'status': 'À implémenter', 'details': []}
        }
    
    def analyser_structure_existante(self):
        """Analyse la structure actuelle de l'application"""
        print("🔍 ANALYSE DE LA STRUCTURE EXISTANTE")
        print("=" * 50)
        
        # 1. Analyse des modèles
        model_analysis = self.analyser_modeles()
        
        # 2. Analyse des APIs existantes
        api_analysis = self.analyser_apis_existantes()
        
        # 3. Analyse des composants analytics
        analytics_analysis = self.analyser_composants_analytics()
        
        # 4. Analyse des dépendances
        dependencies_analysis = self.analyser_dependances()
        
        return {
            'modeles': model_analysis,
            'apis': api_analysis,
            'analytics': analytics_analysis,
            'dependances': dependencies_analysis
        }
    
    def analyser_modeles(self):
        """Analyse les modèles existants pour les nouvelles fonctionnalités"""
        print("\n📊 ANALYSE DES MODÈLES")
        print("-" * 30)
        
        modeles_pertinents = {}
        
        for model in apps.get_models():
            nom_modele = model.__name__
            champs = [f.name for f in model._meta.get_fields()]
            
            # Vérifier l'utilité pour les nouvelles fonctionnalités
            utilite = self._evaluer_utilite_modele(nom_modele, champs)
            
            if utilite:
                modeles_pertinents[nom_modele] = {
                    'champs': champs,
                    'utilite': utilite,
                    'pour_notifications': 'User' in nom_modele or 'Membre' in nom_modele,
                    'pour_api': True,  # Tous les modèles peuvent avoir une API
                    'pour_analytics': any(keyword in nom_modele for keyword in ['Soin', 'Paiement', 'Membre', 'Statistique'])
                }
                print(f"✅ {nom_modele}: {utilite}")
        
        return modeles_pertinents
    
    def _evaluer_utilite_modele(self, nom_modele, champs):
        """Évalue l'utilité d'un modèle pour les nouvelles fonctionnalités"""
        if 'User' in nom_modele or 'Membre' in nom_modele:
            return "Base pour les notifications et l'API mobile"
        elif 'Soin' in nom_modele or 'Paiement' in nom_modele:
            return "Données pour analytics et API"
        elif 'Notification' in nom_modele:
            return "Existant pour le système de notifications"
        elif any(keyword in nom_modele for keyword in ['Stat', 'Analytic', 'Log']):
            return "Composant analytics existant"
        else:
            return "Modèle support"
    
    def analyser_apis_existantes(self):
        """Analyse les endpoints API existants"""
        print("\n🌐 ANALYSE DES APIS EXISTANTES")
        print("-" * 30)
        
        try:
            from membres import urls as membres_urls
            endpoints_api = []
            
            # Analyser les URLs de l'application membres
            for urlpattern in membres_urls.urlpatterns:
                if hasattr(urlpattern, 'pattern'):
                    pattern = str(urlpattern.pattern)
                    if 'api' in pattern.lower():
                        endpoints_api.append({
                            'url': pattern,
                            'nom': getattr(urlpattern, 'name', 'Sans nom'),
                            'type': 'API'
                        })
            
            # Vérifier les vues API dans views.py
            api_endpoints_detectes = self._detecter_vues_api()
            endpoints_api.extend(api_endpoints_detectes)
            
            print(f"📡 {len(endpoints_api)} endpoints API détectés")
            for endpoint in endpoints_api:
                print(f"   🔗 {endpoint['url']} - {endpoint['nom']}")
                
            return endpoints_api
            
        except Exception as e:
            print(f"❌ Erreur analyse APIs: {e}")
            return []
    
    def _detecter_vues_api(self):
        """Détecte les vues API dans le code"""
        endpoints = []
        views_path = '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/membres/views.py'
        
        try:
            with open(views_path, 'r') as f:
                content = f.read()
                
            # Rechercher les vues API (JsonResponse, APIView, etc.)
            if 'JsonResponse' in content:
                endpoints.append({'url': '/api/statistiques/*', 'nom': 'API Statistiques', 'type': 'API Existante'})
            if 'api_' in content:
                endpoints.append({'url': '/api/*', 'nom': 'Divers APIs', 'type': 'API Existante'})
                
        except Exception as e:
            print(f"❌ Erreur lecture views.py: {e}")
            
        return endpoints
    
    def analyser_composants_analytics(self):
        """Analyse les composants analytics existants"""
        print("\n📈 ANALYSE DES COMPOSANTS ANALYTICS")
        print("-" * 35)
        
        composants = {}
        
        # Vérifier les vues d'analytics existantes
        analytics_views = self._detecter_vues_analytics()
        composants['vues'] = analytics_views
        
        # Vérifier les modèles de données pour analytics
        modeles_analytics = self._detecter_modeles_analytics()
        composants['modeles'] = modeles_analytics
        
        # Vérifier les templates d'analytics
        templates_analytics = self._detecter_templates_analytics()
        composants['templates'] = templates_analytics
        
        print(f"✅ {len(analytics_views)} vues analytics détectées")
        print(f"✅ {len(modeles_analytics)} modèles analytics détectés")
        print(f"✅ {len(templates_analytics)} templates analytics détectés")
        
        return composants
    
    def _detecter_vues_analytics(self):
        """Détecte les vues liées aux analytics"""
        vues_analytics = []
        views_path = '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/membres/views.py'
        
        try:
            with open(views_path, 'r') as f:
                content = f.read()
                
            # Rechercher les vues analytics
            if 'statistiques_avancees' in content:
                vues_analytics.append('statistiques_avancees')
            if 'dashboard_analytics' in content:
                vues_analytics.append('dashboard_analytics')
            if 'AnalyseConnexions' in content:
                vues_analytics.append('AnalyseConnexions (Classe)')
            if 'api_statistiques' in content:
                vues_analytics.append('api_statistiques_*')
                
        except Exception as e:
            print(f"❌ Erreur détection vues analytics: {e}")
            
        return vues_analytics
    
    def _detecter_modeles_analytics(self):
        """Détecte les modèles utiles pour les analytics"""
        modeles_analytics = []
        
        for model in apps.get_models():
            nom_modele = model.__name__
            if any(keyword in nom_modele for keyword in ['Soin', 'Paiement', 'Membre', 'Statistique', 'Historique', 'Log']):
                modeles_analytics.append(nom_modele)
                
        return modeles_analytics
    
    def _detecter_templates_analytics(self):
        """Détecte les templates d'analytics"""
        templates_dir = '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/membres/templates/membres'
        templates_analytics = []
        
        try:
            for file in os.listdir(templates_dir):
                if any(keyword in file for keyword in ['analytics', 'statistique', 'dashboard', 'admin']):
                    templates_analytics.append(file)
        except Exception as e:
            print(f"❌ Erreur scan templates: {e}")
            
        return templates_analytics
    
    def analyser_dependances(self):
        """Analyse les dépendances du projet"""
        print("\n📦 ANALYSE DES DÉPENDANCES")
        print("-" * 25)
        
        dependances = {
            'rest_framework': 'DRF' in settings.INSTALLED_APPS,
            'corsheaders': 'corsheaders' in settings.INSTALLED_APPS,
            'channels': 'channels' in settings.INSTALLED_APPS,
            'notifications': any('notification' in app.lower() for app in settings.INSTALLED_APPS),
            'api': any('api' in app.lower() for app in settings.INSTALLED_APPS),
        }
        
        for dep, present in dependances.items():
            status = "✅ PRÉSENTE" if present else "❌ ABSENTE"
            print(f"   {status} {dep}")
            
        return dependances
    
    def generer_recommandations(self, analyse):
        """Génère des recommandations d'implémentation"""
        print("\n🎯 RECOMMANDATIONS D'IMPLÉMENTATION")
        print("=" * 45)
        
        recommendations = {
            'notifications': self._recommandations_notifications(analyse),
            'api_mobile': self._recommandations_api_mobile(analyse),
            'analytics': self._recommandations_analytics(analyse)
        }
        
        return recommendations
    
    def _recommandations_notifications(self, analyse):
        """Recommandations pour le système de notifications"""
        reco = []
        
        if not analyse['dependances']['notifications']:
            reco.append("📱 INSTALLER django-notifications-hq ou créer un modèle Notification personnalisé")
        
        reco.extend([
            "🔔 CRÉER le modèle Notification avec champs: user, titre, message, type, lu, date_creation",
            "🌐 IMPLÉMENTER les WebSockets avec Django Channels pour notifications en temps réel",
            "📧 AJOUTER l'envoi d'emails pour les notifications importantes",
            "📱 CRÉER les endpoints API pour les notifications mobiles",
            "🔔 DÉVELOPPER le système de préférences de notifications par utilisateur"
        ])
        
        return reco
    
    def _recommandations_api_mobile(self, analyse):
        """Recommandations pour l'API mobile"""
        reco = []
        
        if not analyse['dependances']['rest_framework']:
            reco.append("📱 INSTALLER Django REST Framework")
        
        if not analyse['dependances']['corsheaders']:
            reco.append("🌐 INSTALLER django-cors-headers pour les requêtes cross-origin")
        
        reco.extend([
            "🔐 IMPLÉMENTER l'authentification JWT pour l'API mobile",
            "📡 CRÉER les serializers pour tous les modèles principaux",
            "🌐 DÉVELOPPER les endpoints API REST complets",
            "📱 IMPLÉMENTER la pagination et les filtres API",
            "🔒 AJOUTER les permissions et throttling pour l'API",
            "📄 CRÉER la documentation API avec Swagger/OpenAPI"
        ])
        
        return reco
    
    def _recommandations_analytics(self, analyse):
        """Recommandations pour les analytics avancés"""
        reco = []
        
        reco.extend([
            "📊 CRÉER un modèle DashboardAnalytics pour stocker les métriques",
            "📈 IMPLÉMENTER le calcul des KPI: membres actifs, revenus, soins, etc.",
            "📉 AJOUTER les graphiques interactifs avec Chart.js ou D3.js",
            "🔍 DÉVELOPPER le système de rapports personnalisables",
            "📋 CRÉER les vues d'export de données (CSV, Excel, PDF)",
            "⏰ IMPLÉMENTER le traitement par lots pour les calculs lourds",
            "📱 DÉVELOPPER le dashboard responsive pour mobile"
        ])
        
        return reco
    
    def generer_plan_action(self, recommendations):
        """Génère un plan d'action détaillé"""
        print("\n📋 PLAN D'ACTION DÉTAILLÉ")
        print("=" * 35)
        
        plan = {
            'phase_1': {
                'titre': '📦 Infrastructure de Base',
                'taches': [
                    "Installer Django REST Framework",
                    "Installer django-cors-headers", 
                    "Configurer l'authentification JWT",
                    "Créer le modèle Notification de base"
                ],
                'duree_estimee': '2-3 semaines'
            },
            'phase_2': {
                'titre': '🌐 API Mobile',
                'taches': [
                    "Développer les serializers pour tous les modèles",
                    "Créer les endpoints API REST",
                    "Implémenter l'authentification et permissions",
                    "Créer la documentation API"
                ],
                'duree_estimee': '3-4 semaines'
            },
            'phase_3': {
                'titre': '🔔 Système de Notifications',
                'taches': [
                    "Compléter le modèle Notification",
                    "Implémenter les WebSockets avec Channels",
                    "Développer le système d'envoi d'emails",
                    "Créer les préférences utilisateur"
                ],
                'duree_estimee': '2-3 semaines'
            },
            'phase_4': {
                'titre': '📈 Analytics Avancés',
                'taches': [
                    "Développer les calculs de KPI",
                    "Créer les dashboards interactifs",
                    "Implémenter les exports de données",
                    "Optimiser les performances"
                ],
                'duree_estimee': '3-4 semaines'
            }
        }
        
        for phase, details in plan.items():
            print(f"\n{details['titre']} ({details['duree_estimee']})")
            for tache in details['taches']:
                print(f"   ✓ {tache}")
                
        return plan
    
    def generer_fichiers_exemple(self):
        """Génère des exemples de code pour démarrer"""
        print("\n💻 EXEMPLES DE CODE À IMPLÉMENTER")
        print("=" * 40)
        
        # Exemple modèle Notification
        modele_notification = '''
# models.py - Modèle Notification
class Notification(models.Model):
    TYPE_CHOICES = [
        ('INFO', 'Information'),
        ('ALERT', 'Alerte'),
        ('SUCCESS', 'Succès'),
        ('WARNING', 'Avertissement'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    titre = models.CharField(max_length=200)
    message = models.TextField()
    type_notification = models.CharField(max_length=10, choices=TYPE_CHOICES, default='INFO')
    lu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    lien = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['user', 'lu']),
            models.Index(fields=['date_creation']),
        ]
    
    def __str__(self):
        return f"{self.titre} - {self.user.username}"
'''
        
        # Exemple serializer API
        serializer_exemple = '''
# serializers.py - Serializer de base
from rest_framework import serializers
from .models import Membre, Soin, Notification

class MembreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membre
        fields = '__all__'

class SoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soin
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
'''
        
        print("📝 Modèle Notification:")
        print(modele_notification)
        
        print("📝 Serializers API:")
        print(serializer_exemple)
        
        return {
            'modele_notification': modele_notification,
            'serializers': serializer_exemple
        }

def main():
    analyseur = AnalyseurImplementation()
    
    print("🚀 ANALYSE POUR IMPLÉMENTATION DES FONCTIONNALITÉS AVANCÉES")
    print("=" * 60)
    
    # 1. Analyse de l'existant
    analyse = analyseur.analyser_structure_existante()
    
    # 2. Génération des recommandations
    recommendations = analyseur.generer_recommandations(analyse)
    
    # 3. Plan d'action
    plan_action = analyseur.generer_plan_action(recommendations)
    
    # 4. Exemples de code
    exemples = analyseur.generer_fichiers_exemple()
    
    print("\n" + "🎊" * 20)
    print("🎉 ANALYSE TERMINÉE AVEC SUCCÈS!")
    print("🎊" * 20)
    
    print(f"\n📊 RÉSUMÉ:")
    print(f"   • {len(analyse['modeles'])} modèles analysés")
    print(f"   • {len(analyse['apis'])} APIs existantes détectées") 
    print(f"   • {len(analyse['analytics']['vues'])} composants analytics identifiés")
    print(f"   • Plan sur {sum(int(phase['duree_estimee'].split('-')[0]) for phase in plan_action.values())} semaines")
    
    print(f"\n💡 PROCHAINES ÉTAPES:")
    print("   1. Réviser les recommandations")
    print("   2. Commencer par la Phase 1 (Infrastructure)")
    print("   3. Implémenter progressivement chaque composant")
    print("   4. Tester chaque fonctionnalité avant passage à la suivante")

if __name__ == "__main__":
    main()