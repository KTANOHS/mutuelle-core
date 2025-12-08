"""
FICHIER CONSOLIDÉ: check
Catégorie: diagnostic
Fusion de 26 fichiers
Date de consolidation: 2025-12-06 13:55:44
"""

import sys
import os
from pathlib import Path

# =============================================================================
# FICHIERS D'ORIGINE CONSOLIDÉS
# =============================================================================

# ============================================================
# ORIGINE 1: check_assureur_decorators.py (2025-12-06)
# ============================================================


#!/usr/bin/env python
import os
import sys

decorators_path = os.path.join(os.getcwd(), 'assureur', 'decorators.py')

if os.path.exists(decorators_path):
    print(f"🔍 Vérification de: {decorators_path}")
    with open(decorators_path, 'r') as f:
        content = f.read()

    print("📄 Contenu du fichier decorators.py:")
    print("-" * 40)
    print(content)

    # Vérifier si assureur_required existe
    if 'def assureur_required' in content:
        print("\n✅ Décorateur assureur_required trouvé")

        # Extraire la fonction
        import re
        pattern = r'def assureur_required.*?\n(?:    .*\n)*'
        match = re.search(pattern, content, re.DOTALL)

        if match:
            print("\n📝 Code de assureur_required:")
            print("-" * 30)
            print(match.group(0))
    else:
        print("\n❌ Décorateur assureur_required NON trouvé!")

        print("\n💡 Création du décorateur manquant...")
        decorator_code = '''
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from core.utils import user_is_assureur

def assureur_required(view_func):
    """
    Décorateur pour restreindre l'accès aux assureurs
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Vous devez être connecté pour accéder à cette page.")
            return redirect('/accounts/login/')

        if user_is_assureur(request.user):
... (tronqué)

# ============================================================
# ORIGINE 2: check_assureur_view.py (2025-12-06)
# ============================================================


#!/usr/bin/env python
import os
import sys

# Vérifier la vue assureur
views_path = os.path.join(os.getcwd(), 'assureur', 'views.py')

if os.path.exists(views_path):
    print(f"🔍 Vérification de: {views_path}")
    with open(views_path, 'r') as f:
        content = f.read()

    # Chercher des problèmes
    problems = []

    # 1. Vérifier si la vue utilise @staff_member_required
    if '@staff_member_required' in content:
        problems.append("La vue utilise @staff_member_required (problème!)")

    # 2. Vérifier si elle utilise @login_required ou @assureur_required
    if '@login_required' not in content and '@assureur_required' not in content:
        problems.append("La vue n'a pas de décorateur de permission")

    # 3. Vérifier le nom de la fonction de vue
    if 'def dashboard' in content or 'def tableau_de_bord' in content:
        print("✅ Vue tableau de bord trouvée")

    if problems:
        print("❌ Problèmes trouvés:")
        for problem in problems:
            print(f"   - {problem}")
    else:
        print("✅ Aucun problème évident trouvé")

    # Afficher les premières lignes de la vue
    print("\n📄 Extrait de la vue assureur:")
    print("-" * 30)
    lines = content.split('\n')[:20]
    for i, line in enumerate(lines):
        print(f"{i+1:3}: {line}")

else:
    print(f"❌ Fichier non trouvé: {views_path}")



# ============================================================
# ORIGINE 3: check_users.py (2025-12-05)
# ============================================================

# Créer un fichier de vérification

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()

from django.contrib.auth.models import User

print("=== VÉRIFICATION DES UTILISATEURS ===")

# Vérifier DOUA
try:
    doua = User.objects.get(username='DOUA')
    print(f"✓ DOUA existe")
    print(f"  Email: {doua.email}")
    print(f"  Groupes: {[g.name for g in doua.groups.all()]}")
except User.DoesNotExist:
    print("✗ DOUA n'existe pas")

# Vérifier admin
try:
    admin = User.objects.get(username='admin')
    print(f"✓ Admin existe")
    print(f"  Email: {admin.email}")
    print(f"  Superuser: {admin.is_superuser}")
except User.DoesNotExist:
    print("✗ Admin n'existe pas")

print("\n=== TOUS LES UTILISATEURS ===")
for user in User.objects.all():
    groups = [g.name for g in user.groups.all()]
    print(f"- {user.username} (Email: {user.email}, Superuser: {user.is_superuser}, Groupes: {groups})")


# ============================================================
# ORIGINE 4: check_cotisation_data.py (2025-12-04)
# ============================================================

# check_cotisation_data.py
import os
import sys
import django
import csv

sys.path.append('/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db import connection

def check_cotisation_data():
    """Vérifie les données dans les champs inutiles"""

    print("🔍 Vérification des données dans les champs problématiques")
    print("="*60)

    with connection.cursor() as cursor:
        # Récupérer les données des champs problématiques
        cursor.execute("""
            SELECT
                id,
                reference,
                membre_id,
                periode,
                montant,
                montant_clinique,
                montant_pharmacie,
                montant_charges_mutuelle,
                statut
            FROM assureur_cotisation
            WHERE montant_clinique != 0
               OR montant_pharmacie != 0
               OR montant_charges_mutuelle != 0
            ORDER BY id
        """)

        rows = cursor.fetchall()

        if not rows:
            print("✅ Aucune donnée dans les champs problématiques")
            return

        print(f"\n📊 {len(rows)} enregistrements avec des données:")
        print("-" * 100)

        total_clinique = 0
        total_pharmacie = 0
        total_charges = 0
... (tronqué)

# ============================================================
# ORIGINE 5: check_models_data.py (2025-12-03)
# ============================================================

# check_models_data.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("="*70)
print("🔍 COMPARAISON DES MODÈLES MEMBRE")
print("="*70)

try:
    from agents.models import Membre as MembreAgents
    print("✅ agents.models.Membre importé")
    count_agents = MembreAgents.objects.count()
    print(f"  Nombre d'objets: {count_agents}")
    if count_agents > 0:
        m = MembreAgents.objects.first()
        print(f"  Exemple: {m.nom} {m.prenom}")
        print(f"  Champs: {[f.name for f in MembreAgents._meta.fields[:5]]}...")
except Exception as e:
    print(f"❌ agents.models.Membre: {e}")

print()

try:
    from assureur.models import Membre as MembreAssureur
    print("✅ assureur.models.Membre importé")
    count_assureur = MembreAssureur.objects.count()
    print(f"  Nombre d'objets: {count_assureur}")
    if count_assureur > 0:
        m = MembreAssureur.objects.first()
        print(f"  Exemple: {m.nom} {m.prenom}")
        print(f"  Champs: {[f.name for f in MembreAssureur._meta.fields[:5]]}...")
except Exception as e:
    print(f"❌ assureur.models.Membre: {e}")

print("\n" + "="*70)

# ============================================================
# ORIGINE 6: check_membres_data1.py (2025-12-03)
# ============================================================

# check_membres_data.py - VERSION CORRIGÉE
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import Membre
from django.db.models import Q  # AJOUTER CET IMPORT

print("="*70)
print("🔍 VÉRIFICATION DES DONNÉES MEMBRES")
print("="*70)

# Compter tous les membres
total = Membre.objects.count()
print(f"Total membres dans la base: {total}")

# Afficher les 5 premiers
print("\n📋 5 premiers membres:")
for membre in Membre.objects.all()[:5]:
    print(f"  • {membre.id}: {membre.nom} {membre.prenom} - {membre.statut} - Tél: {membre.telephone}")

# Vérifier les statuts
print("\n📊 Répartition par statut:")
# Éviter les doublons dans l'affichage
statuts_distincts = set(Membre.objects.values_list('statut', flat=True))
for statut in statuts_distincts:
    count = Membre.objects.filter(statut=statut).count()
    print(f"  • {statut}: {count} membres")

# Tester la recherche
print("\n🔍 Test de recherche:")
search_terms = ['a', 'e', 'i', 'o', 'u']  # Lettres communes
for term in search_terms:
    results = Membre.objects.filter(
        Q(nom__icontains=term) |
        Q(prenom__icontains=term) |
        Q(telephone__icontains=term) |
        Q(email__icontains=term)
    ).count()
    print(f"  Recherche '{term}': {results} résultats")

# Tester les filtres de statut
print("\n🔍 Test des filtres de statut:")
print(f"  Statut 'actif': {Membre.objects.filter(statut='actif').count()} membres")
... (tronqué)

# ============================================================
# ORIGINE 7: check_membres_data.py (2025-12-03)
# ============================================================

# check_membres_data.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import Membre

print("="*70)
print("🔍 VÉRIFICATION DES DONNÉES MEMBRES")
print("="*70)

# Compter tous les membres
total = Membre.objects.count()
print(f"Total membres dans la base: {total}")

# Afficher les 5 premiers
print("\n📋 5 premiers membres:")
for membre in Membre.objects.all()[:5]:
    print(f"  • {membre.id}: {membre.nom} {membre.prenom} - {membre.statut} - Tél: {membre.telephone}")

# Vérifier les statuts
print("\n📊 Répartition par statut:")
for statut in Membre.objects.values_list('statut', flat=True).distinct():
    count = Membre.objects.filter(statut=statut).count()
    print(f"  • {statut}: {count} membres")

# Tester la recherche
print("\n🔍 Test de recherche:")
search_terms = ['a', 'e', 'i', 'o', 'u']  # Lettres communes
for term in search_terms:
    results = Membre.objects.filter(
        Q(nom__icontains=term) |
        Q(prenom__icontains=term) |
        Q(telephone__icontains=term) |
        Q(email__icontains=term)
    ).count()
    print(f"  Recherche '{term}': {results} résultats")

print("\n" + "="*70)

# ============================================================
# ORIGINE 8: check_membre_model.py (2025-12-03)
# ============================================================

# check_membre_model.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import Membre

print("="*70)
print("🔍 VÉRIFICATION DU MODÈLE MEMBRE")
print("="*70)

print("\n📋 TOUS LES CHAMPS DE MEMBRE:")
for field in Membre._meta.fields:
    field_type = field.get_internal_type()
    is_relation = field.is_relation
    print(f"  • {field.name}: {field_type} (relation: {is_relation})")

print("\n🔍 CHAMPS DE RELATION (pour select_related):")
related_fields = []
for field in Membre._meta.fields:
    if field.is_relation:
        related_fields.append(field.name)
        print(f"  • {field.name} → {field.related_model.__name__}")

print(f"\n✅ Choix valides pour select_related: {related_fields}")

print("\n" + "="*70)

# ============================================================
# ORIGINE 9: check_bonsoin_model.py (2025-12-03)
# ============================================================

# check_bonsoin_model.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("="*70)
print("🔍 VÉRIFICATION DÉTAILLÉE DU MODÈLE BONSOIN")
print("="*70)

from agents.models import BonSoin

print("✅ Modèle BonSoin importé avec succès")

# Afficher tous les champs
print("\n📋 TOUS LES CHAMPS DU MODÈLE BONSOIN:")
for field in BonSoin._meta.fields:
    field_type = field.get_internal_type()
    is_required = "REQUIS" if not field.null and not field.blank else "OPTIONNEL"
    print(f"  • {field.name}: {field_type} ({is_required})")

# Vérifier spécifiquement les champs de date
print("\n🔍 CHAMPS DE DATE SPÉCIFIQUEMENT:")
date_fields = [f for f in BonSoin._meta.fields if f.get_internal_type() in ['DateTimeField', 'DateField']]
for field in date_fields:
    print(f"  • {field.name}: {field.get_internal_type()}")

# Vérifier les champs créés/modifiés
print("\n🎯 VÉRIFICATION DES CHAMPS STANDARD:")
date_creation_exists = hasattr(BonSoin, 'date_creation')
created_at_exists = hasattr(BonSoin, 'created_at')
updated_at_exists = hasattr(BonSoin, 'updated_at')

print(f"  date_creation: {'✅ EXISTE' if date_creation_exists else '❌ ABSENT'}")
print(f"  created_at: {'✅ EXISTE' if created_at_exists else '❌ ABSENT'}")
print(f"  updated_at: {'✅ EXISTE' if updated_at_exists else '❌ ABSENT'}")

# Vérifier un exemple de données
print("\n📊 EXEMPLE DE DONNÉES BONSOIN:")
if BonSoin.objects.exists():
    bon = BonSoin.objects.first()
    print(f"  ID: {bon.id}")
    print(f"  Référence: {bon.reference}")
    print(f"  Statut: {bon.statut}")

... (tronqué)

# ============================================================
# ORIGINE 10: check_bon_model.py (2025-12-03)
# ============================================================

# check_bon_model.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("="*70)
print("🔍 VÉRIFICATION DU MODÈLE BON (BonDeSoin)")
print("="*70)

try:
    # Essayer d'importer le modèle Bon (BonDeSoin)
    from agents.models import Bon  # ou assureur.models selon votre structure

    print("✅ Modèle Bon importé avec succès")

    # Afficher les champs
    print("\n📋 CHAMPS DU MODÈLE BON:")
    for field in Bon._meta.fields:
        field_type = field.get_internal_type()
        print(f"  • {field.name}: {field_type}")

    # Vérifier les champs de date
    print("\n🔍 CHAMPS DE DATE:")
    date_fields = [f for f in Bon._meta.fields if f.get_internal_type() in ['DateTimeField', 'DateField']]
    for field in date_fields:
        print(f"  • {field.name}: {field.get_internal_type()}")

    # Vérifier spécifiquement date_creation
    if hasattr(Bon, 'date_creation'):
        print(f"\n✅ Le modèle Bon a un champ 'date_creation'")
        # Vérifier un exemple
        if Bon.objects.exists():
            bon = Bon.objects.first()
            print(f"  Exemple: {bon.date_creation}")
    else:
        print(f"\n❌ Le modèle Bon n'a pas de champ 'date_creation'")

    if hasattr(Bon, 'created_at'):
        print(f"✅ Le modèle Bon a un champ 'created_at'")
    else:
        print(f"❌ Le modèle Bon n'a pas de champ 'created_at'")

except ImportError as e:
    print(f"❌ Impossible d'importer le modèle Bon: {e}")
... (tronqué)

# ============================================================
# ORIGINE 11: check_system.py (2025-12-03)
# ============================================================

# check_system.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Cotisation, Membre

print("="*60)
print("ÉTAT DU SYSTÈME DE COTISATIONS")
print("="*60)

# Compter les membres
membres = Membre.objects.all()
membres_actifs = Membre.objects.filter(statut='actif')
print(f"📊 MEMBRES:")
print(f"   Total: {membres.count()}")
print(f"   Actifs: {membres_actifs.count()}")
print(f"   Inactifs: {membres.filter(statut='inactif').count()}")

# Afficher les membres actifs
print(f"\n👥 LISTE DES MEMBRES ACTIFS:")
for m in membres_actifs:
    print(f"   - {m.numero_membre}: {m.nom_complet} ({m.get_type_membre_display()})")

# Compter les cotisations
cotisations = Cotisation.objects.all()
print(f"\n💰 COTISATIONS:")
print(f"   Total: {cotisations.count()}")

# Par période
periodes = cotisations.values_list('periode', flat=True).distinct()
print(f"   Périodes: {list(periodes)}")

# Détail par période
print(f"\n📅 DÉTAIL PAR PÉRIODE:")
for periode in periodes:
    nb = cotisations.filter(periode=periode).count()
    montant_total = sum(c.montant for c in cotisations.filter(periode=periode) if c.montant)
    print(f"   {periode}: {nb} cotisations, {montant_total} FCFA")

print("\n" + "="*60)
print("VÉRIFICATION TERMINÉE")
print("="*60)

# ============================================================
# ORIGINE 12: check_choices.py (2025-12-03)
# ============================================================

# check_choices.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Cotisation

print("=== CHOIX DU MODÈLE COTISATION ===")
print(f"\n1. Type de cotisation:")
field = Cotisation._meta.get_field('type_cotisation')
if hasattr(field, 'choices') and field.choices:
    for value, label in field.choices:
        print(f"   - '{value}': {label}")
else:
    print("   Pas de choix définis")

print(f"\n2. Statut:")
field = Cotisation._meta.get_field('statut')
if hasattr(field, 'choices') and field.choices:
    for value, label in field.choices:
        print(f"   - '{value}': {label}")
else:
    print("   Pas de choix définis")

print(f"\n3. Champs obligatoires (non null):")
for field in Cotisation._meta.fields:
    if not field.null and not field.blank and field.name != 'id':
        print(f"   - {field.name}")

# ============================================================
# ORIGINE 13: check_communication.sh (2025-12-02)
# ============================================================

#!/bin/bash
echo "🔄 Vérification rapide du module communication..."
source venv/bin/activate

echo "1. Vérification des modèles..."
python -c "
from communication.models import Message, Conversation
print(f'Messages: {Message.objects.count()}')
print(f'Conversations: {Conversation.objects.count()}')
"

echo "2. Test API..."
curl -s http://127.0.0.1:8000/communication/api/public/test/ | grep -o '"status":".*"' || echo "API non accessible"

echo "3. Nettoyage des sessions..."
python manage.py clearsessions --dry-run | grep "sessions" || echo "Aucune session à nettoyer"

echo "✅ Vérification terminée"

# ============================================================
# ORIGINE 14: check_projet.sh (2025-12-02)
# ============================================================

#!/bin/bash
# Script de diagnostic rapide pour projet Django

echo "🔍 DIAGNOSTIC RAPIDE DU PROJET"
echo "================================"

# 1. Vérifier l'environnement
echo -e "\n1. Environnement Python:"
python --version
pip --version

# 2. Vérifier les dépendances
echo -e "\n2. Dépendances installées:"
pip list | grep -E "(Django|django|psycopg|mysql|Pillow)"

# 3. Vérifier la santé Django
echo -e "\n3. Vérification Django:"
python manage.py check

# 4. Vérifier les migrations
echo -e "\n4. État des migrations:"
python manage.py showmigrations | grep -E "\[ \]|\[X\]" | head -20

# 5. Vérifier la base de données
echo -e "\n5. Connexion base de données:"
python manage.py dbshell -- -c "SELECT 1;" 2>/dev/null && echo "✅ DB Connectée" || echo "❌ DB Erreur"

# 6. Vérifier les URLs
echo -e "\n6. URLs disponibles:"
python manage.py show_urls | head -10

# 7. Vérifier les permissions
echo -e "\n7. Permissions des fichiers:"
ls -la manage.py
ls -la mutuelle_core/settings.py

# 8. Vérifier l'espace disque
echo -e "\n8. Espace disque:"
df -h . | tail -1

# 9. Vérifier la mémoire
echo -e "\n9. Utilisation mémoire:"
free -h | head -2

# 10. Vérifier les logs d'erreur
echo -e "\n10. Dernières erreurs (logs):"
find . -name "*.log" -type f -exec tail -5 {} \; 2>/dev/null | head -20

echo -e "\n✅ Diagnostic terminé!"

# ============================================================
# ORIGINE 15: check_template_name.py (2025-12-01)
# ============================================================

#!/usr/bin/env python3
import os
import sys

views_path = "pharmacien/views.py"

with open(views_path, 'r') as f:
    content = f.read()

# Chercher le template utilisé dans la vue historique_validation
import re

# Chercher le render avec le template
pattern = r'def historique_validation\(request\).*?render\(request,\s*[\'"](.*?)[\'"]'
match = re.search(pattern, content, re.DOTALL)

if match:
    template_name = match.group(1)
    print(f"Template utilisé dans la vue: '{template_name}'")
else:
    print("Template non trouvé dans la vue")

# Vérifier aussi le template minimal
pattern2 = r'render\(request,\s*[\'"]pharmacien/historique'
if re.search(pattern2, content):
    print("La vue utilise 'pharmacien/historique'")

# ============================================================
# ORIGINE 16: check_template.py (2025-12-01)
# ============================================================

#!/usr/bin/env python3
import os

template_path = "templates/pharmacien/historique_validation.html"

if not os.path.exists(template_path):
    print(f"❌ Template non trouvé: {template_path}")
    exit(1)

with open(template_path, 'r') as f:
    content = f.read()

print(f"✓ Template trouvé: {template_path}")
print(f"Taille: {len(content)} caractères, {len(content.split('\\n'))} lignes")

# Vérifications de base
checks = [
    ('{% extends', 'Extends présent'),
    ('{% block content', 'Block content présent'),
    ('{% for', 'Boucle for présente'),
    ('{{', 'Variables Django présentes'),
]

print("\n=== VÉRIFICATIONS DU TEMPLATE ===")
for pattern, description in checks:
    if pattern in content:
        print(f"  ✓ {description}")
    else:
        print(f"  ⚠ {description} - Non trouvé")

# Vérifier les erreurs courantes
print("\n=== RECHERCHE D'ERREURS COURANTES ===")
error_patterns = [
    ('{% endblock %}', 'endblock correct'),
    ('{% endfor %}', 'endfor correct'),
    ('{% endif %}', 'endif correct'),
]

for pattern, description in error_patterns:
    if content.count('{% for') != content.count('{% endfor %}'):
        print("  ⚠ Nombre de 'for' et 'endfor' ne correspond pas")
    if content.count('{% if') != content.count('{% endif %}'):
        print("  ⚠ Nombre de 'if' et 'endif' ne correspond pas")

print("\n=== EXTRACTION DE 10 LIGNES AUTOUR D'UNE ÉVENTUELLE ERREUR ===")
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'erreur' in line.lower() or 'error' in line.lower():
        start = max(0, i-5)
        end = min(len(lines), i+6)
... (tronqué)

# ============================================================
# ORIGINE 17: check_current_view.py (2025-12-01)
# ============================================================

#!/usr/bin/env python3
import os
import sys

views_path = "pharmacien/views.py"

# Trouver et afficher la fonction historique_validation
with open(views_path, 'r') as f:
    lines = f.readlines()

print("=== CONTENU DE historique_validation ===")
in_function = False
function_lines = []

for i, line in enumerate(lines):
    if '@login_required' in line and i+2 < len(lines) and 'historique_validation' in lines[i+2]:
        in_function = True
    if in_function:
        function_lines.append(line)
        if line.strip().startswith('def ') and 'historique_validation' not in line and len(function_lines) > 1:
            break

for line in function_lines:
    print(line.rstrip())

print("\n=== VÉRIFICATION DES IMPORTS ===")
for i, line in enumerate(lines[:50]):
    if 'import' in line:
        print(f"{i+1}: {line.rstrip()}")

# ============================================================
# ORIGINE 18: check_models.py (2025-12-01)
# ============================================================

#!/usr/bin/env python3
import os
import sys
import django

sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()

    # Vérifier la structure des modèles
    from pharmacien.models import OrdonnancePharmacien, Pharmacien

    print("=== STRUCTURE DU MODÈLE OrdonnancePharmacien ===")
    print("Champs disponibles:")
    for field in OrdonnancePharmacien._meta.fields:
        print(f"  - {field.name:25} ({field.get_internal_type()})")

    print("\n=== STRUCTURE DU MODÈLE Pharmacien ===")
    print("Champs disponibles:")
    for field in Pharmacien._meta.fields:
        print(f"  - {field.name:25} ({field.get_internal_type()})")

    print("\n=== RELATIONS ===")
    print("1. OrdonnancePharmacien.pharmacien_validateur ->",
          OrdonnancePharmacien._meta.get_field('pharmacien_validateur').related_model.__name__)

    print("2. Pharmacien.user ->",
          Pharmacien._meta.get_field('user').related_model.__name__)

    print("\n=== CONSEIL POUR LE FILTRE ===")
    print("Pour filtrer les OrdonnancePharmacien d'un utilisateur:")
    print("1. D'abord obtenir son profil Pharmacien:")
    print("   pharmacien = Pharmacien.objects.get(user=request.user)")
    print("2. Puis filtrer:")
    print("   OrdonnancePharmacien.objects.filter(pharmacien_validateur=pharmacien)")

except Exception as e:
    print(f"Erreur: {e}")
    import traceback
    traceback.print_exc()

# ============================================================
# ORIGINE 19: check_ordonnance_sync.py (2025-11-30)
# ============================================================

# check_ordonnance_sync.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyze_ordonnance_flow():
    """Analyser le flux ordonnances médecin → pharmacien"""
    print("🔍 ANALYSE FLUX ORDONNANCES MÉDECIN→PHARMACIEN")
    print("=" * 60)

    from django.db import connection

    # 1. Vérifier l'existence des tables
    print("\n📦 TABLES ORDONNANCES DANS LE SYSTÈME")
    print("-" * 40)

    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%ordonnance%'")
        tables_ordonnance = [row[0] for row in cursor.fetchall()]

        print("Tables ordonnances trouvées:")
        for table in tables_ordonnance:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   📋 {table}: {count} enregistrements")

    # 2. Analyser la structure des tables d'ordonnances
    print("\n🏗️  STRUCTURE DES TABLES ORDONNANCES")
    print("-" * 40)

    tables_to_analyze = ['medecin_ordonnance', 'pharmacien_ordonnance', 'ordonnance_medicament']

    for table in tables_to_analyze:
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                print(f"\n📊 {table}:")
                for col in columns[:8]:  # Afficher 8 premières colonnes
                    print(f"   {col[1]} ({col[2]})")
        except Exception as e:
            print(f"❌ {table}: Table non accessible - {e}")

    # 3. Vérifier les relations entre médecins et pharmaciens
    print("\n🔗 RELATIONS MÉDECIN-PHARMACIEN")
    print("-" * 40)

    with connection.cursor() as cursor:
        # Vérifier si les ordonnances médecins sont liées aux pharmaciens
... (tronqué)

# ============================================================
# ORIGINE 20: check_member_sync.py (2025-11-30)
# ============================================================

# check_member_sync.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyze_member_sync():
    """Analyser la synchronisation des membres entre tous les acteurs"""
    print("🔍 ANALYSE COMPLÈTE SYNCHRONISATION MEMBRES")
    print("=" * 60)

    from django.db import connection

    # 1. Vérifier tous les modèles Membre dans le système
    print("\n📦 MODÈLES MEMBRE DANS LE SYSTÈME")
    print("-" * 40)

    from django.apps import apps
    membre_models = []
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            if 'membre' in model.__name__.lower():
                membre_models.append(f"{app_config.name}.{model.__name__}")

    print("Modèles trouvés:")
    for model in membre_models:
        print(f"   📋 {model}")

    # 2. Analyser les tables de membres
    print("\n🗃️  TABLES MEMBRE DANS LA BASE")
    print("-" * 40)

    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%membre%'")
        tables = [row[0] for row in cursor.fetchall()]

        for table in tables:
            print(f"\n📊 Table: {table}")
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   👥 Nombre d'enregistrements: {count}")

            # Afficher quelques colonnes
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cursor.fetchall()[:5]]  # 5 premières colonnes
            print(f"   📋 Colonnes: {', '.join(columns)}...")

    # 3. Vérifier la cohérence des données
    print("\n🔗 COHÉRENCE DES DONNÉES")
    print("-" * 40)
... (tronqué)

# ============================================================
# ORIGINE 21: check_cotisation_sync.py (2025-11-30)
# ============================================================

# check_cotisation_sync.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyze_cotisation_sync():
    """Analyser la synchronisation assureur/agent pour les cotisations"""
    print("🔍 ANALYSE DE LA SYNCHRONISATION ASSUREUR-AGENT")
    print("=" * 60)

    # Vérifier les modèles existants
    from django.apps import apps

    print("\n📦 MODÈLES EXISTANTS:")
    models_list = []
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            models_list.append(f"{app_config.name}.{model.__name__}")

    # Filtrer les modèles liés aux cotisations
    cotisation_models = [m for m in models_list if 'cotisation' in m.lower()]
    assurance_models = [m for m in models_list if 'assur' in m.lower()]
    agent_models = [m for m in models_list if 'agent' in m.lower()]

    print("📋 Modèles cotisation:", cotisation_models)
    print("📋 Modèles assurance:", assurance_models)
    print("📋 Modèles agent:", agent_models)

    # Vérifier la structure spécifique
    print("\n🔄 FLUX COTISATIONS:")

    try:
        from assureur.models import Cotisation
        print("✅ Modèle Cotisation trouvé dans assureur")

        # Analyser les champs
        fields = [f.name for f in Cotisation._meta.get_fields()]
        print(f"   Champs: {', '.join(fields)}")

    except ImportError:
        print("❌ Modèle Cotisation non trouvé dans assureur")

    try:
        from agents.models import VerificationCotisation
        print("✅ Modèle VerificationCotisation trouvé dans agents")

        # Analyser les champs
        fields = [f.name for f in VerificationCotisation._meta.get_fields()]
... (tronqué)

# ============================================================
# ORIGINE 22: check_imports.py (2025-11-30)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT D'ANALYSE COMPLÈTE POUR DÉTECTER LES ERREURS D'IMPORT
Exécutez: python check_imports.py
"""

import os
import sys
import django
import importlib
import inspect
from pathlib import Path
from django.apps import apps
from django.conf import settings

# Ajouter le répertoire du projet au path Python
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_django():
    """Configurer l'environnement Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    django.setup()

def check_settings():
    """Vérifier la configuration des settings"""
    print("=" * 80)
    print("🔧 ANALYSE DE LA CONFIGURATION DJANGO")
    print("=" * 80)

    issues = []

    # Vérifier les apps installées
    print("\n📋 APPLICATIONS INSTALLÉES:")
    for app in settings.INSTALLED_APPS:
        print(f"  ✅ {app}")

        # Vérifier si l'app existe
        try:
            importlib.import_module(app)
        except ImportError as e:
            issues.append(f"❌ App '{app}' - ImportError: {e}")
            print(f"  ❌ {app} - ERREUR: {e}")

    # Vérifier les templates
    print(f"\n📁 TEMPLATES DIRS: {settings.TEMPLATES[0]['DIRS']}")

    # Vérifier les static files
    print(f"📁 STATIC DIRS: {settings.STATICFILES_DIRS}")

... (tronqué)

# ============================================================
# ORIGINE 23: check_urls1.py (2025-11-19)
# ============================================================

# check_urls.py
import os
import django
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_urls_essentielles():
    urls_essentielles = [
        'communication:liste_notifications',
        'medecin:dashboard_medecin',
        'communication:messagerie',
    ]

    print("🔍 VÉRIFICATION DES URLS ESSENTIELLES")
    print("=" * 50)

    for url_name in urls_essentielles:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name:40} -> {url}")
        except Exception as e:
            print(f"❌ {url_name:40} -> ERREUR: {e}")

if __name__ == "__main__":
    verifier_urls_essentielles()

# ============================================================
# ORIGINE 24: check_templates.py (2025-11-19)
# ============================================================

#!/usr/bin/env python3
"""
Script de mise à jour automatique des templates
VERSION CORRIGÉE - Détection automatique du dossier templates
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
from django.utils import timezone

class TemplateUpdater:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.templates_dir = self.find_templates_directory()
        self.backup_dir = self.project_root / 'templates_backup'
        self.changes_log = []

        # Mapping des remplacements
        self.replacements = {
            'ordonnance.numero': 'ordonnance.ordonnance_medecin.numero',
            'ordonnance.patient': 'ordonnance.ordonnance_medecin.patient',
            'ordonnance.medecin': 'ordonnance.ordonnance_medecin.medecin',
            'ordonnance.date_prescription': 'ordonnance.ordonnance_medecin.date_prescription',
            'ordonnance.date_expiration': 'ordonnance.ordonnance_medecin.date_expiration',
            'ordonnance.diagnostic': 'ordonnance.ordonnance_medecin.diagnostic',
            'ordonnance.medicaments': 'ordonnance.ordonnance_medecin.medicaments',
            'ordonnance.posologie': 'ordonnance.ordonnance_medecin.posologie',
            'ordonnance.duree_traitement': 'ordonnance.ordonnance_medecin.duree_traitement',
            'ordonnance.bon_de_soin': 'ordonnance.bon_prise_charge',
        }

    def find_templates_directory(self):
        """Trouve automatiquement le dossier templates"""
        # Essayer différents emplacements possibles
        possible_locations = [
            self.project_root / 'templates',
            self.project_root / 'mutuelle_core' / 'templates',
            self.project_root / '..' / 'templates',
            self.project_root / 'src' / 'templates',
        ]

        for location in possible_locations:
            absolute_path = location.resolve()
            if absolute_path.exists() and absolute_path.is_dir():
                print(f"✅ Dossier templates trouvé: {absolute_path}")
                return absolute_path

... (tronqué)

# ============================================================
# ORIGINE 25: check_timezone_usage.py (2025-11-19)
# ============================================================

#!/usr/bin/env python
"""
Script de vérification de l'utilisation correcte de timezone dans un projet Django
Vérifie et corrige les utilisations de datetime.now() non sécurisées
"""

import os
import re
import ast
import argparse
from pathlib import Path

class TimezoneChecker:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.issues = []
        self.files_checked = 0

    def check_file(self, file_path):
        """Vérifie un fichier Python pour les problèmes de timezone"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Ignorer les fichiers de migrations et venv
            if 'migrations' in str(file_path) or 'venv' in str(file_path):
                return

            self.files_checked += 1
            lines = content.split('\n')

            # Vérifier les patterns problématiques
            datetime_patterns = [
                (r'datetime\.datetime\.now\(\)', 'datetime.datetime.now()'),
                (r'datetime\.now\(\)', 'datetime.now()'),
                (r'from datetime import datetime', 'import datetime incorrect'),
                (r'import datetime', 'import datetime générique')
            ]

            for i, line in enumerate(lines, 1):
                for pattern, issue_type in datetime_patterns:
                    if re.search(pattern, line) and not line.strip().startswith('#'):
                        # Vérifier si timezone est déjà importé dans le fichier
                        has_timezone_import = any(
                            'from django.utils import timezone' in l or
                            'import timezone' in l
                            for l in lines
                        )

                        self.issues.append({
... (tronqué)

# ============================================================
# ORIGINE 26: check_admin_issues.py (2025-11-18)
# ============================================================

# check_admin_issues.py
import os
import sys
import django
from django.conf import settings

# Configuration Django minimale
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.admin.sites import site

def check_admin_issues():
    """Vérifie tous les ModelAdmin pour des problèmes d'actions"""
    print("🔍 Diagnostic des problèmes Admin...")

    for model, admin_class in site._registry.items():
        admin_instance = admin_class(model, site)

        # Vérifier l'attribut actions
        actions = getattr(admin_instance, 'actions', None)

        if actions is not None:
            if callable(actions):
                print(f"❌ PROBLÈME: {admin_class.__module__}.{admin_class.__name__} - actions est une méthode")
            elif isinstance(actions, str):
                print(f"❌ PROBLÈME: {admin_class.__module__}.{admin_class.__name__} - actions est un string")
            elif not isinstance(actions, (list, tuple)):
                print(f"❌ PROBLÈME: {admin_class.__module__}.{admin_class.__name__} - actions a un type invalide: {type(actions)}")
            else:
                print(f"✅ OK: {admin_class.__module__}.{admin_class.__name__}")

if __name__ == "__main__":
    check_admin_issues()

