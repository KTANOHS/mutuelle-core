"""
FICHIER CONSOLIDÉ: verifier
Catégorie: correction
Fusion de 3 fichiers
Date de consolidation: 2025-12-06 13:55:44
"""

import sys
import os
from pathlib import Path

# =============================================================================
# FICHIERS D'ORIGINE CONSOLIDÉS
# =============================================================================

# ============================================================
# ORIGINE 1: verifier_corrections2.py (2025-11-17)
# ============================================================

# verifier_corrections.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_corrections():
    print("🔍 VÉRIFICATION DES CORRECTIONS APPLIQUÉES")
    print("=" * 50)

    # Vérifier le template
    template_path = 'templates/communication/messagerie.html'
    with open(template_path, 'r') as f:
        template_content = f.read()

    verifs_template = [
        "for conversation in conversations" in template_content,
        "if conversations" in template_content,
        "conversation.participants.all" in template_content
    ]

    print("✅ TEMPLATE:")
    for i, check in enumerate(verifs_template, 1):
        status = "✅" if check else "❌"
        print(f"   {status} Vérification {i}: {'OK' if check else 'NOK'}")

    # Vérifier la vue
    vue_path = 'communication/views.py'
    with open(vue_path, 'r') as f:
        vue_content = f.read()

    verifs_vue = [
        "messages_recents" in vue_content,
        "page_title" in vue_content,
        "total_conversations" in vue_content
    ]

    print("\n✅ VUE:")
    for i, check in enumerate(verifs_vue, 1):
        status = "✅" if check else "❌"
        print(f"   {status} Vérification {i}: {'OK' if check else 'NOK'}")

    if all(verifs_template) and all(verifs_vue):
        print("\n🎉 TOUTES LES CORRECTIONS ONT ÉTÉ APPLIQUÉES AVEC SUCCÈS !")
        print("🌐 Testez maintenant: http://127.0.0.1:8000/communication/")
    else:
        print("\n⚠️  Certaines corrections n'ont pas été appliquées")

if __name__ == "__main__":
... (tronqué)

# ============================================================
# ORIGINE 2: verifier_corrections1.py (2025-11-17)
# ============================================================

# verifier_corrections.py
import os

def verifier_corrections():
    """Vérifier que toutes les corrections ont été appliquées"""

    fichiers = ['communication/views.py', 'agents/views.py']
    problemes_trouves = False

    for fichier in fichiers:
        if os.path.exists(fichier):
            with open(fichier, 'r') as f:
                contenu = f.read()

            if "redirect('communication:liste_messages')" in contenu:
                print(f"❌ Problème trouvé dans {fichier}")
                problemes_trouves = True
            else:
                print(f"✅ {fichier} est correct")

    if not problemes_trouves:
        print("\n🎉 Toutes les corrections ont été appliquées avec succès !")
        print("L'erreur 'liste_messages not found' devrait maintenant être résolue.")
    else:
        print("\n⚠️ Il reste des problèmes à corriger manuellement.")

if __name__ == "__main__":
    verifier_corrections()

# ============================================================
# ORIGINE 3: verifier_correction.py (2025-11-12)
# ============================================================

# verifier_correction.py
import os
import sys
import django
from django.urls import reverse, NoReverseMatch

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/VERIFICATION/projet')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

def verifier_urls():
    print("🔍 VÉRIFICATION DES URLs APRÈS CORRECTION")
    print("=" * 50)

    # URLs à tester
    urls_a_tester = [
        ('agents:dashboard', 'Dashboard principal'),
        ('agents:verification_cotisations', 'Vérification cotisations'),
        ('agents:creer_bon_soin', 'Créer bon de soin'),
        ('agents:historique_bons', 'Historique des bons'),
        ('agents:liste_membres', 'Liste des membres'),
    ]

    print("\n📋 URLs DES AGENTS:")
    print("-" * 40)

    toutes_valides = True
    for nom_url, description in urls_a_tester:
        try:
            url = reverse(nom_url)
            print(f"✅ {description:25} -> {url}")
        except NoReverseMatch as e:
            print(f"❌ {description:25} -> ERREUR: {e}")
            toutes_valides = False

    return toutes_valides

def verifier_template():
    print("\n📄 VÉRIFICATION DU TEMPLATE:")
    print("-" * 40)

    template_path = '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/agents/dashboard.html'

    if not os.path.exists(template_path):
... (tronqué)

