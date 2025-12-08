#!/usr/bin/env python
"""
VÉRIFICATION DES TEMPLATES ET CONFIGURATION
"""

import os

def verifier_configuration():
    """Vérifie que tout est configuré correctement"""
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("🔍 VÉRIFICATION DE LA CONFIGURATION")
    print("=" * 40)
    
    # Vérifier les templates
    templates_dir = os.path.join(current_dir, 'templates')
    if os.path.exists(templates_dir):
        print("✅ Dossier templates trouvé")
        
        assureur_templates = os.path.join(templates_dir, 'assureur')
        if os.path.exists(assureur_templates):
            print("✅ Dossier assureur/templates trouvé")
            
            templates = os.listdir(assureur_templates)
            print(f"📋 Templates trouvés: {len(templates)}")
            for template in templates:
                print(f"   📄 {template}")
        else:
            print("❌ Dossier assureur/templates non trouvé")
    else:
        print("❌ Dossier templates non trouvé")
    
    # Vérifier les vues
    chemin_views = os.path.join(current_dir, 'assureur', 'views.py')
    if os.path.exists(chemin_views):
        print("✅ Fichier views.py trouvé")
        
        with open(chemin_views, 'r') as f:
            content = f.read()
            
        if 'render(' in content and 'assureur/' in content:
            print("✅ Vues configurées pour les templates")
        else:
            print("❌ Vues pas encore adaptées aux templates")
    else:
        print("❌ Fichier views.py non trouvé")
    
    # Vérifier les URLs
    chemin_urls = os.path.join(current_dir, 'assureur', 'urls.py')
    if os.path.exists(chemin_urls):
        print("✅ Fichier urls.py trouvé")
    else:
        print("❌ Fichier urls.py non trouvé")

if __name__ == "__main__":
    verifier_configuration()