import os
import sys

def generate_tree(startpath, exclude_dirs=None, exclude_files=None):
    if exclude_dirs is None:
        exclude_dirs = ['__pycache__', '.git', 'migrations', 'staticfiles', 'media', 'venv', '.vscode', '.idea']
    if exclude_files is None:
        exclude_files = ['*.pyc', '*.pyo', '*.pyd', '.DS_Store']
    
    print(f"📁 {os.path.basename(startpath)}/")
    
    for root, dirs, files in os.walk(startpath):
        # Exclure les dossiers
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}📁 {os.path.basename(root)}/" if level > 0 else '', end='')
        
        subindent = ' ' * 2 * (level + 1)
        
        # Afficher les fichiers
        for file in files:
            if not any(file.endswith(ext.replace('*', '')) for ext in exclude_files):
                file_ext = os.path.splitext(file)[1]
                icon = get_file_icon(file_ext)
                print(f"{subindent}{icon} {file}")
    
    print(f"\n📊 Résumé:")
    print(f"📍 Chemin: {startpath}")
    print(f"🚫 Exclusions: {', '.join(exclude_dirs)}")

def get_file_icon(extension):
    icons = {
        '.py': '🐍',
        '.html': '🌐',
        '.css': '🎨',
        '.js': '📜',
        '.json': '📋',
        '.md': '📝',
        '.txt': '📄',
        '.sql': '🗃️',
        '.env': '🔐',
        '': '📄'
    }
    return icons.get(extension, '📄')

if __name__ == "__main__":
    project_path = os.getcwd()
    generate_tree(project_path)