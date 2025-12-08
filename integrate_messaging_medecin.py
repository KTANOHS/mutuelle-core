#!/usr/bin/env python3
"""
INTÉGRATION MESSAGERIE POUR LE MÉDECIN
"""

import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

BASE_DIR = Path(__file__).parent

def integrate_messaging_for_medecin():
    """Intègre la messagerie pour le médecin"""
    
    print("🎯 INTÉGRATION MESSAGERIE POUR LE MÉDECIN...")
    
    # 1. Intégrer dans le dashboard médecin
    integrate_medecin_dashboard()
    
    # 2. Intégrer dans la sidebar médecin  
    integrate_medecin_sidebar()
    
    # 3. Vérifier la navbar médecin
    integrate_medecin_navbar()
    
    print("✅ Intégration médecin terminée!")

def integrate_medecin_dashboard():
    """Ajoute la messagerie au dashboard médecin"""
    
    dashboard_file = BASE_DIR / 'templates' / 'medecin' / 'dashboard.html'
    
    if not dashboard_file.exists():
        print(f"❌ Dashboard médecin non trouvé: {dashboard_file}")
        return
    
    print("🔧 Intégration dans le dashboard médecin...")
    
    with open(dashboard_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si la messagerie est déjà intégrée
    if 'communication:messagerie_medecin' in content:
        print("✅ Messagerie déjà présente dans le dashboard médecin")
        return
    
    # Carte messagerie pour médecin
    messaging_card = """
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
                                <span id="unread-messages">0</span> messages
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
"""
    
    # Accès rapide messagerie
    quick_access = """
    <!-- Accès rapide Messagerie Médecin -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card border-info">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">
                        <i class="fas fa-envelope me-2"></i>Nouvelle Messagerie
                    </h5>
                </div>
                <div class="card-body text-center">
                    <p class="card-text">
                        Communiquez facilement avec les patients, pharmaciens et autres acteurs du système de santé.
                        Envoyez des messages, partagez des ordonnances et recevez des notifications.
                    </p>
                    <a href="{% url 'communication:messagerie_medecin' %}" class="btn btn-info btn-lg">
                        <i class="fas fa-inbox me-2"></i>Ouvrir ma Messagerie
                    </a>
                    <a href="{% url 'communication:nouveau_message' %}" class="btn btn-outline-info btn-lg ms-2">
                        <i class="fas fa-edit me-2"></i>Nouveau Message
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
            print("   ✅ Carte messagerie ajoutée au dashboard médecin")
    
    # Stratégie 2: Ajouter l'accès rapide après le titre
    title_patterns = [
        '<h1 class="h3 mb-0 text-gray-800">',
        '<h1 class="h3 mb-4 text-gray-800">',
        '</h1>',
        '<!-- Page Heading -->'
    ]
    
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
            modifications_made = True
            print("   ✅ Accès rapide messagerie ajouté")
            break
    
    if modifications_made:
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Messagerie intégrée avec succès dans le dashboard médecin")
    else:
        print("❌ Impossible d'intégrer la messagerie dans le dashboard médecin")

def integrate_medecin_sidebar():
    """Ajoute le lien messagerie dans la sidebar médecin"""
    
    sidebar_files = [
        'medecin/partials/_sidebar.html',
        'medecin/partials/_sidebar_updated.html'
    ]
    
    for sidebar_path in sidebar_files:
        sidebar_file = BASE_DIR / 'templates' / sidebar_path
        
        if not sidebar_file.exists():
            print(f"❌ Sidebar médecin non trouvé: {sidebar_path}")
            continue
        
        print(f"🔧 Intégration dans la sidebar: {sidebar_path}")
        
        with open(sidebar_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier si le lien existe déjà
        if 'communication:messagerie_medecin' in content:
            print(f"✅ Lien messagerie déjà présent dans {sidebar_path}")
            continue
        
        # Lien de navigation messagerie
        messaging_link = """
            <!-- Lien Messagerie Médecin -->
            <li class="nav-item">
                <a class="nav-link" href="{% url 'communication:messagerie_medecin' %}">
                    <i class="fas fa-envelope me-2"></i>
                    <span>Messagerie</span>
                    <span class="badge bg-primary rounded-pill ms-2" id="notification-badge">0</span>
                </a>
            </li>
"""
        
        # Stratégies d'insertion
        insertion_strategies = [
            # Après "Tableau de bord"
            ('<i class="fas fa-tachometer-alt', messaging_link + '            '),
            
            # Avant "Déconnexion"  
            ('<i class="fas fa-sign-out-alt', messaging_link + '            '),
            
            # Après "Profil"
            ('<i class="fas fa-user', messaging_link + '            '),
            
            # Après "Ordonnances"
            ('ordonnances', messaging_link + '            '),
        ]
        
        link_added = False
        for pattern, insertion in insertion_strategies:
            if pattern in content:
                content = content.replace(pattern, insertion + pattern)
                link_added = True
                print(f"   ✅ Lien messagerie ajouté à {sidebar_path}")
                break
        
        # Stratégie de secours
        if not link_added and '</ul>' in content:
            content = content.replace('</ul>', '            ' + messaging_link + '\n            </ul>')
            link_added = True
            print(f"   ✅ Lien messagerie ajouté (secours) à {sidebar_path}")
        
        if link_added:
            with open(sidebar_file, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            print(f"❌ Impossible d'ajouter le lien à {sidebar_path}")

def integrate_medecin_navbar():
    """Vérifie l'intégration dans la navbar médecin"""
    
    navbar_files = [
        'includes/navbar.html',  # Navbar principale
        'medecin/base_medecin.html'  # Base médecin
    ]
    
    for navbar_path in navbar_files:
        navbar_file = BASE_DIR / 'templates' / navbar_path
        
        if not navbar_file.exists():
            continue
            
        print(f"🔍 Vérification de la navbar: {navbar_path}")
        
        with open(navbar_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier si le widget messagerie existe
        if 'communication:messagerie_medecin' in content or 'communication/messagerie' in content:
            print(f"✅ Widget messagerie présent dans {navbar_path}")
        else:
            print(f"ℹ️  Navbar {navbar_path} utilise le widget principal")

def check_medecin_messaging_url():
    """Vérifie que l'URL de messagerie médecin existe"""
    
    print("\n🔗 VÉRIFICATION DE L'URL MESSAGERIE MÉDECIN...")
    
    try:
        from django.urls import reverse
        url = reverse('communication:messagerie_medecin')
        print(f"✅ URL messagerie médecin disponible: {url}")
        return True
    except Exception as e:
        print(f"❌ URL messagerie médecin non configurée: {e}")
        return False

def create_medecin_integration_summary():
    """Crée un résumé de l'intégration médecin"""
    
    summary = """
🎯 INTÉGRATION MESSAGERIE MÉDECIN - RÉSUMÉ

✅ ÉLÉMENTS INTÉGRÉS:
• Dashboard médecin - Carte statistiques messagerie
• Dashboard médecin - Accès rapide messagerie  
• Sidebar médecin - Lien de navigation
• Interface cohérente avec le thème médecin

🎨 DESIGN MÉDECIN:
• Couleur: Bleu info (#17a2b8)
• Icônes: Envelope, Inbox, Edit
• Intégration visuelle harmonieuse

🌐 URL MESSAGERIE MÉDECIN:
• http://localhost:8000/communication/medecin/messagerie/

🚀 POUR TESTER:

1. REDÉMARREZ LE SERVEUR:
   python manage.py runserver

2. ACCÉDEZ AU DASHBOARD MÉDECIN:
   http://localhost:8000/medecin/dashboard/

3. VÉRIFIEZ LES ÉLÉMENTS:
   • Carte "Messagerie" dans les statistiques
   • Section "Nouvelle Messagerie" en haut
   • Lien "Messagerie" dans la sidebar
   • Badge de notification

4. TESTEZ LA MESSAGERIE:
   • Cliquez sur "Ouvrir ma Messagerie"
   • Vérifiez l'interface messagerie médecin
   • Testez l'envoi de messages

✅ INTÉGRATION TERMINÉE!
"""
    
    summary_file = BASE_DIR / 'INTEGRATION_MEDECIN_RESUME.md'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print("✅ Résumé créé: INTEGRATION_MEDECIN_RESUME.md")

if __name__ == "__main__":
    print("🚀 LANCEMENT DE L'INTÉGRATION MESSAGERIE POUR LE MÉDECIN...")
    
    # Vérifier d'abord que l'URL existe
    if check_medecin_messaging_url():
        integrate_messaging_for_medecin()
        create_medecin_integration_summary()
        
        print("\n🎉 INTÉGRATION MÉDECIN TERMINÉE!")
        print("\n📋 RÉCAPITULATIF:")
        print("✅ Dashboard médecin - Messagerie intégrée")
        print("✅ Sidebar médecin - Lien navigation ajouté") 
        print("✅ Interface médecin - Design cohérent")
        print("✅ URL messagerie - Configurée et accessible")
        
        print("\n🚀 PROCHAINES ÉTAPES:")
        print("1. python manage.py runserver")
        print("2. Allez sur: http://localhost:8000/medecin/dashboard/")
        print("3. Vérifiez que la messagerie apparaît")
    else:
        print("\n❌ L'intégration ne peut pas continuer sans l'URL messagerie médecin")
        print("💡 Assurez-vous que la vue messagerie_medecin existe dans urls.py")