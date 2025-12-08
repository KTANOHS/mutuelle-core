# corriger_template_messagerie.py
import os

def corriger_template_messagerie():
    """Corriger le template messagerie.html pour afficher les conversations"""
    
    template_path = 'templates/communication/messagerie.html'
    
    if not os.path.exists(template_path):
        print(f"❌ Template non trouvé: {template_path}")
        return
    
    with open(template_path, 'r') as f:
        contenu = f.read()
    
    # Vérifier si le template a déjà une section pour les conversations
    if 'for conversation in conversations' in contenu:
        print("✅ Le template a déjà une boucle pour les conversations")
        return
    
    # Trouver où insérer la section des conversations
    # Chercher après le bouton test ou dans le contenu principal
    marqueur_insertion = '{% extends "base.html" %}'
    if marqueur_insertion not in contenu:
        marqueur_insertion = '<!-- BOUTON TEST TRÈS VISIBLE -->'
    
    if marqueur_insertion not in contenu:
        print("❌ Impossible de trouver le point d'insertion dans le template")
        return
    
    # Section des conversations à insérer
    section_conversations = '''
    
<!-- SECTION DES CONVERSATIONS -->
<div class="container mt-4">
    <div class="row">
        <div class="col-12">
            <h3 class="mb-4">Mes Conversations</h3>
            
            {% if conversations %}
                <div class="list-group">
                    {% for conversation in conversations %}
                        <a href="{% url 'communication:detail_conversation' conversation.id %}" 
                           class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="mb-1">
                                    {% for participant in conversation.participants.all %}
                                        {% if participant != request.user %}
                                            {{ participant.get_full_name|default:participant.username }}
                                        {% endif %}
                                    {% endfor %}
                                </h6>
                                <p class="mb-1 text-muted">
                                    {% with dernier_message=conversation.messages.last %}
                                        {% if dernier_message %}
                                            {{ dernier_message.contenu|truncatewords:10 }}
                                        {% else %}
                                            Aucun message
                                        {% endif %}
                                    {% endwith %}
                                </p>
                                <small>Dernière activité: {{ conversation.date_modification|timesince }}</small>
                            </div>
                            {% if conversation.nb_messages_non_lus > 0 %}
                                <span class="badge bg-primary rounded-pill">{{ conversation.nb_messages_non_lus }}</span>
                            {% endif %}
                        </a>
                    {% endfor %}
                </div>
            {% else %}
                <div class="alert alert-info">
                    <p class="mb-0">Aucune conversation pour le moment.</p>
                    <p class="mb-0">Envoyez un message pour démarrer une conversation.</p>
                </div>
            {% endif %}
        </div>
    </div>
</div>
<!-- FIN SECTION DES CONVERSATIONS -->
'''
    
    # Insérer la section après le marqueur
    nouveau_contenu = contenu.replace(marqueur_insertion, marqueur_insertion + section_conversations)
    
    with open(template_path, 'w') as f:
        f.write(nouveau_contenu)
    
    print("✅ Template messagerie.html corrigé avec succès !")
    print("✅ Section des conversations ajoutée")

if __name__ == "__main__":
    corriger_template_messagerie()