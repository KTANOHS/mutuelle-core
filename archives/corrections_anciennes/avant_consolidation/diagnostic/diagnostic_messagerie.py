# diagnostic_messagerie.py
import os
import sys
import django
from django.urls import reverse, resolve, NoReverseMatch
from django.core.management import execute_from_command_line

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostiquer_erreur_liste_messages():
    """
    Script complet de diagnostic pour l'erreur 'liste_messages' not found
    """
    print("=" * 80)
    print("DIAGNOSTIC ERREUR 'liste_messages' NOT FOUND")
    print("=" * 80)
    
    # 1. Vérifier les URLs de l'application communication
    print("\n1. VÉRIFICATION DES URLs COMMUNICATION")
    print("-" * 40)
    
    try:
        from django.conf import settings
        from importlib import import_module
        
        # Vérifier si l'application communication est installée
        if 'communication' in settings.INSTALLED_APPS:
            print("✓ Application 'communication' trouvée dans INSTALLED_APPS")
            
            # Essayer d'importer les URLs de communication
            try:
                communication_urls = import_module('communication.urls')
                print("✓ Module communication.urls importé avec succès")
                
                # Vérifier les patterns d'URL
                if hasattr(communication_urls, 'urlpatterns'):
                    url_count = len(communication_urls.urlpatterns)
                    print(f"✓ {url_count} pattern(s) URL trouvé(s) dans communication.urls")
                    
                    # Lister tous les noms d'URL
                    url_names = []
                    for pattern in communication_urls.urlpatterns:
                        if hasattr(pattern, 'name') and pattern.name:
                            url_names.append(pattern.name)
                        elif hasattr(pattern, 'url_patterns'):
                            for subpattern in pattern.url_patterns:
                                if hasattr(subpattern, 'name') and subpattern.name:
                                    url_names.append(subpattern.name)
                    
                    print(f"✓ Noms d'URL trouvés: {url_names}")
                    
                    if 'liste_messages' in url_names:
                        print("✓ 'liste_messages' trouvé dans les URLs!")
                    else:
                        print("✗ 'liste_messages' NON trouvé dans les URLs")
                        
                else:
                    print("✗ Aucun urlpatterns trouvé dans communication.urls")
                    
            except ImportError as e:
                print(f"✗ Erreur d'importation de communication.urls: {e}")
        else:
            print("✗ Application 'communication' NON trouvée dans INSTALLED_APPS")
            
    except Exception as e:
        print(f"✗ Erreur lors de la vérification des URLs: {e}")

    # 2. Vérifier la résolution d'URL
    print("\n2. TEST DE RÉSOLUTION D'URL")
    print("-" * 40)
    
    # Tester différentes variations du nom d'URL
    test_names = [
        'liste_messages',
        'communication:liste_messages',
        'agents:liste_messages',
        'communication_liste_messages'
    ]
    
    for name in test_names:
        try:
            url = reverse(name)
            print(f"✓ reverse('{name}') = {url}")
        except NoReverseMatch as e:
            print(f"✗ reverse('{name}') échoue: {e}")

    # 3. Vérifier les vues
    print("\n3. VÉRIFICATION DES VUES")
    print("-" * 40)
    
    try:
        from communication.views import liste_messages
        print("✓ Vue 'liste_messages' importée depuis communication.views")
        print(f"  Emplacement: {liste_messages.__module__}.{liste_messages.__name__}")
    except ImportError as e:
        print(f"✗ Erreur d'importation de la vue: {e}")

    # 4. Vérifier la structure des URLs principales
    print("\n4. STRUCTURE DES URLs PRINCIPALES")
    print("-" * 40)
    
    try:
        # Vérifier le fichier urls.py principal
        from mutuelle_core import urls as main_urls
        print("✓ Fichier urls.py principal trouvé")
        
        # Compter les patterns inclus
        included_patterns = 0
        for pattern in main_urls.urlpatterns:
            if hasattr(pattern, 'app_name'):
                print(f"  - Application incluse: {pattern.app_name}")
                included_patterns += 1
                
        print(f"  Total des applications incluses: {included_patterns}")
        
    except Exception as e:
        print(f"✗ Erreur avec les URLs principales: {e}")

    # 5. Vérifier les templates problématiques
    print("\n5. RECHERCHE D'UTILISATION DANS LES TEMPLATES")
    print("-" * 40)
    
    template_dirs = []
    if hasattr(settings, 'TEMPLATES'):
        for template_config in settings.TEMPLATES:
            if 'DIRS' in template_config:
                template_dirs.extend(template_config['DIRS'])
    
    # Recherche simplifiée des templates (vous devrez peut-être adapter ceci)
    print("  Recherche de 'liste_messages' dans les templates...")
    print("  (Cette recherche peut nécessiter une adaptation manuelle)")

    # 6. Solution d'urgence
    print("\n6. SOLUTIONS IMMÉDIATES")
    print("-" * 40)
    
    print("a) URL temporaire directe:")
    print('   <a href="/communication/messages/">Liste des messages</a>')
    
    print("\nb) Vérifier le fichier urls.py de communication:")
    print("   Assurez-vous d'avoir:")
    print("   path('messages/', views.liste_messages, name='liste_messages')")
    
    print("\nc) Vérifier l'inclusion dans les URLs principales:")
    print("   path('communication/', include('communication.urls'))")

    # 7. Test de création d'URL d'urgence
    print("\n7. TEST DE CRÉATION D'URL D'URGENCE")
    print("-" * 40)
    
    try:
        # Essayer de créer une URL de secours
        from django.urls import path
        from communication import views
        
        url_pattern_urgence = path('messages-urgence/', views.liste_messages, name='liste_messages_urgence')
        print("✓ URL de secours créée: 'liste_messages_urgence'")
        print("  Utilisez: {% url 'liste_messages_urgence' %}")
    except Exception as e:
        print(f"✗ Erreur création URL secours: {e}")

def verifier_urls_existantes():
    """
    Lister toutes les URLs disponibles dans le projet
    """
    print("\n" + "=" * 80)
    print("LISTE COMPLÈTE DES URLs DISPONIBLES")
    print("=" * 80)
    
    try:
        from django.core.management import execute_from_command_line
        from io import StringIO
        import sys
        
        # Capturer la sortie de show_urls
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            execute_from_command_line(['manage.py', 'show_urls'])
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout
            
        # Filtrer les URLs intéressantes
        lines = output.split('\n')
        for line in lines:
            if 'message' in line.lower() or 'communication' in line.lower():
                print(line)
                
    except Exception as e:
        print(f"Erreur lors de la récupération des URLs: {e}")

def generer_correction_urls():
    """
    Générer le code de correction pour les URLs
    """
    print("\n" + "=" * 80)
    print("CORRECTION RECOMMANDÉE POUR urls.py")
    print("=" * 80)
    
    correction_code = '''
# Fichier: communication/urls.py
from django.urls import path
from . import views

app_name = 'communication'  # Namespace important

urlpatterns = [
    # URLs pour les messages
    path('messages/', views.liste_messages, name='liste_messages'),
    path('messages/envoyer/', views.envoyer_message, name='envoyer_message'),
    path('messages/<int:message_id>/', views.detail_message, name='detail_message'),
    path('messages/<int:message_id>/supprimer/', views.supprimer_message, name='supprimer_message'),
    
    # URLs pour les conversations
    path('conversations/', views.conversations, name='conversations'),
    path('conversations/<int:conversation_id>/', views.detail_conversation, name='detail_conversation'),
    
    # URLs pour les notifications
    path('notifications/', views.liste_notifications, name='liste_notifications'),
    path('notifications/<int:notification_id>/marquer-lue/', views.marquer_notification_lue, name='marquer_notification_lue'),
    
    # URLs API
    path('api/conversations/', views.api_conversations, name='api_conversations'),
    path('api/messages/<int:conversation_id>/', views.api_messages, name='api_messages'),
    path('api/notifications/count/', views.notification_non_lue_count, name='notification_count'),
]

# Fichier: mutuelle_core/urls.py (principal)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('communication/', include('communication.urls')),  # Inclure les URLs de communication
    # ... autres inclusions
]
'''
    print(correction_code)

def verifier_utilisation_template():
    """
    Vérifier comment 'liste_messages' est utilisé dans les templates
    """
    print("\n" + "=" * 80)
    print("VÉRIFICATION DES USAGES TEMPLATE")
    print("=" * 80)
    
    print("Recherchez dans vos templates les utilisations de:")
    print("1. {% url 'liste_messages' %}")
    print("2. {% url 'communication:liste_messages' %}")
    print("3. {% url 'agents:liste_messages' %}")
    print("4. Toute autre variation")
    
    print("\nSi vous utilisez un namespace, assurez-vous que:")
    print("- Votre urls.py a: app_name = 'communication'")
    print("- Vos templates utilisent: {% url 'communication:liste_messages' %}")

if __name__ == "__main__":
    diagnostiquer_erreur_liste_messages()
    verifier_urls_existantes()
    generer_correction_urls()
    verifier_utilisation_template()
    
    print("\n" + "=" * 80)
    print("DIAGNOSTIC TERMINÉ")
    print("=" * 80)