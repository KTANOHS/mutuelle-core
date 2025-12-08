#!/usr/bin/env python3
"""
Script de diagnostic interactif pour le bouton Nouveau Message
"""

import os
import django
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

BASE_DIR = Path(__file__).parent

def check_button_behavior():
    """Analyse le comportement réel du bouton"""
    print("🔍 DIAGNOSTIC INTERACTIF DU BOUTON")
    print("=" * 50)
    
    # 1. Trouver tous les boutons "Nouveau message"
    templates_dir = BASE_DIR / 'templates'
    button_files = []
    
    for template_file in templates_dir.rglob('*.html'):
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if 'nouveau message' in content.lower() or 'fa-plus' in content:
                # Analyser le type de bouton
                button_info = {
                    'file': template_file.relative_to(BASE_DIR),
                    'is_modal': 'data-bs-toggle="modal"' in content or 'data-toggle="modal"' in content,
                    'is_link': 'href=' in content and 'nouveau' in content.lower(),
                    'is_button': '<button' in content and 'nouveau' in content.lower(),
                    'has_js': 'onclick=' in content or 'addEventListener' in content,
                    'content': content
                }
                button_files.append(button_info)
                
        except Exception as e:
            continue
    
    print(f"✅ {len(button_files)} bouton(s) 'Nouveau message' trouvé(s)")
    
    for btn in button_files:
        print(f"\n📄 Fichier: {btn['file']}")
        print(f"   📌 Type: {'Modal' if btn['is_modal'] else 'Lien' if btn['is_link'] else 'Bouton'}")
        print(f"   🎯 JavaScript: {'OUI' if btn['has_js'] else 'NON'}")
        
        # Extraire le code du bouton
        lines = btn['content'].split('\n')
        for i, line in enumerate(lines):
            if 'nouveau' in line.lower() and ('btn' in line or 'button' in line or 'fa-plus' in line):
                print(f"   🔍 Code: {line.strip()[:100]}...")
                break

def check_bootstrap():
    """Vérifie si Bootstrap est correctement chargé"""
    print("\n🔍 VÉRIFICATION BOOTSTRAP")
    print("=" * 50)
    
    base_template = BASE_DIR / 'templates' / 'base.html'
    if base_template.exists():
        with open(base_template, 'r', encoding='utf-8') as f:
            content = f.read()
        
        bootstrap_js = 'bootstrap' in content and ('js' in content or 'cdn' in content)
        bootstrap_css = 'bootstrap' in content and ('css' in content or 'cdn' in content)
        
        print(f"✅ Bootstrap JS: {'OUI' if bootstrap_js else '❌ NON'}")
        print(f"✅ Bootstrap CSS: {'OUI' if bootstrap_css else '❌ NON'}")
        
        if not bootstrap_js:
            print("   ❌ Bootstrap JavaScript n'est pas chargé!")
            print("   💡 Ajoutez: <script src='https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js'></script>")

def check_javascript_errors():
    """Donne des instructions pour debugger JavaScript"""
    print("\n🔍 DEBUG JAVASCRIPT")
    print("=" * 50)
    print("""
INSTRUCTIONS POUR DEBUGGER:

1. OUVREZ LA CONSOLE NAVIGATEUR:
   - F12 → Onglet "Console"
   - Actualisez la page
   - Cliquez sur le bouton
   - Notez les erreurs rouges

2. VÉRIFIEZ LE RÉSEAU:
   - F12 → Onglet "Network"
   - Cliquez sur le bouton
   - Regardez les requêtes HTTP

3. TESTEZ LE BOUTON DIRECTEMENT:
   - Clic droit → Inspecter l'élément
   - Dans la console, tapez:
     document.querySelector('[href*="nouveau"]').click()
     OU
     document.querySelector('[data-bs-target*="message"]').click()

4. VÉRIFIEZ LES ÉVÉNEMENTS:
   - F12 → Onglet "Elements"
   - Clic droit sur le bouton → Break on → Attribute modifications
""")

def test_button_manually():
    """Test manuel du bouton"""
    print("\n🔍 TEST MANUEL")
    print("=" * 50)
    print("""
TESTEZ CES SOLUTIONS:

1. SOLUTION TEMPORAIRE - Ajouter un onclick:
   <a href="#" onclick="alert('Bouton cliqué!'); return false;" class="btn btn-primary">

2. VÉRIFIER LE HTML:
   - Le bouton a-t-il la classe 'btn'?
   - L'URL est-elle correcte?
   - Y a-t-il des erreurs 404?

3. TESTER AVEC JAVASCRIPT:
   - Ajoutez ce code temporairement:
   
   <script>
   document.addEventListener('DOMContentLoaded', function() {
       const btn = document.querySelector('.btn-primary');
       if (btn) {
           btn.addEventListener('click', function(e) {
               e.preventDefault();
               alert('Bouton cliqué!');
               // Votre logique ici
           });
       }
   });
   </script>
""")

def quick_fixes():
    """Solutions rapides à tester"""
    print("\n🔧 SOLUTIONS RAPIDES À TESTER")
    print("=" * 50)
    
    print("""
SOLUTION 1 - Forcer le comportement:
------------------------------------
<a href="{% url 'communication:message_create' %}" 
   class="btn btn-primary"
   onclick="window.location.href='{% url 'communication:message_create' %}'; return false;">
   <i class="fas fa-plus me-2"></i>Nouveau message
</a>

SOLUTION 2 - Utiliser un vrai bouton:
-------------------------------------
<button type="button" 
        class="btn btn-primary"
        onclick="window.location.href='{% url 'communication:message_create' %}';">
   <i class="fas fa-plus me-2"></i>Nouveau message
</button>

SOLUTION 3 - Modal simple:
--------------------------
<button type="button" 
        class="btn btn-primary" 
        data-bs-toggle="modal" 
        data-bs-target="#testModal">
   <i class="fas fa-plus me-2"></i>Nouveau message
</button>

<!-- Modal de test -->
<div class="modal fade" id="testModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Test Modal</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <p>Le modal fonctionne !</p>
      </div>
    </div>
  </div>
</div>
""")

def main():
    print("🎯 DIAGNOSTIC COMPLET DU BOUTON 'NOUVEAU MESSAGE'")
    print("=" * 60)
    
    check_button_behavior()
    check_bootstrap()
    check_javascript_errors()
    test_button_manually()
    quick_fixes()
    
    print("\n" + "=" * 60)
    print("🎯 PROCHAINES ÉTAPES:")
    print("1. Testez la SOLUTION 1 (Forcer le comportement)")
    print("2. Vérifiez la console navigateur pour les erreurs")
    print("3. Testez avec le modal simple (SOLUTION 3)")
    print("4. Signalez ce que vous voyez dans la console")

if __name__ == "__main__":
    main()