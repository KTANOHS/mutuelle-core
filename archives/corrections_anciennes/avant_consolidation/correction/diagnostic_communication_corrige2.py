#!/usr/bin/env python
# diagnostic_communication_corrige.py - Diagnostic complet sans erreur
import os
import sys
import django
from pathlib import Path

# Ajouter le chemin du projet
project_path = Path(__file__).parent
sys.path.append(str(project_path))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation de Django: {e}")
    sys.exit(1)

def diagnostic_communication():
    print("🔍 DIAGNOSTIC COMPLET - MODULE COMMUNICATION")
    print("=" * 60)
    
    try:
        from communication.models import Conversation, Message
        from django.contrib.auth.models import User
        from django.contrib.sessions.models import Session
        from django.utils import timezone
        
        # =============================================================
        # 1. SESSIONS ACTIVES
        # =============================================================
        print("\n1. SESSIONS ACTIVES:")
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        print(f"   {active_sessions.count()} session(s) active(s)")
        
        # =============================================================
        # 2. UTILISATEURS
        # =============================================================
        print("\n2. UTILISATEURS:")
        total_users = User.objects.count()
        print(f"   {total_users} utilisateur(s) au total")
        
        # Afficher les 10 premiers utilisateurs
        for user in User.objects.all()[:10]:
            print(f"   - {user.username} ({user.get_full_name()}) - {user.email}")
        
        # =============================================================
        # 3. MESSAGES
        # =============================================================
        print("\n3. MESSAGES:")
        total_messages = Message.objects.count()
        print(f"   {total_messages} message(s) dans la base")
        
        if total_messages > 0:
            print("   Derniers 5 messages:")
            for msg in Message.objects.all().order_by('-date_envoi')[:5]:
                # CORRECTION: Utiliser msg.titre au lieu de msg.sujet
                print(f"   - Message {msg.id}: {msg.titre} - De {msg.expediteur} à {msg.destinataire}")
                print(f"     Contenu: {msg.contenu[:50]}..." if len(msg.contenu) > 50 else f"     Contenu: {msg.contenu}")
        
        # =============================================================
        # 4. CONVERSATIONS
        # =============================================================
        print("\n4. CONVERSATIONS:")
        total_conversations = Conversation.objects.count()
        print(f"   {total_conversations} conversation(s)")
        
        if total_conversations > 0:
            print("   Détail des conversations:")
            for conv in Conversation.objects.all():
                participants = [p.username for p in conv.participants.all()]
                messages_count = conv.messages.count()
                print(f"   - Conversation {conv.id}: {participants} - {messages_count} message(s)")
        
        # =============================================================
        # 5. STATISTIQUES PAR UTILISATEUR
        # =============================================================
        print("\n5. STATISTIQUES PAR UTILISATEUR:")
        for user in User.objects.all()[:5]:  # Limiter aux 5 premiers
            messages_envoyes = Message.objects.filter(expediteur=user).count()
            messages_recus = Message.objects.filter(destinataire=user).count()
            conversations = Conversation.objects.filter(participants=user).count()
            
            print(f"   - {user.username}:")
            print(f"     Messages envoyés: {messages_envoyes}")
            print(f"     Messages reçus: {messages_recus}")
            print(f"     Conversations: {conversations}")
        
        # =============================================================
        # 6. VÉRIFICATION DES DONNÉES PROBLÉMATIQUES
        # =============================================================
        print("\n6. VÉRIFICATION DES DONNÉES:")
        
        # Messages sans expéditeur
        messages_sans_expediteur = Message.objects.filter(expediteur__isnull=True)
        if messages_sans_expediteur.exists():
            print(f"   ⚠️  {messages_sans_expediteur.count()} message(s) sans expéditeur")
        
        # Messages sans destinataire
        messages_sans_destinataire = Message.objects.filter(destinataire__isnull=True)
        if messages_sans_destinataire.exists():
            print(f"   ⚠️  {messages_sans_destinataire.count()} message(s) sans destinataire")
        
        # Conversations sans participants
        conversations_sans_participants = Conversation.objects.filter(participants__isnull=True)
        if conversations_sans_participants.exists():
            print(f"   ⚠️  {conversations_sans_participants.count()} conversation(s) sans participants")
        
        # =============================================================
        # 7. VÉRIFICATION DES TEMPLATES
        # =============================================================
        print("\n7. TEMPLATES COMMUNICATION:")
        templates_path = project_path / 'templates' / 'communication'
        
        if templates_path.exists():
            templates = list(templates_path.glob('*.html'))
            print(f"   {len(templates)} template(s) trouvé(s)")
            for template in templates[:10]:  # Limiter à 10
                print(f"   - {template.name}")
        else:
            print("   ❌ Répertoire templates/communication non trouvé")
        
        # =============================================================
        # 8. VÉRIFICATION DES URLS
        # =============================================================
        print("\n8. URLS DISPONIBLES:")
        try:
            from django.urls import reverse, NoReverseMatch
            
            urls_a_tester = [
                'communication:messagerie',
                'communication:message_create',
                'communication:detail_conversation',
                'communication:api_public_test',
                'communication:api_public_conversation_messages',
            ]
            
            for url_name in urls_a_tester:
                try:
                    url = reverse(url_name, args=[5] if 'conversation' in url_name else [])
                    print(f"   ✅ {url_name}: {url}")
                except NoReverseMatch:
                    print(f"   ❌ {url_name}: Non trouvée")
        except Exception as e:
            print(f"   ❌ Erreur lors de la vérification des URLs: {e}")
        
        # =============================================================
        # 9. TEST DE L'API
        # =============================================================
        print("\n9. TEST DE L'API:")
        try:
            from django.test import Client
            client = Client()
            
            # Test de l'API publique
            response = client.get('/communication/api/public/test/')
            if response.status_code == 200:
                print(f"   ✅ API Test: {response.status_code} - {response.json()}")
            else:
                print(f"   ❌ API Test: {response.status_code}")
            
            # Test des messages de conversation
            response = client.get('/communication/api/public/conversations/5/messages/')
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Conversation 5: {response.status_code} - {len(data.get('messages', []))} message(s)")
            else:
                print(f"   ❌ Conversation 5: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erreur lors du test API: {e}")
        
        # =============================================================
        # 10. RÉSUMÉ ET RECOMMANDATIONS
        # =============================================================
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DU DIAGNOSTIC")
        print("=" * 60)
        
        summary = {
            "Utilisateurs": total_users,
            "Conversations": total_conversations,
            "Messages": total_messages,
            "Sessions actives": active_sessions.count(),
        }
        
        for key, value in summary.items():
            print(f"• {key}: {value}")
        
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS:")
        
        if total_messages == 0:
            print("  ⚠️  Aucun message dans la base - créer des messages de test")
        
        if active_sessions.count() > 20:
            print("  ⚠️  Nettoyer les sessions expirées avec: python manage.py clearsessions")
        
        if messages_sans_expediteur.exists() or messages_sans_destinataire.exists():
            print("  ⚠️  Corriger les messages sans expéditeur/destinataire")
        
        print(f"\n✅ Diagnostic terminé avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors du diagnostic: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnostic_communication()