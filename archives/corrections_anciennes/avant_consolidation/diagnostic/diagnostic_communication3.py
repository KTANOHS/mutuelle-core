#!/usr/bin/env python3
"""
SCRIPT DE DIAGNOSTIC DU SYSTÈME DE COMMUNICATION - VERSION CORRIGÉE
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.urls import reverse, NoReverseMatch
from django.conf import settings

def print_header(title):
    """Affiche un en-tête de section"""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)

def check_sessions():
    """Vérifie les sessions actives"""
    print_header("SESSIONS ACTIVES")
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    print(f"   {sessions.count()} session(s) active(s)")
    
    for session in sessions[:10]:  # Afficher seulement 10 sessions
        session_data = session.get_decoded()
        if session_data:
            print(f"   - Session {session.session_key}: {session_data}")

def check_users():
    """Vérifie les utilisateurs"""
    print_header("UTILISATEURS")
    
    total_users = User.objects.count()
    print(f"   Total utilisateurs: {total_users}")
    
    # Utilisateurs dans le groupe 'assureur'
    try:
        assureur_group = Group.objects.get(name='assureur')
        assureurs = assureur_group.user_set.all()
        print(f"   {assureurs.count()} assureur(s) trouvé(s)")
        
        for user in assureurs[:5]:  # Afficher seulement 5 assureurs
            print(f"   - {user.username} ({user.get_full_name()})")
    except Group.DoesNotExist:
        print("   ❌ Groupe 'assureur' non trouvé")

def check_communication_models():
    """Vérifie les modèles de communication"""
    print_header("MODÈLES DE COMMUNICATION")
    
    try:
        from communication.models import Message, Conversation, Notification
        
        # Messages
        messages = Message.objects.all()
        print(f"   Messages: {messages.count()}")
        
        # Afficher les 5 derniers messages
        for msg in messages.order_by('-date_envoi')[:5]:
            print(f"   - Message {msg.id}: {msg.expediteur} -> {msg.destinataire}")
            if hasattr(msg, 'objet'):
                print(f"     Objet: {msg.objet}")
            elif hasattr(msg, 'sujet'):
                print(f"     Sujet: {msg.sujet}")
            if hasattr(msg, 'contenu'):
                print(f"     Contenu: {msg.contenu[:50]}...")
        
        # Conversations
        conversations = Conversation.objects.all()
        print(f"   Conversations: {conversations.count()}")
        
        # Notifications
        notifications = Notification.objects.all()
        print(f"   Notifications: {notifications.count()}")
        
    except ImportError as e:
        print(f"   ❌ Erreur d'importation: {e}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

def check_templates():
    """Vérifie les templates"""
    print_header("TEMPLATES")
    
    templates_to_check = [
        'communication/messagerie.html',
        'communication/envoyer_message.html',
        'assureur/communication/messagerie.html',
        'assureur/communication/envoyer_message.html',
    ]
    
    for template in templates_to_check:
        template_path = os.path.join(settings.BASE_DIR, 'templates', template)
        if os.path.exists(template_path):
            print(f"   ✅ {template} existe")
        else:
            print(f"   ❌ {template} manquant")

def check_urls():
    """Vérifie les URLs"""
    print_header("URLS")
    
    urls_to_check = [
        ('communication:messagerie', 'Messagerie communication'),
        ('communication:envoyer_message', 'Envoyer message communication'),
        ('assureur:messagerie_assureur', 'Messagerie assureur'),
        ('assureur:envoyer_message_assureur', 'Envoyer message assureur'),
    ]
    
    for url_name, description in urls_to_check:
        try:
            path = reverse(url_name)
            print(f"   ✅ {description}: {path}")
        except NoReverseMatch as e:
            print(f"   ❌ {description}: {e}")

def check_views():
    """Vérifie les vues"""
    print_header("VUES")
    
    views_to_check = [
        ('communication.views', 'messagerie'),
        ('communication.views', 'envoyer_message'),
        ('assureur.views', 'messagerie_assureur'),
        ('assureur.views', 'envoyer_message_assureur'),
    ]
    
    for module_name, view_name in views_to_check:
        try:
            module = __import__(module_name, fromlist=[view_name])
            view_func = getattr(module, view_name)
            print(f"   ✅ {module_name}.{view_name} existe")
            
            # Vérifier si la vue utilise la variable 'participants'
            import inspect
            source_code = inspect.getsource(view_func)
            if 'participants' in source_code:
                print(f"     → Utilise la variable 'participants'")
            else:
                print(f"     ⚠️  N'utilise pas la variable 'participants'")
                
        except ImportError as e:
            print(f"   ❌ {module_name}.{view_name}: {e}")
        except AttributeError:
            print(f"   ❌ {module_name}.{view_name} n'existe pas")

def check_menu():
    """Vérifie l'intégration dans le menu"""
    print_header("INTÉGRATION MENU")
    
    template_path = os.path.join(settings.BASE_DIR, 'templates', 'assureur', 'base_assureur.html')
    if os.path.exists(template_path):
        with open(template_path, 'r') as f:
            content = f.read()
            
            # Vérifier le lien vers la messagerie
            if 'messagerie_assureur' in content:
                print("   ✅ Lien 'Communication' présent dans le menu")
            else:
                print("   ❌ Lien 'Communication' absent du menu")
                
            # Vérifier l'icône enveloppe
            if 'fa-envelope' in content:
                print("   ✅ Icône enveloppe présente")
            else:
                print("   ❌ Icône enveloppe absente")
    else:
        print(f"   ❌ Template base_assureur.html non trouvé: {template_path}")

def check_database_schema():
    """Vérifie le schéma de la base de données"""
    print_header("SCHÉMA BASE DE DONNÉES")
    
    try:
        from communication.models import Message
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info(communication_message)")
            columns = cursor.fetchall()
            print(f"   Table 'communication_message' a {len(columns)} colonnes:")
            for col in columns:
                print(f"     - {col[1]} ({col[2]})")
                
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

def diagnose_participants_issue():
    """Diagnostique spécifiquement le problème de la variable participants"""
    print_header("DIAGNOSTIC VARIABLE 'PARTICIPANTS'")
    
    # 1. Vérifier la vue communication.views.messagerie
    try:
        from communication.views import messagerie
        import inspect
        
        # Obtenir le code source
        source = inspect.getsource(messagerie)
        
        # Chercher la définition du contexte
        lines = source.split('\n')
        in_context = False
        context_vars = []
        
        for line in lines:
            if 'context = {' in line:
                in_context = True
            elif in_context and '}' in line:
                in_context = False
            
            if in_context and ':' in line and 'context' not in line:
                var_name = line.split(':')[0].strip().strip("'").strip('"')
                context_vars.append(var_name)
        
        print(f"   Variables dans le contexte de messagerie: {', '.join(context_vars)}")
        
        if 'participants' in context_vars:
            print("   ✅ 'participants' est dans le contexte")
        else:
            print("   ❌ 'participants' n'est PAS dans le contexte")
            
    except Exception as e:
        print(f"   ❌ Erreur analyse vue: {e}")
    
    # 2. Vérifier le template
    template_path = os.path.join(settings.BASE_DIR, 'templates', 'communication', 'messagerie.html')
    if os.path.exists(template_path):
        with open(template_path, 'r') as f:
            content = f.read()
            
            if '{{ participants' in content:
                print("   ✅ Template utilise 'participants'")
                
                # Compter les occurrences
                count = content.count('{{ participants')
                print(f"   → {count} occurrence(s) de 'participants' dans le template")
            else:
                print("   ⚠️  Template n'utilise pas 'participants'")

def main():
    """Fonction principale"""
    print_header("DIAGNOSTIC COMPLET DU SYSTÈME DE COMMUNICATION")
    print(f"Django {django.get_version()}")
    print(f"Répertoire: {settings.BASE_DIR}")
    
    check_sessions()
    check_users()
    check_communication_models()
    check_templates()
    check_urls()
    check_views()
    check_menu()
    check_database_schema()
    diagnose_participants_issue()
    
    print_header("RECOMMANDATIONS")
    
    print("""
    1. VÉRIFIER LA VUE communication.views.messagerie:
       - S'assurer qu'elle inclut 'participants' dans le contexte
       - Vérifier que 'active_conversation' n'est jamais None
    
    2. VÉRIFIER LE TEMPLATE communication/messagerie.html:
       - S'assurer qu'il vérifie si 'active_conversation' existe avant d'y accéder
    
    3. SOLUTION RAPIDE:
       - Modifier la vue pour toujours inclure 'participants' dans le contexte
       - Utiliser une valeur par défaut dans le template: {{ active_conversation|default:"" }}
    
    4. TESTS:
       - Accéder à http://localhost:8000/communication/messagerie/
       - Accéder à http://localhost:8000/assureur/communication/
    """)

if __name__ == "__main__":
    main()