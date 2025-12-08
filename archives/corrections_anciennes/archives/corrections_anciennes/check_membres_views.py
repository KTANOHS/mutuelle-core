# check_membres_views.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def check_membres_views():
    """Vérifier la vue des ordonnances membres"""
    print("🔍 VÉRIFICATION VUE ORDONNANCES MEMBRES...")
    
    try:
        with open('membres/views.py', 'r') as f:
            content = f.read()
        
        # Vérifier la vue mes_ordonnances
        if 'def mes_ordonnances' in content:
            print("✅ Vue mes_ordonnances trouvée")
            
            # Extraire la fonction
            start = content.find('def mes_ordonnances')
            end = content.find('def ', start + 1)
            if end == -1:
                end = len(content)
            function_content = content[start:end]
            
            # Vérifier le contexte
            if 'context' in function_content or 'ordonnances' in function_content:
                print("✅ Contexte détecté dans la vue")
            else:
                print("❌ Aucun contexte détecté")
                
            # Afficher un extrait
            print("📋 Extrait de la vue:")
            print(function_content[:300] + "..." if len(function_content) > 300 else function_content)
        else:
            print("❌ Vue mes_ordonnances non trouvée")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    check_membres_views()