"""
FICHIER CONSOLIDÉ: fix
Catégorie: correction
Fusion de 32 fichiers
Date de consolidation: 2025-12-06 13:55:44
"""

import sys
import os
from pathlib import Path

# =============================================================================
# FICHIERS D'ORIGINE CONSOLIDÉS
# =============================================================================

# ============================================================
# ORIGINE 1: fix_assureur_views.py (2025-12-06)
# ============================================================


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
... (tronqué)

# ============================================================
# ORIGINE 2: fix_passwords.py (2025-12-06)
# ============================================================


#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User

print("🔑 RÉINITIALISATION DES MOTS DE PASSE")
print("=" * 40)

users = [
    ("DOUA", "DOUA"),
    ("DOUA1", "DOUA1"),
    ("ktanos", "ktanos"),
    ("ORNELLA", "ORNELLA"),
    ("Yacouba", "Yacouba"),
    ("GLORIA", "GLORIA"),
    ("ASIA", "ASIA"),
]

for username, password in users:
    try:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"✅ {username}: mot de passe défini sur '{password}'")
    except Exception as e:
        print(f"❌ {username}: erreur - {e}")

print("\n✅ Mots de passe mis à jour")
print("\n🔍 Vérification des utilisateurs:")
print("-" * 30)

for username, _ in users:
    try:
        user = User.objects.get(username=username)
        print(f"👤 {username}:")
        print(f"   is_staff: {user.is_staff}")
        print(f"   is_superuser: {user.is_superuser}")
        print(f"   Groupes: {[g.name for g in user.groups.all()]}")
    except:
        print(f"❌ {username}: non trouvé")


# ============================================================
# ORIGINE 3: fix_main_templates.sh (2025-12-04)
# ============================================================

#!/bin/bash

echo "🔧 Correction des templates principaux..."

# 1. liste_membres.html
if [ -f "./templates/assureur/liste_membres.html" ]; then
    echo "📝 Correction de liste_membres.html..."

    # Copie de sauvegarde
    cp ./templates/assureur/liste_membres.html ./templates/assureur/liste_membres.html.backup

    # Remplacement précis
    sed -i '' '
    # Ligne 20 (ou similaire): bouton Créer un bon
    s|<a href="{% url .creer_bon. membre.id %}"|<a href="{% url '\''assureur:creer_bon_pour_membre'\'' membre.id %}"|g

    # Ligne 123 (ou similaire): autre bouton
    s|<a href="{% url .creer_bon. membre.id %}"|<a href="{% url '\''assureur:creer_bon_pour_membre'\'' membre.id %}"|g

    # Tous les autres cas
    s|{% url .creer_bon. membre.id %}|{% url '\''assureur:creer_bon_pour_membre'\'' membre.id %}|g
    s|{% url .creer_bon. %}|{% url '\''assureur:creer_bon'\'' %}|g
    ' ./templates/assureur/liste_membres.html

    echo "✅ liste_membres.html corrigé"
fi

# 2. detail_membre.html
if [ -f "./templates/assureur/detail_membre.html" ]; then
    echo "📝 Correction de detail_membre.html..."

    # Copie de sauvegarde
    cp ./templates/assureur/detail_membre.html ./templates/assureur/detail_membre.html.backup

    # Remplacement précis
    sed -i '' '
    # Ligne 20: bouton principal
    s|<a href="{% url .creer_bon. membre.id %}"|<a href="{% url '\''assureur:creer_bon_pour_membre'\'' membre.id %}"|g

    # Ligne 123: bouton dans l'onglet
    s|<a href="{% url .creer_bon. membre.id %}"|<a href="{% url '\''assureur:creer_bon_pour_membre'\'' membre.id %}"|g

    # Tous les autres cas
    s|{% url .creer_bon. membre.id %}|{% url '\''assureur:creer_bon_pour_membre'\'' membre.id %}|g
    s|{% url .creer_bon. %}|{% url '\''assureur:creer_bon'\'' %}|g
    ' ./templates/assureur/detail_membre.html

    echo "✅ detail_membre.html corrigé"
fi

... (tronqué)

# ============================================================
# ORIGINE 4: fix_all_creer_bon.sh (2025-12-04)
# ============================================================

#!/bin/bash

echo "🔧 Correction de tous les templates avec 'creer_bon'..."

# Trouver tous les templates avec 'creer_bon'
find ./templates -name "*.html" -type f | while read template; do
    if grep -q "creer_bon" "$template"; then
        echo "�� Correction de: $template"

        # Créer une sauvegarde
        cp "$template" "${template}.backup.$(date +%s)"

        # CORRECTION 1: 'creer_bon' avec argument 'membre.id' (vers 'creer_bon_pour_membre')
        sed -i '' "s|{% url 'creer_bon' membre.id %}|{% url 'assureur:creer_bon_pour_membre' membre.id %}|g" "$template"
        sed -i '' "s|{% url \"creer_bon\" membre.id %}|{% url \"assureur:creer_bon_pour_membre\" membre.id %}|g" "$template"

        # CORRECTION 2: 'creer_bon' sans argument (vers 'creer_bon')
        sed -i '' "s|{% url 'creer_bon' %}|{% url 'assureur:creer_bon' %}|g" "$template"
        sed -i '' "s|{% url \"creer_bon\" %}|{% url \"assureur:creer_bon\" %}|g" "$template"

        # CORRECTION 3: 'creer_bon' dans le texte ou autres contextes
        sed -i '' "s|href=\"{% url 'creer_bon'|href=\"{% url 'assureur:creer_bon'|g" "$template"
        sed -i '' "s|href=\"{% url \"creer_bon\"|href=\"{% url \"assureur:creer_bon\"|g" "$template"

        echo "✅ Fichier corrigé"
    fi
done

echo "🎉 Tous les templates corrigés !"

# ============================================================
# ORIGINE 5: fix_template_final.py (2025-12-03)
# ============================================================

# fix_template_final.py
import re

# Lire le template
with open('templates/assureur/generer_cotisations.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("=== CORRECTION DU TEMPLATE ===")

# Vérifier si l'URL incorrecte existe encore
if '{% url "preview_generation" %}' in content:
    print("⚠ URL incorrecte trouvée : {% url \"preview_generation\" %}")
    # Remplacer par la version corrigée
    content = content.replace(
        '{% url "preview_generation" %}',
        '{% url "assureur:preview_generation" %}'
    )
    print("✓ Corrigé en : {% url \"assureur:preview_generation\" %}")

if "url: '{% url \"preview_generation\" %}'" in content:
    print("⚠ URL JavaScript incorrecte trouvée")
    # Remplacer la ligne JavaScript spécifique
    content = content.replace(
        "url: '{% url \"preview_generation\" %}'",
        "url: '{% url \"assureur:preview_generation\" %}'"
    )
    print("✓ Ligne JavaScript corrigée")

# Écrire le fichier corrigé
with open('templates/assureur/generer_cotisations.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n=== VÉRIFICATION FINALE ===")

# Vérifier qu'il n'y a plus d'erreurs
with open('templates/assureur/generer_cotisations.html', 'r', encoding='utf-8') as f:
    content = f.read()

if 'preview_generation' in content:
    # Trouver les lignes avec preview_generation
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if 'preview_generation' in line and 'assureur:preview_generation' not in line:
            print(f"⚠ Ligne {i}: {line.strip()}")
        elif 'assureur:preview_generation' in line:
            print(f"✓ Ligne {i}: Correcte")

print("\nCorrection terminée !")

# ============================================================
# ORIGINE 6: fix_js_url.py (2025-12-03)
# ============================================================

import re

# Lire le template
with open('templates/assureur/generer_cotisations.html', 'r') as f:
    content = f.read()

# Remplacer toutes les occurrences de preview_generation
# Pattern 1: JavaScript avec doubles quotes imbriquées
pattern1 = r"url:\s*'{% url \"preview_generation\" %}'"
replacement1 = "url: '{% url \"assureur:preview_generation\" %}'"

# Pattern 2: JavaScript avec simples quotes imbriquées
pattern2 = r"url:\s*'{% url 'preview_generation' %}'"
replacement2 = "url: '{% url \"assureur:preview_generation\" %}'"

new_content = re.sub(pattern1, replacement1, content)
new_content = re.sub(pattern2, replacement2, new_content)

# Écrire le fichier corrigé
with open('templates/assureur/generer_cotisations.html', 'w') as f:
    f.write(new_content)

print("Template corrigé !")

# ============================================================
# ORIGINE 7: fix_datetime_warnings.py (2025-12-03)
# ============================================================

# fix_datetime_warnings.py
import os
import sys
import django
from pathlib import Path
from datetime import datetime
from django.utils import timezone

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

django.setup()

print("🔧 CORRECTION DES WARNINGS DATETIME")
print("="*50)

from assureur.models import Membre, Bon, Paiement, Soin

def fix_naive_datetimes():
    print("1. Correction des dates naïves dans les modèles...")

    # Membre
    membres = Membre.objects.filter(created_at__isnull=False)
    for membre in membres:
        if membre.created_at and membre.created_at.tzinfo is None:
            membre.created_at = timezone.make_aware(membre.created_at)
            membre.save()
    print(f"   ✅ Membres: {membres.count()} vérifiés")

    # Bon
    bons = Bon.objects.filter(date_creation__isnull=False)
    for bon in bons:
        if bon.date_creation and bon.date_creation.tzinfo is None:
            bon.date_creation = timezone.make_aware(bon.date_creation)
            bon.save()
    print(f"   ✅ Bons: {bons.count()} vérifiés")

    # Paiement
    paiements = Paiement.objects.filter(date_paiement__isnull=False)
    for paiement in paiements:
        if paiement.date_paiement and paiement.date_paiement.tzinfo is None:
            paiement.date_paiement = timezone.make_aware(paiement.date_paiement)
            paiement.save()
    print(f"   ✅ Paiements: {paiements.count()} vérifiés")

    # Soin
    soins = Soin.objects.filter(date_soumission__isnull=False)
    for soin in soins:
        if soin.date_soumission and soin.date_soumission.tzinfo is None:
... (tronqué)

# ============================================================
# ORIGINE 8: fix_redirect_complete1.py (2025-12-03)
# ============================================================

# fix_redirect_complete.py
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

django.setup()

print("🔧 CORRECTION COMPLÈTE DE LA REDIRECTION")
print("="*50)

# 1. Vérifier et corriger core/utils.py
print("\n1. Correction de core/utils.py...")
core_utils_path = BASE_DIR / "core" / "utils.py"

if core_utils_path.exists():
    with open(core_utils_path, 'r') as f:
        content = f.read()

    # Vérifier si la fonction retourne /assureur/dashboard/
    if "return '/assureur/dashboard/'" in content:
        content = content.replace("return '/assureur/dashboard/'", "return '/assureur/'")
        with open(core_utils_path, 'w') as f:
            f.write(content)
        print("✅ core/utils.py corrigé (retourne '/assureur/')")
    elif 'return "/assureur/dashboard/"' in content:
        content = content.replace('return "/assureur/dashboard/"', 'return "/assureur/"')
        with open(core_utils_path, 'w') as f:
            f.write(content)
        print("✅ core/utils.py corrigé (retourne '/assureur/')")
    else:
        print("ℹ️  La fonction get_user_redirect_url ne retourne pas '/assureur/dashboard/'")
else:
    print("❌ core/utils.py non trouvé")

# 2. Vérifier et corriger assureur/urls.py
print("\n2. Correction de assureur/urls.py...")
urls_path = BASE_DIR / "assureur" / "urls.py"

if urls_path.exists():
    with open(urls_path, 'r') as f:
        content = f.read()

    # Vérifier si l'import views_correction existe
    if 'from . import views_correction' not in content:
        # Ajouter après les autres imports
... (tronqué)

# ============================================================
# ORIGINE 9: fix_redirect_complete.py (2025-12-03)
# ============================================================

# fix_redirect_complete.py
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

django.setup()

print("🔧 CORRECTION COMPLÈTE DE LA REDIRECTION")
print("="*50)

# 1. Vérifier et corriger core/utils.py
print("\n1. Correction de core/utils.py...")
core_utils_path = BASE_DIR / "core" / "utils.py"

if core_utils_path.exists():
    with open(core_utils_path, 'r') as f:
        content = f.read()

    # Vérifier si la fonction retourne /assureur/dashboard/
    if 'return \'/assureur/dashboard/\'' in content:
        content = content.replace('return \'/assureur/dashboard/\'', 'return \'/assureur/\'')
        with open(core_utils_path, 'w') as f:
            f.write(content)
        print("✅ core/utils.py corrigé (retourne '/assureur/')")
    elif 'return "/assureur/dashboard/"' in content:
        content = content.replace('return "/assureur/dashboard/"', 'return "/assureur/"')
        with open(core_utils_path, 'w') as f:
            f.write(content)
        print("✅ core/utils.py corrigé (retourne '/assureur/')")
    else:
        print("ℹ️  La fonction get_user_redirect_url ne retourne pas '/assureur/dashboard/'")
else:
    print("❌ core/utils.py non trouvé")

# 2. Vérifier et corriger assureur/urls.py
print("\n2. Correction de assureur/urls.py...")
urls_path = BASE_DIR / "assureur" / "urls.py"

if urls_path.exists():
    with open(urls_path, 'r') as f:
        content = f.read()

    # Vérifier si l'import views_correction existe
    if 'from . import views_correction' not in content:
        # Ajouter après les autres imports
... (tronqué)

# ============================================================
# ORIGINE 10: fix_all_templates.py (2025-12-02)
# ============================================================

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
... (tronqué)

# ============================================================
# ORIGINE 11: fix_all_issues.py (2025-12-02)
# ============================================================

import os
import sys
import re

# Chemin du projet
project_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(project_path)
os.chdir(project_path)

print("🔧 CORRECTION DES PROBLÈMES URL ET TEMPLATES")

# 1. Corriger communication/urls.py
print("\n1. Correction de communication/urls.py...")
urls_path = 'communication/urls.py'

with open(urls_path, 'r') as f:
    content = f.read()

# Vérifier et ajouter l'import JsonResponse
if 'from django.http import JsonResponse' not in content:
    content = content.replace(
        'from django.urls import path',
        'from django.urls import path\nfrom django.http import JsonResponse, HttpResponse'
    )

# Vérifier si message_create existe
if "'message_create'" not in content and '"message_create"' not in content:
    # Trouver le bon endroit pour ajouter
    if 'app_name =' in content:
        # Ajouter après les autres URLs d'API
        api_pattern = r'(path\(\'api/public/test/\'.*?\n)'
        if re.search(api_pattern, content, re.DOTALL):
            # Ajouter une URL temporaire pour message_create
            replacement = r'\1    # URL temporaire pour éviter les erreurs de template\n    path(\'messages/create/\', lambda request: HttpResponse("""<html><body><h1>Création de message</h1><p>Fonctionnalité en développement.</p><a href=\"/\">Retour</a></body></html>"""), name=\'message_create\'),\n'
            content = re.sub(api_pattern, replacement, content, flags=re.DOTALL)
        else:
            # Ajouter à la fin des urlpatterns
            if 'urlpatterns = [' in content:
                url_end = content.find(']', content.find('urlpatterns = ['))
                if url_end != -1:
                    new_url = '    # URL temporaire pour éviter les erreurs de template\n    path(\'messages/create/\', lambda request: HttpResponse("""<html><body><h1>Création de message</h1><p>Fonctionnalité en développement.</p><a href=\"/\">Retour</a></body></html>"""), name=\'message_create\'),'
                    content = content[:url_end] + new_url + '\n' + content[url_end:]

with open(urls_path, 'w') as f:
    f.write(content)
print("✅ communication/urls.py corrigé")

# 2. Corriger mutuelle_core/views.py - Page d'accueil temporaire
print("\n2. Correction de la page d'accueil...")
views_path = 'mutuelle_core/views.py'
... (tronqué)

# ============================================================
# ORIGINE 12: fix_permission_cache.py (2025-12-02)
# ============================================================

#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def test_with_auth():
    """Tester avec authentification réelle"""
    print("🧪 TEST AVEC AUTHENTIFICATION RÉELLE")
    print("=" * 40)

    # Remplacez par le vrai mot de passe de GLORIA1
    password = "votremotdepasse"  # À modifier !

    # Authentifier
    user = authenticate(username='GLORIA1', password=password)

    if not user:
        print("❌ Échec de l'authentification")
        print("💡 Vérifiez le mot de passe dans le script")
        return

    print(f"✅ Authentifié: {user.username}")
    print(f"📋 Groupes: {[g.name for g in user.groups.all()]}")

    # Tester les permissions
    test_permissions = [
        ('medecin.view_ordonnance', 'Voir ordonnances médecin'),
        ('medecin.change_ordonnance', 'Modifier ordonnances médecin'),
        ('medecin.add_ordonnance', 'Ajouter ordonnances médecin'),
        ('medecin.delete_ordonnance', 'Supprimer ordonnances médecin'),
        ('pharmacien.view_ordonnancepharmacien', 'Voir ordonnances pharmacien'),
        ('pharmacien.change_ordonnancepharmacien', 'Modifier ordonnances pharmacien'),
        ('pharmacien.add_ordonnancepharmacien', 'Ajouter ordonnances pharmacien'),
        ('pharmacien.delete_ordonnancepharmacien', 'Supprimer ordonnances pharmacien'),
    ]

    print("\n🔍 TEST DES PERMISSIONS:")
    print("-" * 30)

    for perm_code, perm_name in test_permissions:
        if user.has_perm(perm_code):
            print(f"✅ {perm_name}")
... (tronqué)

# ============================================================
# ORIGINE 13: fix_contenttypes.py (2025-12-02)
# ============================================================

#!/usr/bin/env python
"""
CORRECTION DES CONTENTTYPES EN DOUBLE
Résout l'erreur: get() returned more than one ContentType
"""

import os
import sys
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.db import transaction

def corriger_contenttypes_doubles():
    """Corrige les ContentTypes en double"""
    print("🔧 CORRECTION DES CONTENTTYPES EN DOUBLE")
    print("=" * 60)

    # Trouve les ContentTypes avec le même app_label et model
    from django.db.models import Count
    duplicates = ContentType.objects.values('app_label', 'model').annotate(
        count=Count('id')
    ).filter(count__gt=1)

    print(f"ContentTypes en double trouvés: {duplicates.count()}")

    fixed_count = 0
    for dup in duplicates:
        app_label = dup['app_label']
        model = dup['model']

        ctypes = ContentType.objects.filter(app_label=app_label, model=model)
        print(f"\n📋 {app_label}.{model}: {ctypes.count()} instances")

        # Garde le premier, supprime les autres
        if ctypes.count() > 1:
            keep_ct = ctypes.first()
            delete_cts = ctypes.exclude(id=keep_ct.id)

            print(f"  ✅ Garde: ID {keep_ct.id}")
            print(f"  🗑️  Supprime: {delete_cts.count()} instances")

            # Pour chaque ContentType à supprimer, déplace les permissions
            for delete_ct in delete_cts:
                # Trouve toutes les permissions liées à ce ContentType
... (tronqué)

# ============================================================
# ORIGINE 14: fix_permissions.py (2025-12-02)
# ============================================================

#!/usr/bin/env python
"""
CORRECTION DES PERMISSIONS EN DOUBLE
Résout l'erreur: get() returned more than one Permission
"""

import os
import sys
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

def corriger_permissions_en_double():
    """Corrige les permissions en double"""
    print("🔧 CORRECTION DES PERMISSIONS EN DOUBLE")
    print("=" * 60)

    # Trouve toutes les permissions avec le même codename
    from django.db.models import Count
    duplicates = Permission.objects.values('codename').annotate(
        count=Count('id')
    ).filter(count__gt=1)

    print(f"Permissions en double trouvées: {duplicates.count()}")

    fixed_count = 0
    for dup in duplicates:
        codename = dup['codename']
        perms = Permission.objects.filter(codename=codename)

        print(f"\n📋 Permission '{codename}': {perms.count()} instances")

        # Garde la première, supprime les autres
        if perms.count() > 1:
            keep_perm = perms.first()
            delete_perms = perms.exclude(id=keep_perm.id)

            # Vérifie quelles groupes utilisent ces permissions
            for group in Group.objects.all():
                group_perms = group.permissions.filter(codename=codename)
                if group_perms.count() > 1:
                    # Garde seulement la première permission dans le groupe
                    group.permissions.remove(*delete_perms)
                    print(f"  ✅ Groupe '{group.name}' nettoyé")
... (tronqué)

# ============================================================
# ORIGINE 15: fix_est_actif.py (2025-12-01)
# ============================================================

#!/usr/bin/env python3
"""
Corrige l'erreur 'no such column: p.est_actif'
"""
import os
import sys
import django

sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()

    # Chercher dans les fichiers où il y a une référence à 'est_actif'
    import re

    print("Recherche de 'est_actif' dans les fichiers Python...")

    files_to_check = [
        'medecin/views.py',
        'pharmacien/views.py',
        'core/utils.py',
        'membres/models.py',
    ]

    for file_path in files_to_check:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                if 'est_actif' in content:
                    print(f"\n📁 {file_path}:")
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'est_actif' in line:
                            print(f"  Ligne {i+1}: {line.strip()}")

except Exception as e:
    print(f"Erreur: {e}")

# ============================================================
# ORIGINE 16: fix_final_historique.py (2025-12-01)
# ============================================================


#!/usr/bin/env python3
import os
import sys
import re

# Chemin du fichier views.py
views_path = "pharmacien/views.py"

# Lire le contenu
with open(views_path, 'r') as f:
    content = f.read()

# Trouver et remplacer la fonction historique_validation
# Nouvelle version corrigée
new_function = '''@login_required
@pharmacien_required
@gerer_erreurs
def historique_validation(request):
    """Affiche l'historique des ordonnances validées par le pharmacien"""
    try:
        # Importer les modèles nécessaires
        from pharmacien.models import OrdonnancePharmacien, Pharmacien
        from django.core.paginator import Paginator
        from django.utils import timezone
        from datetime import timedelta
        import logging

        logger = logging.getLogger(__name__)

        # 1. Obtenir le profil Pharmacien de l'utilisateur
        try:
            pharmacien_profile = Pharmacien.objects.get(user=request.user)
        except Pharmacien.DoesNotExist:
            logger.error(f"Profil pharmacien non trouvé pour {request.user.username}")
            from django.contrib import messages
            messages.error(request, "Profil pharmacien introuvable.")
            return redirect('pharmacien:dashboard')

        # 2. Récupérer l'historique des validations
        # CORRECTION: utiliser pharmacien_validateur (Foreign Key vers User)
        validations_qs = OrdonnancePharmacien.objects.filter(
            pharmacien_validateur=request.user,  # CHANGÉ ICI: pharmacien_validateur est un ForeignKey vers User
            date_validation__isnull=False
        ).select_related(
            'ordonnance_medecin__patient',
            'ordonnance_medecin__medecin'
        ).order_by('-date_validation')

        # 3. Adapter les données pour le template
... (tronqué)

# ============================================================
# ORIGINE 17: fix_pharmacien.sh (2025-12-01)
# ============================================================

#!/bin/bash
# Script de correction rapide pour pharmacien/views.py

echo "=== CORRECTION DES PROBLÈMES IDENTIFIÉS ==="

# 1. Créer un fichier de correction pour views.py
cat > /tmp/fix_pharmacien_views.py << 'EOF'
import os
import sys
import django

# Trouver le bon chemin pour les settings
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_path)

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    django.setup()
except:
    # Essayer un autre nom de settings
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
        django.setup()
    except:
        print("Impossible de charger les settings Django")
        sys.exit(1)

# Maintenant, analysons la structure
print("=== STRUCTURE DES MODÈLES ===")

# Vérifier les modèles disponibles
try:
    from django.apps import apps

    # Afficher tous les modèles
    print("Modèles disponibles dans l'application:")
    for model in apps.get_models():
        print(f"  - {model._meta.app_label}.{model.__name__}")

except Exception as e:
    print(f"Erreur: {e}")

# Vérifier spécifiquement les modèles pharmacien
print("\n=== MODÈLES PHARMACIEN ===")
try:
    from pharmacien.models import *
    print("Modèles importés depuis pharmacien.models:")
    for attr in dir():
        if not attr.startswith('_') and attr[0].isupper():
            print(f"  - {attr}")
... (tronqué)

# ============================================================
# ORIGINE 18: fix_message_api.sh (2025-12-01)
# ============================================================

#!/bin/bash

echo "🔧 CORRECTION API ENVOI MESSAGE"
echo "================================"

# Vérifier la vue envoyer_message_api dans views.py
echo "🔍 Analyse de la vue envoyer_message_api:"
grep -n -A 20 "def envoyer_message_api" communication/views.py | head -30

# Vérifier si le décorateur csrf_exempt est présent
if ! grep -q "@csrf_exempt" communication/views.py; then
    echo "⚠️  Décorateur @csrf_exempt manquant, ajout..."

    # Trouver la ligne de la fonction
    LINE=$(grep -n "def envoyer_message_api" communication/views.py | cut -d: -f1)

    if [ -n "$LINE" ]; then
        # Ajouter l'import et le décorateur
        sed -i '' "${LINE}i\\
from django.views.decorators.csrf import csrf_exempt\\
\\
@csrf_exempt" communication/views.py

        echo "✅ Décorateur @csrf_exempt ajouté"
    fi
else
    echo "✅ Décorateur @csrf_exempt déjà présent"
fi

# Vérifier aussi la fonction dans le fichier
echo ""
echo "📝 Vérification de la fonction:"
python -c "
import sys
sys.path.insert(0, '.')
import inspect
from communication.views import envoyer_message_api

print('Signature:')
print(inspect.signature(envoyer_message_api))
print('\\nSource (extrait):')
print(inspect.getsource(envoyer_message_api)[:500])
"

# Test après correction
echo ""
echo "🧪 Test après correction:"
python -c "
import sys
import os
... (tronqué)

# ============================================================
# ORIGINE 19: fix_view_final.py (2025-12-01)
# ============================================================

import sqlite3
from datetime import datetime

def fix_view_final():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    try:
        print("🔧 CORRECTION FINALE DE LA VUE")
        print("=" * 50)

        # 1. Vérifier la structure de auth_user
        cursor.execute("PRAGMA table_info(auth_user)")
        user_columns = [col[1] for col in cursor.fetchall()]
        print("Colonnes auth_user:", user_columns)

        # 2. Recréer la vue avec les bonnes jointures
        cursor.execute("DROP VIEW IF EXISTS pharmacien_ordonnances_view")

        view_sql = '''
            CREATE VIEW pharmacien_ordonnances_view AS
            SELECT
                op.id as partage_id,
                mo.id as ordonnance_id,
                mo.numero,
                mo.date_prescription,
                mo.date_expiration,
                mo.type_ordonnance,
                mo.diagnostic,
                mo.medicaments,
                mo.posologie,
                mo.duree_traitement,
                mo.renouvelable,
                mo.nombre_renouvellements,
                mo.renouvellements_effectues,
                mo.statut,
                mo.est_urgent,
                mo.notes,
                op.date_partage,
                CASE WHEN op.statut = 'ACTIF' THEN 1 ELSE 0 END as partage_actif,
                m.nom as patient_nom,
                m.prenom as patient_prenom,
                u_med.first_name as medecin_prenom,
                u_med.last_name as medecin_nom,
                u_pharm.first_name as pharmacien_prenom,
                u_pharm.last_name as pharmacien_nom
            FROM ordonnance_partage op
            JOIN medecin_ordonnance mo ON op.ordonnance_medecin_id = mo.id
            JOIN membres_membre m ON mo.patient_id = m.id
            JOIN medecin_medecin mm ON mo.medecin_id = mm.id
... (tronqué)

# ============================================================
# ORIGINE 20: fix_final_complete.py (2025-12-01)
# ============================================================

import sqlite3
from datetime import datetime, timedelta

def fix_final_complete():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    try:
        print("🔧 CORRECTION COMPLÈTE - MÉDECIN_ORDONNANCE")
        print("=" * 60)

        # 1. Vérifier la structure de medecin_ordonnance
        cursor.execute("PRAGMA table_info(medecin_ordonnance)")
        columns = cursor.fetchall()
        print("Structure de medecin_ordonnance:")
        for col in columns:
            print(f"  {col[1]} ({col[2]}) - Nullable: {not col[3]}")

        # 2. Vérifier les données de référence
        cursor.execute("SELECT COUNT(*) FROM medecin_medecin")
        medecins_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM membres_membre")
        patients_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM pharmacien_pharmacien")
        pharmaciens_count = cursor.fetchone()[0]

        print(f"\n📊 DONNÉES DE RÉFÉRENCE:")
        print(f"   Médecins: {medecins_count}")
        print(f"   Patients: {patients_count}")
        print(f"   Pharmaciens: {pharmaciens_count}")

        if medecins_count == 0 or patients_count == 0:
            print("❌ Données manquantes - création des données de base...")
            create_base_data(cursor)

        # 3. Créer des ordonnances dans medecin_ordonnance
        date_prescription = datetime.now().strftime('%Y-%m-%d')
        date_expiration = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        date_creation = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        ordonnances_data = [
            # Structure complète de medecin_ordonnance
            (
                'MED-ORD-001', date_prescription, date_expiration, date_creation, date_creation,
                'STANDARD', 'Infection bactérienne des voies respiratoires',
                'Amoxicilline 500mg', '1 comprimé 3 fois par jour pendant 7 jours', 7,
                0, 0, 0, 'ACTIVE', 0,
                'Traitement antibiotique standard - Allergie: Aucune connue',
                1, None, None, 1, 1
            ),
... (tronqué)

# ============================================================
# ORIGINE 21: fix_urgence_v2.py (2025-12-01)
# ============================================================

import sqlite3
import os
from datetime import datetime, timedelta

def fix_urgence_v2():
    # Connexion à la base de données
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    try:
        # 1. Vérifier la structure de la table
        cursor.execute("PRAGMA table_info(medecin_ordonnance)")
        columns = cursor.fetchall()
        print("Structure de medecin_ordonnance:")
        for col in columns:
            print(f"  {col[1]} ({col[2]}) - Nullable: {not col[3]}")

        # 2. Dates pour les ordonnances
        date_prescription = datetime.now().strftime('%Y-%m-%d')
        date_expiration = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        date_creation = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 3. Insérer des données avec la structure correcte
        ordonnances_urgence = [
            # (numero, date_prescription, date_expiration, date_creation, date_modification,
            # type_ordonnance, diagnostic, medicaments, posologie, duree_traitement,
            # renouvelable, nombre_renouvellements, renouvellements_effectues, statut,
            # est_urgent, notes, partage_effectue, medecin_id, patient_id)
            (
                f"ORD-001-{datetime.now().strftime('%Y%m%d')}",
                date_prescription, date_expiration, date_creation, date_creation,
                'STANDARD', 'Infection bactérienne',
                'Amoxicilline 500mg', '1 comprimé 3 fois par jour', 7,
                0, 0, 0, 'ACTIVE', 1,
                'Traitement antibiotique pour infection - Suivi dans 7 jours',
                1, 1, 1
            ),
            (
                f"ORD-002-{datetime.now().strftime('%Y%m%d')}",
                date_prescription, date_expiration, date_creation, date_creation,
                'STANDARD', 'Douleurs inflammatoires',
                'Ibuprofène 400mg', '1 comprimé 3 fois par jour après les repas', 5,
                0, 0, 0, 'ACTIVE', 0,
                'Antidouleur et anti-inflammatoire - Contre-indication estomac vide',
                1, 2, 2
            ),
            (
                f"ORD-003-{datetime.now().strftime('%Y%m%d')}",
                date_prescription, date_expiration, date_creation, date_creation,
                'CHRONIQUE', 'Hypertension artérielle',
... (tronqué)

# ============================================================
# ORIGINE 22: fix_urgence.py (2025-12-01)
# ============================================================

import sqlite3
import os

def fix_urgence():
    # Connexion à la base de données
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    try:
        # 1. Vérifier la structure de la table
        cursor.execute("PRAGMA table_info(medecin_ordonnance)")
        columns = cursor.fetchall()
        print("Structure de medecin_ordonnance:")
        for col in columns:
            print(f"  {col[1]} ({col[2]}) - Nullable: {not col[3]}")

        # 2. Insérer des données avec notes
        ordonnances_urgence = [
            (1, 1, '2024-01-15', 'Traitement urgence', 7, 'Notes médicales standard'),
            (2, 2, '2024-01-16', 'Antibiotique urgence', 10, 'Suivi nécessaire'),
            (3, 3, '2024-01-17', 'Antidouleur urgence', 5, 'Contrôle dans 48h')
        ]

        for ord in ordonnances_urgence:
            cursor.execute('''
                INSERT OR IGNORE INTO medecin_ordonnance
                (patient_id, medecin_id, date_prescription, instructions, duree_traitement, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ord)

        # 3. Créer les partages
        cursor.execute('''
            INSERT OR IGNORE INTO ordonnance_partage
            (ordonnance_id, pharmacien_id, date_partage, est_actif)
            SELECT id, 1, date('now'), 1
            FROM medecin_ordonnance
            WHERE id NOT IN (SELECT ordonnance_id FROM ordonnance_partage)
        ''')

        conn.commit()
        print("✅ Données d'urgence insérées avec succès")

        # 4. Vérification
        cursor.execute("SELECT COUNT(*) FROM medecin_ordonnance")
        count = cursor.fetchone()[0]
        print(f"📊 Ordonnances totales: {count}")

    except Exception as e:
        print(f"❌ Erreur: {e}")
        conn.rollback()
... (tronqué)

# ============================================================
# ORIGINE 23: fix_ordonnance_sharing.py (2025-11-30)
# ============================================================

# fix_ordonnance_sharing.py
import os
import django
from django.db import connection
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyze_ordonnance_structure():
    """Analyser la structure réelle des tables ordonnances"""
    print("🔍 ANALYSE STRUCTURELLE ORDONNANCES")
    print("=" * 50)

    with connection.cursor() as cursor:
        # Structure table médecin
        print("\n📋 STRUCTURE medecin_ordonnance:")
        cursor.execute("PRAGMA table_info(medecin_ordonnance)")
        for col in cursor.fetchall():
            print(f"   {col[1]} ({col[2]})")

        # Structure table pharmacien
        print("\n📋 STRUCTURE pharmacien_ordonnancepharmacien:")
        try:
            cursor.execute("PRAGMA table_info(pharmacien_ordonnancepharmacien)")
            for col in cursor.fetchall():
                print(f"   {col[1]} ({col[2]})")
        except:
            print("   ❌ Table non accessible")

def create_sharing_system():
    """Créer un système de partage entre médecin et pharmacien"""
    print("\n🔗 CRÉATION SYSTÈME DE PARTAGE")
    print("=" * 50)

    # 1. Vérifier et créer la table de liaison si nécessaire
    with connection.cursor() as cursor:
        try:
            # Créer une table de liaison si elle n'existe pas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ordonnance_partage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ordonnance_medecin_id INTEGER,
                    pharmacien_id INTEGER,
                    date_partage DATETIME DEFAULT CURRENT_TIMESTAMP,
                    statut VARCHAR(20) DEFAULT 'en_attente',
                    FOREIGN KEY (ordonnance_medecin_id) REFERENCES medecin_ordonnance(id)
                )
            """)
            print("✅ Table de partage créée/mise à jour")
... (tronqué)

# ============================================================
# ORIGINE 24: fix_missing_sync.py (2025-11-30)
# ============================================================

# fix_missing_sync.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db import connection

def check_table_structures():
    """Vérifier la structure des tables problématiques"""
    print("🔍 STRUCTURE DES TABLES PROBLÉMATIQUES")
    print("=" * 50)

    tables = ['soins_soin', 'medecin_consultation', 'soins_bondesoin']

    for table in tables:
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                print(f"\n📋 {table}:")
                for col in columns:
                    print(f"   {col[1]} ({col[2]})")
        except Exception as e:
            print(f"❌ {table}: {e}")

def create_missing_relations():
    """Créer des relations manquantes pour la synchronisation"""
    print("\n🔗 CRÉATION DE RELATIONS TEST")
    print("=" * 50)

    # Créer quelques enregistrements de test dans les tables vides
    test_data = [
        ('soins_soin', 'Soin de test pour membre 1', 1),
        ('medecin_consultation', 'Consultation test', 2),
    ]

    for table, description, membre_id in test_data:
        try:
            with connection.cursor() as cursor:
                # Vérifier si la table a un champ membre_id
                cursor.execute(f"PRAGMA table_info({table})")
                colonnes = [col[1] for col in cursor.fetchall()]

                if 'membre_id' in colonnes:
                    cursor.execute(f"INSERT INTO {table} (description, membre_id) VALUES (?, ?)",
                                 [description, membre_id])
                    print(f"✅ {table}: Relation créée avec membre_id {membre_id}")
                else:
                    print(f"⚠️  {table}: Pas de champ membre_id")
... (tronqué)

# ============================================================
# ORIGINE 25: fix_membre_conflict.py (2025-11-30)
# ============================================================

# fix_membre_conflict.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnose_membre_conflict():
    """Diagnostiquer le conflit entre modèles Membre"""
    print("🔍 DIAGNOSTIC DU CONFLIT DE MODÈLES MEMBRE")
    print("=" * 60)

    from django.apps import apps

    # Identifier tous les modèles Membre
    membre_models = []
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            if model.__name__ == 'Membre':
                membre_models.append(f"{app_config.name}.{model.__name__}")

    print(f"📋 Modèles Membre trouvés: {membre_models}")

    # Analyser le problème
    if 'membres.Membre' in membre_models and 'assureur.Membre' in membre_models:
        print("🚨 CONFLIT: Deux modèles Membre détectés!")
        print("   ❌ membres.Membre (modèle principal)")
        print("   ❌ assureur.Membre (modèle en conflit)")

        # Vérifier quel modèle est utilisé par Cotisation
        from assureur.models import Cotisation
        membre_field = Cotisation._meta.get_field('membre')
        print(f"🔗 Cotisation.membre pointe vers: {membre_field.related_model}")

        return True
    else:
        print("✅ Aucun conflit détecté")
        return False

def create_cotisation_fix():
    """Créer une solution de contournement"""
    print("\n🔧 CRÉATION SOLUTION DE CONTOURNEMENT")
    print("=" * 60)

    from membres.models import Membre as MembrePrincipal
    from assureur.models import Cotisation, Assureur
    from django.utils import timezone
    from datetime import timedelta

    try:
        # 1. Vérifier l'assureur
... (tronqué)

# ============================================================
# ORIGINE 26: fix_remaining_issues.py (2025-11-30)
# ============================================================

# fix_remaining_issues.py - VERSION ULTIME SIMPLIFIÉE
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def check_and_fix_database():
    """Vérifier et corriger la structure de la base"""
    print("🔍 Vérification de la structure de la base...")

    with connection.cursor() as cursor:
        cursor.execute("PRAGMA table_info(membres_membre)")
        columns = [col[1] for col in cursor.fetchall()]

        if 'score_risque' not in columns:
            print("➕ Ajout de la colonne score_risque...")
            cursor.execute("ALTER TABLE membres_membre ADD COLUMN score_risque INTEGER DEFAULT 0")
            print("✅ Colonne score_risque ajoutée")
        else:
            print("✅ Colonne score_risque existe déjà")

    print("🎯 Structure de base vérifiée")

def create_test_agent():
    """Créer un agent de test si nécessaire"""
    from django.contrib.auth.models import User
    from agents.models import Agent

    try:
        user = User.objects.get(username='LEILA')
        if not Agent.objects.filter(user=user).exists():
            print("👤 Création de l'agent LEILA...")
            Agent.objects.create(
                user=user,
                telephone="0102030405",
                est_actif=True
            )
            print("✅ Agent LEILA créé")
        else:
            print("✅ Agent LEILA existe déjà")
    except User.DoesNotExist:
        print("⚠️  Utilisateur LEILA non trouvé - création de l'utilisateur...")
        user = User.objects.create_user(
            username='LEILA',
            password='test123',
            first_name='Leila',
            last_name='Test',
            email='leila@test.com'
... (tronqué)

# ============================================================
# ORIGINE 27: fix_migrations.py (2025-11-27)
# ============================================================

import os
import glob

def fix_migrations():
    """Corrige les problèmes de migrations"""

    # Supprimer les fichiers de migration sauf __init__.py
    migration_files = glob.glob("*/migrations/0*.py")
    for file in migration_files:
        os.remove(file)
        print(f"Supprimé: {file}")

    # Supprimer la base de données
    if os.path.exists("db.sqlite3"):
        os.remove("db.sqlite3")
        print("Base de données supprimée")

    print("✅ Nettoyage terminé")
    print("🎯 Exécutez maintenant:")
    print("   python manage.py makemigrations")
    print("   python manage.py migrate")
    print("   python manage.py createsuperuser")
    print("   python manage.py runserver")

if __name__ == "__main__":
    fix_migrations()

# ============================================================
# ORIGINE 28: fix_validation_test.py (2025-11-19)
# ============================================================

#!/usr/bin/env python
import os
import sys

def fix_validation_script():
    """Corriger le script final_validation.py pour passer les arguments aux URLs"""

    file_path = 'final_validation.py'

    try:
        with open(file_path, 'r') as file:
            content = file.read()

        print("🔍 RECHERCHE DE LA SECTION DE TEST DES URLs...")

        # Trouver la section où les URLs sont testées
        start_marker = "🌐 TEST COMPLET DES URLs:"
        end_marker = "📊 URLs:"

        start_pos = content.find(start_marker)
        end_pos = content.find(end_marker, start_pos)

        if start_pos == -1 or end_pos == -1:
            print("❌ Impossible de trouver la section des URLs dans final_validation.py")
            return False

        # Extraire la section des URLs
        urls_section = content[start_pos:end_pos]

        # Vérifier si la correction est déjà appliquée
        if "args=[1]" in urls_section:
            print("✅ La correction est déjà appliquée")
            return True

        print("🔧 APPLICATION DE LA CORRECTION...")

        # Remplacer les appels reverse pour les URLs avec paramètres
        old_code = """        try:
            url = reverse(url_name)
            print(f"   ✅ {url_name:45} -> {url}")
            working_urls += 1"""

        new_code = """        try:
            # Gestion des URLs avec paramètres
            if url_name in ['agents:creer_bon_soin_membre', 'agents:confirmation_bon_soin']:
                url = reverse(url_name, args=[1])  # Argument factice pour le test
            else:
                url = reverse(url_name)
            print(f"   ✅ {url_name:45} -> {url}")
            working_urls += 1"""
... (tronqué)

# ============================================================
# ORIGINE 29: fix_final_urls.py (2025-11-19)
# ============================================================

#!/usr/bin/env python
import os

def fix_final_urls():
    """Vérifier et corriger les 2 URLs manquantes dans agents/urls.py"""

    file_path = 'agents/urls.py'

    try:
        with open(file_path, 'r') as file:
            content = file.read()

        print("🔍 VÉRIFICATION DES URLs DANS agents/urls.py...")

        # Vérifier la présence des URLs manquantes
        missing_urls = {
            'creer_bon_soin_membre': "path('creer-bon-soin/<int:membre_id>/', views.creer_bon_soin_membre, name='creer_bon_soin_membre')",
            'confirmation_bon_soin': "path('confirmation-bon-soin/<int:bon_id>/', views.confirmation_bon_soin, name='confirmation_bon_soin')"
        }

        found_urls = []
        missing_urls_list = []

        for url_name, url_pattern in missing_urls.items():
            if url_pattern in content:
                found_urls.append(url_name)
                print(f"✅ {url_name} - PRÉSENT")
            else:
                missing_urls_list.append(url_pattern)
                print(f"❌ {url_name} - MANQUANT")

        if not missing_urls_list:
            print("\n🎯 TOUTES LES URLs SONT PRÉSENTES DANS LE FICHIER!")
            return True
        else:
            print(f"\n🔧 AJOUT DES {len(missing_urls_list)} URLs MANQUANTES...")

            # Trouver la section des bons de soin
            section_marker = "# =========================================================================\n# URLs GESTION BONS DE SOIN"
            section_pos = content.find(section_marker)

            if section_pos != -1:
                # Trouver la fin de la section
                end_section_pos = content.find("# =========================================================================\n#", section_pos + 100)

                if end_section_pos == -1:
                    end_section_pos = content.find("]", section_pos)

                # Insérer les URLs manquantes dans la section
                if end_section_pos != -1:
... (tronqué)

# ============================================================
# ORIGINE 30: fix_syntax_error.py (2025-11-19)
# ============================================================

#!/usr/bin/env python
import os

def fix_syntax_error():
    """Corriger l'erreur de syntaxe dans agents/views.py"""

    file_path = 'agents/views.py'

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        print("🔍 RECHERCHE DE L'ERREUR DE SYNTAXE...")

        # Rechercher la ligne problématique
        problematic_lines = []
        for i, line in enumerate(lines, 1):
            if 'python final_validation.py' in line:
                problematic_lines.append((i, line.strip()))
                print(f"❌ Ligne {i}: {line.strip()}")

        if problematic_lines:
            print(f"\n🔧 SUPPRESSION DE {len(problematic_lines)} LIGNE(S) PROBLÉMATIQUE(S)...")

            # Créer un nouveau contenu sans les lignes problématiques
            new_lines = []
            for i, line in enumerate(lines, 1):
                if not any(prob_line[0] == i for prob_line in problematic_lines):
                    new_lines.append(line)
                else:
                    print(f"✅ Supprimé: '{line.strip()}'")

            # Écrire le fichier corrigé
            with open(file_path, 'w') as file:
                file.writelines(new_lines)

            print("\n🎯 ERREUR DE SYNTAXE CORRIGÉE!")
            return True
        else:
            print("✅ Aucune erreur de syntaxe trouvée")
            return True

    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        return False

def verify_fix():
    """Vérifier que la correction a fonctionné"""

    file_path = 'agents/views.py'
... (tronqué)

# ============================================================
# ORIGINE 31: fix_agents_paths.py (2025-11-19)
# ============================================================

# fix_agents_paths.py
import os
import sys
from pathlib import Path

# Chemin correct - le script est dans le dossier projet
BASE_DIR = Path(__file__).resolve().parent
print(f"📁 BASE_DIR: {BASE_DIR}")

def verifier_structure():
    """Vérifie la structure actuelle"""
    print("\n🔍 STRUCTURE ACTUELLE:")

    # Vérifier l'application agents
    agents_app = BASE_DIR / 'agents'
    if agents_app.exists():
        print(f"✅ Application agents trouvée: {agents_app}")
        fichiers = list(agents_app.glob("*.py"))
        print(f"   Fichiers Python: {len(fichiers)}")
    else:
        print("❌ Application agents NON trouvée")
        return False

    # Vérifier les templates agents
    templates_agents = BASE_DIR / 'templates' / 'agents'
    if templates_agents.exists():
        print(f"✅ Templates agents trouvés: {templates_agents}")
        templates = list(templates_agents.glob("*.html"))
        print(f"   Templates HTML: {len(templates)}")
        for t in templates:
            print(f"     - {t.name}")
    else:
        print("❌ Templates agents NON trouvés")
        return False

    return True

def corriger_urls_principales():
    """Corrige les URLs principales"""
    main_urls_path = BASE_DIR / 'mutuelle_core' / 'urls.py'

    if not main_urls_path.exists():
        print(f"❌ Fichier urls.py principal introuvable: {main_urls_path}")
        return False

    try:
        with open(main_urls_path, 'r') as f:
            content = f.read()

        # Vérifier si agents est déjà inclus
... (tronqué)

# ============================================================
# ORIGINE 32: fix_timezone_issues.py (2025-11-19)
# ============================================================

#!/usr/bin/env python
"""
Script de correction automatique des problèmes de timezone
Corrige les datetime.now() en timezone.now() et ajoute les imports manquants
"""

import os
import re
from pathlib import Path

def fix_timezone_in_file(file_path):
    """Corrige les problèmes de timezone dans un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Vérifier si timezone est déjà importé
        needs_timezone_import = 'from django.utils import timezone' not in content

        # Remplacer les patterns problématiques
        replacements = [
            # Pattern 1: datetime.datetime.now()
            (r'datetime\.datetime\.now\(\)', 'timezone.now()'),
            # Pattern 2: datetime.now() (avec import from datetime)
            (r'(?<!\.)datetime\.now\(\)', 'timezone.now()'),
            # Pattern 3: __import__('datetime').datetime.now()
            (r"__import__\('datetime'\)\.datetime\.now\(\)", "timezone.now()"),
        ]

        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)

        # Ajouter l'import timezone si nécessaire et si des corrections ont été faites
        if needs_timezone_import and any(replacement in content for pattern, replacement in replacements):
            # Trouver où ajouter l'import (après les imports Django)
            lines = content.split('\n')
            new_lines = []
            timezone_import_added = False

            for i, line in enumerate(lines):
                new_lines.append(line)

                # Ajouter après les imports Django standards
                if (not timezone_import_added and
                    ('from django.' in line or 'import django' in line) and
                    i + 1 < len(lines) and
                    not lines[i + 1].strip().startswith('from ') and
                    not lines[i + 1].strip().startswith('import ')):
... (tronqué)

