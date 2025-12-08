#!/usr/bin/env python3
"""
Vérification finale après remplacement du dashboard
"""

from pathlib import Path

def verify_final_state():
    print("🎯 ÉTAT FINAL APRÈS CORRECTIONS")
    print("=" * 50)
    
    # Vérifier que le dashboard actuel est la version vérifiée
    dashboard_path = Path("templates/agents/dashboard.html")
    verified_path = Path("templates/agents/dashboard_verified.html")
    
    if dashboard_path.exists():
        content = dashboard_path.read_text()
        
        # Vérifier les signatures de la version vérifiée
        verified_signatures = [
            'href="{% url \'agents:creer_bon_soin\' %}"',
            'href="{% url \'agents:liste_membres\' %}"',
            'href="{% url \'agents:notifications\' %}"',
            'href="{% url \'agents:verification_cotisation\' %}"'
        ]
        
        print("🔍 VÉRIFICATION DU DASHBOARD ACTUEL:")
        all_good = True
        for signature in verified_signatures:
            if signature in content:
                print(f"   ✅ {signature}")
            else:
                print(f"   ❌ {signature} - MANQUANT")
                all_good = False
        
        if all_good:
            print("\n🎉 DASHBOARD CORRECTEMENT INSTALLÉ!")
            print("   Tous les liens sont bien formatés")
        else:
            print("\n🚨 PROBLÈME: Le dashboard n'est pas la version vérifiée")
    
    # Vérifier les backups
    print(f"\n📦 BACKUPS DISPONIBLES:")
    backups = list(Path("templates/agents").glob("dashboard.html.*backup"))
    for backup in backups:
        print(f"   📁 {backup.name}")

def check_urls_configuration():
    """Vérifier une dernière fois la configuration des URLs"""
    print(f"\n🔗 CONFIGURATION DES URLS:")
    
    urls_path = Path("agents/urls.py")
    if urls_path.exists():
        content = urls_path.read_text()
        
        required_patterns = [
            ("creer_bon_soin", "path('creer-bon-soin/"),
            ("liste_membres", "path('membres/"),
            ("notifications", "path('notifications/"),
            ("verification_cotisation", "path('verification-cotisation/")
        ]
        
        for name, pattern in required_patterns:
            if pattern in content:
                print(f"   ✅ {name}")
            else:
                print(f"   ❌ {name} - PATTERN MANQUANT: {pattern}")

def create_test_instructions():
    """Créer des instructions de test"""
    print(f"\n📋 INSTRUCTIONS DE TEST FINAL:")
    print("=" * 40)
    
    instructions = [
        "1. ✅ Démarrez le serveur: python manage.py runserver 8001",
        "2. 🌐 Allez sur: http://localhost:8001/agent/dashboard/",
        "3. 🔗 Testez chaque lien du dashboard:",
        "   - 📝 Créer Bon Soin",
        "   - 👥 Liste Membres", 
        "   - 🔔 Notifications",
        "   - ✅ Vérification Cotisation",
        "4. 🧪 Vérifiez que chaque page s'affiche correctement",
        "5. 🔄 Si un lien ne marche pas, vérifiez la vue correspondante dans agents/views.py"
    ]
    
    for instruction in instructions:
        print(f"   {instruction}")

if __name__ == "__main__":
    verify_final_state()
    check_urls_configuration()
    create_test_instructions()