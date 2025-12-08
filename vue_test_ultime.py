# vue_test_ultime.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def creer_vue_test_ultime():
    """Créer une vue de test ultime pour vérifier les données"""
    
    vue_path = 'communication/views.py'
    
    with open(vue_path, 'r') as f:
        contenu = f.read()
    
    # Ajouter une vue de test à la fin du fichier
    vue_test = '''

# =============================================================================
# VUE DE TEST ULTIME - À SUPPRIMER APRÈS DIAGNOSTIC
# =============================================================================

@login_required
def test_conversations_ultime(request):
    """Vue de test ultime pour vérifier les conversations"""
    from django.http import HttpResponse
    from communication.models import Conversation, Message
    from django.db.models import Q, Count, Max
    
    html = f"""
    <html>
    <body style="font-family: Arial; padding: 20px;">
        <h1>TEST ULTIME - Conversations</h1>
        <h2>Utilisateur: {request.user.username} (ID: {request.user.id})</h2>
        
        <h3>1. Requête directe des conversations:</h3>
    """
    
    # Test 1: Requête directe
    conversations = Conversation.objects.filter(participants=request.user)
    html += f"<p>Conversations trouvées: <strong>{conversations.count()}</strong></p>"
    
    for conv in conversations:
        participants = list(conv.participants.all())
        html += f"<div style='border: 1px solid #ccc; padding: 10px; margin: 10px;'>"
        html += f"<h4>Conversation {conv.id}</h4>"
        html += f"<p>Participants: {[p.username for p in participants]}</p>"
        html += f"<p>Messages: {conv.messages.count()}</p>"
        html += "</div>"
    
    # Test 2: Requête avec annotations
    html += "<h3>2. Requête avec annotations:</h3>"
    conversations_anno = Conversation.objects.filter(participants=request.user).annotate(
        nb_messages_non_lus=Count('messages', filter=Q(messages__est_lu=False) & ~Q(messages__expediteur=request.user)),
        derniere_activite=Max('messages__date_envoi'),
        total_messages=Count('messages')
    )
    
    html += f"<p>Conversations avec annotations: <strong>{conversations_anno.count()}</strong></p>"
    
    for conv in conversations_anno:
        html += f"<div style='border: 1px solid #369; padding: 10px; margin: 10px; background: #f0f8ff;'>"
        html += f"<h4>Conversation {conv.id} (avec annotations)</h4>"
        html += f"<p>Messages non lus: {conv.nb_messages_non_lus}</p>"
        html += f"<p>Total messages: {conv.total_messages}</p>"
        html += f"<p>Dernière activité: {conv.derniere_activite}</p>"
        html += "</div>"
    
    html += """
        <h3>3. Test de la vue messagerie normale:</h3>
        <p><a href="/communication/">Retour à la messagerie normale</a></p>
    </body>
    </html>
    """
    
    return HttpResponse(html)

'''

    # Ajouter la vue test à la fin du fichier
    with open(vue_path, 'a') as f:
        f.write(vue_test)
    
    # Ajouter l'URL dans urls.py
    urls_path = 'communication/urls.py'
    with open(urls_path, 'r') as f:
        urls_content = f.read()
    
    # Ajouter le path si pas déjà présent
    if 'test_conversations_ultime' not in urls_content:
        urls_content = urls_content.replace('urlpatterns = [', 'urlpatterns = [\n    path(\'test-ultime/\', views.test_conversations_ultime, name=\'test_ultime\'),')
        
        with open(urls_path, 'w') as f:
            f.write(urls_content)
    
    print("✅ VUE DE TEST ULTIME CRÉÉE !")
    print("🌐 Testez: http://127.0.0.1:8000/communication/test-ultime/")

if __name__ == "__main__":
    creer_vue_test_ultime()