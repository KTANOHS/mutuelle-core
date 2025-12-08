#!/usr/bin/env python
"""
Script pour créer l'alias du template base manquant
"""

from pathlib import Path

def create_base_alias():
    """Crée l'alias agents/base.html qui étend base_agent.html"""
    alias_content = """{% extends "agents/base_agent.html" %}

{# 
Ce fichier sert d'alias pour résoudre l'erreur "agents/base.html" non trouvé
Tous les templates qui utilisent {% extends "agents/base.html" %} fonctionneront maintenant
#}"""
    
    template_path = Path('templates/agents/base.html')
    template_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(alias_content)
    
    print("✅ Alias agents/base.html créé")

def check_all_templates():
    """Vérifie tous les templates agents"""
    templates_dir = Path('templates/agents')
    
    if not templates_dir.exists():
        print("❌ Dossier templates/agents introuvable")
        return
    
    print("🔍 Vérification des templates agents...")
    
    for template_file in templates_dir.glob('*.html'):
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if '{% extends ' in content:
                if 'agents/base.html' in content:
                    print(f"  ✅ {template_file.name} - utilise agents/base.html")
                elif 'agents/base_agent.html' in content:
                    print(f"  ✅ {template_file.name} - utilise agents/base_agent.html")
                else:
                    print(f"  ℹ️  {template_file.name} - utilise un autre template de base")
            else:
                print(f"  ℹ️  {template_file.name} - pas de extends")
                
        except Exception as e:
            print(f"  ❌ {template_file.name} - erreur: {e}")

def update_urls_if_needed():
    """Vérifie si les URLs agents sont correctes"""
    urls_path = Path('agents/urls.py')
    
    if not urls_path.exists():
        print("❌ agents/urls.py introuvable")
        return
    
    with open(urls_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier les URLs critiques
    critical_urls = [
        ('dashboard', 'Tableau de bord'),
        ('liste_membres', 'Liste membres'),
        ('creer_bon_soin', 'Créer bon soin'),
    ]
    
    print("🔍 Vérification des URLs agents...")
    
    for url_name, description in critical_urls:
        if f"name='{url_name}'" in content or f'name="{url_name}"' in content:
            print(f"  ✅ {description} - URL configurée")
        else:
            print(f"  ❌ {description} - URL manquante")

def main():
    print("🔧 CRÉATION DE L'ALIAS POUR agents/base.html")
    print("=" * 50)
    
    create_base_alias()
    print()
    check_all_templates()
    print()
    update_urls_if_needed()
    
    print("\n" + "=" * 50)
    print("🎉 CORRECTION TERMINÉE!")
    print("=" * 50)
    print("\n💡 Explication:")
    print("   • Création de agents/base.html comme alias de agents/base_agent.html")
    print("   • Tous les templates qui utilisent 'agents/base.html' fonctionneront maintenant")
    print("   • Votre template base_agent.html existant est préservé")
    
    print("\n🚀 Testez maintenant:")
    print("   python manage.py runserver")
    print("   Accédez à: http://127.0.0.1:8000/agents/")

if __name__ == "__main__":
    main()