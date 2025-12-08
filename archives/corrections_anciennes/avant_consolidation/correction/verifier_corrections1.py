# verifier_corrections.py
import os

def verifier_corrections():
    """Vérifier que toutes les corrections ont été appliquées"""
    
    fichiers = ['communication/views.py', 'agents/views.py']
    problemes_trouves = False
    
    for fichier in fichiers:
        if os.path.exists(fichier):
            with open(fichier, 'r') as f:
                contenu = f.read()
            
            if "redirect('communication:liste_messages')" in contenu:
                print(f"❌ Problème trouvé dans {fichier}")
                problemes_trouves = True
            else:
                print(f"✅ {fichier} est correct")
    
    if not problemes_trouves:
        print("\n🎉 Toutes les corrections ont été appliquées avec succès !")
        print("L'erreur 'liste_messages not found' devrait maintenant être résolue.")
    else:
        print("\n⚠️ Il reste des problèmes à corriger manuellement.")

if __name__ == "__main__":
    verifier_corrections()