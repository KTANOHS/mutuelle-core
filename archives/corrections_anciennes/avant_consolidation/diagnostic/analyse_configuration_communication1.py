# analyse_configuration_communication.py
import os
import django
import sys

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps
from django.conf import settings
import os

class AnalyseurConfigurationCommunication:
    """
    Script pour analyser et corriger la configuration de la communication
    dans les applications agents et assureur
    """
    
    def __init__(self):
        self.results = {
            'success': [],
            'warnings': [],
            'errors': []
        }
    
    def log_success(self, message):
        self.results['success'].append(message)
        print(f"✅ {message}")
    
    def log_warning(self, message):
        self.results['warnings'].append(message)
        print(f"⚠️ {message}")
    
    def log_error(self, message):
        self.results['errors'].append(message)
        print(f"❌ {message}")
    
    def analyser_installation_apps(self):
        """Analyser l'installation des applications dans settings.py"""
        print("🔍 ANALYSE DE LA CONFIGURATION DJANGO")
        print("="*50)
        
        # Vérifier si communication est dans INSTALLED_APPS
        installed_apps = getattr(settings, 'INSTALLED_APPS', [])
        
        apps_requises = ['communication', 'agents', 'assureur']
        
        for app in apps_requises:
            if app in installed_apps:
                self.log_success(f"Application '{app}' installée")
            else:
                self.log_error(f"Application '{app}' NON installée")
        
        return 'communication' in installed_apps
    
    def analyser_fichiers_communication(self):
        """Analyser la structure des fichiers de communication"""
        print("\n📁 ANALYSE DES FICHIERS DE COMMUNICATION")
        print("="*50)
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        dossiers_verifies = []
        
        # Vérifier les dossiers importants
        dossiers_importants = [
            'communication',
            'agents',
            'assureur',
            'communication/templates',
            'communication/static',
            'agents/templates',
            'assureur/templates'
        ]
        
        for dossier in dossiers_importants:
            chemin = os.path.join(base_dir, dossier)
            if os.path.exists(chemin):
                dossiers_verifies.append(dossier)
                self.log_success(f"Dossier trouvé: {dossier}")
            else:
                self.log_warning(f"Dossier manquant: {dossier}")
        
        # Vérifier les fichiers modèles importants
        fichiers_modeles = [
            'communication/models.py',
            'agents/models.py', 
            'assureur/models.py'
        ]
        
        for fichier in fichiers_modeles:
            chemin = os.path.join(base_dir, fichier)
            if os.path.exists(chemin):
                self.log_success(f"Fichier trouvé: {fichier}")
            else:
                self.log_error(f"Fichier manquant: {fichier}")
    
    def analyser_urls_communication(self):
        """Analyser la configuration des URLs"""
        print("\n🌐 ANALYSE DE LA CONFIGURATION DES URLS")
        print("="*50)
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Vérifier les fichiers urls.py
        fichiers_urls = [
            'communication/urls.py',
            'agents/urls.py',
            'assureur/urls.py'
        ]
        
        for fichier in fichiers_urls:
            chemin = os.path.join(base_dir, fichier)
            if os.path.exists(chemin):
                # Lire le fichier pour vérifier le contenu
                with open(chemin, 'r') as f:
                    contenu = f.read()
                
                if 'communication' in contenu or 'Message' in contenu or 'Notification' in contenu:
                    self.log_success(f"URLs de communication détectées dans: {fichier}")
                else:
                    self.log_warning(f"URLs de communication manquantes dans: {fichier}")
            else:
                self.log_error(f"Fichier URLs manquant: {fichier}")
    
    def analyser_vues_communication(self):
        """Analyser les vues de communication"""
        print("\n👁️ ANALYSE DES VUES DE COMMUNICATION")
        print("="*50)
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        fichiers_vues = [
            'communication/views.py',
            'agents/views.py',
            'assureur/views.py'
        ]
        
        for fichier in fichiers_vues:
            chemin = os.path.join(base_dir, fichier)
            if os.path.exists(chemin):
                with open(chemin, 'r') as f:
                    contenu = f.read()
                
                # Vérifier les imports de communication
                imports_comm = ['Message', 'Notification', 'Conversation', 'from communication']
                imports_trouves = [imp for imp in imports_comm if imp in contenu]
                
                if imports_trouves:
                    self.log_success(f"Imports communication dans {fichier}: {', '.join(imports_trouves)}")
                else:
                    self.log_warning(f"Aucun import communication dans {fichier}")
            else:
                self.log_warning(f"Fichier vues manquant: {fichier}")
    
    def analyser_templates_communication(self):
        """Analyser les templates de communication"""
        print("\n🎨 ANALYSE DES TEMPLATES DE COMMUNICATION")
        print("="*50)  # CORRECTION: Cette ligne avait une erreur de syntaxe
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        templates_comm = [
            'communication/templates/communication',
            'agents/templates/communication',
            'assureur/templates/communication'
        ]
        
        for template_dir in templates_comm:
            chemin = os.path.join(base_dir, template_dir)
            if os.path.exists(chemin):
                templates = os.listdir(chemin)
                if templates:
                    self.log_success(f"Templates trouvés dans {template_dir}: {len(templates)} fichiers")
                else:
                    self.log_warning(f"Dossier template vide: {template_dir}")
            else:
                self.log_warning(f"Dossier template manquant: {template_dir}")
    
    def generer_scripts_correction(self):
        """Générer les scripts de correction automatique"""
        print("\n🔧 GÉNÉRATION DES SCRIPTS DE CORRECTION")
        print("="*50)
        
        corrections = []
        
        # Script pour ajouter communication aux URLs agents
        corrections.append({
            'fichier': 'agents/urls.py',
            'description': 'Ajouter les URLs de communication aux agents',
            'code': '''
# Ajouter en haut du fichier
from communication import views as communication_views

# Ajouter dans urlpatterns
path('communication/', include('communication.urls')),
path('messages/', communication_views.liste_messages, name='liste_messages'),
path('notifications/', communication_views.liste_notifications, name='liste_notifications'),
'''
        })
        
        # Script pour ajouter communication aux URLs assureur
        corrections.append({
            'fichier': 'assureur/urls.py', 
            'description': 'Ajouter les URLs de communication à l\'assureur',
            'code': '''
# Ajouter en haut du fichier
from communication import views as communication_views

# Ajouter dans urlpatterns  
path('communication/', include('communication.urls')),
path('messages/', communication_views.liste_messages, name='liste_messages'),
path('notifications/', communication_views.liste_notifications, name='liste_notifications'),
'''
        })
        
        # Script pour ajouter les vues de communication aux agents
        corrections.append({
            'fichier': 'agents/views.py',
            'description': 'Ajouter les fonctions de communication aux vues agents',
            'code': '''
# Ajouter ces imports en haut
from communication.models import Message, Notification
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Ajouter ces vues
@login_required
def liste_messages_agent(request):
    """Afficher les messages de l'agent"""
    messages = Message.objects.filter(destinataire=request.user)
    return render(request, 'communication/liste_messages.html', {'messages': messages})

@login_required  
def liste_notifications_agent(request):
    """Afficher les notifications de l'agent"""
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'communication/liste_notifications.html', {'notifications': notifications})
'''
        })
        
        # Script pour ajouter les vues de communication à l'assureur
        corrections.append({
            'fichier': 'assureur/views.py',
            'description': 'Ajouter les fonctions de communication aux vues assureur',
            'code': '''
# Ajouter ces imports en haut
from communication.models import Message, Notification
from django.contrib.auth.decorators import login_required

# Ajouter ces vues
@login_required
def liste_messages_assureur(request):
    """Afficher les messages de l'assureur"""
    messages = Message.objects.filter(destinataire=request.user)
    return render(request, 'communication/liste_messages.html', {'messages': messages})

@login_required
def liste_notifications_assureur(request):
    """Afficher les notifications de l'assureur"""
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'communication/liste_notifications.html', {'notifications': notifications})
'''
        })
        
        for correction in corrections:
            print(f"\n📝 {correction['description']}")
            print(f"   📁 Fichier: {correction['fichier']}")
            print(f"   💻 Code à ajouter:\n{correction['code']}")
            
            # Vérifier si le fichier existe
            chemin_fichier = os.path.join(os.path.dirname(__file__), correction['fichier'])
            if os.path.exists(chemin_fichier):
                self.log_success(f"Fichier existe: {correction['fichier']}")
            else:
                self.log_error(f"Fichier manquant: {correction['fichier']}")
    
    def creer_fichiers_manquants(self):
        """Créer les fichiers manquants pour la communication"""
        print("\n🛠️ CRÉATION DES FICHIERS MANQUANTS")
        print("="*50)
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Structure à créer
        structure = {
            'agents/templates/communication': [
                'liste_messages.html',
                'liste_notifications.html', 
                'envoyer_message.html'
            ],
            'assureur/templates/communication': [
                'liste_messages.html',
                'liste_notifications.html',
                'envoyer_message.html'
            ]
        }
        
        for dossier, fichiers in structure.items():
            chemin_dossier = os.path.join(base_dir, dossier)
            
            # Créer le dossier s'il n'existe pas
            if not os.path.exists(chemin_dossier):
                os.makedirs(chemin_dossier, exist_ok=True)
                self.log_success(f"Dossier créé: {dossier}")
            
            # Créer les fichiers templates basiques
            for fichier in fichiers:
                chemin_fichier = os.path.join(chemin_dossier, fichier)
                if not os.path.exists(chemin_fichier):
                    with open(chemin_fichier, 'w') as f:
                        if 'messages' in fichier:
                            f.write('''{% extends "base.html" %}
{% block content %}
<h2>Messages</h2>
<div class="messages-list">
    {% for message in messages %}
    <div class="message-item">
        <strong>De:</strong> {{ message.expediteur.username }}<br>
        <strong>Date:</strong> {{ message.date_envoi }}<br>
        <p>{{ message.contenu }}</p>
    </div>
    {% empty %}
    <p>Aucun message.</p>
    {% endfor %}
</div>
{% endblock %}
''')
                        elif 'notifications' in fichier:
                            f.write('''{% extends "base.html" %}
{% block content %}
<h2>Notifications</h2>
<div class="notifications-list">
    {% for notification in notifications %}
    <div class="notification-item {% if not notification.est_lue %}non-lue{% endif %}">
        <strong>{{ notification.titre }}</strong><br>
        <p>{{ notification.message }}</p>
        <small>{{ notification.date_creation }}</small>
    </div>
    {% empty %}
    <p>Aucune notification.</p>
    {% endfor %}
</div>
{% endblock %}
''')
                        else:
                            f.write(f"<!-- Template {fichier} -->")
                    
                    self.log_success(f"Fichier créé: {dossier}/{fichier}")
    
    def verifier_migrations(self):
        """Vérifier l'état des migrations"""
        print("\n🔄 VÉRIFICATION DES MIGRATIONS")
        print("="*50)
        
        try:
            from django.core.management import execute_from_command_line
            from io import StringIO
            import sys
            
            # Capturer la sortie de showmigrations
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            try:
                execute_from_command_line(['manage.py', 'showmigrations', 'communication'])
                output = sys.stdout.getvalue()
            finally:
                sys.stdout = old_stdout
            
            if '] X' in output:
                self.log_warning("Migrations communication non appliquées")
            else:
                self.log_success("Migrations communication appliquées")
                
        except Exception as e:
            self.log_error(f"Erreur vérification migrations: {e}")
    
    def generer_rapport_configuration(self):
        """Générer un rapport complet de configuration"""
        print("\n" + "="*80)
        print("📊 RAPPORT DE CONFIGURATION COMMUNICATION")
        print("="*80)
        
        # Résumé
        print(f"\n🎯 RÉSUMÉ DE CONFIGURATION:")
        print(f"   • Tests réussis: {len(self.results['success'])}")
        print(f"   • Avertissements: {len(self.results['warnings'])}")
        print(f"   • Erreurs critiques: {len(self.results['errors'])}")
        
        # État des applications
        print(f"\n🔧 ÉTAT DES APPLICATIONS:")
        apps_etat = {
            'communication': '✅ Installée' if 'communication' in getattr(settings, 'INSTALLED_APPS', []) else '❌ NON installée',
            'agents': '✅ Installée' if 'agents' in getattr(settings, 'INSTALLED_APPS', []) else '❌ NON installée',
            'assureur': '✅ Installée' if 'assureur' in getattr(settings, 'INSTALLED_APPS', []) else '❌ NON installée'
        }
        
        for app, etat in apps_etat.items():
            print(f"   • {app}: {etat}")
        
        # Problèmes identifiés
        if self.results['errors']:
            print(f"\n❌ PROBLÈMES CRITIQUES:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        if self.results['warnings']:
            print(f"\n⚠️  PROBLÈMES À CORRIGER:")
            for warning in self.results['warnings']:
                print(f"   • {warning}")
        
        # Plan d'action
        print(f"\n🎯 PLAN D'ACTION POUR CORRECTION:")
        print("   1. 🔧 Ajouter 'communication' aux INSTALLED_APPS si manquant")
        print("   2. 🌐 Configurer les URLs dans agents/urls.py et assureur/urls.py")
        print("   3. 👁️ Ajouter les vues de communication aux agents/views.py et assureur/views.py")
        print("   4. 🎨 Créer les templates manquants")
        print("   5. 🔄 Appliquer les migrations: python manage.py migrate communication")
        print("   6. 🧪 Tester le système de communication")
        
        print(f"\n💡 RECOMMANDATIONS:")
        print("   • Utiliser les scripts de correction générés ci-dessus")
        print("   • Vérifier les permissions d'accès aux messages")
        print("   • Configurer les notifications automatiques par email")
        print("   • Tester tous les scénarios de communication")
        
        print(f"\n🕒 Analyse effectuée le: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
    
    def executer_analyse_complete(self):
        """Exécuter l'analyse complète de configuration"""
        print("🚀 ANALYSE DE CONFIGURATION COMMUNICATION AGENTS/ASSUREUR")
        print("="*60)
        
        # Étape 1: Analyse installation apps
        self.analyser_installation_apps()
        
        # Étape 2: Analyse fichiers
        self.analyser_fichiers_communication()
        
        # Étape 3: Analyse URLs
        self.analyser_urls_communication()
        
        # Étape 4: Analyse vues
        self.analyser_vues_communication()
        
        # Étape 5: Analyse templates
        self.analyser_templates_communication()
        
        # Étape 6: Vérification migrations
        self.verifier_migrations()
        
        # Étape 7: Génération corrections
        self.generer_scripts_correction()
        
        # Étape 8: Création fichiers manquants
        self.creer_fichiers_manquants()
        
        # Étape 9: Rapport final
        self.generer_rapport_configuration()
        
        return len(self.results['errors']) == 0

def main():
    """Fonction principale"""
    analyseur = AnalyseurConfigurationCommunication()
    succes = analyseur.executer_analyse_complete()
    
    if succes:
        print("\n🎉 CONFIGURATION VALIDÉE!")
        print("💡 La communication est correctement configurée")
        sys.exit(0)
    else:
        print("\n💥 CONFIGURATION INCOMPLÈTE")
        print("🔧 Suivre le plan d'action pour corriger les problèmes")
        sys.exit(1)

if __name__ == "__main__":
    main()