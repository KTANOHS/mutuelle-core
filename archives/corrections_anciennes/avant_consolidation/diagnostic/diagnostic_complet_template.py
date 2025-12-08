import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

def diagnostic_complet_template():
    print("🔍 DIAGNOSTIC COMPLET DU TEMPLATE")
    print("=" * 50)
    
    # 1. Vérifier l'existence physique
    template_path = 'templates/medecin/suivi_chronique/tableau_bord.html'
    absolute_path = os.path.abspath(template_path)
    
    print(f"1. 📁 CHEMIN ABSOLU: {absolute_path}")
    print(f"   📍 Existe: {os.path.exists(absolute_path)}")
    
    if os.path.exists(absolute_path):
        print(f"   📏 Taille: {os.path.getsize(absolute_path)} octets")
        print(f"   🔐 Permissions: {oct(os.stat(absolute_path).st_mode)[-3:]}")
        
        # Lire le contenu
        with open(absolute_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"   📄 Lignes: {len(content.splitlines())}")
            print(f"   🔍 Début: {content[:100]}...")
    else:
        print("   ❌ FICHIER NON TROUVÉ - Création immédiate...")
        # Créer le fichier immédiatement
        os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
        with open(absolute_path, 'w', encoding='utf-8') as f:
            f.write('''<!DOCTYPE html>
<html>
<head>
    <title>Suivi Chronique</title>
</head>
<body>
    <h1>Suivi des Maladies Chroniques</h1>
    <p>Module en développement</p>
</body>
</html>''')
        print("   ✅ Fichier créé!")
    
    # 2. Vérifier la structure des templates
    print("\n2. 📂 STRUCTURE TEMPLATES MEDECIN:")
    templates_dir = 'templates/medecin'
    if os.path.exists(templates_dir):
        for root, dirs, files in os.walk(templates_dir):
            level = root.replace(templates_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}📁 {os.path.basename(root)}/')
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                if file.endswith('.html'):
                    print(f'{subindent}📄 {file}')
    else:
        print("   ❌ Dossier templates/medecin non trouvé")
    
    # 3. Vérifier via Django
    print("\n3. 🐍 VÉRIFICATION DJANGO:")
    try:
        django.setup()
        from django.template.loader import get_template
        
        try:
            template = get_template('medecin/suivi_chronique/tableau_bord.html')
            print("   ✅ Django peut charger le template")
            print(f"   📍 Chemin Django: {template.origin.name}")
        except Exception as e:
            print(f"   ❌ Erreur Django: {e}")
            
            # Essayer de trouver où Django cherche
            from django.template.loaders.filesystem import Loader
            loader = Loader()
            try:
                sources = loader.get_template_sources('medecin/suivi_chronique/tableau_bord.html')
                print("   🔍 Django cherche dans:")
                for source in sources:
                    print(f"      - {source}")
            except:
                pass
                
    except Exception as e:
        print(f"   ❌ Erreur setup Django: {e}")
    
    # 4. Vérifier les settings TEMPLATES
    print("\n4. ⚙️ CONFIGURATION TEMPLATES:")
    try:
        from django.conf import settings
        for template_config in settings.TEMPLATES:
            if 'DIRS' in template_config:
                print(f"   📁 DIRS: {template_config['DIRS']}")
            if 'APP_DIRS' in template_config:
                print(f"   📱 APP_DIRS: {template_config['APP_DIRS']}")
    except Exception as e:
        print(f"   ❌ Erreur configuration: {e}")

diagnostic_complet_template()