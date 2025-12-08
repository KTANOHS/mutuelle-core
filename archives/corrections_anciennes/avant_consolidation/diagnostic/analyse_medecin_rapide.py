#!/usr/bin/env python3
import os, sys, re
from pathlib import Path

def quick_analyze():
    project = Path("/Users/koffitanohsoualiho/Documents/sup/projet 21.49.30")
    medecin = project / "medecin"
    
    print("⚡ ANALYSE RAPIDE MEDECIN")
    print("=" * 40)
    
    # Structure
    print("📁 Structure:")
    for f in medecin.glob("*.py"):
        print(f"  📄 {f.name}")
    
    # URLs critiques
    urls_file = medecin / "urls.py"
    if urls_file.exists():
        content = urls_file.read_text()
        print(f"\n🔗 URLs: {len(re.findall(r'path\(', content))}")
        if "views_suivi_chronique" in content:
            print("🚨 URGENT: 'views_suivi_chronique' trouvé dans urls.py")
    
    # Vues principales
    views_file = medecin / "views.py"
    if views_file.exists():
        content = views_file.read_text()
        views = re.findall(r"def (\w+)\(", content)
        print(f"👁️  Vues: {len(views)}")
        for v in ['dashboard', 'liste_bons', 'mes_rendez_vous']:
            if any(v in view for view in views):
                print(f"  ✅ {v}")
            else:
                print(f"  ❌ {v}")
    
    # Test final
    try:
        sys.path.insert(0, str(project))
        from medecin import urls, views
        print("✅ Import réussi")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    quick_analyze()