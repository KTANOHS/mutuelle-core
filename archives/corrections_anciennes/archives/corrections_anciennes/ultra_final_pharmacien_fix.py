# ultra_final_pharmacien_fix.py
import re

def ultra_final_pharmacien_fix():
    """Correction ULTIME des tests pharmacien"""
    print("🔧 CORRECTION ULTIME PHARMACIEN...")
    
    with open('pharmacien/tests.py', 'r') as f:
        content = f.read()
    
    # CORRECTIONS MANUELLES PRÉCISES
    corrections = [
        # Remplacer medicament= par medicament_delivre=
        (r"medicament='Paracétamol'", "medicament_delivre='Paracétamol'"),
        (r"medicament='Aspirine'", "medicament_delivre='Aspirine'"),
        
        # Remplacer posologie= par posologie_appliquee=
        (r"posologie='1 comprimé 3 fois par jour'", "posologie_appliquee='1 comprimé 3 fois par jour'"),
        
        # Remplacer duree= par duree_traitement=
        (r"duree=7", "duree_traitement=7"),
        
        # Stock corrections
        (r"medicament='Paracétamol'", "nom_medicament='Paracétamol'"),
        (r"quantite_en_stock=100", "quantite_stock=100"),
    ]
    
    for old, new in corrections:
        if old in content:
            content = content.replace(old, new)
            print(f"✅ Remplacé: {old} → {new}")
        else:
            print(f"⚠️  Non trouvé: {old}")
    
    with open('pharmacien/tests.py', 'w') as f:
        f.write(content)
    
    print("✅ Correction ultime appliquée!")

ultra_final_pharmacien_fix()