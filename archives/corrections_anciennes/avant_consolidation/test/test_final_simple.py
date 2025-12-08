# test_final_simple.py
import os
import sys

# Ajouter le chemin du projet
sys.path.append('/Users/koffitanohsoualiho/Documents/VERIFICATION/projet')

def test_templates():
    print("🧪 TEST FINAL - TEMPLATES")
    print("=" * 40)
    
    # Vérifier les templates critiques
    templates_critiques = [
        'templates/agents/base_agent.html',
        'templates/agents/dashboard.html', 
        'templates/agents/creer_bon_soin.html',
        'templates/agents/error.html'
    ]
    
    probleme_trouve = False
    
    for template_relatif in templates_critiques:
        template_path = os.path.join(
            '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet',
            template_relatif
        )
        
        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                content = f.read()
            
            # Vérifier les problèmes
            if 'tableau_de_bord_agent' in content:
                print(f"❌ {template_relatif}: Contient 'tableau_de_bord_agent'")
                probleme_trouve = True
            elif "{% url 'agents:dashboard' %}" in content or '{% url "agents:dashboard" %}' in content:
                print(f"✅ {template_relatif}: URLs corrigées")
            else:
                print(f"⚠️  {template_relatif}: Aucune URL dashboard détectée")
        else:
            print(f"⚠️  {template_relatif}: Non trouvé")
    
    return not probleme_trouve

def test_urls_config():
    print("\n🔗 TEST CONFIGURATION URLs")
    print("-" * 30)
    
    # Vérifier agents/urls.py
    urls_path = '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/agents/urls.py'
    if os.path.exists(urls_path):
        with open(urls_path, 'r') as f:
            content = f.read()
        
        if "name='dashboard'" in content and 'tableau-de-bord/' in content:
            print("✅ agents/urls.py: Configuration dashboard correcte")
        else:
            print("❌ agents/urls.py: Problème de configuration")
            return False
    else:
        print("❌ agents/urls.py: Fichier non trouvé")
        return False
    
    return True

def main():
    print("🚀 TEST FINAL SIMPLIFIÉ")
    print("=" * 40)
    
    # Test des templates
    templates_ok = test_templates()
    
    # Test de la configuration URLs
    urls_ok = test_urls_config()
    
    # Résumé
    print("\n" + "=" * 40)
    if templates_ok and urls_ok:
        print("🎉 TOUT EST PRÊT !")
        print("\n✅ Prochaines étapes:")
        print("   1. Activez l'environnement virtuel:")
        print("      source venv/bin/activate")
        print("   2. Redémarrez le serveur:")
        print("      python manage.py runserver")
        print("   3. Testez l'accès:")
        print("      http://localhost:8000/agents/tableau-de-bord/")
    else:
        print("❌ Problèmes détectés")
        if not templates_ok:
            print("   - Templates à corriger")
        if not urls_ok:
            print("   - Configuration URLs à vérifier")

if __name__ == "__main__":
    main()