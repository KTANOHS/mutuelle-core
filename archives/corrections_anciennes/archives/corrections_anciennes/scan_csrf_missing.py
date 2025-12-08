# scan_csrf_missing.py
import os
import re
from pathlib import Path

def scan_form_missing_csrf(file_path):
    """Scan un fichier template pour trouver les formulaires POST sans CSRF"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except:
            print(f"❌ Impossible de lire le fichier: {file_path}")
            return []
    
    issues = []
    
    # Pattern pour trouver tous les formulaires
    form_pattern = r'<form[^>]*>'
    forms = re.finditer(form_pattern, content, re.IGNORECASE)
    
    for form_match in forms:
        form_tag = form_match.group(0)
        form_start = form_match.start()
        
        # Trouver la fin du formulaire
        form_end_pos = content.find('</form>', form_start)
        if form_end_pos == -1:
            continue
            
        form_content = content[form_start:form_end_pos]
        
        # Vérifier si c'est un formulaire POST
        is_post_form = False
        method_match = re.search(r'method\s*=\s*["\'](.*?)["\']', form_tag, re.IGNORECASE)
        
        if method_match:
            method = method_match.group(1).lower()
            if method == 'post':
                is_post_form = True
        else:
            # Si pas de method spécifiée, c'est GET par défaut, mais vérifions s'il y a des inputs de soumission
            if ('type="submit"' in form_content.lower() or 
                '<button' in form_content.lower() or
                'input type="submit"' in form_content.lower()):
                is_post_form = True
        
        if is_post_form:
            # Vérifier si le token CSRF est présent
            if not ('{% csrf_token %}' in form_content or 'csrf_token' in form_content):
                issues.append({
                    'form_tag': form_tag,
                    'position': form_start,
                    'line_number': content[:form_start].count('\n') + 1
                })
    
    return issues

def generate_report():
    """Génère un rapport complet des templates avec CSRF manquant"""
    
    template_directories = [
        'assureur',
        'core', 
        'emails',
        'errors',
        'includes',
        'inscription',
        'medecin',
        'membres',
        'paiements',
        'pharmacien',
        'registration',
        'soins'
    ]
    
    root_files = ['base.html', 'dashboard.html', 'home.html']
    
    report = {
        'critical': [],    # Fichiers avec formulaires POST sans CSRF
        'warning': [],     # Fichiers avec formulaires sans method (potentiellement POST)
        'clean': []        # Fichiers sans problème
    }
    
    print("🔍 Scan des templates pour CSRF manquants...")
    print("=" * 80)
    
    # Scanner les dossiers
    for directory in template_directories:
        if not os.path.exists(directory):
            print(f"⚠️  Dossier introuvable: {directory}")
            continue
            
        print(f"\n📁 Dossier: {directory}")
        print("-" * 40)
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    issues = scan_form_missing_csrf(file_path)
                    
                    if issues:
                        report['critical'].append({
                            'file': file_path,
                            'issues': issues
                        })
                        print(f"❌ {file_path}")
                        for issue in issues[:3]:  # Montre max 3 problèmes par fichier
                            print(f"   📋 Ligne {issue['line_number']}: {issue['form_tag'][:80]}...")
                    else:
                        report['clean'].append(file_path)
                        print(f"✅ {file_path}")
    
    # Scanner les fichiers racine
    print(f"\n📄 Fichiers racine:")
    print("-" * 40)
    
    for file in root_files:
        if os.path.exists(file):
            issues = scan_form_missing_csrf(file)
            
            if issues:
                report['critical'].append({
                    'file': file,
                    'issues': issues
                })
                print(f"❌ {file}")
                for issue in issues[:3]:
                    print(f"   📋 Ligne {issue['line_number']}: {issue['form_tag'][:80]}...")
            else:
                report['clean'].append(file)
                print(f"✅ {file}")
        else:
            print(f"⚠️  Fichier introuvable: {file}")
    
    return report

def save_detailed_report(report, output_file='csrf_scan_report.txt'):
    """Sauvegarde un rapport détaillé"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("RAPPORT DE SCAN CSRF - Templates avec tokens manquants\n")
        f.write("=" * 60 + "\n\n")
        
        if report['critical']:
            f.write("🔴 FICHIERS CRITIQUES (CSRF manquant):\n")
            f.write("-" * 50 + "\n")
            
            for item in report['critical']:
                f.write(f"\n📄 {item['file']}:\n")
                for issue in item['issues']:
                    f.write(f"   📍 Ligne {issue['line_number']}: {issue['form_tag']}\n")
        
        f.write(f"\n\n📊 STATISTIQUES:\n")
        f.write("-" * 30 + "\n")
        f.write(f"🔴 Fichiers critiques: {len(report['critical'])}\n")
        f.write(f"✅ Fichiers propres: {len(report['clean'])}\n")
        f.write(f"📁 Total fichiers scannés: {len(report['critical']) + len(report['clean'])}\n")
    
    print(f"\n📊 Rapport détaillé sauvegardé dans: {output_file}")

def create_fix_script(report):
    """Crée un script de correction basé sur le rapport"""
    
    if not report['critical']:
        print("🎉 Aucune correction nécessaire !")
        return
    
    script_content = '''# auto_fix_csrf.py
import os
import re

def fix_csrf_in_file(file_path):
    """Corrige les CSRF manquants dans un fichier spécifique"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern pour les formulaires POST sans CSRF
    patterns = [
        (r'(<form\\\\s+[^>]*method\\\\s*=\\\\s*["\\\\']post["\\\\'][^>]*>)(?![\s\S]*?{%\\\\s*csrf_token\\\\s*%})', r'\\\\1\\\\n    {% csrf_token %}'),
        (r'(<form[^>]*>)(?![\s\S]*?{%\\\\s*csrf_token\\\\s*%})(?=[\s\S]*?<input[^>]*type=["\\\\']submit["\\\\'])', r'\\\\1\\\\n    {% csrf_token %}'),
    ]
    
    original_content = content
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE | re.DOTALL)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Fichiers à corriger
files_to_fix = [
'''
    
    for item in report['critical']:
        script_content += f"    '{item['file']}',\n"
    
    script_content += ''']

print("🔧 Correction automatique des tokens CSRF...")
fixed_count = 0

for file_path in files_to_fix:
    if os.path.exists(file_path):
        try:
            if fix_csrf_in_file(file_path):
                print(f"✅ Corrigé: {file_path}")
                fixed_count += 1
            else:
                print(f"ℹ️  Déjà corrigé: {file_path}")
        except Exception as e:
            print(f"❌ Erreur avec {file_path}: {e}")
    else:
        print(f"⚠️  Fichier introuvable: {file_path}")

print(f"\\\\n📊 {fixed_count} fichiers corrigés sur {len(files_to_fix)}")
'''
    
    with open('auto_fix_csrf.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("🔧 Script de correction généré: auto_fix_csrf.py")

def main():
    """Fonction principale"""
    
    print("CSRF SCANNER - Identification des tokens manquants")
    print("=" * 60)
    
    # Générer le rapport
    report = generate_report()
    
    # Afficher le résumé
    print(f"\n{'='*60}")
    print("📊 RAPPORT FINAL")
    print(f"{'='*60}")
    
    if report['critical']:
        print(f"🔴 {len(report['critical'])} FICHIERS AVEC CSRF MANQUANT:")
        for item in report['critical']:
            print(f"   📄 {item['file']} ({len(item['issues'])} formulaire(s))")
    else:
        print("🎉 Aucun problème détecté ! Tous les formulaires ont le token CSRF.")
    
    print(f"\n✅ {len(report['clean'])} fichiers sans problème")
    
    # Sauvegarder le rapport détaillé
    save_detailed_report(report)
    
    # Générer le script de correction si nécessaire
    if report['critical']:
        create_fix_script(report)
        print(f"\n💡 NEXT STEPS:")
        print("   1. Vérifiez le rapport détaillé: csrf_scan_report.txt")
        print("   2. Exécutez le script de correction: python auto_fix_csrf.py")
        print("   3. Testez votre application")
    else:
        print(f"\n🎉 Tous vos templates sont conformes CSRF !")

if __name__ == "__main__":
    main()