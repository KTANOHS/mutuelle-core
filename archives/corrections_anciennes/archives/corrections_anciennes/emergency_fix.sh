# emergency_fix.sh
#!/bin/bash

echo "Application de la correction d'urgence..."

# Faire une sauvegarde
cp templates/communication/message_list.html templates/communication/message_list.html.backup.emergency

# Créer une version corrigée du template
cat > templates/communication/message_list.html << 'EOF'
{% extends "base.html" %}
{% load static %}

{% block title %}Messagerie{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="row">
        <div class="col-md-3">
            <div class="card">
                <div class="card-header">
                    <h6 class="mb-0">Filtres</h6>
                </div>
                <div class="card-body">
                    <div class="list-group list-group-flush">
                        <a href="?" class="list-group-item list-group-item-action {% if not request.GET.filtre %}active{% endif %}">
                            Tous les messages
                        </a>
                        <a href="?filtre=non_lus" class="list-group-item list-group-item-action {% if request.GET.filtre == 'non_lus' %}active{% endif %}">
                            Non lus
                        </a>
                        <a href="?filtre=envoyes" class="list-group-item list-group-item-action {% if request.GET.filtre == 'envoyes' %}active{% endif %}">
                            Messages envoyés
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-md-9">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Messagerie</h5>
                </div>
                <div class="card-body">
                    {% if messages %}
                        <div class="list-group">
                            {% for message in messages %}
                            <div class="list-group-item">
                                <h6>
                                    {% if message.expediteur == user %}
                                        À: {{ message.destinataire.username }}
                                    {% else %}
                                        De: {{ message.expediteur.username }}
                                    {% endif %}
                                </h6>
                                <p>{{ message.contenu }}</p>
                                <small>{{ message.date_creation }}</small>
                            </div>
                            {% endfor %}
                        </div>
                    {% else %}
                        <p>Aucun message.</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
EOF

echo "✓ Correction d'urgence appliquée!"
echo "✓ Le site devrait maintenant fonctionner"
echo "✓ Testez: python manage.py runserver"