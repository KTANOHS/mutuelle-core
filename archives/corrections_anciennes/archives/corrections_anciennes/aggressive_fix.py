#!/usr/bin/env python3
"""
CORRECTION AGGRESSIVE des URLs cassées - VERSION FINALE
"""

from pathlib import Path
import re

def aggressive_fix_broken_urls():
    dashboard_path = Path("templates/agents/dashboard.html")
    
    if not dashboard_path.exists():
        print("❌ Dashboard non trouvé")
        return
    
    content = dashboard_path.read_text()
    original_content = content
    
    print("🚨 CORRECTION AGGRESSIVE DES URLS CASSÉES")
    print("=" * 50)
    
    # AFFICHER CE QUI NE VA PAS
    print("🔍 ANALYSE DES PROBLÈMES:")
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if 'href="{% url ' in line and '%}"' not in line:
            print(f"   Ligne {i}: {line.strip()}")
    
    # CORRECTION MANUELLE DES PATTERNS SPÉCIFIQUES
    url_mappings = {
        'agents:creer_bon_soin': 'creer_bon_soin',
        'agents:liste_membres': 'liste_membres', 
        'agents:historique_bons': 'historique_bons',
        'agents:notifications': 'notifications',
        'agents:verification_cotisation': 'verification_cotisation'
    }
    
    # PATTERN 1: href="{% url 'agents:xxx' %}" (correct) → rien à faire
    # PATTERN 2: href="{% url 'agents:xxx' %} (manque la fermeture)
    
    corrections_made = 0
    for template_url, url_name in url_mappings.items():
        # Pattern cassé: href="{% url 'agents:xxx' %} (sans la dernière quote)
        broken_pattern = f'href="\\{{% url \\\'{template_url}\\\' %}}'
        fixed_pattern = f'href="\\{{% url \\\'{template_url}\\\' %}}"'
        
        if broken_pattern in content:
            content = content.replace(broken_pattern, fixed_pattern)
            corrections_made += 1
            print(f"✅ Fixé: {template_url}")
    
    # CORRECTION GÉNÉRIQUE POUR LES RESTANTS
    # Trouver tous les href avec des URLs Django mal fermées
    broken_hrefs = re.findall(r'href="\{% url \'[^\']+\' %}[^"]*', content)
    for broken in broken_hrefs:
        if broken.count('"') == 1:  # Manque la fermeture du href
            fixed = broken + '"'
            content = content.replace(broken, fixed)
            corrections_made += 1
            print(f"✅ Correction générique: {broken[:50]}...")
    
    if content != original_content:
        # Sauvegarde
        backup_path = dashboard_path.with_suffix('.html.aggressive_fix_backup')
        Path(backup_path).write_text(original_content)
        
        # Écrire la version corrigée
        dashboard_path.write_text(content)
        print(f"\n🎯 RÉSULTAT:")
        print(f"✅ {corrections_made} corrections appliquées")
        print(f"📦 Backup sauvegardé: {backup_path}")
        
        # VÉRIFICATION
        verify_aggressive_fix()
    else:
        print("ℹ️  Aucune correction nécessaire")

def verify_aggressive_fix():
    """Vérification détaillée après correction"""
    print(f"\n🔍 VÉRIFICATION DÉTAILLÉE:")
    print("=" * 40)
    
    dashboard_path = Path("templates/agents/dashboard.html")
    content = dashboard_path.read_text()
    
    # Vérifier chaque URL individuellement
    urls_to_check = [
        'agents:creer_bon_soin',
        'agents:liste_membres',
        'agents:historique_bons', 
        'agents:notifications',
        'agents:verification_cotisation'
    ]
    
    for url in urls_to_check:
        # Vérifier si l'URL est bien formatée
        pattern = f'href="\\{{% url \\\'{url}\\\' %}}"'
        if pattern in content:
            print(f"   ✅ {url} - BIEN FORMATÉ")
        else:
            # Chercher des versions mal formatées
            broken_versions = [
                f'href="\\{{% url \\\'{url}\\\' %}}',  # Sans la dernière quote
                f'href="\\{{% url \\\'{url}',           # Très cassé
            ]
            for broken in broken_versions:
                if broken in content:
                    print(f"   ❌ {url} - TOUJOURS CASSÉ: {broken}")
                    break
            else:
                print(f"   ⚠️  {url} - NON TROUVÉ")

def fix_missing_urls_and_views():
    """Corriger les URLs et vues manquantes"""
    print(f"\n🔧 CORRECTION URLs ET VUES MANQUANTES")
    print("=" * 50)
    
    # 1. CORRIGER agents/urls.py
    urls_path = Path("agents/urls.py")
    if urls_path.exists():
        content = urls_path.read_text()
        
        # Ajouter l'URL notifications si manquante
        if "name='notifications'" not in content and 'name="notifications"' not in content:
            # Trouver où ajouter (après les autres URLs de notifications)
            if "path('notifications/" in content:
                # Remplacer le name existant
                content = content.replace(
                    "path('notifications/', views.agents_notifications, name='notifications'),",
                    "path('notifications/', views.agents_notifications, name='notifications'),"
                )
            else:
                # Ajouter après les autres URLs
                new_url = "    path('notifications/', views.agents_notifications, name='notifications'),\n"
                if "path('bons-soin/" in content:
                    content = content.replace(
                        "path('bons-soin/', views.historique_bons_soin, name='historique_bons'),",
                        "path('bons-soin/', views.historique_bons_soin, name='historique_bons'),\n" + new_url
                    )
                    print("✅ URL 'notifications' ajoutée à urls.py")
        
        # Ajouter l'URL verification_cotisation si manquante
        if "name='verification_cotisation'" not in content and 'name="verification_cotisation"' not in content:
            new_url = "    path('verification-cotisation/', views.verification_cotisation, name='verification_cotisation'),\n"
            if "path('membres/" in content:
                content = content.replace(
                    "path('membres/', views.liste_membres, name='liste_membres'),",
                    "path('membres/', views.liste_membres, name='liste_membres'),\n" + new_url
                )
                print("✅ URL 'verification_cotisation' ajoutée à urls.py")
        
        urls_path.write_text(content)
    
    # 2. CORRIGER agents/views.py (ajouter la vue manquante)
    views_path = Path("agents/views.py")
    if views_path.exists():
        content = views_path.read_text()
        
        # Ajouter la vue verification_cotisation si manquante
        if "def verification_cotisation" not in content:
            # Ajouter après la vue liste_membres
            new_view = """
def verification_cotisation(request):
    \"\"\"
    Vue pour la vérification des cotisations des membres
    \"\"\"
    # TODO: Implémenter la logique de vérification des cotisations
    context = {
        'title': 'Vérification des Cotisations',
        'membres': [],  # Remplacer par les vraies données
    }
    return render(request, 'agents/verification_cotisation.html', context)
"""
            if "def liste_membres" in content:
                # Trouver la fin de la fonction liste_membres
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if "def liste_membres" in line:
                        # Trouver la prochaine fonction
                        for j in range(i+1, len(lines)):
                            if lines[j].startswith('def ') or lines[j].startswith('class '):
                                # Insérer avant la prochaine fonction
                                lines.insert(j, new_view)
                                content = '\n'.join(lines)
                                print("✅ Vue 'verification_cotisation' ajoutée à views.py")
                                break
                        break
        
        views_path.write_text(content)

if __name__ == "__main__":
    aggressive_fix_broken_urls()
    fix_missing_urls_and_views()
    
    print(f"\n🎉 CORRECTION TERMINÉE!")
    print("🔍 Vérifiez maintenant avec: python diagnose_dashboard_urls.py")