import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def corriger_recherche_ajax():
    """Corriger la recherche AJAX qui utilise un champ 'matricule' inexistant"""
    print("🔧 CORRECTION RECHERCHE AJAX")
    print("============================")
    
    # Chemin vers le fichier de vues des agents
    vue_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'agents', 'views.py')
    
    if os.path.exists(vue_path):
        print(f"📁 Fichier de vues trouvé: {vue_path}")
        
        with open(vue_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier si 'matricule' est utilisé dans la recherche
        if 'matricule' in content:
            print("⚠️  Champ 'matricule' détecté dans la recherche")
            
            # Remplacer matricule par numero_unique (le champ correct)
            new_content = content.replace("matricule", "numero_unique")
            
            with open(vue_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Recherche corrigée: 'matricule' → 'numero_unique'")
        else:
            print("✅ Aucun champ 'matricule' problématique trouvé")
            
    else:
        print(f"❌ Fichier de vues non trouvé: {vue_path}")
        return False
    
    return True

if __name__ == "__main__":
    success = corriger_recherche_ajax()
    
    if success:
        print("\n🎉 RECHERCHE AJAX CORRIGÉE!")
        print("🔁 Redémarrez le serveur pour appliquer les changements")
    else:
        print("\n⚠️  CORRECTION ÉCHOUÉE")