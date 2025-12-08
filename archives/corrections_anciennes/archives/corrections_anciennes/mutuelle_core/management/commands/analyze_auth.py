from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.sessions.models import Session
import os

class Command(BaseCommand):
    help = 'Analyse les problèmes d\'authentification et de redirection'
    
    def handle(self, *args, **options):
        self.stdout.write("=" * 80)
        self.stdout.write("🔍 ANALYSE DES PROBLÈMES DE CONNEXION - COMMANDE MANAGEMENT")
        self.stdout.write("=" * 80)
        
        self.analyze_configuration()
        self.analyze_users_groups()
        self.analyze_redirections()
        self.analyze_sessions()
        self.give_recommendations()
    
    def analyze_configuration(self):
        self.stdout.write("\n1. 📋 CONFIGURATION DE SÉCURITÉ")
        self.stdout.write("-" * 40)
        
        security_settings = [
            ('DEBUG', settings.DEBUG),
            ('SESSION_COOKIE_SECURE', getattr(settings, 'SESSION_COOKIE_SECURE', 'Non défini')),
            ('CSRF_COOKIE_SECURE', getattr(settings, 'CSRF_COOKIE_SECURE', 'Non défini')),
            ('SESSION_COOKIE_HTTPONLY', getattr(settings, 'SESSION_COOKIE_HTTPONLY', 'Non défini')),
            ('CSRF_COOKIE_HTTPONLY', getattr(settings, 'CSRF_COOKIE_HTTPONLY', 'Non défini')),
            ('SESSION_COOKIE_SAMESITE', getattr(settings, 'SESSION_COOKIE_SAMESITE', 'Non défini')),
            ('SESSION_COOKIE_AGE', getattr(settings, 'SESSION_COOKIE_AGE', 'Non défini')),
            ('LOGIN_URL', getattr(settings, 'LOGIN_URL', 'Non défini')),
            ('LOGIN_REDIRECT_URL', getattr(settings, 'LOGIN_REDIRECT_URL', 'Non défini')),
            ('LOGOUT_REDIRECT_URL', getattr(settings, 'LOGOUT_REDIRECT_URL', 'Non défini')),
        ]
        
        for setting, value in security_settings:
            if setting in ['SESSION_COOKIE_SECURE', 'CSRF_COOKIE_SECURE']:
                status = self.style.WARNING("⚠️  À vérifier") if value and settings.DEBUG else self.style.SUCCESS("✅ OK")
            else:
                status = self.style.SUCCESS("✅ OK")
            self.stdout.write(f"{setting}: {value} {status}")
    
    def analyze_users_groups(self):
        self.stdout.write("\n2. 👥 UTILISATEURS ET GROUPES")
        self.stdout.write("-" * 40)
        
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        self.stdout.write(f"Utilisateurs totaux: {total_users}")
        self.stdout.write(f"Utilisateurs actifs: {active_users}")
        
        groups = Group.objects.all()
        self.stdout.write("\nGroupes existants:")
        for group in groups:
            members_count = group.user_set.count()
            status = self.style.SUCCESS("✅") if members_count > 0 else self.style.WARNING("⚠️")
            self.stdout.write(f"  {status} {group.name}: {members_count} membres")
    
    def analyze_redirections(self):
        self.stdout.write("\n3. 🧭 TEST DES REDIRECTIONS")
        self.stdout.write("-" * 40)
        
        try:
            from mutuelle_core.views import get_user_redirect_url
            
            # Test superuser
            superuser = User.objects.filter(is_superuser=True).first()
            if superuser:
                redirect_url = get_user_redirect_url(superuser)
                self.stdout.write(f"Superuser: {superuser.username} -> {redirect_url}")
            
            # Test par groupe
            for group in Group.objects.all():
                user = User.objects.filter(groups=group).first()
                if user:
                    redirect_url = get_user_redirect_url(user)
                    self.stdout.write(f"{group.name}: {user.username} -> {redirect_url}")
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Erreur test redirections: {e}"))
    
    def analyze_sessions(self):
        self.stdout.write("\n4. 🔐 SESSIONS ACTIVES")
        self.stdout.write("-" * 40)
        
        active_sessions = Session.objects.count()
        self.stdout.write(f"Sessions en base: {active_sessions}")
        
        if active_sessions > 0:
            self.stdout.write("\nDernières sessions:")
            for session in Session.objects.all()[:3]:
                session_data = session.get_decoded()
                self.stdout.write(f"  - {session.session_key}: {session_data}")
    
    def give_recommendations(self):
        self.stdout.write("\n5. 💡 RECOMMANDATIONS")
        self.stdout.write("-" * 40)
        
        recommendations = []
        
        if settings.DEBUG:
            if getattr(settings, 'SESSION_COOKIE_SECURE', False):
                recommendations.append("• Désactiver SESSION_COOKIE_SECURE en développement")
            if getattr(settings, 'CSRF_COOKIE_SECURE', False):
                recommendations.append("• Désactiver CSRF_COOKIE_SECURE en développement")
            recommendations.append("• Tester en navigation privée pour éviter les cookies corrompus")
        
        # Vérifier les groupes manquants
        required_groups = ['Assureur', 'Medecin', 'Pharmacien', 'Membre']
        existing_groups = [g.name for g in Group.objects.all()]
        
        for group in required_groups:
            if group not in existing_groups:
                recommendations.append(f"• Créer le groupe '{group}'")
        
        if recommendations:
            for rec in recommendations:
                self.stdout.write(self.style.WARNING(rec))
        else:
            self.stdout.write(self.style.SUCCESS("✅ Aucune action critique nécessaire"))
        
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("🎯 ACTIONS IMMÉDIATES")
        self.stdout.write("=" * 80)
        self.stdout.write("1. python manage.py migrate")
        self.stdout.write("2. python manage.py createsuperuser (si besoin)")
        self.stdout.write("3. Créer les groupes manquants dans l'admin Django")
        self.stdout.write("4. Nettoyer les cookies du navigateur")
        self.stdout.write("5. Tester en navigation privée")