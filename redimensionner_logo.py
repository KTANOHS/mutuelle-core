# redimensionner_logo.py
from PIL import Image
import os

def redimensionner_logo():
    print("🖼️  REDIMENSIONNEMENT DU LOGO")
    print("============================")
    
    chemin_logo = "mutuelle_core/static/mutuelle_core/images/logo.jpg"
    
    if not os.path.exists(chemin_logo):
        print("❌ Logo non trouvé :", chemin_logo)
        return False
    
    try:
        # Ouvrir l'image
        with Image.open(chemin_logo) as img:
            print(f"📐 Taille originale: {img.size}")
            
            # Calculer les nouvelles dimensions (largeur max 120px)
            ratio = 120 / img.width
            nouvelle_largeur = 120
            nouvelle_hauteur = int(img.height * ratio)
            
            # Redimensionner
            img_redimensionnee = img.resize((nouvelle_largeur, nouvelle_hauteur), Image.Resampling.LANCZOS)
            
            # Sauvegarder (écraser l'original ou créer une copie)
            img_redimensionnee.save(chemin_logo, optimize=True, quality=85)
            
            print(f"✅ Nouvelle taille: {img_redimensionnee.size}")
            print("🎯 Logo redimensionné avec succès !")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    redimensionner_logo()