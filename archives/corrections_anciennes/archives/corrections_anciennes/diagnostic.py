#!/usr/bin/env python3
"""
DIAGNOSTIC DU SYSTÈME DE MESSAGERIE
"""

import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

BASE_DIR = Path(__file__).parent

def diagnostic():
    """Vérifie que tout fonctionne correctement"""
    
    print("🔍 DIAGNOSTIC DU SYSTÈME DE MESSAGERIE...")
    
    # 1. Vérifier les templates
    templates = [
        'communication/messagerie_membre.html',
        'communication/messagerie_assureur.html',
        'communication/messagerie_medecin.html', 
        'communication/messagerie_agent.html',
        'communication/partials/_universal_message_modal.html',
        'communication/test_messagerie.html'
    ]
    
    print("\n📄 VÉRIFICATION DES TEMPLATES:")
    for template in templates:
        template_file = BASE_DIR / 'templates' / template
        if template_file.exists():
            size = template_file.stat().st_size
            print(f"   ✅ {template} ({size} octets)")
        else:
            print(f"   ❌ {template} - MANQUANT")
    
    # 2. Vérifier les vues
    print("\n🔧 VÉRIFICATION DES VUES:")
    views_file = BASE_DIR / 'communication' / 'views.py'
    if views_file.exists():
        with open(views_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        views_to_check = [
            'messagerie_membre',
            'messagerie_assureur', 
            'messagerie_medecin',
            'messagerie_agent',
            'test_messagerie'
        ]
        
        for view in views_to_check:
            if f'def {view}(' in content:
                print(f"   ✅ Vue {view} présente")
            else:
                print(f"   ❌ Vue {view} manquante")
    else:
        print("   ❌ Fichier views.py non trouvé")
    
    # 3. Vérifier les URLs
    print("\n🌐 VÉRIFICATION DES URLs:")
    urls_file = BASE_DIR / 'communication' / 'urls.py'
    if urls_file.exists():
        with open(urls_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        urls_to_check = [
            'messagerie_membre',
            'messagerie_assureur',
            'messagerie_medecin', 
            'messagerie_agent',
            'test_messagerie'
        ]
        
        for url in urls_to_check:
            if url in content:
                print(f"   ✅ URL {url} présente")
            else:
                print(f"   ❌ URL {url} manquante")
    else:
        print("   ❌ Fichier urls.py non trouvé")
    
    # 4. Vérifier le modal
    print("\n🎯 VÉRIFICATION DU MODAL:")
    modal_file = BASE_DIR / 'templates' / 'communication' / 'partials' / '_universal_message_modal.html'
    if modal_file.exists():
        with open(modal_file, 'r', encoding='utf-8') as f:
            modal_content = f.read()
        
        modal_elements = [
            'id="nouveauMessageModal"',
            'data-bs-toggle="modal"',
            'data-bs-target="#nouveauMessageModal"',
            'envoyerMessage()'
        ]
        
        for element in modal_elements:
            if element in modal_content:
                print(f"   ✅ Élément {element} présent")
            else:
                print(f"   ❌ Élément {element} manquant")
    else:
        print("   ❌ Fichier modal non trouvé")
    
    print("\n📋 RÉSUMÉ DU DIAGNOSTIC:")
    print("Si tout est ✅ vert, le système est prêt!")
    print("En cas de problèmes ❌ rouges, exécutez le script de correction.")

def quick_fix():
    """Correction rapide des problèmes courants"""
    
    print("\n🔧 APPLICATION DES CORRECTIONS RAPIDES...")
    
    # Vérifier l'inclusion du modal dans les templates
    templates_to_check = [
        'messagerie_membre.html',
        'messagerie_assureur.html',
        'messagerie_medecin.html',
        'messagerie_agent.html'
    ]
    
    for template_name in templates_to_check:
        template_file = BASE_DIR / 'templates' / 'communication' / template_name
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier si le modal est inclus
            if '_universal_message_modal.html' not in content:
                print(f"   🔧 Ajout du modal dans {template_name}")
                # Ajouter l'inclusion avant la fermeture du block content
                if '</script>' in content:
                    content = content.replace('</script>', '</script>\n{% include "communication/partials/_universal_message_modal.html" %}')
                elif '{% endblock %}' in content:
                    content = content.replace('{% endblock %}', '{% include "communication/partials/_universal_message_modal.html" %}\n{% endblock %}')
                
                with open(template_file, 'w', encoding='utf-8') as f:
                    f.write(content)
    
    print("   ✅ Corrections appliquées")

if __name__ == "__main__":
    diagnostic()
    quick_fix()
    
    print("\n🎯 DIAGNOSTIC TERMINÉ!")
    print("\n🚀 POUR TESTER:")
    print("1. python manage.py runserver")
    print("2. Allez sur: http://localhost:8000/test-messagerie/")
    print("3. Testez chaque interface")
    print("4. Cliquez sur 'Nouveau Message' dans chaque interface")
    print("\n🐛 EN CAS DE PROBLÈME:")
    print("• Ouvrez la console du navigateur (F12)")
    print("• Vérifiez les erreurs JavaScript")
    print("• Vérifiez que Bootstrap est chargé")