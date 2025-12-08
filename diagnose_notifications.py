#!/usr/bin/env python3
"""
Diagnostic spécifique du problème notifications
"""

from pathlib import Path

def diagnose_notifications_issue():
    print("🔍 DIAGNOSTIC DU PROBLÈME NOTIFICATIONS")
    print("=" * 50)
    
    # 1. Vérifier agents/urls.py
    urls_path = Path("agents/urls.py")
    if urls_path.exists():
        content = urls_path.read_text()
        print("📋 CONTENU DE agents/urls.py:")
        print("-" * 30)
        
        # Afficher les lignes pertinentes
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if 'notifications' in line.lower():
                print(f"Ligne {i}: {line.strip()}")
        
        # Vérifier spécifiquement l'URL notifications
        if "name='notifications'" in content or 'name="notifications"' in content:
            print("\n✅ URL 'notifications' trouvée dans agents/urls.py")
        else:
            print("\n❌ URL 'notifications' NON trouvée dans agents/urls.py")
            
            # Chercher des noms similaires
            import re
            notification_patterns = re.findall(r"name=['\"](.*notifications.*)['\"]", content)
            if notification_patterns:
                print(f"⚠️  Noms similaires trouvés: {notification_patterns}")

def fix_notifications_url():
    """Corriger l'URL notifications manquante"""
    urls_path = Path("agents/urls.py")
    
    if not urls_path.exists():
        print("❌ agents/urls.py non trouvé")
        return
    
    content = urls_path.read_text()
    original_content = content
    
    print("\n🔧 CORRECTION DE L'URL NOTIFICATIONS")
    print("=" * 40)
    
    # Vérifier si l'URL notifications existe mais avec un mauvais nom
    if "path('notifications/" in content:
        # L'URL existe mais le nom est différent
        if "name='agents_notifications'" in content:
            content = content.replace("name='agents_notifications'", "name='notifications'")
            print("✅ Nom corrigé: agents_notifications → notifications")
        elif 'name="agents_notifications"' in content:
            content = content.replace('name="agents_notifications"', 'name="notifications"')
            print('✅ Nom corrigé: agents_notifications → notifications')
        else:
            # Ajouter le nom manquant
            content = content.replace(
                "path('notifications/', views.agents_notifications),",
                "path('notifications/', views.agents_notifications, name='notifications'),"
            )
            print("✅ Nom 'notifications' ajouté à l'URL existante")
    else:
        # L'URL n'existe pas du tout - l'ajouter
        new_url = "    path('notifications/', views.agents_notifications, name='notifications'),\n"
        
        # Trouver où l'ajouter (après l'URL membres)
        if "path('membres/', views.liste_membres, name='liste_membres')," in content:
            content = content.replace(
                "path('membres/', views.liste_membres, name='liste_membres'),",
                "path('membres/', views.liste_membres, name='liste_membres'),\n" + new_url
            )
            print("✅ URL 'notifications' ajoutée après 'membres'")
        else:
            # Ajouter à la fin des URLs
            content = content.replace(
                "urlpatterns = [",
                "urlpatterns = [\n" + new_url
            )
            print("✅ URL 'notifications' ajoutée au début des URLs")
    
    if content != original_content:
        urls_path.write_text(content)
        print("✅ Correction appliquée")
    else:
        print("ℹ️  Aucune correction nécessaire")

def verify_notifications_view():
    """Vérifier que la vue notifications existe"""
    views_path = Path("agents/views.py")
    
    if not views_path.exists():
        print("❌ agents/views.py non trouvé")
        return
    
    content = views_path.read_text()
    
    print("\n👁️ VÉRIFICATION DE LA VUE NOTIFICATIONS:")
    if "def agents_notifications" in content:
        print("✅ Vue 'agents_notifications' trouvée")
    else:
        print("❌ Vue 'agents_notifications' NON trouvée")
        
        # Chercher des vues similaires
        import re
        notification_views = re.findall(r"def (.*notification.*)\(", content)
        if notification_views:
            print(f"⚠️  Vues similaires trouvées: {notification_views}")

if __name__ == "__main__":
    diagnose_notifications_issue()
    fix_notifications_url()
    verify_notifications_view()
    
    print("\n🎯 TEST FINAL APRÈS CORRECTION:")
    from test_urls_after_fix import test_agent_urls_after_fix
    test_agent_urls_after_fix()