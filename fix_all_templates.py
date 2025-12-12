#!/usr/bin/env python
# fix_all_templates.py
import os
import re
import shutil
from pathlib import Path

class TemplateFixer:
    def __init__(self):
        self.templates_dir = self.find_templates_dir()
        self.static_dir = self.find_static_dir()
        
    def find_templates_dir(self):
        for path in ['templates', 'mutuelle_core/templates']:
            if os.path.exists(path):
                return path
        raise Exception("Aucun dossier templates trouvé")
    
    def find_static_dir(self):
        for path in ['static', 'staticfiles', 'mutuelle_core/static']:
            if os.path.exists(path):
                return path
        return 'static'
    
    def fix_missing_files(self):
        """Crée les fichiers manquants ou ajuste les références"""
        print("🔧 Correction des fichiers manquants...")
        
        # Mapping des fichiers manquants et leurs alternatives
        missing_files = {
            'videos/presentation.webm': 'static/videos/presentation.webm',
            'videos/presentation.mp4': 'static/videos/presentation.mp4',
            'img/patient-avatar.png': 'static/images/avatar-placeholder.png',
        }
        
        # Créer les dossiers nécessaires
        for dir_path in ['static/videos', 'static/images', 'static/img']:
            os.makedirs(dir_path, exist_ok=True)
        
        # Créer des fichiers placeholder si nécessaires
        placeholder_image = os.path.join(self.static_dir, 'images', 'avatar-placeholder.png')
        if not os.path.exists(placeholder_image):
            # Créer un simple fichier texte comme placeholder
            with open(placeholder_image.replace('.png', '.txt'), 'w') as f:
                f.write("Placeholder pour patient-avatar.png")
            print(f"📝 Créé placeholder: {placeholder_image}")
        
        # Chercher des alternatives pour les vidéos
        for missing_file in ['presentation.webm', 'presentation.mp4']:
            possible_locations = [
                os.path.join(self.static_dir, 'videos', missing_file),
                os.path.join('static', 'videos', missing_file),
                os.path.join('mutuelle_core', 'static', 'videos', missing_file),
            ]
            
            found = False
            for location in possible_locations:
                if os.path.exists(location):
                    found = True
                    print(f"✅ Fichier trouvé: {location}")
                    break
            
            if not found:
                print(f"⚠️  Fichier non trouvé: {missing_file}")
                print(f"   Vous pouvez: ")
                print(f"   1. Ajouter le fichier dans static/videos/")
                print(f"   2. Modifier le template pour retirer la référence")
                print(f"   3. Utiliser une URL externe")
    
    def fix_template_syntax_errors(self):
        """Corrige les erreurs de syntaxe courantes"""
        print("\n🔧 Correction des erreurs de syntaxe...")
        
        # Patterns de correction
        fixes = [
            # 1. Fermetures de balises incorrectes
            (r'(\{\{[^}]*\}\}\s*)\{%', r'\1 {%'),
            (r'%\}(\s*)\}\}', r'%}\1}}'),
            
            # 2. Balises mal formatées
            (r'\{%\s*(endif|endfor|endblock|endwith|empty)([^%]*)\}\}', r'{% \1\2 %}'),
            (r'\{%\s*(if|for|block|with|extends|include|load)([^%]*)\}\}', r'{% \1\2 %}'),
            
            # 3. Variables mal placées
            (r'src="\{\{\s*([^}]+)\s*\}\}"', r'src="{{ \1 }}"'),
            (r'href="\{\{\s*([^}]+)\s*\}\}"', r'href="{{ \1 }}"'),
            
            # 4. Problèmes d'espacement
            (r'\{\{\s*([^}]+)\s*\}\}\s*\{\%', r'{{ \1 }} {%'),
            (r'\%\}\s*\{\{\s*([^}]+)\s*\}\}', r'%} {{ \1 }}'),
            
            # 5. Tags mal fermés (cas spécifiques)
            (r'(\{%[^%]*%\}\s*)\{\{', r'\1 {{'),
            (r'\}\}(\s*\{%[^%]*%\})', r'}} \1'),
        ]
        
        problematic_files = [
            'medecin/detail_ordonnance_public.html',
            'medecin/detail_bon.html',
            'medecin/liste_bons.html',
            'medecin/dashboard.html',
            'medecin/bons_attente.html',
            'medecin/detail_ordonnance.html',
            'agents/historique_bons.html',
            'agents/liste_membres.html',
            'assureur/liste_paiements.html',
            # ... ajoutez d'autres fichiers problématiques
        ]
        
        files_fixed = 0
        
        for root, dirs, files in os.walk(self.templates_dir):
            for file in files:
                if not file.endswith('.html'):
                    continue
                    
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, self.templates_dir)
                
                # Si on a une liste de fichiers problématiques, ne corriger que ceux-là
                if problematic_files and rel_path not in problematic_files:
                    continue
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original = content
                
                # Appliquer toutes les corrections
                for pattern, replacement in fixes:
                    content = re.sub(pattern, replacement, content)
                
                # Vérifier les corrections spécifiques par type de template
                if 'medecin' in rel_path:
                    # Corrections spécifiques aux templates médecins
                    content = re.sub(r'(\{%[^%]*%\}\s*)\{\{', r'\1 {{', content)
                
                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    files_fixed += 1
                    print(f"✅ Corrigé: {rel_path}")
        
        print(f"📊 {files_fixed} fichiers corrigés")
    
    def create_placeholder_videos(self):
        """Crée des vidéos placeholder si nécessaires"""
        print("\n🎥 Création de vidéos placeholder...")
        
        videos_dir = os.path.join(self.static_dir, 'videos')
        os.makedirs(videos_dir, exist_ok=True)
        
        # Créer un simple fichier HTML comme placeholder pour les vidéos
        placeholder_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Placeholder Video</title>
    <style>
        body { 
            margin: 0; 
            padding: 0; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-family: Arial, sans-serif;
        }
        .content {
            text-align: center;
            padding: 2rem;
        }
        h1 { font-size: 3rem; margin-bottom: 1rem; }
        p { font-size: 1.2rem; opacity: 0.9; }
    </style>
</head>
<body>
    <div class="content">
        <h1>🎬 MaSante Direct</h1>
        <p>Vidéo de présentation</p>
        <p><small>Placeholder - Ajoutez votre vidéo dans static/videos/</small></p>
    </div>
</body>
</html>
"""
        
        # Créer des fichiers placeholder
        for video_file in ['presentation.webm', 'presentation.mp4']:
            placeholder_path = os.path.join(videos_dir, video_file.replace('.mp4', '.html').replace('.webm', '.html'))
            
            with open(placeholder_path, 'w') as f:
                f.write(placeholder_html)
            
            print(f"📝 Créé placeholder: {placeholder_path}")
        
        # Mettre à jour les références dans home.html
        home_path = os.path.join(self.templates_dir, 'home.html')
        if os.path.exists(home_path):
            with open(home_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remplacer les références vidéos par un placeholder
            content = re.sub(
                r'<source src="{% static \'videos/presentation\.(webm|mp4)\' %}" type="video/\1">',
                '<!-- Video placeholder -->',
                content
            )
            
            with open(home_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Mises à jour des références vidéos dans home.html")
    
    def run_all_fixes(self):
        """Exécute toutes les corrections"""
        print("🔨 LANCEMENT DES CORRECTIONS 🔨")
        print("="*50)
        
        self.fix_missing_files()
        self.fix_template_syntax_errors()
        self.create_placeholder_videos()
        
        print("\n" + "="*50)
        print("🎉 CORRECTIONS TERMINÉES")
        print("="*50)
        print("\n📋 PROCHAINES ÉTAPES:")
        print("1. Testez les templates: python manage.py runserver")
        print("2. Vérifiez qu'il n'y a plus d'erreurs dans la console")
        print("3. Si nécessaire, ajoutez vos vraies vidéos dans static/videos/")
        print("4. Pour Render: git add . && git commit -m 'Fix templates' && git push")

if __name__ == "__main__":
    fixer = TemplateFixer()
    fixer.run_all_fixes()