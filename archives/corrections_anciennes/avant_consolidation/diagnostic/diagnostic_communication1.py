#!/usr/bin/env python
# diagnostic_communication.py - Script complet de diagnostic
import os
import sys
import django
from pathlib import Path

# Ajouter le chemin du projet
project_path = Path(__file__).parent.parent
sys.path.append(str(project_path))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation de Django: {e}")
    sys.exit(1)

print("🔍 DIAGNOSTIC COMPLET - MODULE COMMUNICATION")
print("=" * 60)

# =============================================================================
# 1. VÉRIFICATION DES MODÈLES
# =============================================================================
print("\n📦 1. VÉRIFICATION DES MODÈLES")
print("-" * 40)

try:
    from communication import models
    from django.apps import apps
    from django.db import connection
    
    # Vérifier si le modèle est enregistré
    app_config = apps.get_app_config('communication')
    print(f"✅ Application 'communication' trouvée")
    
    # Lister tous les modèles de l'application
    print(f"📋 Modèles dans l'application:")
    for model in app_config.get_models():
        print(f"   • {model.__name__}")
        
        # Vérifier le nombre d'objets
        try:
            count = model.objects.count()
            print(f"     → {count} objet(s) en base")
            
            # Vérifier les 3 premiers objets
            if count > 0:
                sample = model.objects.all()[:3]
                for obj in sample:
                    print(f"       - {obj}")
        except Exception as e:
            print(f"     → ❌ Erreur: {e}")
    
    # Vérifier les champs du modèle Conversation
    print(f"\n🔍 Structure du modèle Conversation:")
    from communication.models import Conversation
    for field in Conversation._meta.fields:
        print(f"   • {field.name} ({field.get_internal_type()})")
    
except Exception as e:
    print(f"❌ Erreur lors de la vérification des modèles: {e}")

# =============================================================================
# 2. VÉRIFICATION DES VUES
# =============================================================================
print("\n👁️  2. VÉRIFICATION DES VUES")
print("-" * 40)

try:
    import inspect
    from communication import views
    
    # Lister toutes les vues
    print("📋 Vues disponibles dans communication.views:")
    for name, obj in inspect.getmembers(views):
        if inspect.isfunction(obj) and not name.startswith('_'):
            print(f"   • {name}()")
    
    # Vérifier les vues principales
    important_views = ['messagerie', 'envoyer_message_api', 'detail_conversation']
    print(f"\n🔍 Vérification des vues principales:")
    for view_name in important_views:
        if hasattr(views, view_name):
            print(f"   ✅ {view_name}() - Présente")
        else:
            print(f"   ❌ {view_name}() - Absente")
    
except Exception as e:
    print(f"❌ Erreur lors de la vérification des vues: {e}")

# =============================================================================
# 3. VÉRIFICATION DES URLS
# =============================================================================
print("\n🔗 3. VÉRIFICATION DES URLS")
print("-" * 40)

try:
    from django.urls import reverse, resolve, NoReverseMatch
    from communication.urls import urlpatterns
    
    print("📋 URLs définies dans communication.urls:")
    for pattern in urlpatterns:
        print(f"   • {pattern.pattern}")
        if hasattr(pattern, 'name') and pattern.name:
            print(f"     → Nom: {pattern.name}")
    
    # Tester les URLs importantes
    test_urls = [
        ('communication:messagerie', 'Messagerie principale'),
        ('communication:message_create', 'Création message'),
        ('communication:envoyer_message_api', 'API envoi message'),
        ('communication:detail_conversation', 'Détail conversation'),
    ]
    
    print(f"\n🔍 Test des URLs importantes:")
    for url_name, description in test_urls:
        try:
            url = reverse(url_name)
            print(f"   ✅ {url_name}: {url}")
        except NoReverseMatch:
            print(f"   ❌ {url_name}: Non trouvée")
    
except Exception as e:
    print(f"❌ Erreur lors de la vérification des URLs: {e}")

# =============================================================================
# 4. VÉRIFICATION DES TEMPLATES
# =============================================================================
print("\n🎨 4. VÉRIFICATION DES TEMPLATES")
print("-" * 40)

# Chemin des templates communication
templates_path = project_path / 'templates' / 'communication'

print(f"📂 Chemin des templates: {templates_path}")

if templates_path.exists():
    # Lister tous les templates
    print("📋 Templates disponibles:")
    for template_file in templates_path.glob('*.html'):
        print(f"   • {template_file.name}")
        # Vérifier la taille
        size = template_file.stat().st_size
        print(f"     → {size} octets")
    
    # Vérifier les templates principaux
    important_templates = ['messagerie.html', 'message_list.html', 'detail_conversation.html']
    print(f"\n🔍 Templates principaux:")
    for template_name in important_templates:
        template_file = templates_path / template_name
        if template_file.exists():
            print(f"   ✅ {template_name} - Présent")
        else:
            print(f"   ❌ {template_name} - Absent")
else:
    print(f"❌ Le répertoire des templates n'existe pas")

# =============================================================================
# 5. VÉRIFICATION DE LA BASE DE DONNÉES
# =============================================================================
print("\n🗄️  5. VÉRIFICATION DE LA BASE DE DONNÉES")
print("-" * 40)

try:
    from communication.models import Conversation, Message
    from django.contrib.auth.models import User
    
    # Vérifier les conversations
    conversations_count = Conversation.objects.count()
    print(f"📊 Conversations: {conversations_count}")
    
    if conversations_count > 0:
        print(f"   Détail des 5 premières conversations:")
        for conv in Conversation.objects.all()[:5]:
            participants = [p.username for p in conv.participants.all()]
            messages_count = conv.messages.count()
            print(f"   • ID {conv.id}: {participants} - {messages_count} message(s)")
    
    # Vérifier les messages
    messages_count = Message.objects.count()
    print(f"\n📨 Messages: {messages_count}")
    
    if messages_count > 0:
        print(f"   Derniers 5 messages:")
        for msg in Message.objects.all().order_by('-date_envoi')[:5]:
            print(f"   • ID {msg.id}: {msg.titre} - De {msg.expediteur} à {msg.destinataire}")
            print(f"     → Contenu: {msg.contenu[:50]}...")
    
    # Vérifier les utilisateurs avec conversations
    print(f"\n👥 Utilisateurs avec conversations:")
    users_with_conversations = User.objects.filter(
        conversation_participants__isnull=False
    ).distinct()
    
    for user in users_with_conversations[:10]:
        conv_count = user.conversation_participants.count()
        print(f"   • {user.username} ({user.get_full_name()}): {conv_count} conversation(s)")
    
except Exception as e:
    print(f"❌ Erreur lors de la vérification de la base de données: {e}")

# =============================================================================
# 6. VÉRIFICATION DES MIGRATIONS
# =============================================================================
print("\n🔄 6. VÉRIFICATION DES MIGRATIONS")
print("-" * 40)

try:
    from django.db.migrations.loader import MigrationLoader
    from django.db import connection
    
    loader = MigrationLoader(connection)
    
    # Vérifier les migrations de l'application communication
    app_migrations = loader.graph.nodes.get(('communication', None), {})
    
    print(f"📋 Migrations pour 'communication':")
    for migration_key in app_migrations:
        print(f"   • {migration_key[1]}")
    
    # Vérifier si des migrations sont en attente
    from django.core.management import call_command
    from io import StringIO
    
    output = StringIO()
    call_command('showmigrations', 'communication', stdout=output)
    output.seek(0)
    
    print(f"\n🔍 État des migrations:")
    lines = output.readlines()
    for line in lines:
        if '[ ]' in line or '[X]' in line:
            print(f"   {line.strip()}")
    
except Exception as e:
    print(f"❌ Erreur lors de la vérification des migrations: {e}")

# =============================================================================
# 7. VÉRIFICATION DES PERMISSIONS
# =============================================================================
print("\n🔐 7. VÉRIFICATION DES PERMISSIONS")
print("-" * 40)

try:
    from django.contrib.auth.models import Permission, Group
    from django.contrib.contenttypes.models import ContentType
    
    # Vérifier les permissions pour le modèle Message
    message_content_type = ContentType.objects.get_for_model(Message)
    message_permissions = Permission.objects.filter(content_type=message_content_type)
    
    print(f"📋 Permissions pour le modèle Message:")
    for perm in message_permissions:
        print(f"   • {perm.codename}: {perm.name}")
    
    # Vérifier les groupes
    print(f"\n👥 Groupes définis:")
    for group in Group.objects.all():
        print(f"   • {group.name}: {group.permissions.count()} permission(s)")
        for user in group.user_set.all()[:3]:
            print(f"     → {user.username}")
    
except Exception as e:
    print(f"❌ Erreur lors de la vérification des permissions: {e}")

# =============================================================================
# 8. TEST DE L'API
# =============================================================================
print("\n🌐 8. TEST DE L'API")
print("-" * 40)

try:
    from django.test import Client
    from django.contrib.auth.models import User
    
    # Créer un client de test
    client = Client()
    
    # Tester l'API publique
    print("🔗 Test de l'API publique:")
    
    # Tester /communication/api/public/test/
    response = client.get('/communication/api/public/test/')
    if response.status_code == 200:
        print(f"   ✅ /communication/api/public/test/ - {response.status_code}")
        print(f"     → Réponse: {response.json()}")
    else:
        print(f"   ❌ /communication/api/public/test/ - {response.status_code}")
    
    # Tester /communication/api/public/conversations/5/messages/
    response = client.get('/communication/api/public/conversations/5/messages/')
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ /communication/api/public/conversations/5/messages/ - {response.status_code}")
        print(f"     → {len(data.get('messages', []))} message(s)")
    else:
        print(f"   ❌ /communication/api/public/conversations/5/messages/ - {response.status_code}")
    
except Exception as e:
    print(f"❌ Erreur lors du test de l'API: {e}")

# =============================================================================
# 9. VÉRIFICATION DES FICHIERS
# =============================================================================
print("\n📁 9. VÉRIFICATION DES FICHIERS")
print("-" * 40)

# Lister les fichiers du module communication
communication_dir = project_path / 'communication'

print(f"📂 Structure du module communication:")
for root, dirs, files in os.walk(communication_dir):
    # Ignorer les répertoires __pycache__
    dirs[:] = [d for d in dirs if '__pycache__' not in d]
    
    level = root.replace(str(communication_dir), '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}📁 {os.path.basename(root) or "communication"}')
    
    subindent = ' ' * 2 * (level + 1)
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)
            print(f'{subindent}📄 {file} ({size} octets)')

# =============================================================================
# RÉSUMÉ DU DIAGNOSTIC
# =============================================================================
print("\n" + "=" * 60)
print("📊 RÉSUMÉ DU DIAGNOSTIC")
print("=" * 60)

try:
    from communication.models import Conversation, Message
    from django.contrib.auth.models import User
    
    stats = {
        'Utilisateurs': User.objects.count(),
        'Conversations': Conversation.objects.count(),
        'Messages': Message.objects.count(),
        'Templates communication': len(list(templates_path.glob('*.html'))) if templates_path.exists() else 0,
        'Vues définies': len([name for name, obj in inspect.getmembers(views) if inspect.isfunction(obj) and not name.startswith('_')]),
        'URLs configurées': len(urlpatterns),
    }
    
    for key, value in stats.items():
        print(f"• {key}: {value}")
    
    # Recommandations
    print(f"\n💡 RECOMMANDATIONS:")
    
    if stats['Conversations'] == 0:
        print("  ⚠️  Créer des conversations de test")
    
    if stats['Templates communication'] < 5:
        print("  ⚠️  Vérifier les templates manquants")
    
    if stats['Vues définies'] < 10:
        print("  ⚠️  Vérifier l'implémentation des vues")
    
    print(f"\n✅ Diagnostic terminé avec succès!")
    print(f"📍 Projet: {project_path}")
    
except Exception as e:
    print(f"❌ Erreur lors du résumé: {e}")

print("\n" + "=" * 60)
print("🎯 POUR EXÉCUTER CE DIAGNOSTIC:")
print("python diagnostic_communication.py")
print("=" * 60)