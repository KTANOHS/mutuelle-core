# correctif_communication.py
#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur Django: {e}")
    sys.exit(1)

print("🔧 APPLICATIONS DES CORRECTIONS")

# 1. Ajouter la vue manquante
views_file = 'communication/views.py'
print(f"📝 Mise à jour de {views_file}...")

vue_code = '''
@login_required
def envoyer_message_conversation(request, conversation_id):
    """Envoyer un message dans une conversation existante"""
    if request.method == 'POST':
        try:
            conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
            contenu = request.POST.get('contenu', '').strip()
            
            if not contenu:
                messages.error(request, "Le message ne peut pas être vide.")
                return redirect('communication:detail_conversation', conversation_id=conversation_id)
            
            message = Message.objects.create(
                expediteur=request.user,
                contenu=contenu,
                conversation=conversation
            )
            
            destinataires = conversation.participants.exclude(id=request.user.id)
            message.destinataires.add(*destinataires)
            
            messages.success(request, "Message envoyé avec succès!")
            return redirect('communication:detail_conversation', conversation_id=conversation_id)
            
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
            return redirect('communication:detail_conversation', conversation_id=conversation_id)
    
    return redirect('communication:detail_conversation', conversation_id=conversation_id)
'''

# Lire le fichier views.py
with open(views_file, 'r') as f:
    content = f.read()

# Vérifier si la vue existe déjà
if 'def envoyer_message_conversation' in content:
    print("✅ La vue existe déjà")
else:
    # Trouver la dernière fonction et ajouter après
    lines = content.split('\n')
    last_func_index = -1
    
    for i, line in enumerate(lines):
        if line.strip().startswith('def ') and 'login_required' not in lines[max(0, i-1)]:
            last_func_index = i
    
    if last_func_index != -1:
        lines.insert(last_func_index + 1, vue_code)
        with open(views_file, 'w') as f:
            f.write('\n'.join(lines))
        print("✅ Vue ajoutée")
    else:
        print("⚠️  Impossible de trouver où insérer la vue")

# 2. Ajouter l'URL
urls_file = 'communication/urls.py'
print(f"\n📝 Mise à jour de {urls_file}...")

with open(urls_file, 'r') as f:
    urls_content = f.read()

if 'envoyer_message_conversation' in urls_content:
    print("✅ L'URL existe déjà")
else:
    # Chercher la ligne detail_conversation
    lines = urls_content.split('\n')
    new_lines = []
    
    for line in lines:
        new_lines.append(line)
        if 'detail_conversation' in line and '<int:conversation_id>' in line:
            # Ajouter la nouvelle URL après
            indent = ' ' * (len(line) - len(line.lstrip()))
            new_lines.append(f"{indent}path('conversations/<int:conversation_id>/envoyer/', views.envoyer_message_conversation, name='envoyer_message_conversation'),")
    
    with open(urls_file, 'w') as f:
        f.write('\n'.join(new_lines))
    print("✅ URL ajoutée")

# 3. Corriger le template
template_file = 'templates/communication/detail_conversation.html'
print(f"\n📝 Correction du template {template_file}...")

if os.path.exists(template_file):
    with open(template_file, 'r') as f:
        template_content = f.read()
    
    # Remplacer les URLs incorrectes
    template_content = template_content.replace(
        'action="{% url \'communication:envoyer_message_api\' %}"',
        'action="{% url \'communication:envoyer_message_conversation\' conversation.id %}"'
    )
    
    template_content = template_content.replace(
        'href="{% url \'communication:messages_liste\' %}"',
        'href="{% url \'communication:messagerie\' %}"'
    )
    
    with open(template_file, 'w') as f:
        f.write(template_content)
    print("✅ Template corrigé")
else:
    print(f"❌ Fichier template introuvable: {template_file}")

print("\n✅ Corrections appliquées avec succès !")
print("\n📋 Prochaines étapes:")
print("1. Redémarrez le serveur: python manage.py runserver")
print("2. Testez la conversation: http://127.0.0.1:8000/communication/conversations/5/")
print("3. Essayez d'envoyer un message")