# diagnostic_communication_corrige.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'votre_projet.settings')
django.setup()

from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from django.utils import timezone

def diagnostic_complet():
    User = get_user_model()
    
    print("=== DIAGNOSTIC COMPLET SYSTÈME ===")
    
    # 1. Nettoyage des sessions corrompues
    print("\n1. NETTOYAGE DES SESSIONS:")
    sessions_count_before = Session.objects.count()
    print(f"   Sessions avant nettoyage: {sessions_count_before}")
    
    # Commande pour nettoyer les sessions
    os.system('python manage.py clearsessions')
    
    sessions_count_after = Session.objects.count()
    print(f"   Sessions après nettoyage: {sessions_count_after}")
    
    # 2. Diagnostic utilisateurs et groupes
    print("\n2. DIAGNOSTIC UTILISATEURS:")
    try:
        from django.contrib.auth.models import Group
        assureurs_group = Group.objects.filter(name='ASSUREUR').first()
        
        if assureurs_group:
            assureurs = assureurs_group.user_set.all()
            print(f"   Groupe ASSUREUR trouvé: {assureurs.count()} utilisateur(s)")
            
            for user in assureurs:
                print(f"   - {user.username} ({user.email})")
        else:
            print("   ❌ Groupe ASSUREUR non trouvé")
            
    except Exception as e:
        print(f"   ❌ Erreur groupes: {e}")
    
    # 3. Vérification de tous les utilisateurs
    all_users = User.objects.all()
    print(f"   Total utilisateurs: {all_users.count()}")
    
    for user in all_users[:10]:  # Afficher les 10 premiers
        print(f"   - {user.username} | {user.email} | Staff: {user.is_staff}")
    
    # 4. Diagnostic modèles de communication
    print("\n3. DIAGNOSTIC MODÈLES:")
    try:
        from communication.models import Message
        
        messages = Message.objects.all()
        print(f"   Messages dans la base: {messages.count()}")
        
        # Vérifier la structure du premier message
        if messages.exists():
            first_msg = messages.first()
            print(f"   Structure du premier message:")
            print(f"   - ID: {first_msg.id}")
            print(f"   - Champs disponibles: {[f.name for f in first_msg._meta.fields]}")
            
            # Afficher les données du message
            for field in first_msg._meta.fields:
                try:
                    value = getattr(first_msg, field.name)
                    print(f"   - {field.name}: {value}")
                except Exception as e:
                    print(f"   - {field.name}: ERREUR - {e}")
    except Exception as e:
        print(f"   ❌ Erreur modèle Message: {e}")
    
    # 5. Vérification configuration
    print("\n4. CONFIGURATION:")
    print(f"   DEBUG: {settings.DEBUG}")
    print(f"   TIME_ZONE: {settings.TIME_ZONE}")
    print(f"   USE_TZ: {settings.USE_TZ}")
    print(f"   INSTALLED_APPS avec communication: {'communication' in settings.INSTALLED_APPS}")
    
    # 6. Vérification des URLs de communication
    print("\n5. URLS DE COMMUNICATION:")
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        url_patterns = []
        
        def list_urls(patterns, base=''):
            for pattern in patterns:
                if hasattr(pattern, 'pattern'):
                    if hasattr(pattern, 'url_patterns'):
                        list_urls(pattern.url_patterns, base + str(pattern.pattern))
                    else:
                        url_patterns.append(base + str(pattern.pattern))
        
        list_urls(resolver.url_patterns)
        comm_urls = [url for url in url_patterns if 'communication' in url or 'message' in url]
        print(f"   URLs de communication trouvées: {len(comm_urls)}")
        for url in comm_urls[:5]:  # Afficher les 5 premières
            print(f"   - {url}")
            
    except Exception as e:
        print(f"   ❌ Erreur analyse URLs: {e}")

if __name__ == "__main__":
    diagnostic_complet()