
#!/usr/bin/env python
import os
import sys
import re

views_path = os.path.join(os.getcwd(), 'assureur', 'views.py')

if not os.path.exists(views_path):
    print(f"❌ Fichier non trouvé: {views_path}")
    exit(1)

print(f"🔧 Correction de: {views_path}")

# Lire le contenu
with open(views_path, 'r') as f:
    content = f.read()

# Créer une sauvegarde
backup_path = views_path + '.backup'
with open(backup_path, 'w') as f:
    f.write(content)
print(f"✅ Backup créé: {backup_path}")

# 1. Vérifier et corriger les imports
if 'from .decorators import assureur_required' not in content:
    print("⚠️  Import assureur_required manquant")
    
    # Ajouter l'import après les autres imports
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        new_lines.append(line)
        if 'from django.contrib.auth.decorators import' in line:
            # Ajouter notre import après
            new_lines.append('from .decorators import assureur_required')
    
    content = '\n'.join(new_lines)

# 2. Chercher et remplacer @staff_member_required
if '@staff_member_required' in content:
    print("🔧 Remplacement de @staff_member_required par @assureur_required")
    content = content.replace('@staff_member_required', '@assureur_required')

# 3. Chercher et remplacer user_passes_test(lambda u: u.is_staff)
if 'user_passes_test' in content:
    print("🔧 Recherche de user_passes_test problématique...")
    
    # Pattern pour user_passes_test avec vérification staff
    pattern = r'user_passes_test\(.*lambda u:.*is_staff.*\)'
    matches = re.findall(pattern, content)
    
    for match in matches:
        print(f"   Trouvé: {match}")
        # Remplacer par assureur_required
        content = content.replace(match, 'assureur_required')

# 4. S'assurer que la vue dashboard utilise @assureur_required
lines = content.split('\n')
new_lines = []
in_dashboard_function = False
dashboard_has_decorator = False

for i, line in enumerate(lines):
    # Vérifier si c'est la fonction dashboard
    if 'def dashboard' in line and '(' in line and '):' in line:
        in_dashboard_function = True
        
        # Vérifier la ligne précédente pour un décorateur
        if i > 0 and ('@assureur_required' in lines[i-1] or '@login_required' in lines[i-1]):
            dashboard_has_decorator = True
        else:
            # Ajouter le décorateur manquant
            indent = len(line) - len(line.lstrip())
            new_lines.append(' ' * indent + '@assureur_required')
            print(f"✅ Décorateur @assureur_required ajouté à la fonction dashboard")
    
    new_lines.append(line)

if not dashboard_has_decorator and in_dashboard_function:
    content = '\n'.join(new_lines)

# 5. Écrire le fichier corrigé
with open(views_path, 'w') as f:
    f.write(content)

print(f"✅ Vue assureur corrigée")
print("\n📋 Résumé des corrections:")
print("   1. Backup créé")
print("   2. Import assureur_required vérifié")
print("   3. @staff_member_required remplacé")
print("   4. user_passes_test avec is_staff corrigé")
print("   5. Décorateur @assureur_required ajouté si manquant")

print("\n🔍 Pour vérifier, affichez le début du fichier corrigé:")
print("-" * 40)
with open(views_path, 'r') as f:
    lines = f.readlines()[:30]
    for i, line in enumerate(lines):
        print(f"{i+1:3}: {line}", end='')


