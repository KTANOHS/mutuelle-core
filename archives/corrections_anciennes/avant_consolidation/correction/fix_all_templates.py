import os
import re

def fix_template(filepath):
    """Corrige les références d'URL dans un template"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Corriger les différentes formes de références
    corrections = [
        # communication:message_create
        (r'\{%\s*url\s+[\'"]communication:message_create[\'"]\s*%\}', 
         '{% url "communication:message_create" %}'),
        
        # 'message_create' sans namespace
        (r'\{%\s*url\s+[\'"]message_create[\'"]\s*%\}', 
         '{% url "communication:message_create" %}'),
    ]
    
    modified = False
    for pattern, replacement in corrections:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            modified = True
    
    if modified:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✅ {filepath} corrigé")
        return True
    return False

# Templates à corriger
templates = [
    'templates/home.html',
    'templates/base.html',
    'templates/accounts/login.html',
    'templates/includes/sidebar_communication.html',
    'templates/includes/communication_widget.html',
    'templates/communication/search_results.html',
    'templates/communication/message_list.html',
    'templates/communication/partials/_conversations_list.html',
]

print("🔧 Correction des templates...")
for template in templates:
    if os.path.exists(template):
        fix_template(template)
    else:
        print(f"⚠️  {template} non trouvé")

print("\n🎯 Tous les templates ont été corrigés !")
print("🔄 Redémarrez le serveur pour voir les changements.")
