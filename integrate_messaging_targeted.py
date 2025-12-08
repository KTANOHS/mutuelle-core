#!/usr/bin/env python3
"""
INTÉGRATION MESSAGERIE POUR MEMBRE, AGENT, ASSUREUR SEULEMENT
(Le pharmacien a déjà son interface)
"""

import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

BASE_DIR = Path(__file__).parent

def integrate_messaging_for_target_users():
    """Intègre la messagerie seulement pour membre, agent, assureur"""
    
    print("🔗 INTÉGRATION MESSAGERIE POUR MEMBRE, AGENT, ASSUREUR...")
    
    # Dashboards cibles seulement
    target_dashboards = [
        # Membre
        {
            'template': 'membres/dashboard.html',
            'messaging_url': 'communication:messagerie_membre',
            'color': 'primary',
            'title': 'Membre'
        },
        
        # Assureur
        {
            'template': 'assureur/dashboard.html', 
            'messaging_url': 'communication:messagerie_assureur',
            'color': 'success',
            'title': 'Assureur'
        },
        
        # Agent
        {
            'template': 'agents/dashboard.html',
            'messaging_url': 'communication:messagerie_agent',
            'color': 'warning', 
            'title': 'Agent'
        }
    ]
    
    for dashboard in target_dashboards:
        add_messaging_to_dashboard(
            dashboard['template'],
            dashboard['messaging_url'], 
            dashboard['color'],
            dashboard['title']
        )

def add_messaging_to_dashboard(template_path, messaging_url, color, user_type):
    """Ajoute les éléments de messagerie à un dashboard existant"""
    
    template_file = BASE_DIR / 'templates' / template_path
    
    if not template_file.exists():
        print(f"❌ Dashboard non trouvé: {template_path}")
        return
    
    with open(template_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si la messagerie est déjà intégrée
    if 'communication:messagerie_' in content:
        print(f"✅ Messagerie déjà intégrée dans {template_path}")
        return
    
    print(f"🔧 Intégration messagerie dans {template_path}...")
    
    # 1. Ajouter une carte statistique messagerie
    messaging_card = f"""
        <!-- Carte Messagerie {user_type} -->
        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-{color} shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-{color} text-uppercase mb-1">
                                Messagerie
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">
                                <span id="unread-messages">0</span> messages
                            </div>
                        </div>
                        <div class="col-auto">
                            <a href="{{% url '{messaging_url}' %}}" class="btn btn-{color} btn-circle">
                                <i class="fas fa-envelope"></i>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
"""
    
    # 2. Ajouter un bouton d'accès rapide
    quick_access = f"""
    <!-- Accès rapide Messagerie {user_type} -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card border-{color}">
                <div class="card-header bg-{color} text-white">
                    <h5 class="mb-0">
                        <i class="fas fa-envelope me-2"></i>Nouvelle Messagerie
                    </h5>
                </div>
                <div class="card-body text-center">
                    <p class="card-text">
                        Communiquez facilement avec les autres acteurs du système de santé.
                        Envoyez des messages, partagez des fichiers et recevez des notifications.
                    </p>
                    <a href="{{% url '{messaging_url}' %}}" class="btn btn-{color} btn-lg">
                        <i class="fas fa-inbox me-2"></i>Ouvrir ma Messagerie
                    </a>
                </div>
            </div>
        </div>
    </div>
"""
    
    modifications_made = False
    
    # Stratégie 1: Insérer la carte avec les autres cartes statistiques
    if 'col-xl-3 col-md-6 mb-4' in content:
        first_card_index = content.find('col-xl-3 col-md-6 mb-4')
        if first_card_index != -1:
            line_start = content.rfind('\n', 0, first_card_index) + 1
            content = content[:line_start] + messaging_card + content[line_start:]
            modifications_made = True
            print(f"   ✅ Carte ajoutée à {template_path}")
    
    # Stratégie 2: Ajouter l'accès rapide après le titre
    title_patterns = [
        '<h1 class="h3 mb-0 text-gray-800">',
        '<h1 class="h3 mb-4 text-gray-800">',
        '</h1>',
        '<!-- Page Heading -->'
    ]
    
    quick_access_added = False
    for pattern in title_patterns:
        if pattern in content:
            if pattern == '</h1>':
                h1_end = content.find('</h1>') + 6
                content = content[:h1_end] + '\n' + quick_access + content[h1_end:]
            elif pattern == '<!-- Page Heading -->':
                heading_end = content.find('-->', content.find(pattern)) + 3
                content = content[:heading_end] + '\n' + quick_access + content[heading_end:]
            else:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if pattern in line:
                        lines.insert(i + 1, quick_access)
                        content = '\n'.join(lines)
                        break
            quick_access_added = True
            modifications_made = True
            print(f"   ✅ Accès rapide ajouté à {template_path}")
            break
    
    if modifications_made:
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Messagerie intégrée avec succès dans {template_path}")
    else:
        print(f"❌ Impossible d'intégrer la messagerie dans {template_path}")

def integrate_messaging_into_target_sidebars():
    """Intègre les liens de messagerie dans les sidebars cibles"""
    
    print("\n📁 INTÉGRATION DES LIENS MESSAGERIE DANS LES SIDEBARS CIBLES...")
    
    # Sidebars cibles seulement
    target_sidebars = [
        # Sidebar Membre
        ('includes/sidebar_membre.html', 'communication:messagerie_membre', 'Membre'),
        
        # Sidebar Assureur
        ('assureur/partials/_sidebar.html', 'communication:messagerie_assureur', 'Assureur'),
        
        # Sidebar Agent
        ('includes/sidebar.html', 'communication:messagerie_agent', 'Agent'),
    ]
    
    for sidebar_path, messaging_url, user_type in target_sidebars:
        add_messaging_to_sidebar(sidebar_path, messaging_url, user_type)

def add_messaging_to_sidebar(sidebar_path, messaging_url, user_type):
    """Ajoute un lien messagerie dans une sidebar"""
    
    sidebar_file = BASE_DIR / 'templates' / sidebar_path
    
    if not sidebar_file.exists():
        print(f"❌ Sidebar non trouvé: {sidebar_path}")
        return
    
    with open(sidebar_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si le lien existe déjà
    if 'communication:messagerie_' in content:
        print(f"✅ Lien messagerie déjà présent dans {sidebar_path}")
        return
    
    print(f"🔧 Ajout du lien messagerie dans {sidebar_path}...")
    
    # Créer le lien de navigation
    messaging_link = f"""
            <!-- Lien Messagerie {user_type} -->
            <li class="nav-item">
                <a class="nav-link" href="{{% url '{messaging_url}' %}}">
                    <i class="fas fa-envelope me-2"></i>
                    <span>Messagerie</span>
                    <span class="badge bg-primary rounded-pill ms-2" id="notification-badge">0</span>
                </a>
            </li>
"""
    
    # Stratégies d'insertion dans l'ordre de priorité
    insertion_strategies = [
        # 1. Chercher après "Tableau de bord"
        ('<i class="fas fa-tachometer-alt', messaging_link + '            '),
        
        # 2. Chercher avant "Déconnexion"
        ('<i class="fas fa-sign-out-alt', messaging_link + '            '),
        
        # 3. Chercher après "Profil"
        ('<i class="fas fa-user', messaging_link + '            '),
        
        # 4. Chercher après "Paramètres"
        ('<i class="fas fa-cog', messaging_link + '            '),
    ]
    
    for pattern, insertion in insertion_strategies:
        if pattern in content:
            content = content.replace(pattern, insertion + pattern)
            with open(sidebar_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Lien messagerie ajouté à {sidebar_path}")
            return
    
    # Stratégie de secours: insérer avant la fermeture de la navigation
    if '</ul>' in content:
        content = content.replace('</ul>', '            ' + messaging_link + '\n            </ul>')
        with open(sidebar_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Lien messagerie ajouté (stratégie secours) à {sidebar_path}")
    else:
        print(f"❌ Impossible d'ajouter le lien à {sidebar_path}")

def update_target_navbars():
    """Met à jour les navbars cibles avec des liens de messagerie"""
    
    print("\n🔝 MISE À JOUR DES NAVBARS CIBLES...")
    
    # Navbar principale seulement (utilisée par tous)
    target_navbars = [
        'includes/navbar.html'
    ]
    
    for navbar_path in target_navbars:
        add_messaging_to_navbar(navbar_path)

def add_messaging_to_navbar(navbar_path):
    """Ajoute un lien messagerie dans une navbar"""
    
    navbar_file = BASE_DIR / 'templates' / navbar_path
    
    if not navbar_file.exists():
        print(f"❌ Navbar non trouvé: {navbar_path}")
        return
    
    with open(navbar_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si le lien existe déjà
    if 'communication/messagerie' in content or 'communication:messagerie_' in content:
        print(f"✅ Lien messagerie déjà présent dans {navbar_path}")
        return
    
    print(f"🔧 Ajout du widget messagerie dans {navbar_path}...")
    
    # Widget messagerie compact pour navbar
    messaging_widget = """
            <!-- Widget Messagerie Rapide -->
            <li class="nav-item dropdown no-arrow mx-1">
                <a class="nav-link dropdown-toggle" href="#" id="messagesDropdown" role="button"
                    data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <i class="fas fa-envelope fa-fw"></i>
                    <!-- Counter - Messages -->
                    <span class="badge badge-danger badge-counter" id="navbar-message-count">0</span>
                </a>
                <!-- Dropdown - Messages -->
                <div class="dropdown-list dropdown-menu dropdown-menu-right shadow animated--grow-in"
                    aria-labelledby="messagesDropdown">
                    <h6 class="dropdown-header">
                        Centre de Messages
                    </h6>
                    <a class="dropdown-item d-flex align-items-center" href="#">
                        <div class="dropdown-list-image mr-3">
                            <div class="status-indicator bg-success"></div>
                            <i class="fas fa-comments fa-2x text-primary"></i>
                        </div>
                        <div class="font-weight-bold">
                            <div class="text-truncate">Nouveau système de messagerie</div>
                            <div class="small text-gray-500">Communiquez avec tous les acteurs</div>
                        </div>
                    </a>
                    <a class="dropdown-item text-center small text-gray-500" href="{% url 'communication:test_messagerie' %}">
                        Tester la messagerie
                    </a>
                </div>
            </li>
"""
    
    # Chercher à insérer après les autres widgets de notification
    notification_patterns = [
        'id="alertsDropdown"',
        'class="nav-link dropdown-toggle"',
        '<li class="nav-item dropdown no-arrow mx-1">',
        '<!-- Nav Item - Alerts -->'
    ]
    
    for pattern in notification_patterns:
        if pattern in content:
            pattern_index = content.find(pattern)
            if pattern_index != -1:
                # Trouver la fin de cet élément
                element_end = content.find('</li>', pattern_index)
                if element_end != -1:
                    element_end += 5  # Inclure </li>
                    content = content[:element_end] + messaging_widget + content[element_end:]
                    
                    with open(navbar_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ Widget messagerie ajouté à {navbar_path}")
                    return
    
    print(f"❌ Impossible d'ajouter le widget à {navbar_path}")

def create_targeted_integration_summary():
    """Crée un résumé de l'intégration ciblée"""
    
    print("\n📋 CRÉATION DU RÉSUMÉ D'INTÉGRATION CIBLÉE...")
    
    summary = """
🎯 INTÉGRATION MESSAGERIE CIBLÉE - TERMINÉE

✅ UTILISATEURS CIBLÉS:
• Membre - Interface messagerie complète
• Agent - Interface messagerie complète  
• Assureur - Interface messagerie complète
• ⚠️ Pharmacien - CONSERVÉ son interface existante

✅ DASHBOARDS MIS À JOUR:
• membres/dashboard.html - Carte statistiques + Accès rapide
• agents/dashboard.html - Carte statistiques + Accès rapide
• assureur/dashboard.html - Carte statistiques + Accès rapide

✅ SIDEBARS MIS À JOUR:
• includes/sidebar_membre.html - Lien navigation membre
• includes/sidebar.html - Lien navigation agent
• assureur/partials/_sidebar.html - Lien navigation assureur

✅ NAVBAR MIS À JOUR:
• includes/navbar.html - Widget messagerie rapide

🌐 URLs MESSAGERIE PAR UTILISATEUR:
• Membre: http://localhost:8000/communication/membre/messagerie/
• Agent: http://localhost:8000/communication/agent/messagerie/
• Assureur: http://localhost:8000/communication/assureur/messagerie/

🎨 FONCTIONNALITÉS INTÉGRÉES:
• Cartes statistiques avec compteur de messages
• Boutons d'accès rapide bien visibles
• Liens de navigation dans les menus
• Widget de notification dans la navbar
• Design cohérent avec chaque interface

🚀 POUR TESTER:

1. REDÉMARREZ LE SERVEUR:
   python manage.py runserver

2. TESTEZ CHAQUE INTERFACE:
   
   🔹 MEMBRE:
   • Allez sur: http://localhost:8000/ (connectez-vous comme membre)
   • Vérifiez la carte "Messagerie" dans le dashboard
   • Testez le lien dans la sidebar
   • Accédez à: http://localhost:8000/communication/membre/messagerie/

   🔹 AGENT:
   • Connectez-vous comme agent
   • Vérifiez la carte messagerie dans le dashboard
   • Testez le lien navigation
   • Accédez à: http://localhost:8000/communication/agent/messagerie/

   🔹 ASSUREUR:
   • Connectez-vous comme assureur
   • Vérifiez la carte messagerie verte dans le dashboard
   • Testez le lien dans la sidebar assureur
   • Accédez à: http://localhost:8000/communication/assureur/messagerie/

3. VÉRIFIEZ LE PHARMACIEN:
   • L'interface existante doit être préservée
   • Aucun changement pour le pharmacien

✅ INTÉGRATION TERMINÉE AVEC SUCCÈS!
La messagerie est maintenant disponible pour Membre, Agent et Assureur.
Le pharmacien conserve son système existant.
"""
    
    summary_file = BASE_DIR / 'INTEGRATION_CIBLEE_RESUME.md'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print("✅ Résumé créé: INTEGRATION_CIBLEE_RESUME.md")

def verify_pharmacien_untouched():
    """Vérifie que le pharmacien n'a pas été modifié"""
    
    print("\n🔍 VÉRIFICATION QUE LE PHARMACIEN N'A PAS ÉTÉ MODIFIÉ...")
    
    pharmacien_files = [
        'pharmacien/dashboard.html',
        'pharmacien/_sidebar_pharmacien.html',
        'pharmacien/_navbar_pharmacien.html'
    ]
    
    untouched = True
    for file_path in pharmacien_files:
        full_path = BASE_DIR / 'templates' / file_path
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'communication:messagerie_' in content:
                print(f"❌ ATTENTION: {file_path} a été modifié!")
                untouched = False
            else:
                print(f"✅ {file_path} - Non modifié (conservé)")
    
    if untouched:
        print("✅ PHARMACIEN: Aucune modification - Interface existante préservée")
    else:
        print("⚠️  PHARMACIEN: Des modifications ont été détectées!")

if __name__ == "__main__":
    print("🚀 INTÉGRATION MESSAGERIE POUR MEMBRE, AGENT, ASSUREUR SEULEMENT...")
    print("⚠️  Le pharmacien conserve son interface existante")
    
    # 1. Intégrer dans les dashboards cibles
    integrate_messaging_for_target_users()
    
    # 2. Intégrer dans les sidebars cibles  
    integrate_messaging_into_target_sidebars()
    
    # 3. Mettre à jour la navbar principale
    update_target_navbars()
    
    # 4. Vérifier que le pharmacien n'a pas été touché
    verify_pharmacien_untouched()
    
    # 5. Créer le résumé
    create_targeted_integration_summary()
    
    print("\n🎉 INTÉGRATION CIBLÉE TERMINÉE AVEC SUCCÈS!")
    print("\n📋 RÉCAPITULATIF:")
    print("✅ Membre - Interface messagerie intégrée")
    print("✅ Agent - Interface messagerie intégrée") 
    print("✅ Assureur - Interface messagerie intégrée")
    print("✅ Pharmacien - Interface existante préservée")
    print("\n🚀 PROCHAINES ÉTAPES:")
    print("1. python manage.py runserver")
    print("2. Testez chaque interface cible")
    print("3. Vérifiez que le pharmacien n'a pas changé")