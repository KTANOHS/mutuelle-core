#!/usr/bin/env python3
"""
DIAGNOSTIC ET CORRECTION DE LA COMMUNICATION ASSUREUR
Version 1.0 - Vérifications complètes
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Django configuré avec succès")
except Exception as e:
    print(f"❌ Erreur Django: {e}")
    sys.exit(1)

print("\n" + "="*80)
print("DIAGNOSTIC COMMUNICATION ASSUREUR")
print("="*80)

# ============================================================================
# PARTIE 1: VÉRIFICATION DES VUES DE COMMUNICATION
# ============================================================================

print("\n🔍 VÉRIFICATION DES VUES DE COMMUNICATION")

try:
    from assureur.views import (
        messagerie_assureur,
        envoyer_message_assureur,
        detail_message,
        repondre_message
    )
    print("✅ Vues de communication trouvées dans assureur.views")
except ImportError as e:
    print(f"❌ Vues de communication non trouvées: {e}")

# ============================================================================
# PARTIE 2: VÉRIFICATION DES URLS
# ============================================================================

print("\n🔍 VÉRIFICATION DES URLS DE COMMUNICATION")

try:
    from django.urls import get_resolver
    
    def find_urls_containing(pattern):
        """Trouve les URLs contenant un pattern"""
        urls = []
        resolver = get_resolver()
        
        def collect_urls(patterns, prefix=''):
            for p in patterns:
                if hasattr(p, 'pattern'):
                    full_path = f"{prefix}/{p.pattern}"
                    if pattern in str(full_path):
                        urls.append(full_path)
                    if hasattr(p, 'url_patterns'):
                        collect_urls(p.url_patterns, full_path)
        
        collect_urls(resolver.url_patterns)
        return urls
    
    # Chercher les URLs de communication
    communication_urls = find_urls_containing('communication')
    messagerie_urls = find_urls_containing('messagerie')
    
    print(f"   URLs communication trouvées: {len(communication_urls)}")
    for url in communication_urls[:10]:  # Limiter à 10
        print(f"   → {url}")
    
    print(f"   URLs messagerie trouvées: {len(messagerie_urls)}")
    for url in messagerie_urls[:10]:
        print(f"   → {url}")
        
except Exception as e:
    print(f"❌ Erreur vérification URLs: {e}")

# ============================================================================
# PARTIE 3: VÉRIFICATION DES TEMPLATES
# ============================================================================

print("\n🔍 VÉRIFICATION DES TEMPLATES DE COMMUNICATION")

templates_dir = BASE_DIR / "templates" / "assureur" / "communication"
if templates_dir.exists():
    print(f"✅ Dossier templates communication trouvé: {templates_dir}")
    
    # Lister les fichiers
    template_files = list(templates_dir.glob("*.html"))
    print(f"   Templates trouvés: {len(template_files)}")
    for tpl in template_files:
        print(f"   → {tpl.name}")
else:
    print(f"❌ Dossier templates communication non trouvé: {templates_dir}")

# Vérifier les templates spécifiques
critical_templates = [
    'assureur/communication/messagerie.html',
    'assureur/communication/envoyer_message.html',
    'assureur/communication/liste_messages.html',
    'assureur/communication/detail_message.html',
    'assureur/communication/liste_notifications.html',
]

print("\n🔍 VÉRIFICATION TEMPLATES CRITIQUES:")
for template in critical_templates:
    template_path = BASE_DIR / "templates" / template
    if template_path.exists():
        print(f"✅ {template}")
    else:
        print(f"❌ {template} - NON TROUVÉ")

# ============================================================================
# PARTIE 4: VÉRIFICATION DU DASHBOARD ASSUREUR
# ============================================================================

print("\n" + "="*80)
print("DIAGNOSTIC DU DASHBOARD ASSUREUR")
print("="*80)

# Vérifier le template dashboard
dashboard_template = BASE_DIR / "templates" / "assureur" / "dashboard.html"
if dashboard_template.exists():
    print(f"✅ Template dashboard trouvé: {dashboard_template}")
    
    # Lire le contenu pour vérifier les liens de communication
    with open(dashboard_template, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Rechercher les liens de communication
    if 'communication' in content.lower():
        print("✅ Liens de communication détectés dans le dashboard")
    else:
        print("❌ Aucun lien de communication dans le dashboard")
        
    # Rechercher des liens spécifiques
    search_terms = ['messagerie', 'messages', 'notifications', 'envoyer']
    found = []
    for term in search_terms:
        if term in content.lower():
            found.append(term)
    
    if found:
        print(f"✅ Termes trouvés: {', '.join(found)}")
    else:
        print("❌ Aucun terme de communication trouvé")
        
else:
    print(f"❌ Template dashboard non trouvé: {dashboard_template}")

# ============================================================================
# PARTIE 5: ANALYSE DU MENU DE NAVIGATION
# ============================================================================

print("\n🔍 ANALYSE DU MENU DE NAVIGATION")

# Vérifier le template de base
base_template = BASE_DIR / "templates" / "assureur" / "base_assureur.html"
if base_template.exists():
    print(f"✅ Template base assureur trouvé")
    
    with open(base_template, 'r', encoding='utf-8') as f:
        base_content = f.read()
    
    # Rechercher le menu de navigation
    if 'navbar' in base_content or 'menu' in base_content or 'sidebar' in base_content:
        print("✅ Structure de menu détectée")
    else:
        print("❌ Structure de menu non détectée")
else:
    print(f"❌ Template base assureur non trouvé")

# ============================================================================
# PARTIE 6: PROPOSITION DE CORRECTIONS
# ============================================================================

print("\n" + "="*80)
print("PROPOSITION DE CORRECTIONS")
print("="*80)

print("""
📋 ACTIONS RECOMMANDÉES :

1. AJOUTER LE LIEN COMMUNICATION DANS LE DASHBOARD :
   - Modifier le template dashboard.html
   - Ajouter une carte ou un lien vers la messagerie

2. CONFIGURER LE MENU DE NAVIGATION :
   - Ajouter un lien "Communication" dans le menu principal
   - Inclure des sous-menus pour Messagerie et Notifications

3. CRÉER LES TEMPLATES MANQUANTS :
   - Créer les templates de communication s'ils n'existent pas
   - S'assurer que les vues correspondent aux templates

4. TESTER LES FONCTIONNALITÉS :
   - Tester l'accès à /assureur/communication/
   - Vérifier l'envoi et réception de messages
""")

# ============================================================================
# PARTIE 7: SCRIPT DE CORRECTION AUTOMATIQUE
# ============================================================================

print("\n" + "="*80)
print("SCRIPT DE CORRECTION AUTOMATIQUE")
print("="*80)

def create_missing_templates():
    """Crée les templates manquants"""
    templates_to_create = {
        'messagerie.html': '''{% extends 'assureur/base_assureur.html' %}
{% load static %}

{% block content %}
<div class="container-fluid">
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-gray-800">Messagerie</h1>
        <a href="{% url 'assureur:envoyer_message_assureur' %}" class="btn btn-primary">
            <i class="fas fa-paper-plane me-1"></i>Nouveau message
        </a>
    </div>

    <div class="row">
        <!-- Messages reçus -->
        <div class="col-lg-6">
            <div class="card shadow mb-4">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">Messages reçus</h6>
                </div>
                <div class="card-body">
                    {% if messages_recus %}
                        <div class="list-group">
                            {% for message in messages_recus %}
                            <a href="{% url 'assureur:detail_message' message.id %}" 
                               class="list-group-item list-group-item-action flex-column align-items-start">
                                <div class="d-flex w-100 justify-content-between">
                                    <h6 class="mb-1">{{ message.expediteur.username }}</h6>
                                    <small>{{ message.date_envoi|date:"d/m/Y H:i" }}</small>
                                </div>
                                <p class="mb-1">{{ message.contenu|truncatechars:100 }}</p>
                                {% if not message.lu %}
                                <span class="badge badge-primary">Nouveau</span>
                                {% endif %}
                            </a>
                            {% endfor %}
                        </div>
                    {% else %}
                        <p class="text-muted">Aucun message reçu</p>
                    {% endif %}
                </div>
            </div>
        </div>

        <!-- Messages envoyés -->
        <div class="col-lg-6">
            <div class="card shadow mb-4">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-success">Messages envoyés</h6>
                </div>
                <div class="card-body">
                    {% if messages_envoyes %}
                        <div class="list-group">
                            {% for message in messages_envoyes %}
                            <a href="{% url 'assureur:detail_message' message.id %}" 
                               class="list-group-item list-group-item-action flex-column align-items-start">
                                <div class="d-flex w-100 justify-content-between">
                                    <h6 class="mb-1">À: {{ message.destinataire.username }}</h6>
                                    <small>{{ message.date_envoi|date:"d/m/Y H:i" }}</small>
                                </div>
                                <p class="mb-1">{{ message.contenu|truncatechars:100 }}</p>
                            </a>
                            {% endfor %}
                        </div>
                    {% else %}
                        <p class="text-muted">Aucun message envoyé</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',
        
        'envoyer_message.html': '''{% extends 'assureur/base_assureur.html' %}
{% load static %}

{% block content %}
<div class="container-fluid">
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-gray-800">Envoyer un message</h1>
        <a href="{% url 'assureur:messagerie_assureur' %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left me-1"></i>Retour à la messagerie
        </a>
    </div>

    <div class="card shadow mb-4">
        <div class="card-body">
            <form method="post" id="messageForm">
                {% csrf_token %}
                
                <div class="form-group">
                    <label for="destinataire">Destinataire</label>
                    <select class="form-control" id="destinataire" name="destinataire" required>
                        <option value="">Sélectionnez un destinataire</option>
                        <!-- Options seront ajoutées par JavaScript -->
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="contenu">Message</label>
                    <textarea class="form-control" id="contenu" name="contenu" 
                              rows="6" placeholder="Tapez votre message ici..." required></textarea>
                </div>
                
                <div class="form-group">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-paper-plane me-1"></i>Envoyer le message
                    </button>
                    <a href="{% url 'assureur:messagerie_assureur' %}" class="btn btn-secondary">Annuler</a>
                </div>
            </form>
        </div>
    </div>
</div>

<script>
// Script pour charger les destinataires (agents, médecins, etc.)
$(document).ready(function() {
    // À compléter selon vos besoins
});
</script>
{% endblock %}'''
    }
    
    # Créer le dossier s'il n'existe pas
    comm_dir = BASE_DIR / "templates" / "assureur" / "communication"
    comm_dir.mkdir(parents=True, exist_ok=True)
    
    created = []
    for filename, content in templates_to_create.items():
        filepath = comm_dir / filename
        if not filepath.exists():
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            created.append(filename)
    
    if created:
        print(f"✅ Templates créés: {', '.join(created)}")
    else:
        print("✅ Tous les templates existent déjà")

def add_communication_to_dashboard():
    """Ajoute la section communication au dashboard"""
    dashboard_path = BASE_DIR / "templates" / "assureur" / "dashboard.html"
    
    if not dashboard_path.exists():
        print(f"❌ Dashboard non trouvé: {dashboard_path}")
        return
    
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Section à ajouter (carte de communication)
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
                            {{ messages_non_lus|default:"0" }} messages
                        </div>
                        <div class="mt-2 mb-0">
                            <a href="{% url 'assureur:messagerie_assureur' %}" class="btn btn-sm btn-info">
                                <i class="fas fa-envelope fa-sm"></i> Voir messagerie
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
    
    # Chercher où insérer la carte (après les autres cartes)
    if '<!-- Communication Card -->' not in content:
        # Trouver la section des cartes
        if '<div class="row">' in content:
            # Ajouter après la dernière carte existante
            lines = content.split('\n')
            new_lines = []
            in_cards_section = False
            cards_added = False
            
            for i, line in enumerate(lines):
                new_lines.append(line)
                
                # Détecter la fin de la section des cartes
                if '<div class="row">' in line:
                    in_cards_section = True
                
                # Après la dernière carte, ajouter notre carte
                if in_cards_section and '</div><!-- End of cards -->' in line:
                    new_lines.append(communication_card)
                    cards_added = True
                    in_cards_section = False
            
            if not cards_added:
                # Chercher la fin des cartes autrement
                for i, line in enumerate(lines):
                    new_lines.append(line)
                    if '<!-- /.container-fluid -->' in line:
                        # Ajouter avant cette ligne
                        new_lines.insert(-1, communication_card)
                        break
            
            # Sauvegarder
            with open(dashboard_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            
            print("✅ Section communication ajoutée au dashboard")
        else:
            print("❌ Section des cartes non trouvée dans le dashboard")
    else:
        print("✅ Section communication déjà présente dans le dashboard")

def add_communication_to_menu():
    """Ajoute un lien communication dans le menu"""
    base_path = BASE_DIR / "templates" / "assureur" / "base_assureur.html"
    
    if not base_path.exists():
        print(f"❌ Template base non trouvé: {base_path}")
        return
    
    with open(base_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Item de menu à ajouter
    menu_item = '''
    <!-- Communication -->
    <li class="nav-item">
        <a class="nav-link" href="{% url 'assureur:messagerie_assureur' %}">
            <i class="fas fa-envelope"></i>
            <span>Communication</span>
        </a>
    </li>
    '''
    
    # Chercher où ajouter dans le menu
    if 'href="{% url \'assureur:messagerie_assureur\' %}' not in content:
        # Chercher la navigation
        if '<nav class="navbar' in content or '<ul class="navbar-nav' in content:
            # Ajouter après d'autres items de menu
            items_to_find = ['{% url \'assureur:dashboard\' %}', 'Dashboard', 'Tableau de bord']
            
            for item in items_to_find:
                if item in content:
                    lines = content.split('\n')
                    new_lines = []
                    
                    for line in lines:
                        new_lines.append(line)
                        if item in line and 'nav-item' in line:
                            # Ajouter notre item après
                            new_lines.append(menu_item)
                    
                    # Sauvegarder
                    with open(base_path, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(new_lines))
                    
                    print("✅ Lien communication ajouté au menu")
                    return
        
        print("❌ Menu de navigation non trouvé ou format non reconnu")
    else:
        print("✅ Lien communication déjà présent dans le menu")

# ============================================================================
# EXÉCUTION DES CORRECTIONS
# ============================================================================

print("\n🎯 APPLIQUER LES CORRECTIONS ?")
print("1. Créer les templates manquants")
print("2. Ajouter la communication au dashboard")
print("3. Ajouter la communication au menu")
print("4. Tout appliquer")
print("5. Annuler")

choice = input("\nChoisissez une option (1-5): ").strip()

if choice == '1':
    create_missing_templates()
elif choice == '2':
    add_communication_to_dashboard()
elif choice == '3':
    add_communication_to_menu()
elif choice == '4':
    create_missing_templates()
    add_communication_to_dashboard()
    add_communication_to_menu()
    print("\n✅ Toutes les corrections ont été appliquées !")
elif choice == '5':
    print("❌ Correction annulée")
else:
    print("❌ Choix invalide")

print("\n" + "="*80)
print("INSTRUCTIONS POUR COMPLÉTER LA MISE EN ŒUVRE")
print("="*80)
print("""
📋 ÉTAPES MANUELLES NÉCESSAIRES :

1. CRÉER/MODIFIER LES VUES DANS views.py :
   - Assurez-vous que les vues existent
   - Ajoutez la logique de récupération des messages

2. METTRE À JOUR LE CONTEXTE DANS dashboard_assureur :
   - Ajoutez 'messages_non_lus' au contexte
   - Exemple: context['messages_non_lus'] = Message.objects.filter(destinataire=request.user, lu=False).count()

3. CONFIGURER LES MODÈLES DE MESSAGERIE :
   - Vérifiez que le modèle Message existe
   - Ajoutez les relations nécessaires

4. TESTER LES FONCTIONNALITÉS :
   - Accédez à /assureur/communication/
   - Testez l'envoi de messages
   - Vérifiez les notifications

🔧 POUR UNE SOLUTION COMPLÈTE :
   Consultez le module communication/ de votre projet pour intégrer
   le système de messagerie existant.
""")

print("\n🎯 PROCHAINE ÉTAPE :")
print("Redémarrez le serveur et testez :")
print("  python manage.py runserver")
print("  http://localhost:8000/assureur/")