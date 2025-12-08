#!/usr/bin/env python3
"""
Correcteur complet pour agents/urls.py - Assure que toutes les URLs sont correctes
"""

from pathlib import Path
import re

def complete_agents_urls_fix():
    urls_path = Path("agents/urls.py")
    
    if not urls_path.exists():
        print("❌ agents/urls.py non trouvé")
        return
    
    content = urls_path.read_text()
    original_content = content
    
    print("🔧 CORRECTION COMPLÈTE DE agents/urls.py")
    print("=" * 50)
    
    # 1. Vérifier et corriger chaque URL nécessaire
    required_urls = {
        'notifications': {
            'path': "path('notifications/', views.agents_notifications, name='notifications')",
            'after': 'liste_membres'
        },
        'api_derniers_bons': {
            'path': "path('api/derniers-bons/', views.api_derniers_bons, name='api_derniers_bons')",
            'after': 'notifications'
        },
        'api_stats_quotidiens': {
            'path': "path('api/stats-quotidiens/', views.api_stats_quotidiens, name='api_stats_quotidiens')", 
            'after': 'api_derniers_bons'
        },
        'api_analytics_dashboard': {
            'path': "path('api/analytics-dashboard/', views.api_analytics_dashboard, name='api_analytics_dashboard')",
            'after': 'api_stats_quotidiens'
        }
    }
    
    corrections_made = 0
    
    for url_name, url_config in required_urls.items():
        # Vérifier si l'URL existe déjà
        pattern = f"name=['\\\"']{url_name}['\\\"']"
        if re.search(pattern, content):
            print(f"✅ {url_name} - Déjà présent")
            continue
        
        # Vérifier si le chemin existe mais avec un mauvais nom
        path_pattern = url_config['path'].split(', name=')[0] + ")"
        if path_pattern in content:
            # Le chemin existe mais pas le bon nom - corriger le nom
            wrong_name_pattern = path_pattern + r",\s*name=['\"]([^'\"]+)['\"]"
            match = re.search(wrong_name_pattern, content)
            if match:
                wrong_name = match.group(1)
                content = content.replace(
                    f"{path_pattern}, name='{wrong_name}'",
                    url_config['path']
                )
                print(f"✅ {url_name} - Nom corrigé: {wrong_name} → {url_name}")
                corrections_made += 1
        else:
            # L'URL n'existe pas - l'ajouter
            after_pattern = f"name=['\\\"']{url_config['after']}['\\\"']"
            if after_pattern in content:
                # Trouver la ligne après laquelle ajouter
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if after_pattern in line:
                        # Insérer après cette ligne
                        lines.insert(i + 1, "    " + url_config['path'] + ",")
                        content = '\n'.join(lines)
                        print(f"✅ {url_name} - Ajouté après {url_config['after']}")
                        corrections_made += 1
                        break
            else:
                # Ajouter à la fin
                content = content.replace(
                    "]",
                    "    " + url_config['path'] + ",\n]"
                )
                print(f"✅ {url_name} - Ajouté à la fin")
                corrections_made += 1
    
    # 2. Vérifier l'import des vues manquantes
    if corrections_made > 0:
        # Vérifier si toutes les vues sont importées
        required_views = ['agents_notifications', 'api_derniers_bons', 'api_stats_quotidiens', 'api_analytics_dashboard']
        
        for view_name in required_views:
            if f" {view_name}" in content and f"def {view_name}" not in content:
                # La vue est utilisée mais pas importée - ajouter l'import
                if "from . import views" in content:
                    # Remplacer par un import spécifique
                    content = content.replace(
                        "from . import views",
                        f"from . import views\nfrom .views import {view_name}"
                    )
                    print(f"✅ Import ajouté pour {view_name}")
                elif "from .views import" in content:
                    # Ajouter à l'import existant
                    import_pattern = r"(from .views import [^\n]+)"
                    match = re.search(import_pattern, content)
                    if match:
                        current_import = match.group(1)
                        new_import = current_import + f", {view_name}"
                        content = content.replace(current_import, new_import)
                        print(f"✅ {view_name} ajouté aux imports")
    
    if content != original_content:
        # Sauvegarde
        backup_path = urls_path.with_suffix('.py.complete_fix_backup')
        urls_path.rename(backup_path)
        
        # Écrire la version corrigée
        urls_path.write_text(content)
        print(f"\n🎯 RÉSULTAT:")
        print(f"✅ {corrections_made} corrections appliquées")
        print(f"📦 Backup: {backup_path}")
    else:
        print("\nℹ️  Aucune correction nécessaire")

def create_missing_views():
    """Créer les vues manquantes si nécessaire"""
    views_path = Path("agents/views.py")
    
    if not views_path.exists():
        print("❌ agents/views.py non trouvé")
        return
    
    content = views_path.read_text()
    
    missing_views = []
    
    # Vérifier chaque vue nécessaire
    if "def agents_notifications" not in content:
        missing_views.append("""
def agents_notifications(request):
    \"\"\"
    Vue pour afficher les notifications de l'agent
    \"\"\"
    # TODO: Implémenter la logique des notifications
    from django.shortcuts import render
    context = {
        'title': 'Notifications Agent',
        'notifications': [],  # Remplacer par les vraies notifications
    }
    return render(request, 'agents/notifications.html', context)
""")
    
    if "def api_derniers_bons" not in content:
        missing_views.append("""
def api_derniers_bons(request):
    \"\"\"
    API pour récupérer les derniers bons de soin
    \"\"\"
    from django.http import JsonResponse
    # TODO: Implémenter la logique
    data = {
        'derniers_bons': [],
        'total': 0
    }
    return JsonResponse(data)
""")
    
    if "def api_stats_quotidiens" not in content:
        missing_views.append("""
def api_stats_quotidiens(request):
    \"\"\"
    API pour les statistiques quotidiennes
    \"\"\"
    from django.http import JsonResponse
    # TODO: Implémenter la logique
    data = {
        'bons_du_jour': 0,
        'verifications_du_jour': 0,
        'membres_contactes': 0
    }
    return JsonResponse(data)
""")
    
    if "def api_analytics_dashboard" not in content:
        missing_views.append("""
def api_analytics_dashboard(request):
    \"\"\"
    API pour les analytics du dashboard
    \"\"\"
    from django.http import JsonResponse
    # TODO: Implémenter la logique
    data = {
        'performance': {},
        'activites_recentes': []
    }
    return JsonResponse(data)
""")
    
    if missing_views:
        print("\n🔨 CRÉATION DES VUES MANQUANTES:")
        # Ajouter à la fin du fichier
        new_content = content + "\n" + "\n".join(missing_views)
        views_path.write_text(new_content)
        print(f"✅ {len(missing_views)} vues créées")
    else:
        print("✅ Toutes les vues nécessaires existent")

if __name__ == "__main__":
    complete_agents_urls_fix()
    create_missing_views()
    
    print("\n🎉 CORRECTIONS TERMINÉES!")
    print("🔍 Testez à nouveau avec: python test_urls_after_fix.py")