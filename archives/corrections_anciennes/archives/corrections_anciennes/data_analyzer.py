# data_analyzer.py
import os
import sys
import django
from pathlib import Path
from django.db.models import Count, Q, Max  # AJOUT: Importer Max
from datetime import datetime, timedelta

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from communication.models import Message, Notification, GroupeCommunication

User = get_user_model()

class DataAnalyzer:
    """Analyse les données existantes dans le système"""
    
    def analyze_system_data(self):
        """Analyse complète des données du système"""
        print("📈 ANALYSE DES DONNÉES EXISTANTES")
        print("=" * 80)
        
        self.analyze_users()
        self.analyze_communication_data()
        self.analyze_recent_activity()
        self.generate_statistics()
    
    def analyze_users(self):
        """Analyse des utilisateurs et leurs rôles"""
        print("\n👥 ANALYSE DES UTILISATEURS")
        print("-" * 50)
        
        try:
            total_users = User.objects.count()
            active_users = User.objects.filter(is_active=True).count()
            staff_users = User.objects.filter(is_staff=True).count()
            superusers = User.objects.filter(is_superuser=True).count()
            
            print(f"📊 Total utilisateurs: {total_users}")
            print(f"✅ Utilisateurs actifs: {active_users}")
            print(f"👨‍💼 Staff: {staff_users}")
            print(f"⚡ Superusers: {superusers}")
            
            # Détection des types d'utilisateurs basée sur le username
            user_patterns = {
                'agent': User.objects.filter(username__icontains='agent').count(),
                'medecin': User.objects.filter(username__icontains='medecin').count(),
                'pharmacien': User.objects.filter(username__icontains='pharmacien').count(),
                'technicien': User.objects.filter(username__icontains='technicien').count(),
                'admin': User.objects.filter(username__icontains='admin').count(),
            }
            
            print("\n🎭 Répartition par type (basé sur username):")
            for role, count in user_patterns.items():
                if count > 0:
                    print(f"   {role.capitalize()}: {count}")
            
        except Exception as e:
            print(f"❌ Erreur analyse utilisateurs: {e}")
    
    def analyze_communication_data(self):
        """Analyse des données de communication"""
        print("\n💬 ANALYSE DE LA COMMUNICATION")
        print("-" * 50)
        
        try:
            # Messages
            total_messages = Message.objects.count()
            unread_messages = Message.objects.filter(est_lu=False).count()
            messages_by_type = Message.objects.values('type_message').annotate(count=Count('id'))
            
            print(f"📧 Total messages: {total_messages}")
            print(f"📨 Messages non lus: {unread_messages}")
            print("\n📊 Messages par type:")
            for item in messages_by_type:
                print(f"   {item['type_message']}: {item['count']}")
            
            # Notifications
            total_notifications = Notification.objects.count()
            unread_notifications = Notification.objects.filter(est_lue=False).count()
            
            print(f"\n🔔 Total notifications: {total_notifications}")
            print(f"🔕 Notifications non lues: {unread_notifications}")
            
            # Groupes
            total_groups = GroupeCommunication.objects.count()
            active_groups = GroupeCommunication.objects.filter(est_actif=True).count()
            public_groups = GroupeCommunication.objects.filter(est_public=True).count()
            
            print(f"\n👥 Total groupes: {total_groups}")
            print(f"✅ Groupes actifs: {active_groups}")
            print(f"🌐 Groupes publics: {public_groups}")
            
        except Exception as e:
            print(f"❌ Erreur analyse communication: {e}")
    
    def analyze_recent_activity(self):
        """Analyse de l'activité récente"""
        print("\n🕒 ACTIVITÉ RÉCENTE (7 derniers jours)")
        print("-" * 50)
        
        try:
            last_week = datetime.now() - timedelta(days=7)
            
            recent_messages = Message.objects.filter(date_envoi__gte=last_week).count()
            recent_notifications = Notification.objects.filter(date_creation__gte=last_week).count()
            
            print(f"📧 Messages récents: {recent_messages}")
            print(f"🔔 Notifications récentes: {recent_notifications}")
            
            # Top expéditeurs
            top_senders = Message.objects.filter(
                date_envoi__gte=last_week
            ).values('expediteur__username').annotate(
                count=Count('id')
            ).order_by('-count')[:5]
            
            if top_senders:
                print("\n🏆 Top expéditeurs récents:")
                for sender in top_senders:
                    username = sender['expediteur__username'] or 'Inconnu'
                    print(f"   {username}: {sender['count']} messages")
            
        except Exception as e:
            print(f"❌ Erreur analyse activité récente: {e}")
    
    def generate_statistics(self):
        """Génère des statistiques globales"""
        print("\n📈 STATISTIQUES GLOBALES")
        print("-" * 50)
        
        try:
            # Utilisateurs avec le plus d'activité
            active_users = Message.objects.values(
                'expediteur__username'
            ).annotate(
                message_count=Count('id'),
                last_activity=Max('date_envoi')  # ✅ CORRIGÉ : Utilisation de Max importé
            ).order_by('-message_count')[:10]
            
            print("🏅 Utilisateurs les plus actifs:")
            for user in active_users:
                username = user['expediteur__username'] or 'Inconnu'
                print(f"   {username}: {user['message_count']} messages")
            
            # Distribution temporelle
            from django.utils import timezone
            today = timezone.now().date()
            messages_today = Message.objects.filter(date_envoi__date=today).count()
            
            print(f"\n📅 Aujourd'hui: {messages_today} messages")
            
        except Exception as e:
            print(f"❌ Erreur génération statistiques: {e}")

def check_system_health():
    """Vérifie la santé du système"""
    print("\n❤️  VÉRIFICATION DE SANTÉ DU SYSTÈME")
    print("-" * 50)
    
    checks = [
        ("Base de données accessible", check_database),
        ("Applications chargées", check_apps_loaded),
        ("Modèles communication", check_communication_models),
    ]
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            status = "✅" if result else "❌"
            print(f"{status} {check_name}: {'OK' if result else 'Échec'}")
        except Exception as e:
            print(f"❌ {check_name}: Erreur - {e}")

def check_database():
    """Vérifie que la base de données est accessible"""
    try:
        User.objects.count()
        return True
    except:
        return False

def check_apps_loaded():
    """Vérifie que les applications sont chargées"""
    try:
        from django.apps import apps
        required_apps = ['membres', 'agents', 'communication', 'medecin', 'pharmacien']
        return all(apps.is_installed(app) for app in required_apps)
    except:
        return False

def check_communication_models():
    """Vérifie que les modèles de communication sont accessibles"""
    try:
        Message.objects.count()
        Notification.objects.count()
        return True
    except:
        return False

if __name__ == "__main__":
    print("🔍 LANCEMENT DE L'ANALYSE DES DONNÉES")
    print("=" * 80)
    
    # Vérification de santé
    check_system_health()
    
    # Analyse des données
    analyzer = DataAnalyzer()
    analyzer.analyze_system_data()
    
    print("\n" + "=" * 80)
    print("🎯 ANALYSE DES DONNÉES TERMINÉE")
    print("=" * 80)