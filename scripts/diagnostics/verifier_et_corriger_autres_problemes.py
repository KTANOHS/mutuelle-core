# verifier_et_corriger_autres_problemes.py
import re

def corriger_ordonnance_medecin():
    """Corrige les références à medecin dans Ordonnance"""
    
    fichiers = ['medecin/models.py', 'medecin/admin.py']
    
    print("🔧 CORRECTION RÉFÉRENCES ORDONNANCE")
    print("=" * 40)
    
    for fichier in fichiers:
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Remplacer Ordonnance.objects.filter(medecin=...) par le bon champ
            contenu_corrige = re.sub(
                r'Ordonnance\.objects\.filter\(medecin=([^)]+)\)',
                r'Ordonnance.objects.filter(bon_de_soin__medecin=\1)',
                contenu
            )
            
            if contenu != contenu_corrige:
                with open(fichier, 'w', encoding='utf-8') as f:
                    f.write(contenu_corrige)
                print(f"✅ {fichier} corrigé")
            else:
                print(f"ℹ️  {fichier}: Aucune correction nécessaire")
                
        except FileNotFoundError:
            print(f"❌ Fichier non trouvé: {fichier}")

def verifier_structure_soin():
    """Affiche la structure réelle du modèle Soin"""
    print("\n🔍 STRUCTURE DU MODÈLE SOIN")
    print("=" * 40)
    print("Champs disponibles dans Soin:")
    print("  - patient (ForeignKey)")
    print("  - medecin (ForeignKey)") 
    print("  - type_soin (ForeignKey)")
    print("  - date_soin (DateField)")
    print("  - statut (CharField)")
    print("  - et autres champs...")
    print("\n💡 Utilisez 'medecin' au lieu de 'bon_de_soin__medecin'")

if __name__ == "__main__":
    corriger_ordonnance_medecin()
    verifier_structure_soin()