import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def corriger_route_api():
    """Corriger la route API pour qu'elle corresponde à ce que l'interface attend"""
    print("🔧 CORRECTION ROUTE API")
    print("======================")
    
    # 1. Vérifier le urls.py principal
    urls_principal_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mutuelle_core', 'urls.py')
    
    if os.path.exists(urls_principal_path):
        print("📁 Modification du urls.py principal...")
        
        with open(urls_principal_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ajouter la route globale si elle n'existe pas
        if "path('api/agents/'" not in content:
            # Trouver où insérer (après les imports)
            lines = content.split('\n')
            new_lines = []
            
            for i, line in enumerate(lines):
                new_lines.append(line)
                # Après les imports, ajouter l'include des agents API
                if 'from django.urls import path, include' in line and i+1 < len(lines) and 'urlpatterns' not in lines[i+1]:
                    new_lines.append('from agents.views import details_bon_soin_api')
            
            # Reconstruire le contenu
            content = '\n'.join(new_lines)
            
            # Ajouter la route dans urlpatterns
            if 'urlpatterns = [' in content:
                nouvelle_route = "    path('api/agents/bons/<int:bon_id>/details/', details_bon_soin_api, name='api_details_bon_global'),"
                
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'urlpatterns = [' in line:
                        # Insérer après l'ouverture de urlpatterns
                        j = i + 1
                        while j < len(lines) and (lines[j].strip().startswith('#') or lines[j].strip() == ''):
                            j += 1
                        lines.insert(j, nouvelle_route)
                        break
                
                content = '\n'.join(lines)
            
            with open(urls_principal_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Route globale API ajoutée")
        else:
            print("✅ Route globale API existe déjà")
    
    return True

if __name__ == "__main__":
    success = corriger_route_api()
    
    if success:
        print("\n🎉 ROUTE API CORRIGÉE!")
        print("🔁 Redémarrez le serveur pour appliquer les changements")
    else:
        print("\n⚠️  CORRECTION ÉCHOUÉE")