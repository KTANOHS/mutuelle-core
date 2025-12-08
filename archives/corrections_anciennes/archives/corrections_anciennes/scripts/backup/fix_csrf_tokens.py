# fix_csrf_tokens.py
import os
import re

def add_csrf_to_login_templates():
    """Ajoute les tokens CSRF manquants dans les templates de login"""
    
    print("🔐 CORRECTION DES TOKENS CSRF MANQUANTS")
    print("=" * 45)
    
    # Templates à corriger
    templates_to_fix = {
        'templates/registration/login.html': {
            'pattern': r'<form method="post"[^>]*>',
            'replacement': r'\g<0>\n            {% csrf_token %}'
        },
        'templates/registration/login_ajax.html': {
            'pattern': r'<form method="post"[^>]*>',
            'replacement': r'\g<0>\n        {% csrf_token %}'
        }
    }
    
    fixed_count = 0
    for template_path, fix_info in templates_to_fix.items():
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier si le CSRF token est déjà présent
            if '{% csrf_token %}' not in content:
                # Ajouter le CSRF token après la balise form
                new_content = re.sub(
                    fix_info['pattern'], 
                    fix_info['replacement'], 
                    content
                )
                
                if new_content != content:
                    with open(template_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"✅ CSRF token ajouté à: {template_path}")
                    fixed_count += 1
                else:
                    print(f"⚠️  Aucun formulaire POST trouvé dans: {template_path}")
            else:
                print(f"✅ CSRF token déjà présent dans: {template_path}")
        else:
            print(f"❌ Fichier non trouvé: {template_path}")
    
    return fixed_count

def verify_csrf_tokens():
    """Vérifie que tous les formulaires POST ont des tokens CSRF"""
    
    print("\n🔍 VÉRIFICATION DES TOKENS CSRF")
    print("=" * 35)
    
    templates_with_forms = []
    
    for root, dirs, files in os.walk('templates'):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Chercher les formulaires POST
                post_forms = re.findall(r'<form method="post"', content, re.IGNORECASE)
                
                if post_forms:
                    templates_with_forms.append((filepath, len(post_forms)))
                    
                    # Vérifier la présence du CSRF token
                    if '{% csrf_token %}' not in content:
                        print(f"❌ {filepath} → {len(post_forms)} formulaire(s) POST SANS CSRF token")
                    else:
                        print(f"✅ {filepath} → {len(post_forms)} formulaire(s) POST AVEC CSRF token")
    
    return templates_with_forms

def fix_all_post_forms():
    """Corrige tous les formulaires POST sans CSRF token"""
    
    print("\n🛠️  CORRECTION DE TOUS LES FORMULAIRES POST")
    print("=" * 50)
    
    fixed_count = 0
    
    for root, dirs, files in os.walk('templates'):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Vérifier s'il y a des formulaires POST sans CSRF
                post_forms = re.findall(r'<form method="post"', content, re.IGNORECASE)
                
                if post_forms and '{% csrf_token %}' not in content:
                    # Ajouter CSRF token après chaque balise form POST
                    new_content = re.sub(
                        r'(<form method="post"[^>]*>)',
                        r'\1\n    {% csrf_token %}',
                        content
                    )
                    
                    if new_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"✅ CSRF tokens ajoutés à: {filepath}")
                        fixed_count += 1
    
    print(f"📊 {fixed_count} templates corrigés")
    return fixed_count

if __name__ == "__main__":
    # 1. Corriger spécifiquement les templates de login
    fixed_login = add_csrf_to_login_templates()
    
    # 2. Vérifier tous les templates
    forms_list = verify_csrf_tokens()
    
    # 3. Corriger tous les formulaires POST manquants
    fixed_all = fix_all_post_forms()
    
    print(f"\n🎉 RÉSUMÉ DE LA CORRECTION CSRF:")
    print(f"   - Templates login corrigés: {fixed_login}")
    print(f"   - Templates avec formulaires POST: {len(forms_list)}")
    print(f"   - Templates généraux corrigés: {fixed_all}")
    
    if fixed_login + fixed_all > 0:
        print("\n🔄 Redémarrez le serveur pour appliquer les corrections:")
        print("   python manage.py runserver")