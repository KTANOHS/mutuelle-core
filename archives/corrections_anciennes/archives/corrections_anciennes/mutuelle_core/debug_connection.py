"""
Script d'analyse des problèmes de connexion et redirection - VERSION CORRIGÉE
Usage: python manage.py shell < debug_connection.py
"""
import os
import django
import sys

# Configuration Django AVANT tout import
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

from django.conf import settings
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User, Group
from django.core.management import call_command

def analyze_connection_issues():
    print("=" * 80)
    print("🔍 ANALYSE DES PROBLÈMES DE CONNEXION")
    print("=" * 80)
    
    # 1. Vérification de la configuration
    print("\n1. 📋 CONFIGURATION DE SÉCURITÉ")
    print("-" * 40)
    
    security_settings = [
        ('DEBUG', settings.DEBUG),
        ('SESSION_COOKIE_SECURE', getattr(settings, 'SESSION_COOKIE_SECURE', 'Non défini')),
        ('CSRF_COOKIE_SECURE', getattr(settings, 'CSRF_COOKIE_SECURE', 'Non défini')),
        ('SESSION_COOKIE_HTTPONLY', getattr(settings, 'SESSION_COOKIE_HTTPONLY', 'Non défini')),
        ('CSRF_COOKIE_HTTPONLY', getattr(settings, 'CSRF_COOKIE_HTTPONLY', 'Non défini')),
        ('SESSION_COOKIE_SAMESITE', getattr(settings, 'SESSION_COOKIE_SAMESITE', 'Non défini')),
        ('CSRF_COOKIE_SAMESITE', getattr(settings, 'CSRF_COOKIE_SAMESITE', 'Non défini')),
        ('SESSION_COOKIE_AGE', getattr(settings, 'SESSION_COOKIE_AGE', 'Non défini')),
        ('LOGIN_URL', getattr(settings, 'LOGIN_URL', 'Non défini')),
        ('LOGIN_REDIRECT_URL', getattr(settings, 'LOGIN_REDIRECT_URL', 'Non défini')),
        ('LOGOUT_REDIRECT_URL', getattr(settings, 'LOGOUT_REDIRECT_URL', 'Non défini')),
    ]
    
    for setting, value in security_settings:
        # Logique de statut simplifiée
        if setting in ['SESSION_COOKIE_SECURE', 'CSRF_COOKIE_SECURE']:
            status = "⚠️  À vérifier" if value and settings.DEBUG else "✅ OK"
        else:
            status = "✅ OK"
        print(f"{setting}: {value} {status}")
    
    # 2. Vérification des sessions actives
    print("\n2. 🔐 SESSIONS ACTIVES")
    print("-" * 40)
    
    try:
        active_sessions = Session.objects.count()
        print(f"Sessions actives en base: {active_sessions}")
    except Exception as e:
        print(f"❌ Erreur accès sessions: {e}")
    
    # 3. Vérification des utilisateurs et groupes
    print("\n3. 👥 UTILISATEURS ET GROUPES")
    print("-" * 40)
    
    try:
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        print(f"Utilisateurs totaux: {total_users}")
        print(f"Utilisateurs actifs: {active_users}")
        
        # Liste des groupes et leurs membres
        groups = Group.objects.all()
        print("\nGroupes existants:")
        for group in groups:
            members_count = group.user_set.count()
            print(f"  - {group.name}: {members_count} membres")
            
    except Exception as e:
        print(f"❌ Erreur accès utilisateurs: {e}")
    
    # 4. Vérification des URLs de redirection
    print("\n4. 🧭 URLS DE REDIRECTION")
    print("-" * 40)
    
    try:
        from mutuelle_core.views import get_user_redirect_url
        
        print("Test des redirections par groupe:")
        for group in Group.objects.all():
            # Créer un utilisateur test pour ce groupe
            test_user = User.objects.filter(groups=group).first()
            if test_user:
                redirect_url = get_user_redirect_url(test_user)
                print(f"  - {group.name}: {redirect_url}")
        
        # Test superuser
        superuser = User.objects.filter(is_superuser=True).first()
        if superuser:
            redirect_url = get_user_redirect_url(superuser)
            print(f"  - Superuser: {redirect_url}")
            
    except Exception as e:
        print(f"❌ Erreur test redirections: {e}")
    
    # 5. Vérification des middlewares
    print("\n5. ⚙️  MIDDLEWARES CONFIGURÉS")
    print("-" * 40)
    
    try:
        for i, middleware in enumerate(settings.MIDDLEWARE):
            print(f"  {i+1}. {middleware}")
    except Exception as e:
        print(f"❌ Erreur accès middlewares: {e}")
    
    # 6. Vérification des templates
    print("\n6. 🎨 TEMPLATES DE CONNEXION")
    print("-" * 40)
    
    try:
        template_dirs = settings.TEMPLATES[0]['DIRS']
        print("Dossiers de templates:")
        for dir in template_dirs:
            exists = os.path.exists(dir)
            status = "✅ Existe" if exists else "❌ Manquant"
            print(f"  - {dir} {status}")
        
        # Vérifier si le template login existe
        login_template_path = os.path.join(template_dirs[0], 'registration', 'login.html')
        login_exists = os.path.exists(login_template_path)
        print(f"Template login.html: {'✅ Trouvé' if login_exists else '❌ Manquant'}")
        
    except Exception as e:
        print(f"❌ Erreur vérification templates: {e}")
    
    # 7. Analyse des problèmes courants
    print("\n7. 🚨 DIAGNOSTIC DES PROBLÈMES COURANTS")
    print("-" * 40)
    
    issues = []
    
    try:
        # Vérifier CSRF
        if 'django.middleware.csrf.CsrfViewMiddleware' not in settings.MIDDLEWARE:
            issues.append("❌ Middleware CSRF manquant")
        
        # Vérifier sessions
        if 'django.contrib.sessions.middleware.SessionMiddleware' not in settings.MIDDLEWARE:
            issues.append("❌ Middleware Session manquant")
        
        # Vérifier authentication
        if 'django.contrib.auth.middleware.AuthenticationMiddleware' not in settings.MIDDLEWARE:
            issues.append("❌ Middleware Authentication manquant")
        
        # Vérifier la configuration SameSite
        same_site = getattr(settings, 'SESSION_COOKIE_SAMESITE', None)
        if same_site == 'None':
            issues.append("⚠️  SESSION_COOKIE_SAMESITE='None' peut causer des problèmes")
        
        if issues:
            for issue in issues:
                print(issue)
        else:
            print("✅ Aucun problème critique détecté")
            
    except Exception as e:
        print(f"❌ Erreur diagnostic: {e}")
    
    # 8. Recommandations
    print("\n8. 💡 RECOMMANDATIONS")
    print("-" * 40)
    
    recommendations = []
    
    if settings.DEBUG:
        recommendations.append("• En développement, utiliser SESSION_COOKIE_SECURE=False")
        recommendations.append("• En développement, utiliser CSRF_COOKIE_SECURE=False")
        recommendations.append("• Tester en navigation privée pour éviter les cookies corrompus")
    
    if getattr(settings, 'SESSION_COOKIE_SAMESITE', 'Lax') != 'Lax':
        recommendations.append("• Utiliser SESSION_COOKIE_SAMESITE='Lax' pour une meilleure compatibilité")
    
    for rec in recommendations:
        print(rec)

def test_user_redirections():
    """Test des redirections pour différents types d'utilisateurs"""
    print("\n" + "=" * 80)
    print("🧪 TEST DES REDIRECTIONS PAR UTILISATEUR")
    print("=" * 80)
    
    try:
        from mutuelle_core.views import get_user_redirect_url
        
        # Test avec différents scénarios
        test_cases = [
            ("Superuser", User.objects.filter(is_superuser=True).first()),
            ("Assureur", User.objects.filter(groups__name='Assureur').first()),
            ("Medecin", User.objects.filter(groups__name='Medecin').first()),
            ("Pharmacien", User.objects.filter(groups__name='Pharmacien').first()),
            ("Membre", User.objects.filter(groups__name='Membre').first()),
            ("Utilisateur sans groupe", User.objects.filter(groups__isnull=True).first()),
        ]
        
        for user_type, user in test_cases:
            if user:
                redirect_url = get_user_redirect_url(user)
                status = "✅" if redirect_url else "❌"
                print(f"{status} {user_type}: {user.username} -> {redirect_url}")
            else:
                print(f"⚠️  {user_type}: Aucun utilisateur trouvé")
                
    except Exception as e:
        print(f"❌ Erreur test redirections: {e}")

def check_session_data():
    """Vérifie les données de session problématiques"""
    print("\n" + "=" * 80)
    print("📊 ANALYSE DES SESSIONS")
    print("=" * 80)
    
    try:
        sessions = Session.objects.all()[:5]  # Premières 5 sessions
        
        for i, session in enumerate(sessions):
            session_data = session.get_decoded()
            print(f"\nSession {i+1}:")
            print(f"  Clé: {session.session_key}")
            print(f"  Expire: {session.expire_date}")
            print(f"  Données: {session_data}")
            
    except Exception as e:
        print(f"❌ Erreur analyse sessions: {e}")

if __name__ == "__main__":
    # Exécution des analyses
    analyze_connection_issues()
    test_user_redirections()
    check_session_data()
    
    print("\n" + "=" * 80)
    print("🎯 ACTIONS IMMÉDIATES")
    print("=" * 80)
    print("1. Nettoyer les cookies du navigateur")
    print("2. Tester en navigation privée")
    print("3. Vérifier les logs Django pour les erreurs CSRF")
    print("4. S'assurer que tous les groupes d'utilisateurs existent")
    print("5. Vérifier que les URLs de redirection sont accessibles")