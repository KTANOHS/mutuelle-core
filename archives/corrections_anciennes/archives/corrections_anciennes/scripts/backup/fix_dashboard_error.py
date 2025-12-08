#!/usr/bin/env python
"""
CORRECTION DE L'ERREUR DASHBOARD ASSUREUR
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def fix_dashboard_template():
    """Corrige l'erreur dans le template dashboard"""
    print("🔧 Correction du template dashboard...")
    
    dashboard_path = BASE_DIR / 'templates' / 'assureur' / 'dashboard.html'
    
    if not dashboard_path.exists():
        print("❌ dashboard.html non trouvé")
        return
    
    with open(dashboard_path, 'r') as f:
        content = f.read()
    
    # Solution 1: Remplacer l'URL problématique
    old_code = "fetch('{% url \"assureur:statistiques_temps_reel\" %}')"
    new_code = "// fetch('{% url \"assureur:statistiques_temps_reel\" %}')  // FONCTIONNALITÉ TEMPORAIREMENT DÉSACTIVÉE"
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        print("✅ Ligne problématique commentée")
    
    # Solution 2: Commenter toute la fonction si nécessaire
    if 'function actualiserStats()' in content:
        # Trouver le début et la fin de la fonction
        lines = content.split('\n')
        in_function = False
        function_lines = []
        
        for i, line in enumerate(lines):
            if 'function actualiserStats()' in line:
                in_function = True
                function_lines.append(i)
            elif in_function and 'setInterval(actualiserStats' in line:
                function_lines.append(i)
                in_function = False
                break
        
        if len(function_lines) == 2:
            start, end = function_lines
            # Commenter le bloc
            for i in range(start, end + 1):
                if lines[i].strip() and not lines[i].strip().startswith('//'):
                    lines[i] = '// ' + lines[i]
            
            content = '\n'.join(lines)
            print("✅ Fonction actualiserStats commentée")
    
    with open(dashboard_path, 'w') as f:
        f.write(content)
    
    print("✅ Template dashboard corrigé")

def create_simple_stat_view():
    """Crée une vue simple pour les statistiques temps réel"""
    print("🔧 Création d'une vue statistiques temporaire...")
    
    views_path = BASE_DIR / 'assureur' / 'views.py'
    
    # Vérifier si la vue existe déjà
    with open(views_path, 'r') as f:
        content = f.read()
    
    if 'def statistiques_temps_reel' not in content:
        # Ajouter la vue manquante
        stats_view = '''

# ==============================================================================
# VUE TEMPORAIRE POUR CORRIGER L'ERREUR
# ==============================================================================

@login_required
@assureur_required
def statistiques_temps_reel(request):
    """API temporaire pour les statistiques temps réel"""
    from django.http import JsonResponse
    from membres.models import Membre, Bon
    from django.utils import timezone
    from datetime import timedelta
    
    try:
        stats = {
            'membres_actifs': Membre.objects.filter(statut='AC').count(),
            'bons_ce_mois': Bon.objects.filter(
                date_emission__month=timezone.now().month
            ).count(),
            'success': True
        }
        return JsonResponse({'success': True, 'stats': stats})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
'''
        
        with open(views_path, 'a') as f:
            f.write(stats_view)
        print("✅ Vue statistiques_temps_reel créée")
    else:
        print("✅ Vue statistiques_temps_reel existe déjà")

def add_url_pattern():
    """Ajoute le pattern d'URL manquant"""
    print("🔧 Ajout de l'URL manquante...")
    
    urls_path = BASE_DIR / 'assureur' / 'urls.py'
    
    with open(urls_path, 'r') as f:
        content = f.read()
    
    # Vérifier si l'URL existe déjà
    if 'statistiques_temps_reel' not in content:
        # Ajouter l'URL à la liste existante
        if 'urlpatterns = [' in content:
            content = content.replace(
                "urlpatterns = [",
                "urlpatterns = [\n    # API temps réel\n    path('api/statistiques/', views.statistiques_temps_reel, name='statistiques_temps_reel'),"
            )
            print("✅ URL statistiques_temps_reel ajoutée")
        else:
            print("❌ Structure URLs non reconnue")
    else:
        print("✅ URL statistiques_temps_reel existe déjà")
    
    with open(urls_path, 'w') as f:
        f.write(content)

if __name__ == "__main__":
    print("🔄 CORRECTION DE L'ERREUR DASHBOARD")
    print("=" * 50)
    
    fix_dashboard_template()
    create_simple_stat_view()
    add_url_pattern()
    
    print("\n🎉 CORRECTION APPLIQUÉE !")
    print("📋 Redémarrez le serveur et testez :")
    print("   python manage.py runserver")
    print("   http://127.0.0.1:8000/assureur/dashboard/")