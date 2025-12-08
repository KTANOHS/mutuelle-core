#!/usr/bin/env python3
"""
Script d'analyse pour diagnostiquer le problème du bouton "Nouveau message"
"""

import os
import django
import re
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.urls import get_resolver
from django.core.management import execute_from_command_line

BASE_DIR = Path(__file__).parent

def analyze_urls():
    """Analyse les URLs de l'application communication"""
    print("🔍 ANALYSE DES URLs")
    print("=" * 50)
    
    try:
        resolver = get_resolver()
        urls_communication = []
        
        # Parcourir toutes les URLs enregistrées
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'url_patterns'):  # Namespace
                for sub_pattern in pattern.url_patterns:
                    url_info = {
                        'pattern': str(sub_pattern.pattern),
                        'name': getattr(sub_pattern, 'name', 'N/A'),
                        'app_name': getattr(pattern, 'app_name', 'N/A')
                    }
                    if 'communication' in str(url_info).lower():
                        urls_communication.append(url_info)
            else:
                url_info = {
                    'pattern': str(pattern.pattern),
                    'name': getattr(pattern, 'name', 'N/A'),
                    'app_name': 'N/A'
                }
                if 'communication' in str(url_info).lower():
                    urls_communication.append(url_info)
        
        if urls_communication:
            print("✅ URLs trouvées dans communication:")
            for url in urls_communication:
                print(f"   - {url['pattern']} (name: {url['name']})")
        else:
            print("❌ Aucune URL trouvée pour l'app communication")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse des URLs: {e}")

def analyze_communication_views():
    """Analyse les vues de l'application communication"""
    print("\n🔍 ANALYSE DES VUES COMMUNICATION")
    print("=" * 50)
    
    views_file = BASE_DIR / 'communication' / 'views.py'
    if views_file.exists():
        with open(views_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Rechercher les fonctions de vue
        view_functions = re.findall(r'def (\w+)\(request.*?\):', content)
        print(f"✅ Vues trouvées dans communication/views.py:")
        for view in view_functions:
            print(f"   - {view}")
            
        # Vérifier la présence de nouveau_message
        if 'nouveau_message' in view_functions:
            print("✅ Vue 'nouveau_message' trouvée")
        else:
            print("❌ Vue 'nouveau_message' NON trouvée")
            
    else:
        print("❌ Fichier communication/views.py non trouvé")

def analyze_communication_urls_file():
    """Analyse le fichier urls.py de communication"""
    print("\n🔍 ANALYSE DU FICHIER URLs COMMUNICATION")
    print("=" * 50)
    
    urls_file = BASE_DIR / 'communication' / 'urls.py'
    if urls_file.exists():
        with open(urls_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        print("✅ Contenu de communication/urls.py:")
        print(content)
        
        # Vérifier la présence de nouveau_message
        if 'nouveau_message' in content:
            print("✅ URL 'nouveau_message' trouvée dans urls.py")
        else:
            print("❌ URL 'nouveau_message' NON trouvée dans urls.py")
            
    else:
        print("❌ Fichier communication/urls.py non trouvé")

def analyze_templates_for_button():
    """Analyse les templates pour trouver le bouton Nouveau message"""
    print("\n🔍 ANALYSE DES TEMPLATES")
    print("=" * 50)
    
    templates_dir = BASE_DIR / 'templates'
    button_patterns = [
        r'nouveau.message',
        r'nouveau.message',
        r'btn.*nouveau',
        r'btn.*message',
        r'fa-plus.*message'
    ]
    
    found_templates = []
    
    for template_file in templates_dir.rglob('*.html'):
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for pattern in button_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    # Trouver l'URL utilisée
                    url_pattern = r"{% url ['\"]([^'\"]+)['\"] %}"
                    urls_in_template = re.findall(url_pattern, content)
                    
                    found_templates.append({
                        'file': template_file.relative_to(BASE_DIR),
                        'urls': urls_in_template,
                        'content_snippet': content[content.find('nouveau'):content.find('nouveau')+200] if 'nouveau' in content.lower() else 'N/A'
                    })
                    break
                    
        except Exception as e:
            continue
    
    if found_templates:
        print("✅ Boutons 'Nouveau message' trouvés dans:")
        for template in found_templates:
            print(f"   📄 {template['file']}")
            print(f"      URLs utilisées: {template['urls']}")
            if template['content_snippet'] != 'N/A':
                print(f"      Extrait: {template['content_snippet'][:100]}...")
    else:
        print("❌ Aucun bouton 'Nouveau message' trouvé dans les templates")

def analyze_base_urls():
    """Analyse le fichier urls.py principal"""
    print("\n🔍 ANALYSE DES URLs PRINCIPALES")
    print("=" * 50)
    
    base_urls = BASE_DIR / 'mutuelle_core' / 'urls.py'
    if base_urls.exists():
        with open(base_urls, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Vérifier l'inclusion de communication.urls
        if 'communication' in content:
            print("✅ Application communication incluse dans les URLs principales")
            # Extraire la ligne d'inclusion
            lines = content.split('\n')
            for line in lines:
                if 'communication' in line:
                    print(f"   Ligne: {line.strip()}")
        else:
            print("❌ Application communication NON incluse dans les URLs principales")

def check_url_resolution():
    """Teste la résolution de l'URL nouveau_message"""
    print("\n🔍 TEST DE RÉSOLUTION D'URL")
    print("=" * 50)
    
    try:
        from django.urls import reverse, NoReverseMatch
        
        urls_to_test = [
            'communication:nouveau_message',
            'communication:messagerie',
            'communication:notification_list',
        ]
        
        for url_name in urls_to_test:
            try:
                url = reverse(url_name)
                print(f"✅ {url_name} → {url}")
            except NoReverseMatch:
                print(f"❌ {url_name} → URL NON TROUVÉE")
                
    except Exception as e:
        print(f"❌ Erreur lors du test des URLs: {e}")

def analyze_button_functionality():
    """Analyse la fonctionnalité du bouton"""
    print("\n🔍 ANALYSE FONCTIONNELLE")
    print("=" * 50)
    
    print("1. Vérifiez dans le navigateur:")
    print("   - Ouvrez les outils de développement (F12)")
    print("   - Allez dans l'onglet 'Console'")
    print("   - Cliquez sur le bouton 'Nouveau message'")
    print("   - Regardez les erreurs JavaScript")
    
    print("\n2. Vérifiez dans l'onglet 'Network':")
    print("   - Les requêtes HTTP générées par le clic")
    print("   - Les codes de réponse (404, 500, etc.)")
    
    print("\n3. Scénarios possibles:")
    print("   📌 URL inexistante → Créer la vue et l'URL")
    print("   📌 Erreur JavaScript → Vérifier les event listeners")
    print("   📌 Modal non initialisé → Vérifier Bootstrap")
    print("   📌 Permission refusée → Vérifier les décorateurs")

def generate_solutions():
    """Génère des solutions basées sur l'analyse"""
    print("\n🔧 SOLUTIONS RECOMMANDÉES")
    print("=" * 50)
    
    print("""
SOLUTION 1: Créer la vue et l'URL manquantes
--------------------------------------------
1. Ajouter dans communication/views.py:
   
   @login_required
   def nouveau_message(request):
       return render(request, 'communication/nouveau_message.html')

2. Ajouter dans communication/urls.py:
   
   path('nouveau-message/', views.nouveau_message, name='nouveau_message'),

SOLUTION 2: Rediriger vers la messagerie
----------------------------------------
Remplacer l'URL dans le template:
<a href="{% url 'communication:messagerie' %}" class="btn btn-primary">

SOLUTION 3: Utiliser un modal Bootstrap
---------------------------------------
Ajouter un modal dans le template et utiliser:
<button data-bs-toggle="modal" data-bs-target="#messageModal">

SOLUTION 4: Vérifier les imports Bootstrap
------------------------------------------
Assurez-vous que Bootstrap JS est chargé:
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
""")

def main():
    """Fonction principale"""
    print("🚀 DÉBUT DE L'ANALYSE DU BOUTON 'NOUVEAU MESSAGE'")
    print("=" * 60)
    
    try:
        analyze_urls()
        analyze_communication_views()
        analyze_communication_urls_file()
        analyze_templates_for_button()
        analyze_base_urls()
        check_url_resolution()
        analyze_button_functionality()
        generate_solutions()
        
        print("\n" + "=" * 60)
        print("✅ ANALYSE TERMINÉE")
        print("\n📋 RÉSUMÉ DES ACTIONS:")
        print("1. Vérifiez la console navigateur pour les erreurs JavaScript")
        print("2. Vérifiez que l'URL 'communication:nouveau_message' existe")
        print("3. Vérifiez que la vue 'nouveau_message' existe")
        print("4. Vérifiez que Bootstrap est correctement chargé")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")

if __name__ == "__main__":
    main()