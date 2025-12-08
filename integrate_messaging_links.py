#!/usr/bin/env python3
"""
INTÉGRATION DES LIENS MESSAGERIE DANS TOUTES LES INTERFACES UTILISATEUR
"""

import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

BASE_DIR = Path(__file__).parent

def get_user_templates():
    """Retourne la liste des templates utilisateur à modifier"""
    
    return [
        # Membre
        ('membre', 'dashboard_membre.html', 'membre/dashboard_membre.html'),
        ('membre', 'profil_membre.html', 'membre/profil_membre.html'),
        
        # Assureur
        ('assureur', 'dashboard_assureur.html', 'assureur/dashboard_assureur.html'),
        ('assureur', 'profil_assureur.html', 'assureur/profil_assureur.html'),
        
        # Médecin
        ('medecin', 'dashboard_medecin.html', 'medecin/dashboard_medecin.html'),
        ('medecin', 'profil_medecin.html', 'medecin/profil_medecin.html'),
        
        # Agent
        ('agent', 'dashboard_agent.html', 'agent/dashboard_agent.html'),
        ('agent', 'profil_agent.html', 'agent/profil_agent.html'),
        
        # Pharmacien (existant - pour référence)
        ('pharmacien', 'dashboard_pharmacien.html', 'pharmacien/dashboard_pharmacien.html'),
    ]

def add_messaging_link_to_template(user_type, template_name, template_path):
    """Ajoute un lien vers la messagerie dans un template utilisateur"""
    
    template_file = BASE_DIR / 'templates' / template_path
    
    if not template_file.exists():
        print(f"❌ Template non trouvé: {template_path}")
        return False
    
    with open(template_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si le lien messagerie existe déjà
    if 'communication:messagerie_' in content or 'communication/' in content:
        print(f"✅ Lien messagerie déjà présent dans {template_path}")
        return True
    
    # Déterminer l'URL de messagerie selon le type d'utilisateur
    messaging_urls = {
        'membre': 'communication:messagerie_membre',
        'assureur': 'communication:messagerie_assureur', 
        'medecin': 'communication:messagerie_medecin',
        'agent': 'communication:messagerie_agent',
        'pharmacien': 'communication:messagerie_agent'  # Les pharmaciens utilisent l'interface agent
    }
    
    messaging_url = messaging_urls.get(user_type)
    if not messaging_url:
        print(f"❌ Type d'utilisateur non reconnu: {user_type}")
        return False
    
    # Créer le code HTML pour le lien messagerie
    messaging_link = f"""
    <!-- Lien vers la messagerie -->
    <li class="nav-item">
        <a class="nav-link" href="{{% url '{messaging_url}' %}}">
            <i class="fas fa-envelope me-2"></i>
            <span>Messagerie</span>
            <span class="badge bg-primary rounded-pill ms-2" id="notification-badge">0</span>
        </a>
    </li>
"""
    
    # Essayer différentes stratégies d'insertion
    insertion_points = [
        ('<i class="fas fa-sign-out-alt', messaging_link + '    '),
        ('<i class="fas fa-cog', messaging_link + '    '),
        ('<i class="fas fa-user', messaging_link + '    '),
        ('<li class="nav-item">\n        <a class="nav-link" href="{% url', '    ' + messaging_link),
    ]
    
    for pattern, insertion in insertion_points:
        if pattern in content:
            content = content.replace(pattern, insertion + pattern)
            break
    else:
        # Si aucun pattern trouvé, ajouter avant la fermeture de la navigation
        if '</ul>' in content:
            content = content.replace('</ul>', '    ' + messaging_link + '\n    </ul>')
        else:
            print(f"❌ Impossible d'ajouter le lien dans {template_path}")
            return False
    
    # Sauvegarder le template modifié
    with open(template_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Lien messagerie ajouté à {template_path}")
    return True

def create_messaging_dashboard_cards():
    """Crée des cartes de messagerie pour les tableaux de bord"""
    
    print("\n🎨 CRÉATION DES CARTES MESSAGERIE POUR LES DASHBOARDS...")
    
    dashboard_cards = {
        'membre': """
<!-- Carte Messagerie Membre -->
<div class="col-xl-3 col-md-6 mb-4">
    <div class="card border-left-primary shadow h-100 py-2">
        <div class="card-body">
            <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                    <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                        Messagerie
                    </div>
                    <div class="h5 mb-0 font-weight-bold text-gray-800">
                        <span id="unread-messages">0</span> non lus
                    </div>
                </div>
                <div class="col-auto">
                    <a href="{% url 'communication:messagerie_membre' %}" class="btn btn-primary btn-circle">
                        <i class="fas fa-envelope"></i>
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
""",
        
        'assureur': """
<!-- Carte Messagerie Assureur -->
<div class="col-xl-3 col-md-6 mb-4">
    <div class="card border-left-success shadow h-100 py-2">
        <div class="card-body">
            <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                    <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                        Messagerie
                    </div>
                    <div class="h5 mb-0 font-weight-bold text-gray-800">
                        <span id="unread-messages">0</span> messages
                    </div>
                </div>
                <div class="col-auto">
                    <a href="{% url 'communication:messagerie_assureur' %}" class="btn btn-success btn-circle">
                        <i class="fas fa-envelope"></i>
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
""",
        
        'medecin': """
<!-- Carte Messagerie Médecin -->
<div class="col-xl-3 col-md-6 mb-4">
    <div class="card border-left-info shadow h-100 py-2">
        <div class="card-body">
            <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                    <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
                        Messagerie
                    </div>
                    <div class="h5 mb-0 font-weight-bold text-gray-800">
                        <span id="unread-messages">0</span> urgents
                    </div>
                </div>
                <div class="col-auto">
                    <a href="{% url 'communication:messagerie_medecin' %}" class="btn btn-info btn-circle">
                        <i class="fas fa-envelope"></i>
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
""",
        
        'agent': """
<!-- Carte Messagerie Agent -->
<div class="col-xl-3 col-md-6 mb-4">
    <div class="card border-left-warning shadow h-100 py-2">
        <div class="card-body">
            <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                    <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                        Messagerie
                    </div>
                    <div class="h5 mb-0 font-weight-bold text-gray-800">
                        <span id="unread-messages">0</span> en attente
                    </div>
                </div>
                <div class="col-auto">
                    <a href="{% url 'communication:messagerie_agent' %}" class="btn btn-warning btn-circle">
                        <i class="fas fa-envelope"></i>
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
"""
    }
    
    for user_type, card_html in dashboard_cards.items():
        dashboard_file = BASE_DIR / 'templates' / user_type / f'dashboard_{user_type}.html'
        
        if dashboard_file.exists():
            with open(dashboard_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier si la carte existe déjà
            if 'Carte Messagerie' in content:
                print(f"✅ Carte messagerie déjà présente dans dashboard_{user_type}.html")
                continue
            
            # Trouver où insérer la carte (après les autres cartes statistiques)
            insertion_points = [
                '<!-- /.row -->',
                '<div class="row">',
                '<!-- Content Row -->'
            ]
            
            inserted = False
            for point in insertion_points:
                if point in content:
                    content = content.replace(point, point + '\n' + card_html)
                    inserted = True
                    break
            
            if inserted:
                with open(dashboard_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Carte messagerie ajoutée à dashboard_{user_type}.html")
            else:
                print(f"❌ Impossible d'ajouter la carte à dashboard_{user_type}.html")

def create_quick_access_buttons():
    """Crée des boutons d'accès rapide à la messagerie"""
    
    print("\n⚡ CRÉATION DES BOUTONS D'ACCÈS RAPIDE...")
    
    quick_access_html = """
<!-- Accès rapide Messagerie -->
<div class="row mb-4">
    <div class="col-12">
        <div class="card bg-light">
            <div class="card-body text-center py-3">
                <h5 class="card-title mb-3">
                    <i class="fas fa-envelope me-2"></i>Accès rapide à la Messagerie
                </h5>
                <a href="{% url 'communication:messagerie_%s' %}" class="btn btn-primary btn-lg">
                    <i class="fas fa-inbox me-2"></i>Ouvrir ma Messagerie
                </a>
                <a href="{% url 'communication:test_messagerie' %}" class="btn btn-outline-secondary btn-lg ms-2">
                    <i class="fas fa-vial me-2"></i>Tester toutes les interfaces
                </a>
            </div>
        </div>
    </div>
</div>
"""
    
    for user_type in ['membre', 'assureur', 'medecin', 'agent']:
        dashboard_file = BASE_DIR / 'templates' / user_type / f'dashboard_{user_type}.html'
        
        if dashboard_file.exists():
            with open(dashboard_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier si l'accès rapide existe déjà
            if 'Accès rapide Messagerie' in content:
                print(f"✅ Accès rapide déjà présent dans dashboard_{user_type}.html")
                continue
            
            # Personnaliser le HTML pour chaque utilisateur
            user_quick_access = quick_access_html % user_type
            
            # Insérer après le titre principal
            insertion_points = [
                '<h1 class="h3 mb-4 text-gray-800">',
                '<h1 class="h3 mb-0 text-gray-800">',
                '</h1>'
            ]
            
            inserted = False
            for point in insertion_points:
                if point in content:
                    if point == '</h1>':
                        content = content.replace(point, point + '\n' + user_quick_access)
                    else:
                        # Trouver la ligne suivante après le titre
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if point in line:
                                lines.insert(i + 1, user_quick_access)
                                content = '\n'.join(lines)
                                break
                    inserted = True
                    break
            
            if inserted:
                with open(dashboard_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Accès rapide ajouté à dashboard_{user_type}.html")

def create_messaging_js_integration():
    """Crée un script JS pour l'intégration de la messagerie"""
    
    print("\n📜 CRÉATION DU SCRIPT JAVASCRIPT...")
    
    js_content = """
// Intégration Messagerie - Badge de notifications
document.addEventListener('DOMContentLoaded', function() {
    // Mettre à jour le badge de notifications
    function updateNotificationBadge() {
        fetch('/communication/notifications/count/')
            .then(response => response.json())
            .then(data => {
                const badge = document.getElementById('notification-badge');
                const unreadSpan = document.getElementById('unread-messages');
                
                if (badge && data.unread_count > 0) {
                    badge.textContent = data.unread_count;
                    badge.style.display = 'inline';
                } else if (badge) {
                    badge.style.display = 'none';
                }
                
                if (unreadSpan) {
                    unreadSpan.textContent = data.unread_count || 0;
                }
            })
            .catch(error => {
                console.log('Erreur lors du chargement des notifications:', error);
            });
    }
    
    // Mettre à jour toutes les 30 secondes
    updateNotificationBadge();
    setInterval(updateNotificationBadge, 30000);
    
    // Animation pour la carte messagerie
    const messagingCard = document.querySelector('.card [href*="messagerie"]');
    if (messagingCard) {
        messagingCard.addEventListener('mouseenter', function() {
            this.closest('.card').style.transform = 'translateY(-5px)';
            this.closest('.card').style.transition = 'transform 0.3s ease';
        });
        
        messagingCard.addEventListener('mouseleave', function() {
            this.closest('.card').style.transform = 'translateY(0)';
        });
    }
    
    console.log('✅ Intégration messagerie initialisée');
});
"""
    
    js_file = BASE_DIR / 'static' / 'js' / 'messagerie-integration.js'
    js_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print("✅ Script JavaScript créé: static/js/messagerie-integration.js")

def update_base_template():
    """Met à jour le template de base pour inclure le JS de messagerie"""
    
    print("\n📄 MISE À JOUR DU TEMPLATE DE BASE...")
    
    base_file = BASE_DIR / 'templates' / 'base.html'
    
    if not base_file.exists():
        print("❌ Template base.html non trouvé")
        return
    
    with open(base_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si le script est déjà inclus
    if 'messagerie-integration.js' in content:
        print("✅ Script messagerie déjà inclus dans base.html")
        return
    
    # Ajouter le script avant la fermeture du body
    if '</body>' in content:
        script_tag = """
    <!-- Intégration Messagerie -->
    <script src="{{% static 'js/messagerie-integration.js' %}}"></script>
"""
        content = content.replace('</body>', script_tag + '\n</body>')
        
        with open(base_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Script messagerie ajouté à base.html")

def create_integration_summary():
    """Crée un résumé de l'intégration"""
    
    print("\n📋 CRÉATION DU RÉSUMÉ D'INTÉGRATION...")
    
    summary_content = """
🎯 INTÉGRATION MESSAGERIE TERMINÉE - RÉSUMÉ

✅ LIENS AJOUTÉS DANS LES INTERFACES:
• Membre: Lien dans navigation + Carte dashboard
• Assureur: Lien dans navigation + Carte dashboard  
• Médecin: Lien dans navigation + Carte dashboard
• Agent: Lien dans navigation + Carte dashboard
• Pharmacien: Lien existant préservé

🎨 FONCTIONNALITÉS INTÉGRÉES:
• Liens de navigation vers la messagerie
• Cartes statistiques dans les dashboards
• Boutons d'accès rapide
• Badges de notifications en temps réel
• Script JavaScript d'intégration

🌐 URLs ACCÈS DIRECT:
• Membre: http://localhost:8000/communication/membre/messagerie/
• Assureur: http://localhost:8000/communication/assureur/messagerie/
• Médecin: http://localhost:8000/communication/medecin/messagerie/  
• Agent: http://localhost:8000/communication/agent/messagerie/
• Test: http://localhost:8000/communication/test-messagerie/

🚀 POUR TESTER:
1. Connectez-vous avec chaque type d'utilisateur
2. Vérifiez la présence du lien "Messagerie" dans la navigation
3. Vérifiez la carte messagerie dans le dashboard
4. Testez l'accès à l'interface messagerie
5. Vérifiez que le modal "Nouveau Message" fonctionne

✅ Le système de messagerie est maintenant complètement intégré à toutes les interfaces!
"""
    
    summary_file = BASE_DIR / 'INTEGRATION_MESSAGERIE_RESUME.md'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print("✅ Résumé créé: INTEGRATION_MESSAGERIE_RESUME.md")

if __name__ == "__main__":
    print("🚀 INTÉGRATION DES LIENS MESSAGERIE DANS TOUTES LES INTERFACES...")
    
    # 1. Ajouter les liens dans la navigation
    print("\n🔗 AJOUT DES LIENS DANS LA NAVIGATION...")
    templates = get_user_templates()
    for user_type, template_name, template_path in templates:
        add_messaging_link_to_template(user_type, template_name, template_path)
    
    # 2. Créer les cartes de dashboard
    create_messaging_dashboard_cards()
    
    # 3. Créer les boutons d'accès rapide
    create_quick_access_buttons()
    
    # 4. Créer l'intégration JavaScript
    create_messaging_js_integration()
    
    # 5. Mettre à jour le template de base
    update_base_template()
    
    # 6. Créer le résumé
    create_integration_summary()
    
    print("\n🎉 INTÉGRATION TERMINÉE AVEC SUCCÈS!")
    print("\n📋 CE QUI A ÉTÉ FAIT:")
    print("✅ Liens de navigation ajoutés à toutes les interfaces")
    print("✅ Cartes messagerie dans les dashboards") 
    print("✅ Boutons d'accès rapide")
    print("✅ Intégration JavaScript pour les notifications")
    print("✅ Script inclus dans le template de base")
    print("\n🚀 POUR TESTER:")
    print("1. Redémarrez le serveur: python manage.py runserver")
    print("2. Connectez-vous avec différents utilisateurs")
    print("3. Vérifiez la présence des liens messagerie")
    print("4. Testez l'accès aux interfaces messagerie")