# find_dynamic_forms.py
import os
import re

def find_dynamic_forms():
    """Trouve les formulaires créés via JavaScript"""
    
    print("🔍 Recherche de formulaires dynamiques et AJAX...")
    print("=" * 60)
    
    js_patterns = [
        # Création de formulaires en JS
        r'document\.createElement\s*\(\s*[\'"]form[\'"]\s*\)',
        r'\.innerHTML\s*.*<form',
        r'\.insertAdjacentHTML\s*.*<form',
        # Événements AJAX
        r'\.addEventListener\s*\(\s*[\'"]submit[\'"]',
        r'\$\([\'"]form[\'"]\)\.submit',
        r'\.submit\s*\(\s*function',
        # Fetch et AJAX
        r'fetch\s*\(',
        r'\$\.ajax\s*\(',
        r'\$\.post\s*\(',
        r'XMLHttpRequest'
    ]
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(('.html', '.js', '.py')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    issues = []
                    for pattern in js_patterns:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            line_num = content[:match.start()].count('\n') + 1
                            issues.append(f"Ligne {line_num}: {match.group()[:80]}...")
                    
                    if issues:
                        print(f"\n📄 {file_path}")
                        for issue in issues[:3]:  # Montre 3 premiers problèmes
                            print(f"   ⚠️  {issue}")
                            
                except Exception as e:
                    print(f"❌ Erreur lecture {file_path}: {e}")

if __name__ == "__main__":
    find_dynamic_forms()