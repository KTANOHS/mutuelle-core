# diagnostic_contexte_vue.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostiquer_contexte_vue():
    """Diagnostiquer pourquoi les conversations ne sont pas dans le contexte"""
    
    print("🔍 DIAGNOSTIC DU CONTEXTE DE LA VUE")
    print("=" * 60)
    
    # 1. Vérifier la vue messagerie
    vue_path = 'communication/views.py'
    with open(vue_path, 'r') as f:
        vue_content = f.read()
    
    print("1. 📝 ANALYSE DE LA VUE MESSAGERIE:")
    print("-" * 40)
    
    # Extraire la fonction messagerie
    debut_vue = vue_content.find('def messagerie(request):')
    fin_vue = vue_content.find('def ', debut_vue + 1)
    if fin_vue == -1:
        fin_vue = len(vue_content)
    
    fonction_messagerie = vue_content[debut_vue:fin_vue]
    
    # Vérifier les éléments critiques
    elements_vue = {
        'conversations = ': 'conversations = ' in fonction_messagerie,
        'context = {': 'context = {' in fonction_messagerie,
        "'conversations'": "'conversations'" in fonction_messagerie,
        'return render': 'return render' in fonction_messagerie
    }
    
    for element, present in elements_vue.items():
        status = "✅" if present else "❌"
        print(f"   {status} {element}: {'PRÉSENT' if present else 'ABSENT'}")
    
    # 2. Tester la vue directement
    print(f"\n2. 🧪 TEST DIRECT DE LA VUE:")
    print("-" * 40)
    
    from communication.views import messagerie
    from django.test import RequestFactory
    from django.contrib.auth.models import User
    
    try:
        pharmacien = User.objects.get(username='test_pharmacien')
        factory = RequestFactory()
        request = factory.get('/communication/')
        request.user = pharmacien
        
        # Appeler la vue
        response = messagerie(request)
        
        print(f"   📊 Statut: {response.status_code}")
        
        # Vérifier le contexte
        if hasattr(response, 'context_data'):
            context = response.context_data
            print(f"   📦 Contexte disponible: {len(context)} éléments")
            for key, value in context.items():
                if key == 'conversations':
                    print(f"      - {key}: {len(value) if hasattr(value, '__len__') else value} éléments")
                else:
                    print(f"      - {key}: {type(value)}")
        else:
            print("   ❌ Aucun contexte_data disponible")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

def corriger_vue_messagerie():
    """Corriger la vue messagerie pour s'assurer que les conversations sont dans le contexte"""
    
    vue_path = 'communication/views.py'
    
    with open(vue_path, 'r') as f:
        contenu = f.read()
    
    print(f"\n3. 🔧 CORRECTION DE LA VUE:")
    print("-" * 40)
    
    # Rechercher la fonction messagerie
    debut = contenu.find('def messagerie(request):')
    if debut == -1:
        print("   ❌ Fonction messagerie non trouvée")
        return
    
    # Vérifier si la vue utilise la bonne structure
    if "conversations = Conversation.objects.filter" not in contenu:
        print("   ❌ La vue n'utilise pas la bonne requête pour les conversations")
        
        # Remplacer toute la fonction messagerie
        ancienne_fonction = '''def messagerie(request):
    """Page principale de messagerie - VERSION AMÉLIORÉE"""
    try:
        # Récupérer les conversations avec annotations
        conversations = Conversation.objects.filter(participants=request.user).annotate(
            nb_messages_non_lus=Count('messages', filter=Q(messages__est_lu=False) & ~Q(messages__expediteur=request.user)),
            derniere_activite=Max('messages__date_envoi'),
            total_messages=Count('messages')
        ).order_by('-derniere_activite')
        
        # Récupérer les messages récents pour affichage
        messages_recents = Message.objects.filter(
            Q(expediteur=request.user) | Q(destinataire=request.user)
        ).select_related('expediteur', 'destinataire').order_by('-date_envoi')[:10]
        
        context = {
            'conversations': conversations,
            'messages_recents': messages_recents,
            'form': MessageForm(),
            'page_title': 'Messagerie',
            'total_conversations': conversations.count(),
            'total_messages': Message.objects.filter(
                Q(expediteur=request.user) | Q(destinataire=request.user)
            ).count()
        }
        return render(request, 'communication/messagerie.html', context)
        
    except Exception as e:
        # Fallback en cas d'erreur
        context = {
            'conversations': [],
            'messages_recents': [],
            'form': MessageForm(),
            'error': str(e),
            'page_title': 'Messagerie',
            'total_conversations': 0,
            'total_messages': 0
        }
        return render(request, 'communication/messagerie.html', context)'''
        
        nouvelle_fonction = '''def messagerie(request):
    """Page principale de messagerie - VERSION CORRIGÉE URGENCE"""
    try:
        from django.db.models import Q, Count, Max
        from communication.models import Conversation, Message
        from communication.forms import MessageForm
        
        print(f"🔍 VUE MESSAGERIE - Utilisateur: {request.user.username}")
        
        # Récupérer les conversations de l'utilisateur
        conversations = Conversation.objects.filter(participants=request.user).annotate(
            nb_messages_non_lus=Count('messages', filter=Q(messages__est_lu=False) & ~Q(messages__expediteur=request.user)),
            derniere_activite=Max('messages__date_envoi'),
            total_messages=Count('messages')
        ).order_by('-derniere_activite')
        
        print(f"🔍 Conversations trouvées: {conversations.count()}")
        
        # Messages récents
        messages_recents = Message.objects.filter(
            Q(expediteur=request.user) | Q(destinataire=request.user)
        ).select_related('expediteur', 'destinataire').order_by('-date_envoi')[:10]
        
        # Créer le contexte AVEC les conversations
        context = {
            'conversations': conversations,  # CEci est CRITIQUE
            'messages_recents': messages_recents,
            'form': MessageForm(),
            'page_title': 'Messagerie',
            'total_conversations': conversations.count(),
            'total_messages': Message.objects.filter(
                Q(expediteur=request.user) | Q(destinataire=request.user)
            ).count()
        }
        
        print(f"🔍 Contexte créé avec {len(context)} éléments")
        print(f"🔍 Conversations dans contexte: {len(conversations)}")
        
        return render(request, 'communication/messagerie.html', context)
        
    except Exception as e:
        print(f"❌ Erreur dans vue messagerie: {e}")
        # Fallback
        from communication.forms import MessageForm
        context = {
            'conversations': [],
            'messages_recents': [],
            'form': MessageForm(),
            'error': str(e),
            'page_title': 'Messagerie',
            'total_conversations': 0,
            'total_messages': 0
        }
        return render(request, 'communication/messagerie.html', context)'''
        
        if ancienne_fonction in contenu:
            contenu = contenu.replace(ancienne_fonction, nouvelle_fonction)
            print("   ✅ Vue messagerie complètement remplacée")
        else:
            print("   ❌ Impossible de trouver l'ancienne fonction à remplacer")
    else:
        print("   ✅ La vue semble correcte structurellement")
    
    # Écrire les modifications
    with open(vue_path, 'w') as f:
        f.write(contenu)

def creer_template_debug_simple():
    """Créer un template de debug simple"""
    
    template_path = 'templates/communication/messagerie.html'
    
    template_simple = '''{% extends "base.html" %}
{% load static %}

{% block title %}Messagerie - DEBUG SIMPLE{% endblock %}

{% block content %}
<div class="container py-4">

    <!-- DEBUG SIMPLE -->
    <div class="alert alert-info">
        <h4>DEBUG: Test d'affichage des conversations</h4>
        <p><strong>Conversations dans le contexte:</strong> {{ conversations|length }}</p>
    </div>

    <!-- TEST DIRECT -->
    <div class="card">
        <div class="card-header bg-primary text-white">
            <h3>Test d'affichage direct</h3>
        </div>
        <div class="card-body">
            {% if conversations %}
                <div class="alert alert-success">
                    ✅ Il y a {{ conversations|length }} conversation(s) dans le contexte!
                </div>
                
                {% for conversation in conversations %}
                <div class="border p-3 mb-3 bg-light">
                    <h5>Conversation #{{ conversation.id }}</h5>
                    <p><strong>Participants:</strong></p>
                    <ul>
                    {% for participant in conversation.participants.all %}
                        <li>{{ participant.username }} ({{ participant.id }})</li>
                    {% endfor %}
                    </ul>
                    <p><strong>Messages non lus:</strong> {{ conversation.nb_messages_non_lus }}</p>
                    <p><strong>Total messages:</strong> {{ conversation.total_messages }}</p>
                </div>
                {% endfor %}
            {% else %}
                <div class="alert alert-danger">
                    ❌ AUCUNE CONVERSATION dans le contexte!
                    <p>Mais en base il y a 2 conversations pour {{ request.user.username }}</p>
                </div>
            {% endif %}
        </div>
    </div>

</div>
{% endblock %}
'''

    # Sauvegarder et écrire
    if os.path.exists(template_path):
        os.rename(template_path, template_path + '.backup_pre_simple')
    
    with open(template_path, 'w') as f:
        f.write(template_simple)
    
    print("   ✅ Template debug simple créé")

if __name__ == "__main__":
    diagnostiquer_contexte_vue()
    corriger_vue_messagerie()
    creer_template_debug_simple()
    
    print(f"\n🎯 ACTIONS EFFECTUÉES:")
    print("1. Diagnostic de la vue et du contexte")
    print("2. Correction de la vue messagerie avec debug")
    print("3. Création d'un template debug simple")
    print("🌐 Testez: http://127.0.0.1:8000/communication/")