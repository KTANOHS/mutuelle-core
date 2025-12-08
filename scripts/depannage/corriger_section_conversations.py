# corriger_section_conversations.py
import os

def corriger_section_conversations():
    """Corriger la section des conversations dans le template"""
    
    template_path = 'templates/communication/messagerie.html'
    
    with open(template_path, 'r') as f:
        contenu = f.read()
    
    print("🔍 RECHERCHE DE LA SECTION CONVERSATIONS...")
    
    # Vérifier si la section existe déjà
    if "<!-- SECTION DES CONVERSATIONS -->" in contenu:
        print("✅ Section conversations trouvée")
        
        # Extraire la section actuelle
        debut = contenu.find("<!-- SECTION DES CONVERSATIONS -->")
        fin = contenu.find("<!-- FIN SECTION DES CONVERSATIONS -->")
        
        if debut != -1 and fin != -1:
            section_actuelle = contenu[debut:fin + len("<!-- FIN SECTION DES CONVERSATIONS -->")]
            print("📝 Section actuelle extraite")
            
            # Remplacer par une version corrigée
            nouvelle_section = '''<!-- SECTION DES CONVERSATIONS -->
<div class="container mt-4">
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h3 class="mb-0"><i class="fas fa-comments me-2"></i>Mes Conversations</h3>
                </div>
                <div class="card-body">
                    {% if conversations %}
                        <div class="list-group">
                            {% for conversation in conversations %}
                                <div class="list-group-item list-group-item-action">
                                    <div class="d-flex w-100 justify-content-between">
                                        <h5 class="mb-1">
                                            <i class="fas fa-user-circle me-2"></i>
                                            {% for participant in conversation.participants.all %}
                                                {% if participant != request.user %}
                                                    {{ participant.get_full_name|default:participant.username }}
                                                {% endif %}
                                            {% endfor %}
                                        </h5>
                                        {% if conversation.nb_messages_non_lus > 0 %}
                                            <span class="badge bg-danger rounded-pill">{{ conversation.nb_messages_non_lus }} non lu(s)</span>
                                        {% endif %}
                                    </div>
                                    <p class="mb-1">
                                        {% with dernier_message=conversation.messages.last %}
                                            {% if dernier_message %}
                                                <strong>{{ dernier_message.expediteur.username }}:</strong> 
                                                {{ dernier_message.contenu|truncatewords:15 }}
                                            {% else %}
                                                <em>Aucun message</em>
                                            {% endif %}
                                        {% endwith %}
                                    </p>
                                    <small class="text-muted">
                                        Dernière activité: 
                                        {% if conversation.derniere_activite %}
                                            {{ conversation.derniere_activite|timesince }}
                                        {% else %}
                                            Jamais
                                        {% endif %}
                                    </small>
                                    <div class="mt-2">
                                        <a href="{% url 'communication:detail_conversation' conversation.id %}" 
                                           class="btn btn-sm btn-outline-primary">
                                            <i class="fas fa-eye me-1"></i>Voir la conversation
                                        </a>
                                    </div>
                                </div>
                            {% endfor %}
                        </div>
                    {% else %}
                        <div class="text-center py-4">
                            <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
                            <h5 class="text-muted">Aucune conversation</h5>
                            <p class="text-muted">Commencez une nouvelle conversation pour voir vos messages ici.</p>
                            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#nouveauMessageModal">
                                <i class="fas fa-plus me-1"></i>Nouvelle conversation
                            </button>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
<!-- FIN SECTION DES CONVERSATIONS -->'''
            
            # Remplacer l'ancienne section
            nouveau_contenu = contenu.replace(section_actuelle, nouvelle_section)
            
            with open(template_path, 'w') as f:
                f.write(nouveau_contenu)
            
            print("✅ Section des conversations corrigée avec succès !")
            return
    
    print("❌ Section conversations non trouvée, création d'une nouvelle section...")
    
    # Si la section n'existe pas, l'ajouter après le bouton test
    marqueur = '<!-- BOUTON TEST TRÈS VISIBLE -->'
    if marqueur in contenu:
        # Trouver la fin de la section test
        fin_test = contenu.find('</div>', contenu.find(marqueur)) + len('</div>')
        
        nouvelle_section = '''

<!-- SECTION DES CONVERSATIONS -->
<div class="container mt-4">
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h3 class="mb-0"><i class="fas fa-comments me-2"></i>Mes Conversations</h3>
                </div>
                <div class="card-body">
                    {% if conversations %}
                        <div class="list-group">
                            {% for conversation in conversations %}
                                <div class="list-group-item list-group-item-action">
                                    <div class="d-flex w-100 justify-content-between">
                                        <h5 class="mb-1">
                                            <i class="fas fa-user-circle me-2"></i>
                                            {% for participant in conversation.participants.all %}
                                                {% if participant != request.user %}
                                                    {{ participant.get_full_name|default:participant.username }}
                                                {% endif %}
                                            {% endfor %}
                                        </h5>
                                        {% if conversation.nb_messages_non_lus > 0 %}
                                            <span class="badge bg-danger rounded-pill">{{ conversation.nb_messages_non_lus }} non lu(s)</span>
                                        {% endif %}
                                    </div>
                                    <p class="mb-1">
                                        {% with dernier_message=conversation.messages.last %}
                                            {% if dernier_message %}
                                                <strong>{{ dernier_message.expediteur.username }}:</strong> 
                                                {{ dernier_message.contenu|truncatewords:15 }}
                                            {% else %}
                                                <em>Aucun message</em>
                                            {% endif %}
                                        {% endwith %}
                                    </p>
                                    <small class="text-muted">
                                        Dernière activité: 
                                        {% if conversation.derniere_activite %}
                                            {{ conversation.derniere_activite|timesince }}
                                        {% else %}
                                            Jamais
                                        {% endif %}
                                    </small>
                                    <div class="mt-2">
                                        <a href="{% url 'communication:detail_conversation' conversation.id %}" 
                                           class="btn btn-sm btn-outline-primary">
                                            <i class="fas fa-eye me-1"></i>Voir la conversation
                                        </a>
                                    </div>
                                </div>
                            {% endfor %}
                        </div>
                    {% else %}
                        <div class="text-center py-4">
                            <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
                            <h5 class="text-muted">Aucune conversation</h5>
                            <p class="text-muted">Commencez une nouvelle conversation pour voir vos messages ici.</p>
                            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#nouveauMessageModal">
                                <i class="fas fa-plus me-1"></i>Nouvelle conversation
                            </button>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
<!-- FIN SECTION DES CONVERSATIONS -->'''
        
        nouveau_contenu = contenu[:fin_test] + nouvelle_section + contenu[fin_test:]
        
        with open(template_path, 'w') as f:
            f.write(nouveau_contenu)
        
        print("✅ Nouvelle section des conversations ajoutée avec succès !")

if __name__ == "__main__":
    corriger_section_conversations()