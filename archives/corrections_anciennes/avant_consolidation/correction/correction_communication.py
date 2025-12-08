#!/usr/bin/env python3
"""
SCRIPT DE CORRECTION RAPIDE - COMMUNICATION ASSUREUR
Version 3.0 - Résout les problèmes identifiés
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
print(f"📁 Répertoire de travail: {BASE_DIR}")

# ============================================================================
# 1. CRÉER LE TEMPLATE messagerie.html MANQUANT
# ============================================================================

print("\n1. 🎨 CRÉATION DU TEMPLATE messagerie.html")

messagerie_path = BASE_DIR / "templates" / "assureur" / "communication" / "messagerie.html"

if not messagerie_path.exists():
    content = '''{% extends 'assureur/base_assureur.html' %}
{% load static %}

{% block content %}
<div class="container-fluid">
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-gray-800">Messagerie</h1>
        <div>
            <a href="{% url 'assureur:envoyer_message_assureur' %}" class="btn btn-primary">
                <i class="fas fa-paper-plane me-1"></i>Nouveau message
            </a>
            <a href="{% url 'assureur:liste_notifications_assureur' %}" class="btn btn-warning ml-2">
                <i class="fas fa-bell me-1"></i>Notifications
                {% if notifications_non_lues > 0 %}
                <span class="badge badge-light">{{ notifications_non_lues }}</span>
                {% endif %}
            </a>
        </div>
    </div>

    <!-- Statistiques rapides -->
    <div class="row mb-4">
        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-primary shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                                Messages reçus
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">
                                {{ messages_recus|length }}
                            </div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-inbox fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-success shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                                Messages envoyés
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">
                                {{ messages_envoyes|length }}
                            </div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-paper-plane fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-warning shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                                Non lus
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">
                                {{ messages_non_lus }}
                            </div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-envelope fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-info shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
                                En attente
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">
                                0
                            </div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-clock fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="row">
        <!-- Messages reçus -->
        <div class="col-lg-6">
            <div class="card shadow mb-4">
                <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                    <h6 class="m-0 font-weight-bold text-primary">
                        <i class="fas fa-inbox me-1"></i>Messages reçus
                    </h6>
                </div>
                <div class="card-body">
                    {% if messages_recus %}
                        <div class="list-group">
                            {% for message in messages_recus %}
                            <a href="{% url 'assureur:detail_message_assureur' message.id %}" 
                               class="list-group-item list-group-item-action flex-column align-items-start">
                                <div class="d-flex w-100 justify-content-between">
                                    <h6 class="mb-1">
                                        <i class="fas fa-user me-1"></i>{{ message.expediteur.username|default:"Expéditeur inconnu" }}
                                    </h6>
                                    <small class="text-muted">{{ message.date_envoi|date:"d/m/Y H:i" }}</small>
                                </div>
                                <p class="mb-1 text-truncate" style="max-width: 400px;">
                                    {{ message.contenu|truncatechars:100 }}
                                </p>
                                {% if not message.lu %}
                                <span class="badge badge-primary badge-pill">Nouveau</span>
                                {% endif %}
                            </a>
                            {% endfor %}
                        </div>
                    {% else %}
                        <div class="text-center py-4">
                            <i class="fas fa-inbox fa-3x text-gray-300 mb-3"></i>
                            <p class="text-muted">Aucun message reçu</p>
                        </div>
                    {% endif %}
                </div>
                <div class="card-footer text-center">
                    <a href="{% url 'assureur:liste_messages_assureur' %}" class="btn btn-sm btn-outline-primary">
                        <i class="fas fa-list me-1"></i>Voir tous les messages
                    </a>
                </div>
            </div>
        </div>

        <!-- Messages envoyés -->
        <div class="col-lg-6">
            <div class="card shadow mb-4">
                <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                    <h6 class="m-0 font-weight-bold text-success">
                        <i class="fas fa-paper-plane me-1"></i>Messages envoyés
                    </h6>
                </div>
                <div class="card-body">
                    {% if messages_envoyes %}
                        <div class="list-group">
                            {% for message in messages_envoyes %}
                            <a href="{% url 'assureur:detail_message_assureur' message.id %}" 
                               class="list-group-item list-group-item-action flex-column align-items-start">
                                <div class="d-flex w-100 justify-content-between">
                                    <h6 class="mb-1">
                                        <i class="fas fa-user me-1"></i>À: {{ message.destinataire.username|default:"Destinataire inconnu" }}
                                    </h6>
                                    <small class="text-muted">{{ message.date_envoi|date:"d/m/Y H:i" }}</small>
                                </div>
                                <p class="mb-1 text-truncate" style="max-width: 400px;">
                                    {{ message.contenu|truncatechars:100 }}
                                </p>
                                <small class="text-muted">
                                    {% if message.lu %}
                                        <i class="fas fa-check text-success"></i> Lu
                                    {% else %}
                                        <i class="fas fa-clock text-warning"></i> Non lu
                                    {% endif %}
                                </small>
                            </a>
                            {% endfor %}
                        </div>
                    {% else %}
                        <div class="text-center py-4">
                            <i class="fas fa-paper-plane fa-3x text-gray-300 mb-3"></i>
                            <p class="text-muted">Aucun message envoyé</p>
                        </div>
                    {% endif %}
                </div>
                <div class="card-footer text-center">
                    <a href="{% url 'assureur:envoyer_message_assureur' %}" class="btn btn-sm btn-outline-success">
                        <i class="fas fa-plus me-1"></i>Écrire un nouveau message
                    </a>
                </div>
            </div>
        </div>
    </div>

    <!-- Notifications récentes -->
    <div class="row">
        <div class="col-lg-12">
            <div class="card shadow mb-4">
                <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                    <h6 class="m-0 font-weight-bold text-warning">
                        <i class="fas fa-bell me-1"></i>Notifications récentes
                    </h6>
                    <a href="{% url 'assureur:liste_notifications_assureur' %}" class="btn btn-sm btn-warning">
                        Voir toutes
                    </a>
                </div>
                <div class="card-body">
                    {% if notifications %}
                        <div class="list-group">
                            {% for notification in notifications %}
                            <div class="list-group-item list-group-item-action flex-column align-items-start 
                                       {% if not notification.lue %}list-group-item-warning{% endif %}">
                                <div class="d-flex w-100 justify-content-between">
                                    <h6 class="mb-1">{{ notification.titre }}</h6>
                                    <small>{{ notification.date_creation|date:"d/m/Y H:i" }}</small>
                                </div>
                                <p class="mb-1">{{ notification.contenu }}</p>
                                {% if notification.lien %}
                                <a href="{{ notification.lien }}" class="btn btn-sm btn-outline-primary mt-2">
                                    Voir
                                </a>
                                {% endif %}
                            </div>
                            {% endfor %}
                        </div>
                    {% else %}
                        <div class="text-center py-4">
                            <i class="fas fa-bell-slash fa-3x text-gray-300 mb-3"></i>
                            <p class="text-muted">Aucune notification</p>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    
    messagerie_path.parent.mkdir(parents=True, exist_ok=True)
    with open(messagerie_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Template messagerie.html créé: {messagerie_path}")
else:
    print(f"✅ Template messagerie.html existe déjà")

# ============================================================================
# 2. AJOUTER LES VUES MANQUANTES DANS views.py
# ============================================================================

print("\n2. 🔧 AJOUT DES VUES MANQUANTES DANS views.py")

views_path = BASE_DIR / "assureur" / "views.py"
if views_path.exists():
    with open(views_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si les vues existent déjà
    views_to_check = [
        'def messagerie_assureur',
        'def liste_messages_assureur',
        'def liste_notifications_assureur',
        'def detail_message_assureur',
    ]
    
    missing_views = []
    for view in views_to_check:
        if view not in content:
            missing_views.append(view)
    
    if missing_views:
        print(f"❌ Vues manquantes: {missing_views}")
        
        # Ajouter les vues manquantes à la fin du fichier
        new_views = '''
# ==========================================================================
# VUES DE COMMUNICATION - AJOUTÉES AUTOMATIQUEMENT
# ==========================================================================

@login_required
@user_passes_test(assureur_required, login_url='/admin/login/')
def messagerie_assureur(request):
    """Messagerie principale pour l'assureur"""
    try:
        # Récupérer les messages
        messages_recus = []
        messages_envoyes = []
        notifications = []
        
        # Essayer d'importer les modèles de communication
        try:
            from communication.models import Message, Notification
            
            # Messages reçus (les 10 plus récents)
            messages_recus = Message.objects.filter(
                destinataire=request.user
            ).select_related('expediteur').order_by('-date_envoi')[:10]
            
            # Messages envoyés (les 10 plus récents)
            messages_envoyes = Message.objects.filter(
                expediteur=request.user
            ).select_related('destinataire').order_by('-date_envoi')[:10]
            
            # Notifications non lues
            notifications = Notification.objects.filter(
                utilisateur=request.user,
                lue=False
            ).order_by('-date_creation')[:5]
            
            # Compter les messages non lus
            messages_non_lus = Message.objects.filter(
                destinataire=request.user,
                lu=False
            ).count()
            
        except ImportError:
            # Si le module communication n'existe pas, utiliser des données vides
            messages_recus = []
            messages_envoyes = []
            notifications = []
            messages_non_lus = 0
        
        context = {
            'assureur': get_assureur_from_request(request),
            'messages_recus': messages_recus,
            'messages_envoyes': messages_envoyes,
            'notifications': notifications,
            'messages_non_lus': messages_non_lus,
        }
        
        return render(request, 'assureur/communication/messagerie.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement de la messagerie: {str(e)}")
        context = {'assureur': get_assureur_from_request(request)}
        return render(request, 'assureur/communication/messagerie.html', context)

@login_required
@user_passes_test(assureur_required, login_url='/admin/login/')
def liste_messages_assureur(request):
    """Liste complète des messages"""
    try:
        # Essayer d'importer les modèles
        try:
            from communication.models import Message
            
            # Tous les messages (reçus et envoyés)
            messages_recus = Message.objects.filter(
                destinataire=request.user
            ).select_related('expediteur').order_by('-date_envoi')
            
            messages_envoyes = Message.objects.filter(
                expediteur=request.user
            ).select_related('destinataire').order_by('-date_envoi')
            
        except ImportError:
            messages_recus = []
            messages_envoyes = []
        
        context = {
            'assureur': get_assureur_from_request(request),
            'messages_recus': messages_recus,
            'messages_envoyes': messages_envoyes,
        }
        
        return render(request, 'assureur/communication/liste_messages.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement des messages: {str(e)}")
        return redirect('assureur:messagerie_assureur')

@login_required
@user_passes_test(assureur_required, login_url='/admin/login/')
def liste_notifications_assureur(request):
    """Liste complète des notifications"""
    try:
        # Essayer d'importer les modèles
        try:
            from communication.models import Notification
            
            notifications = Notification.objects.filter(
                utilisateur=request.user
            ).order_by('-date_creation')
            
            # Marquer toutes comme lues
            notifications.filter(lue=False).update(lue=True)
            
        except ImportError:
            notifications = []
        
        context = {
            'assureur': get_assureur_from_request(request),
            'notifications': notifications,
        }
        
        return render(request, 'assureur/communication/liste_notifications.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement des notifications: {str(e)}")
        context = {'assureur': get_assureur_from_request(request)}
        return render(request, 'assureur/communication/liste_notifications.html', context)

@login_required
@user_passes_test(assureur_required, login_url='/admin/login/')
def detail_message_assureur(request, message_id):
    """Détail d'un message spécifique"""
    try:
        # Essayer d'importer les modèles
        try:
            from communication.models import Message
            
            message = Message.objects.get(id=message_id)
            
            # Marquer comme lu si le destinataire est l'utilisateur courant
            if message.destinataire == request.user and not message.lu:
                message.lu = True
                message.save()
                
        except Message.DoesNotExist:
            messages.error(request, "Message non trouvé")
            return redirect('assureur:messagerie_assureur')
        except ImportError:
            messages.error(request, "Module communication non disponible")
            return redirect('assureur:messagerie_assureur')
        
        context = {
            'assureur': get_assureur_from_request(request),
            'message': message,
        }
        
        return render(request, 'assureur/communication/detail_message.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement du message: {str(e)}")
        return redirect('assureur:messagerie_assureur')
'''
        
        # Ajouter à la fin du fichier (avant la dernière ligne s'il y a des commentaires)
        lines = content.split('\n')
        new_content = []
        added = False
        
        for line in lines:
            new_content.append(line)
            # Si on arrive à la fin du fichier (après la dernière fonction)
            if line.strip() == '' and not added:
                # Vérifier si les 10 lignes suivantes sont vides ou des commentaires
                next_lines = '\n'.join(lines[len(new_content):])
                if 'def ' not in next_lines and 'class ' not in next_lines:
                    new_content.append(new_views)
                    added = True
        
        if not added:
            # Ajouter tout à la fin
            new_content.append(new_views)
        
        with open(views_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_content))
        
        print("✅ Vues de communication ajoutées à views.py")
    else:
        print("✅ Toutes les vues de communication existent déjà")
else:
    print(f"❌ Fichier views.py non trouvé: {views_path}")

# ============================================================================
# 3. AJOUTER LA COMMUNICATION AU DASHBOARD
# ============================================================================

print("\n3. 📊 AJOUT DE LA COMMUNICATION AU DASHBOARD")

dashboard_path = BASE_DIR / "templates" / "assureur" / "dashboard.html"
if dashboard_path.exists():
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si la section communication existe déjà
    if 'Messagerie' not in content or 'communication' not in content.lower():
        # Trouver une bonne place pour insérer la section
        # Chercher la section des cartes ou une section appropriée
        lines = content.split('\n')
        new_lines = []
        inserted = False
        
        # Chercher après les autres cartes statistiques
        for i, line in enumerate(lines):
            new_lines.append(line)
            
            # Après la section des cartes principales, insérer notre carte
            if not inserted and ('<!-- End Row -->' in line or '<!-- /.row -->' in line):
                communication_card = '''
                <!-- Communication Card -->
                <div class="col-xl-3 col-md-6 mb-4">
                    <div class="card border-left-info shadow h-100 py-2">
                        <div class="card-body">
                            <div class="row no-gutters align-items-center">
                                <div class="col mr-2">
                                    <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
                                        Communication
                                    </div>
                                    <div class="h5 mb-0 font-weight-bold text-gray-800">
                                        <span id="message-count">0</span> messages
                                    </div>
                                    <div class="mt-2 mb-0">
                                        <a href="{% url 'assureur:messagerie_assureur' %}" class="btn btn-sm btn-info">
                                            <i class="fas fa-envelope fa-sm"></i> Messagerie
                                        </a>
                                        <a href="{% url 'assureur:envoyer_message_assureur' %}" class="btn btn-sm btn-outline-info ml-2">
                                            <i class="fas fa-paper-plane fa-sm"></i> Nouveau
                                        </a>
                                    </div>
                                </div>
                                <div class="col-auto">
                                    <i class="fas fa-comments fa-2x text-gray-300"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                '''
                
                new_lines.append(communication_card)
                inserted = True
        
        # Si on n'a pas trouvé l'endroit idéal, ajouter avant la fin du content
        if not inserted:
            if '{% endblock %}' in content:
                new_content = content.replace('{% endblock %}', communication_card + '\n{% endblock %}')
                with open(dashboard_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print("✅ Section communication ajoutée au dashboard (à la fin)")
            else:
                print("❌ Impossible de trouver l'endroit pour insérer la carte")
        else:
            with open(dashboard_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            print("✅ Section communication ajoutée au dashboard")
    else:
        print("✅ Section communication déjà présente dans le dashboard")
else:
    print(f"❌ Template dashboard non trouvé: {dashboard_path}")

# ============================================================================
# 4. AJOUTER LE LIEN AU MENU (base_assureur.html)
# ============================================================================

print("\n4. 🍔 AJOUT DU LIEN COMMUNICATION AU MENU")

base_path = BASE_DIR / "templates" / "assureur" / "base_assureur.html"
if base_path.exists():
    with open(base_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si le lien communication existe déjà
    if 'messagerie_assureur' not in content and 'communication' not in content.lower():
        # Chercher le menu de navigation
        menu_item = '''
        <!-- Communication -->
        <li class="nav-item">
            <a class="nav-link" href="{% url 'assureur:messagerie_assureur' %}">
                <i class="fas fa-envelope"></i>
                <span>Communication</span>
                {% if messages_non_lus and messages_non_lus > 0 %}
                <span class="badge badge-danger badge-pill">{{ messages_non_lus }}</span>
                {% endif %}
            </a>
        </li>
        '''
        
        # Chercher où insérer (après les autres liens de menu)
        # Chercher le menu des membres ou autre repère
        insert_after = ['liste_membres', 'Dashboard', 'Tableau de bord']
        
        for pattern in insert_after:
            if pattern in content:
                lines = content.split('\n')
                new_lines = []
                inserted = False
                
                for line in lines:
                    new_lines.append(line)
                    if pattern in line and 'nav-item' in line and not inserted:
                        new_lines.append(menu_item)
                        inserted = True
                
                if inserted:
                    with open(base_path, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(new_lines))
                    print("✅ Lien communication ajouté au menu")
                    break
        
        if not inserted:
            print("❌ Impossible de trouver l'endroit pour insérer dans le menu")
    else:
        print("✅ Lien communication déjà présent dans le menu")
else:
    print(f"❌ Template base_assureur.html non trouvé: {base_path}")

# ============================================================================
# 5. METTRE À JOUR LES URLs
# ============================================================================

print("\n5. 🔗 MISE À JOUR DES URLs")

urls_path = BASE_DIR / "assureur" / "urls.py"
if urls_path.exists():
    with open(urls_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si les URLs de communication existent
    urls_to_add = [
        "path('communication/', views.messagerie_assureur, name='messagerie_assureur'),",
        "path('communication/envoyer/', views.envoyer_message_assureur, name='envoyer_message_assureur'),",
        "path('communication/messages/', views.liste_messages_assureur, name='liste_messages_assureur'),",
        "path('communication/notifications/', views.liste_notifications_assureur, name='liste_notifications_assureur'),",
        "path('communication/message/<int:message_id>/', views.detail_message_assureur, name='detail_message_assureur'),",
    ]
    
    missing_urls = []
    for url in urls_to_add:
        if url.split("'")[1] not in content:
            missing_urls.append(url)
    
    if missing_urls:
        print(f"❌ URLs manquantes: {len(missing_urls)}")
        
        # Trouver où ajouter (dans la section API ou communication)
        if '# API ENDPOINTS' in content:
            # Ajouter après la section API
            lines = content.split('\n')
            new_lines = []
            added = False
            
            for line in lines:
                new_lines.append(line)
                if '# API ENDPOINTS' in line and not added:
                    # Ajouter une section Communication
                    new_lines.append('')
                    new_lines.append('    # ==========================================================================')
                    new_lines.append('    # COMMUNICATION ASSUREUR')
                    new_lines.append('    # ==========================================================================')
                    for url in missing_urls:
                        new_lines.append(f'    {url}')
                    added = True
            
            if added:
                with open(urls_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_lines))
                print("✅ URLs de communication ajoutées")
            else:
                print("❌ Impossible de trouver l'endroit pour ajouter les URLs")
        else:
            # Ajouter à la fin avant la dernière parenthèse
            if ']' in content:
                # Insérer avant le dernier ]
                last_bracket = content.rfind(']')
                before = content[:last_bracket]
                after = content[last_bracket:]
                
                new_content = before + '\n\n    # Communication\n'
                for url in missing_urls:
                    new_content += f'    {url}\n'
                new_content += after
                
                with open(urls_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print("✅ URLs de communication ajoutées (à la fin)")
    else:
        print("✅ Toutes les URLs de communication existent déjà")
else:
    print(f"❌ Fichier urls.py non trouvé: {urls_path}")

print("\n" + "="*80)
print("✅ CORRECTIONS TERMINÉES !")
print("="*80)
print("""
📋 RÉCAPITULATIF DES ACTIONS :

1. ✅ Template messagerie.html créé
2. ✅ Vues de communication ajoutées à views.py
3. ✅ Section communication ajoutée au dashboard
4. ✅ Lien communication ajouté au menu
5. ✅ URLs de communication vérifiées/mises à jour

🚀 PROCHAINES ÉTAPES :

1. Redémarrez le serveur :
   python manage.py runserver

2. Testez la communication :
   - http://localhost:8000/assureur/communication/
   - http://localhost:8000/assureur/communication/envoyer/

3. Vérifiez le dashboard :
   - La carte "Communication" doit apparaître
   - Le lien "Communication" doit être dans le menu

🔧 SI VOUS AVEZ DES PROBLÈMES :

1. Vérifiez les logs Django pour les erreurs
2. Testez les URLs directement
3. Vérifiez que le module 'communication' existe
4. Consultez la console navigateur (F12) pour les erreurs JS

📞 POUR ALLER PLUS LOIN :

- Personnalisez les templates selon vos besoins
- Ajoutez des fonctionnalités : recherche, filtres, pièces jointes
- Intégrez avec le système de notifications existant
""")