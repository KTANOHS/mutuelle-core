#!/usr/bin/env python3
"""
Vérification ultra-rapide après toutes les corrections
"""

import os
import django
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def ultra_quick_check():
    """Vérification ultra-rapide"""
    print("⚡ VÉRIFICATION ULTRA-RAPIDE MEDECIN")
    print("=" * 50)
    
    # Vérification des templates
    templates_dir = BASE_DIR / 'templates' / 'medecin'
    if templates_dir.exists():
        html_files = list(templates_dir.glob('*.html'))
        print(f"📄 Templates: {len(html_files)} OK")
    else:
        print("❌ Templates: dossier manquant")
        return
    
    # Test rapide des URLs principales
    from django.test import Client
    from django.urls import reverse
    from medecin.models import Medecin
    
    client = Client()
    
    try:
        medecin = Medecin.objects.first()
        if not medecin:
            print("❌ Aucun médecin")
            return
        
        client.force_login(medecin.user)
        
        print("🌐 Test URLs:")
        urls = [
            ('medecin:dashboard', 'Dashboard'),
            ('medecin:mes_ordonnances', 'Mes Ordonnances'),
            ('medecin:profil_medecin', 'Profil'),
        ]
        
        for url_name, desc in urls:
            try:
                response = client.get(reverse(url_name))
                status = "✅" if response.status_code == 200 else "⚠️ "
                print(f"   {status} {desc}: {response.status_code}")
            except:
                print(f"   ❌ {desc}: erreur")
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print("\n🎯 STATUT: Si tout est ✅, l'application medecin est OPÉRATIONNELLE!")

if __name__ == "__main__":
    ultra_quick_check()