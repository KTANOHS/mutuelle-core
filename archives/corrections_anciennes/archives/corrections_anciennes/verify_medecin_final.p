#!/usr/bin/env python3
"""
Vérification finale après corrections
"""

import os
import django
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def final_verification():
    """Vérification finale que tout fonctionne"""
    print("🔍 VÉRIFICATION FINALE MEDECIN")
    print("=" * 50)
    
    # 1. Vérifier les templates
    templates_dir = BASE_DIR / 'templates' / 'medecin'
    if templates_dir.exists():
        html_files = list(templates_dir.glob('*.html'))
        print(f"✅ {len(html_files)} templates dans medecin/")
        
        # Vérifier base_medecin.html
        base_template = templates_dir / 'base_medecin.html'
        if base_template.exists():
            with open(base_template, 'r') as f:
                content = f.read()
                if '{% block content %}' in content:
                    print("✅ base_medecin.html valide")
                else:
                    print("❌ base_medecin.html invalide")
        else:
            print("❌ base_medecin.html manquant")
    else:
        print("❌ Dossier templates/medecin manquant")
    
    # 2. Vérifier les vues
    views_file = BASE_DIR / 'medecin' / 'views.py'
    if views_file.exists():
        with open(views_file, 'r') as f:
            content = f.read()
        
        required_views = ['dashboard', 'mes_ordonnances']
        missing_views = [v for v in required_views if f'def {v}(' not in content]
        
        if not missing_views:
            print("✅ Toutes les vues importantes existent")
        else:
            print(f"❌ Vues manquantes: {', '.join(missing_views)}")
    else:
        print("❌ medecin/views.py manquant")
    
    # 3. Vérifier les URLs
    try:
        from django.urls import reverse
        
        urls_to_check = [
            'medecin:dashboard',
            'medecin:mes_ordonnances', 
            'medecin:creer_ordonnance',
            'medecin:liste_bons'
        ]
        
        print("✅ URLs configurées:")
        for url_name in urls_to_check:
            try:
                url = reverse(url_name)
                print(f"   📍 {url_name} → {url}")
            except:
                print(f"   ❌ {url_name} non configurée")
                
    except Exception as e:
        print(f"❌ Erreur vérification URLs: {e}")
    
    # 4. Test rapide
    print(f"\n🧪 TEST RAPIDE:")
    from django.test import Client
    from medecin.models import Medecin
    
    client = Client()
    
    try:
        medecin = Medecin.objects.first()
        if medecin:
            client.force_login(medecin.user)
            
            try:
                url = reverse('medecin:dashboard')
                response = client.get(url)
                if response.status_code == 200:
                    print("✅ Dashboard: Accessible (200 OK)")
                else:
                    print(f"❌ Dashboard: Erreur {response.status_code}")
            except Exception as e:
                print(f"❌ Dashboard: {e}")
        else:
            print("❌ Aucun médecin trouvé pour le test")
            
    except Exception as e:
        print(f"❌ Erreur test: {e}")
    
    print(f"\n🎯 RÉSULTAT FINAL:")
    print("Si tout est ✅, l'application medecin est fonctionnelle!")
    print("Sinon, exécutez à nouveau le correcteur ultime.")

if __name__ == "__main__":
    final_verification()