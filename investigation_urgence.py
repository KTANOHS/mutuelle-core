# investigation_urgence.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def investigation_complete():
    print("🚨 INVESTIGATION URGENTE - SECTION CONVERSATIONS MANQUANTE")
    print("=" * 70)
    
    # 1. Vérifier le template actuel
    template_path = 'templates/communication/messagerie.html'
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    print("1. 📄 ANALYSE DU TEMPLATE MESSAGERIE.HTML")
    print("-" * 50)
    
    # Vérifier si la section existe dans le template
    if "<!-- SECTION DES CONVERSATIONS -->" in template_content:
        print("✅ Section conversations trouvée dans le template")
        
        # Extraire la section
        debut = template_content.find("<!-- SECTION DES CONVERSATIONS -->")
        fin = template_content.find("<!-- FIN SECTION DES CONVERSATIONS -->")
        
        if debut != -1 and fin != -1:
            section = template_content[debut:fin + len("<!-- FIN SECTION DES CONVERSATIONS -->")]
            print(f"📏 Taille de la section: {len(section)} caractères")
            
            # Vérifier le contenu de la section
            verifs_section = [
                "{% if conversations %}" in section,
                "{% for conversation in conversations %}" in section,
                "{{ participant.username }}" in section,
                "list-group-item" in section
            ]
            
            for i, check in enumerate(verifs_section, 1):
                status = "✅" if check else "❌"
                print(f"   {status} Élément {i}: {'PRÉSENT' if check else 'ABSENT'}")
            
            # Afficher un extrait de la section
            print(f"\n📋 EXTRAT DE LA SECTION:")
            print(section[:500] + "..." if len(section) > 500 else section)
        else:
            print("❌ Balises de section incomplètes")
    else:
        print("❌ Section conversations NON TROUVÉE dans le template")
    
    # 2. Test de rendu manuel
    print("\n2. 🧪 TEST DE RENDU MANUEL")
    print("-" * 50)
    
    from django.template.loader import render_to_string
    from django.contrib.auth.models import User
    from communication.models import Conversation, Message
    from django.db.models import Q, Count, Max
    from communication.forms import MessageForm
    
    try:
        pharmacien = User.objects.get(username='test_pharmacien')
        
        # Récupérer les données EXACTEMENT comme la vue
        conversations = Conversation.objects.filter(participants=pharmacien).annotate(
            nb_messages_non_lus=Count('messages', filter=Q(messages__est_lu=False) & ~Q(messages__expediteur=pharmacien)),
            derniere_activite=Max('messages__date_envoi'),
            total_messages=Count('messages')
        ).order_by('-derniere_activite')
        
        print(f"📊 Données récupérées:")
        print(f"   - Conversations: {conversations.count()}")
        
        for conv in conversations:
            participants = list(conv.participants.all())
            autres = [p for p in participants if p != pharmacien]
            print(f"   - Conversation {conv.id}: {len(autres)} autre(s) participant(s)")
            for p in autres:
                print(f"     → {p.username}")
        
        # Créer le contexte
        context = {
            'conversations': conversations,
            'messages_recents': Message.objects.filter(
                Q(expediteur=pharmacien) | Q(destinataire=pharmacien)
            ).select_related('expediteur', 'destinataire').order_by('-date_envoi')[:10],
            'form': MessageForm(),
            'page_title': 'Messagerie',
            'total_conversations': conversations.count(),
            'total_messages': Message.objects.filter(
                Q(expediteur=pharmacien) | Q(destinataire=pharmacien)
            ).count(),
            'request': type('Obj', (object,), {'user': pharmacien})()  # Mock request
        }
        
        # Rendre le template
        html = render_to_string('communication/messagerie.html', context)
        
        print(f"\n🎨 RENDU DU TEMPLATE:")
        print(f"   - Taille HTML: {len(html)} caractères")
        
        # Vérifier ce qui est dans le HTML rendu
        checks = {
            'Section conversations': 'SECTION DES CONVERSATIONS' in html,
            'List group item': 'list-group-item' in html,
            'test_agent': 'test_agent' in html,
            'test_medecin': 'test_medecin' in html,
            'Card body': 'card-body' in html
        }
        
        for check, result in checks.items():
            status = "✅" if result else "❌"
            print(f"   {status} {check}: {'TROUVÉ' if result else 'NON TROUVÉ'}")
        
        # Trouver où est la section dans le HTML rendu
        if 'SECTION DES CONVERSATIONS' in html:
            debut_section = html.find('SECTION DES CONVERSATIONS')
            fin_section = html.find('FIN SECTION DES CONVERSATIONS')
            if debut_section != -1 and fin_section != -1:
                section_rendue = html[debut_section:fin_section + len('FIN SECTION DES CONVERSATIONS')]
                print(f"\n📄 SECTION RENDUE (extrait):")
                print(section_rendue[:1000] + "..." if len(section_rendue) > 1000 else section_rendue)
        
    except Exception as e:
        print(f"❌ Erreur lors du test de rendu: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    investigation_complete()