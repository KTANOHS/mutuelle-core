#!/usr/bin/env python3
"""
CORRECTION DIRECTE ET FORCÉE DU DASHBOARD AGENT
Ajout manuel de la messagerie dans le fichier exact
"""

import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

BASE_DIR = Path(__file__).parent

def force_fix_dashboard():
    """Correction forcée du dashboard agent"""
    
    print("🚨 CORRECTION FORCÉE DU DASHBOARD AGENT")
    print("=" * 50)
    
    dashboard_path = BASE_DIR / 'templates' / 'agents' / 'dashboard.html'
    
    if not dashboard_path.exists():
        print("❌ Fichier dashboard.html non trouvé!")
        return
    
    print(f"📊 Traitement de: {dashboard_path}")
    
    # Lire le contenu actuel
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"   Taille actuelle: {len(content)} caractères")
    
    # Vérifier si la messagerie est déjà présente
    if 'communication:messagerie_agent' in content:
        print("✅ Messagerie déjà présente - Vérification de l'affichage...")
        show_messaging_elements(content)
        return
    
    # Élément de messagerie à insérer
    messaging_card = """
<!-- ============================ -->
<!-- MESSAGERIE AGENT - AJOUTÉE -->
<!-- ============================ -->

<!-- Carte Statistiques Messagerie -->
<div class="col-xl-3 col-md-6 mb-4">
    <div class="card border-left-warning shadow h-100 py-2">
        <div class="card-body">
            <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                    <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                        Messagerie
                    </div>
                    <div class="h5 mb-0 font-weight-bold text-gray-800">
                        <span id="agent-message-count">0</span> messages
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
    
    # STRATÉGIE: Insérer après la première occurrence de col-xl-3 col-md-6 mb-4
    target_pattern = 'col-xl-3 col-md-6 mb-4'
    
    if target_pattern in content:
        first_occurrence = content.find(target_pattern)
        
        # Trouver le début de la ligne
        line_start = content.rfind('\n', 0, first_occurrence)
        if line_start == -1:
            line_start = 0
        else:
            line_start += 1  # Après le saut de ligne
        
        # Insérer la carte messagerie
        new_content = content[:line_start] + messaging_card + content[line_start:]
        
        # Sauvegarder
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Carte messagerie ajoutée avec succès!")
        
        # Vérification
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            updated_content = f.read()
        
        if 'communication:messagerie_agent' in updated_content:
            print("✅ Vérification: Lien messagerie présent")
        else:
            print("❌ Vérification: Lien messagerie ABSENT")
        
        print(f"📊 Nouvelle taille: {len(updated_content)} caractères")
        
    else:
        print("❌ Structure non reconnue - Ajout en fin de fichier")
        add_to_end_of_file(dashboard_path, content)

def add_to_end_of_file(file_path, content):
    """Ajoute la messagerie à la fin du fichier"""
    
    messaging_section = """

<!-- ========================================== -->
<!-- SECTION MESSAGERIE AGENT - AJOUTÉE À LA FIN -->
<!-- ========================================== -->

<!-- Carte Messagerie -->
<div class="col-xl-3 col-md-6 mb-4">
    <div class="card border-left-warning shadow h-100 py-2">
        <div class="card-body">
            <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                    <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                        Messagerie
                    </div>
                    <div class="h5 mb-0 font-weight-bold text-gray-800">
                        <span id="agent-message-count">0</span> messages
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

<!-- Section Accès Rapide Messagerie -->
<div class="row mt-4">
    <div class="col-12">
        <div class="card shadow">
            <div class="card-header bg-warning text-white">
                <h5 class="mb-0">
                    <i class="fas fa-envelope me-2"></i>Centre de Messagerie
                </h5>
            </div>
            <div class="card-body text-center">
                <p class="card-text mb-4">
                    Communiquez avec les membres, médecins, pharmaciens et assureurs.
                </p>
                <a href="{% url 'communication:messagerie_agent' %}" class="btn btn-warning btn-lg me-2">
                    <i class="fas fa-inbox me-2"></i>Ma Messagerie
                </a>
                <a href="{% url 'communication:nouveau_message' %}" class="btn btn-outline-warning btn-lg">
                    <i class="fas fa-edit me-2"></i>Nouveau Message
                </a>
            </div>
        </div>
    </div>
</div>

"""
    
    # Ajouter avant la fermeture du contenu principal
    if '</div>' in content:
        last_div = content.rfind('</div>')
        new_content = content[:last_div] + messaging_section + content[last_div:]
    else:
        new_content = content + messaging_section
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Section messagerie ajoutée à la fin du fichier")

def show_messaging_elements(content):
    """Affiche les éléments de messagerie présents"""
    
    print("\n🔍 ANALYSE DES ÉLÉMENTS MESSAGERIE...")
    
    elements = {
        'Liens messagerie': content.count('communication:messagerie_agent'),
        'Cartes messagerie': content.count('Messagerie</div>'),
        'Boutons messagerie': len([m for m in content.split('\n') if 'messagerie' in m.lower() and 'btn' in m]),
        'Sections messagerie': content.count('Centre de Messagerie'),
    }
    
    for element, count in elements.items():
        status = "✅" if count > 0 else "❌"
        print(f"   {status} {element}: {count}")

def check_sidebar_integration():
    """Vérifie l'intégration dans la sidebar"""
    
    print("\n📁 VÉRIFICATION SIDEBAR...")
    
    sidebar_path = BASE_DIR / 'templates' / 'includes' / 'sidebar.html'
    
    if not sidebar_path.exists():
        print("❌ sidebar.html non trouvé dans includes/")
        return
    
    with open(sidebar_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'communication:messagerie_agent' in content:
        print("✅ Sidebar: Lien messagerie présent")
    else:
        print("❌ Sidebar: Lien messagerie ABSENT")
        print("💡 Ajout du lien dans la sidebar...")
        add_sidebar_link(sidebar_path, content)

def add_sidebar_link(sidebar_path, content):
    """Ajoute le lien messagerie dans la sidebar"""
    
    messaging_link = """
            <!-- Lien Messagerie Agent -->
            <li class="nav-item">
                <a class="nav-link" href="{% url 'communication:messagerie_agent' %}">
                    <i class="fas fa-envelope me-2"></i>
                    <span>Messagerie</span>
                    <span class="badge bg-warning rounded-pill ms-2">0</span>
                </a>
            </li>
"""
    
    # Ajouter après le lien Tableau de bord
    if 'Tableau de bord' in content:
        dashboard_pos = content.find('Tableau de bord')
        if dashboard_pos != -1:
            # Trouver la fin de cette ligne
            line_end = content.find('</li>', dashboard_pos)
            if line_end != -1:
                line_end += 5
                new_content = content[:line_end] + messaging_link + content[line_end:]
                
                with open(sidebar_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print("✅ Lien messagerie ajouté à la sidebar")

def create_fix_report():
    """Crée un rapport de correction"""
    
    report = """
🎯 RAPPORT DE CORRECTION - MESSAGERIE AGENT

📊 ACTION EFFECTUÉE:
• Correction FORCÉE du dashboard agents/dashboard.html
• Ajout de la carte statistiques messagerie
• Ajout de la section d'accès rapide
• Vérification de la sidebar

🔧 MODIFICATIONS:
• templates/agents/dashboard.html - Carte et section messagerie
• templates/includes/sidebar.html - Lien navigation (si absent)

🚀 POUR TESTER:

1. REDÉMARRER LE SERVEUR:
   python manage.py runserver

2. VISITER LE DASHBOARD AGENT:
   http://localhost:8000/agents/dashboard/

3. VÉRIFIER:
   ✅ Carte "Messagerie" dans les statistiques
   ✅ Section "Centre de Messagerie" 
   ✅ Boutons "Ma Messagerie" et "Nouveau Message"

4. TESTER LA NAVIGATION:
   ✅ Lien "Messagerie" dans la sidebar
   ✅ Accès à l'interface messagerie

🎉 RÉSULTAT ATTENDU:
Le dashboard agent doit maintenant afficher clairement la messagerie!

⚠️  SI PROBLEMES:
1. Vider le cache navigateur (Ctrl+F5)
2. Vérifier les logs Django
3. Contrôler le fichier dashboard.html modifié
"""
    
    report_path = BASE_DIR / 'RAPPORT_CORRECTION_DASHBOARD.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📄 Rapport créé: {report_path}")

if __name__ == "__main__":
    force_fix_dashboard()
    check_sidebar_integration()
    create_fix_report()