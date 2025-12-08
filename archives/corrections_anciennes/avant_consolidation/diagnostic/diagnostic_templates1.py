import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    def diagnostic_templates():
        print("🔍 DIAGNOSTIC DES TEMPLATES MANQUANTS")
        print("=" * 50)
        
        # Vérifier la structure des templates medecin
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates', 'medecin')
        
        print("1. 📁 STRUCTURE DES TEMPLATES MEDECIN:")
        if os.path.exists(templates_dir):
            for root, dirs, files in os.walk(templates_dir):
                level = root.replace(templates_dir, '').count(os.sep)
                indent = ' ' * 2 * level
                print(f'{indent}📂 {os.path.basename(root)}/')
                subindent = ' ' * 2 * (level + 1)
                for file in files:
                    if file.endswith('.html'):
                        print(f'{subindent}📄 {file}')
        else:
            print("   ❌ Dossier templates/medecin non trouvé")
        
        # Vérifier le template manquant spécifiquement
        template_manquant = 'medecin/suivi_chronique/tableau_bord.html'
        print(f"\n2. 🔎 RECHERCHE DU TEMPLATE: {template_manquant}")
        
        from django.template.loader import get_template
        try:
            template = get_template(template_manquant)
            print("   ✅ Template trouvé!")
        except:
            print("   ❌ Template non trouvé")
            
        # Lister tous les templates medecin disponibles
        print("\n3. 📋 TEMPLATES MEDECIN DISPONIBLES:")
        templates_base = os.path.join(templates_dir)
        if os.path.exists(templates_base):
            for file in os.listdir(templates_base):
                if file.endswith('.html'):
                    print(f"   📄 {file}")
        
        # Vérifier le dossier suivi_chronique
        suivi_dir = os.path.join(templates_dir, 'suivi_chronique')
        print(f"\n4. 📁 DOSSIER SUIVI CHRONIQUE:")
        if os.path.exists(suivi_dir):
            print("   ✅ Dossier existe")
            for file in os.listdir(suivi_dir):
                print(f"   📄 {file}")
        else:
            print("   ❌ Dossier suivi_chronique n'existe pas")
    
    diagnostic_templates()
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()