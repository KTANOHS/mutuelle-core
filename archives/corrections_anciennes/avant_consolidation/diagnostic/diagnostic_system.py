#!/usr/bin/env python
# diagnostic_system.py - Script complet de diagnostic du système

import os
import sys
import django
from pathlib import Path

# Ajouter le répertoire parent au chemin Python
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur lors du setup Django: {e}")
    sys.exit(1)

from django.core.management import execute_from_command_line
from django.conf import settings
from django.urls import reverse, resolve, Resolver404
from django.template.loader import get_template
from django.contrib.auth.models import User, Group
from django.apps import apps
from django.db import connection

def print_header(title):
    """Affiche un en-tête stylisé"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)

def check_django_setup():
    """Vérifie la configuration Django"""
    print_header("VÉRIFICATION DJANGO")
    
    try:
        # Vérifier les settings
        print(f"✅ Django version: {django.get_version()}")
        print(f"✅ BASE_DIR: {settings.BASE_DIR}")
        print(f"✅ DEBUG: {settings.DEBUG}")
        print(f"✅ Installed apps: {len(settings.INSTALLED_APPS)} apps")
        
        # Vérifier la base de données
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Connexion DB: OK")
            
    except Exception as e:
        print(f"❌ Erreur Django: {e}")
        return False
    return True

def check_templates():
    """Vérifie tous les templates"""
    print_header("VÉRIFICATION DES TEMPLATES")
    
    templates_to_check = [
        'base.html',
        'medecin/base.html',
        'pharmacien/base_pharmacien.html',
        'communication/detail_conversation.html',
        'communication/messagerie.html',
        'pharmacien/dashboard.html',
        'medecin/dashboard.html',
    ]
    
    missing = []
    existing = []
    
    for template in templates_to_check:
        try:
            template_obj = get_template(template)
            existing.append(f"✅ {template}")
        except Exception as e:
            missing.append(f"❌ {template}: {str(e)[:100]}")
    
    print("\n".join(existing))
    print("\n".join(missing))
    
    # Vérifier la structure des dossiers
    print("\n📁 Structure des templates:")
    templates_dir = BASE_DIR / 'templates'
    if templates_dir.exists():
        for root, dirs, files in os.walk(templates_dir):
            level = root.replace(str(templates_dir), '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files[:10]:  # Limiter à 10 fichiers par dossier
                if file.endswith('.html'):
                    print(f"{subindent}{file}")
            if len(files) > 10:
                print(f"{subindent}... et {len(files) - 10} autres fichiers")
    else:
        print("❌ Dossier templates/ introuvable")
    
    return len(missing) == 0

def check_urls():
    """Vérifie toutes les URLs"""
    print_header("VÉRIFICATION DES URLs")
    
    urls_to_check = [
        ('communication:detail_conversation', {'conversation_id': 1}),
        ('communication:messagerie', {}),
        ('pharmacien:dashboard', {}),
        ('medecin:dashboard', {}),
        ('communication:envoyer_message', {}),
        ('communication:envoyer_message_conversation', {'conversation_id': 1}),
    ]
    
    working = []
    broken = []
    
    for url_name, kwargs in urls_to_check:
        try:
            url = reverse(url_name, kwargs=kwargs)
            try:
                match = resolve(url)
                working.append(f"✅ {url_name} -> {url} (vue: {match.func.__name__})")
            except Resolver404:
                broken.append(f"⚠️  {url_name} -> {url} (résolution échouée)")
        except Exception as e:
            broken.append(f"❌ {url_name}: {str(e)[:100]}")
    
    print("\n".join(working))
    print("\n".join(broken))
    
    # Lister toutes les URLs
    print("\n🌐 URLs disponibles (extrait):")
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        url_patterns = []
        
        def list_urls(patterns, prefix=''):
            for pattern in patterns:
                if hasattr(pattern, 'pattern'):
                    if hasattr(pattern, 'name') and pattern.name:
                        url_patterns.append(f"  {prefix}/{pattern.pattern} -> {pattern.name}")
                    if hasattr(pattern, 'url_patterns'):
                        list_urls(pattern.url_patterns, f"{prefix}/{pattern.pattern}")
        
        list_urls(resolver.url_patterns)
        for pattern in url_patterns[:20]:  # Limiter l'affichage
            print(pattern)
        if len(url_patterns) > 20:
            print(f"  ... et {len(url_patterns) - 20} autres URLs")
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
    
    return len(broken) == 0

def check_models():
    """Vérifie tous les modèles"""
    print_header("VÉRIFICATION DES MODÈLES")
    
    models_to_check = [
        'communication.Conversation',
        'communication.Message',
        'pharmacien.Pharmacien',
        'medecin.Medecin',
        'agents.Agent',
    ]
    
    existing = []
    missing = []
    
    for model_name in models_to_check:
        try:
            model = apps.get_model(model_name)
            count = model.objects.count()
            existing.append(f"✅ {model_name}: {count} enregistrements")
            
            # Vérifier les champs
            fields = [f.name for f in model._meta.get_fields()]
            print(f"   Champs: {', '.join(fields[:10])}")
            if len(fields) > 10:
                print(f"   ... et {len(fields) - 10} autres champs")
                
        except Exception as e:
            missing.append(f"❌ {model_name}: {str(e)[:100]}")
    
    print("\n".join(existing))
    print("\n".join(missing))
    
    return len(missing) == 0

def check_users_groups():
    """Vérifie les utilisateurs et groupes"""
    print_header("UTILISATEURS ET GROUPES")
    
    try:
        # Compter les utilisateurs
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        print(f"👥 Utilisateurs: {total_users} total, {active_users} actifs")
        
        # Lister les utilisateurs avec leurs groupes
        print("\n📋 Liste des utilisateurs (max 10):")
        for user in User.objects.all()[:10]:
            groups = user.groups.all()
            group_names = [g.name for g in groups]
            print(f"  {user.username} ({user.email}) - Groupes: {', '.join(group_names) or 'Aucun'}")
        
        if total_users > 10:
            print(f"  ... et {total_users - 10} autres utilisateurs")
        
        # Vérifier les groupes
        print("\n🏷️  Groupes disponibles:")
        for group in Group.objects.all():
            count = group.user_set.count()
            print(f"  {group.name}: {count} utilisateur(s)")
        
        # Vérifier l'utilisateur courant (si possible)
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            # Essayer de trouver un pharmacien
            pharmacien_group = Group.objects.filter(name='Pharmacien').first()
            if pharmacien_group:
                pharmaciens = pharmacien_group.user_set.all()
                if pharmaciens:
                    print(f"\n👨‍⚕️  Pharmaciens trouvés: {pharmaciens.count()}")
                    for p in pharmaciens[:3]:
                        print(f"  - {p.username}")
        
        except Exception as e:
            print(f"⚠️  Erreur vérification groupes: {e}")
            
    except Exception as e:
        print(f"❌ Erreur vérification utilisateurs: {e}")
        return False
    
    return True

def check_migrations():
    """Vérifie l'état des migrations"""
    print_header("VÉRIFICATION DES MIGRATIONS")
    
    try:
        from django.db.migrations.executor import MigrationExecutor
        from django.db import connection
        
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        
        if plan:
            print(f"⚠️  Migrations en attente: {len(plan)}")
            for migration, _ in plan[:5]:
                print(f"  - {migration.app_label}.{migration.name}")
            if len(plan) > 5:
                print(f"  ... et {len(plan) - 5} autres")
        else:
            print("✅ Toutes les migrations sont appliquées")
            
        # Vérifier les migrations appliquées
        print("\n📊 Migrations appliquées (extrait):")
        applied = list(executor.loader.applied_migrations)
        for mig in applied[:10]:
            print(f"  {mig[0]}.{mig[1]}")
        if len(applied) > 10:
            print(f"  ... et {len(applied) - 10} autres")
            
    except Exception as e:
        print(f"❌ Erreur vérification migrations: {e}")
        return False
    
    return True

def check_static_files():
    """Vérifie les fichiers statiques"""
    print_header("VÉRIFICATION DES FICHIERS STATIQUES")
    
    try:
        static_dirs = []
        if hasattr(settings, 'STATICFILES_DIRS'):
            static_dirs = settings.STATICFILES_DIRS
        
        print(f"📁 Dossiers statiques configurés: {len(static_dirs)}")
        for i, static_dir in enumerate(static_dirs, 1):
            if os.path.exists(static_dir):
                print(f"  {i}. {static_dir} ✓")
                # Compter les fichiers
                count = sum(len(files) for _, _, files in os.walk(static_dir))
                print(f"     {count} fichiers trouvés")
            else:
                print(f"  {i}. {static_dir} ✗ (introuvable)")
        
        print(f"\n🌐 URL statique: {settings.STATIC_URL}")
        print(f"📦 Répertoire statique racine: {getattr(settings, 'STATIC_ROOT', 'Non défini')}")
        
    except Exception as e:
        print(f"⚠️  Erreur vérification fichiers statiques: {e}")
    
    return True

def check_communication_system():
    """Vérifie spécifiquement le système de communication"""
    print_header("DIAGNOSTIC SYSTÈME DE COMMUNICATION")
    
    issues = []
    
    try:
        from communication.models import Conversation, Message
        
        # 1. Vérifier les modèles
        conv_count = Conversation.objects.count()
        msg_count = Message.objects.count()
        print(f"💬 Conversations: {conv_count}")
        print(f"📨 Messages: {msg_count}")
        
        # 2. Vérifier les vues
        views_to_check = [
            'communication.views.detail_conversation',
            'communication.views.messagerie',
            'communication.views.envoyer_message',
            'communication.views.envoyer_message_conversation',
        ]
        
        for view_path in views_to_check:
            try:
                module_name, func_name = view_path.rsplit('.', 1)
                module = __import__(module_name, fromlist=[func_name])
                getattr(module, func_name)
                print(f"✅ Vue {func_name} trouvée")
            except Exception as e:
                issues.append(f"❌ Vue {func_name}: {str(e)[:100]}")
                print(f"❌ Vue {func_name}: {str(e)[:100]}")
        
        # 3. Vérifier les templates
        template_files = [
            'communication/detail_conversation.html',
            'communication/messagerie.html',
            'communication/conversations.html',
            'communication/nouveau_message.html',
        ]
        
        for template in template_files:
            template_path = BASE_DIR / 'templates' / template
            if template_path.exists():
                size = os.path.getsize(template_path)
                print(f"✅ Template {template}: {size} octets")
            else:
                issues.append(f"❌ Template {template} manquant")
                print(f"❌ Template {template} manquant")
        
        # 4. Vérifier une conversation spécifique (ID 5)
        try:
            conversation = Conversation.objects.filter(id=5).first()
            if conversation:
                messages = conversation.messages.count()
                participants = conversation.participants.count()
                print(f"\n🔍 Conversation #5:")
                print(f"   Messages: {messages}")
                print(f"   Participants: {participants}")
                
                # Vérifier l'accès
                try:
                    from django.contrib.auth.models import User
                    test_user = User.objects.first()
                    if test_user and test_user in conversation.participants.all():
                        print(f"   Accès utilisateur {test_user.username}: ✓")
                    else:
                        print(f"   ⚠️  L'utilisateur de test n'est pas participant")
                except:
                    pass
            else:
                print(f"⚠️  Conversation #5 non trouvée")
        except Exception as e:
            issues.append(f"❌ Erreur vérification conversation: {e}")
        
    except Exception as e:
        issues.append(f"❌ Erreur système communication: {e}")
        print(f"❌ Erreur système communication: {e}")
    
    if issues:
        print(f"\n⚠️  {len(issues)} problème(s) détecté(s) dans la communication")
        return False
    
    return True

def check_pharmacien_system():
    """Vérifie spécifiquement le système pharmacien"""
    print_header("DIAGNOSTIC SYSTÈME PHARMACIEN")
    
    try:
        # Vérifier si le modèle Pharmacien existe
        try:
            from pharmacien.models import Pharmacien
            count = Pharmacien.objects.count()
            print(f"💊 Pharmaciens enregistrés: {count}")
            
            if count > 0:
                for p in Pharmacien.objects.all()[:3]:
                    print(f"  - {p.user.username if p.user else 'Sans utilisateur'}")
        except Exception as e:
            print(f"⚠️  Modèle Pharmacien: {str(e)[:100]}")
        
        # Vérifier les vues
        try:
            from pharmacien import views
            views_list = ['dashboard', 'liste_ordonnances', 'historique']
            for view_name in views_list:
                if hasattr(views, view_name):
                    print(f"✅ Vue pharmacien.{view_name} trouvée")
                else:
                    print(f"❌ Vue pharmacien.{view_name} manquante")
        except Exception as e:
            print(f"⚠️  Erreur vérification vues pharmacien: {e}")
        
        # Vérifier les templates
        templates = ['pharmacien/dashboard.html', 'pharmacien/base_pharmacien.html']
        for template in templates:
            template_path = BASE_DIR / 'templates' / template
            if template_path.exists():
                print(f"✅ Template {template} trouvé")
            else:
                print(f"❌ Template {template} manquant")
                
    except Exception as e:
        print(f"❌ Erreur système pharmacien: {e}")
        return False
    
    return True

def check_medecin_system():
    """Vérifie spécifiquement le système médecin"""
    print_header("DIAGNOSTIC SYSTÈME MÉDECIN")
    
    try:
        # Vérifier si le modèle Medecin existe
        try:
            from medecin.models import Medecin
            count = Medecin.objects.count()
            print(f"👨‍⚕️  Médecins enregistrés: {count}")
            
            if count > 0:
                for m in Medecin.objects.all()[:3]:
                    print(f"  - {m.user.username if m.user else 'Sans utilisateur'}")
        except Exception as e:
            print(f"⚠️  Modèle Medecin: {str(e)[:100]}")
        
        # Vérifier les vues
        try:
            from medecin import views
            views_list = ['dashboard', 'creer_ordonnance', 'mes_ordonnances']
            for view_name in views_list:
                if hasattr(views, view_name):
                    print(f"✅ Vue medecin.{view_name} trouvée")
                else:
                    print(f"❌ Vue medecin.{view_name} manquante")
        except Exception as e:
            print(f"⚠️  Erreur vérification vues médecin: {e}")
        
        # Vérifier les templates
        templates = ['medecin/dashboard.html', 'medecin/base.html']
        for template in templates:
            template_path = BASE_DIR / 'templates' / template
            if template_path.exists():
                print(f"✅ Template {template} trouvé")
            else:
                print(f"❌ Template {template} manquant")
                
    except Exception as e:
        print(f"❌ Erreur système médecin: {e}")
        return False
    
    return True

def check_permissions():
    """Vérifie les permissions et décorateurs"""
    print_header("VÉRIFICATION DES PERMISSIONS")
    
    try:
        # Vérifier les fonctions utilitaires
        try:
            from core.utils import est_pharmacien, est_medecin, est_agent
            print("✅ Fonctions de permission trouvées:")
            print(f"  - est_pharmacien: {est_pharmacien}")
            print(f"  - est_medecin: {est_medecin}")
            print(f"  - est_agent: {est_agent}")
        except Exception as e:
            print(f"⚠️  Fonctions de permission: {str(e)[:100]}")
        
        # Vérifier les décorateurs
        decorators = ['pharmacien_required', 'medecin_required', 'agent_required']
        for decorator in decorators:
            try:
                # Chercher dans les views
                import communication.views as comm_views
                import pharmacien.views as pharma_views
                import medecin.views as medecin_views
                
                found = False
                for module in [comm_views, pharma_views, medecin_views]:
                    if hasattr(module, decorator):
                        print(f"✅ Décorateur {decorator} trouvé dans {module.__name__}")
                        found = True
                        break
                
                if not found:
                    print(f"⚠️  Décorateur {decorator} non trouvé")
                    
            except Exception as e:
                print(f"⚠️  Erreur vérification décorateur {decorator}: {e}")
                
    except Exception as e:
        print(f"❌ Erreur vérification permissions: {e}")
    
    return True

def generate_summary(results):
    """Génère un résumé du diagnostic"""
    print_header("📊 RÉSUMÉ DU DIAGNOSTIC")
    
    total_checks = len(results)
    passed_checks = sum(1 for _, passed in results if passed)
    failed_checks = total_checks - passed_checks
    
    print(f"✅ Tests réussis: {passed_checks}/{total_checks}")
    print(f"❌ Tests échoués: {failed_checks}/{total_checks}")
    
    if failed_checks > 0:
        print("\n⚠️  PROBLÈMES IDENTIFIÉS:")
        for check_name, passed in results:
            if not passed:
                print(f"  • {check_name}")
    
    print(f"\n📈 TAUX DE RÉUSSITE: {passed_checks/total_checks*100:.1f}%")
    
    if failed_checks == 0:
        print("\n🎉 Tous les tests sont passés avec succès !")
    else:
        print(f"\n🔧 {failed_checks} problème(s) à résoudre")

def run_diagnostics():
    """Exécute tous les diagnostics"""
    results = []
    
    # Liste des diagnostics à exécuter
    diagnostics = [
        ("Configuration Django", check_django_setup),
        ("Migrations", check_migrations),
        ("Modèles", check_models),
        ("Utilisateurs et groupes", check_users_groups),
        ("Templates", check_templates),
        ("URLs", check_urls),
        ("Fichiers statiques", check_static_files),
        ("Permissions", check_permissions),
        ("Système communication", check_communication_system),
        ("Système pharmacien", check_pharmacien_system),
        ("Système médecin", check_medecin_system),
    ]
    
    for name, func in diagnostics:
        try:
            print_header(f"EXÉCUTION: {name}")
            success = func()
            results.append((name, success))
        except Exception as e:
            print(f"❌ Erreur lors du diagnostic {name}: {e}")
            results.append((name, False))
    
    generate_summary(results)
    
    # Suggestions de correctifs
    print_header("💡 SUGGESTIONS")
    
    if any("communication" in name.lower() and not success for name, success in results):
        print("Problèmes de communication détectés:")
        print("1. Vérifiez que le template detail_conversation.html existe")
        print("2. Vérifiez la vue envoyer_message_conversation dans communication/views.py")
        print("3. Vérifiez l'URL dans communication/urls.py")
    
    if any("template" in name.lower() and not success for name, success in results):
        print("\nProblèmes de templates détectés:")
        print("1. Vérifiez les chemins des templates")
        print("2. Assurez-vous que base.html existe dans templates/")
    
    if any("migration" in name.lower() and not success for name, success in results):
        print("\nProblèmes de migrations détectés:")
        print("1. Exécutez: python manage.py makemigrations")
        print("2. Exécutez: python manage.py migrate")
    
    return all(success for _, success in results)

if __name__ == "__main__":
    print("🔍 LANCEMENT DU DIAGNOSTIC SYSTÈME")
    print(f"📁 Répertoire: {BASE_DIR}")
    print(f"🐍 Python: {sys.version}")
    
    try:
        success = run_diagnostics()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Diagnostic interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erreur fatale: {e}")
        sys.exit(1)