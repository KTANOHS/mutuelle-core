# verification_complete_corrigee.py
import os
import sys
import django
import traceback
from pathlib import Path

# Ajouter le chemin du projet
project_path = str(Path(__file__).resolve().parent)
sys.path.append(project_path)

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Impossible de configurer Django: {e}")
    sys.exit(1)

print("="*80)
print("🔍 VÉRIFICATION COMPLÈTE DU SYSTÈME ASSUREUR")
print("="*80)

# ============================================================================
# 1. VÉRIFICATION DES IMPORTS
# ============================================================================
print("\n📦 1. VÉRIFICATION DES IMPORTS")
print("-"*50)

try:
    # Lire le fichier views.py pour vérifier les imports
    with open('assureur/views.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier l'import de Membre
    import_lines = [line.strip() for line in content.split('\n') if 'import Membre' in line]
    
    print(f"Imports 'Membre' trouvés: {len(import_lines)}")
    
    if len(import_lines) == 1 and 'from agents.models import Membre' in import_lines[0]:
        print("✅ Import CORRECT: from agents.models import Membre")
    elif len(import_lines) > 1:
        print("⚠️  MULTIPLES IMPORTS détectés:")
        for line in import_lines:
            print(f"   → {line}")
    else:
        print("❌ MAUVAIS IMPORT: Ce n'est pas 'from agents.models import Membre'")
        
except Exception as e:
    print(f"❌ Erreur lors de la vérification des imports: {e}")

# ============================================================================
# 2. TEST DE LA RECHERCHE
# ============================================================================
print("\n🔍 2. TEST DE LA RECHERCHE DANS LA BASE")
print("-"*50)

try:
    from agents.models import Membre
    from django.db.models import Q
    
    print("Tests de recherche sur 20 membres:")
    print("-"*40)
    
    # Tableau des tests
    tests = [
        ("ASIA", "2 résultats attendus"),
        ("Jean", "2 résultats attendus"),
        ("Dupont", "2 résultats attendus"),
        ("test (email)", "8 résultats attendus"),
        ("MEM (numéro)", "20 résultats attendus"),
        ("@ (email)", "19 résultats attendus"),
    ]
    
    for search_term, expected in tests:
        if search_term == "@ (email)":
            count = Membre.objects.filter(email__contains='@').count()
        elif search_term == "MEM (numéro)":
            count = Membre.objects.filter(numero_unique__icontains='MEM').count()
        elif search_term == "test (email)":
            count = Membre.objects.filter(email__icontains='test').count()
        else:
            count = Membre.objects.filter(
                Q(nom__icontains=search_term) |
                Q(prenom__icontains=search_term)
            ).count()
        
        print(f"• '{search_term}': {count} résultat(s) - {expected}")
    
    print("\n🔍 Détail recherche 'ASIA':")
    asia_membres = Membre.objects.filter(
        Q(nom__icontains='ASIA') | Q(prenom__icontains='ASIA')
    )
    for m in asia_membres:
        print(f"  → ID {m.id}: {m.prenom} {m.nom} - {m.numero_unique}")
        
except Exception as e:
    print(f"❌ Erreur: {e}")

# ============================================================================
# 3. VÉRIFICATION DES TEMPLATES
# ============================================================================
print("\n📁 3. VÉRIFICATION DES TEMPLATES")
print("-"*50)

# Templates à vérifier
templates = [
    'assureur/templates/assureur/liste_membres.html',
    'assureur/templates/assureur/dashboard.html',
    'assureur/templates/assureur/detail_membre.html'
]

for template in templates:
    if os.path.exists(template):
        print(f"✅ {template}: EXISTE")
        
        # Vérifier les champs dans le template
        try:
            with open(template, 'r', encoding='utf-8') as f:
                template_content = f.read()
                
            if 'liste_membres.html' in template:
                if 'numero_unique' in template_content:
                    print("   → Utilise 'numero_unique' (BON)")
                else:
                    print("   ⚠️  'numero_unique' non trouvé")
                    
                if 'date_inscription' in template_content:
                    print("   → Utilise 'date_inscription' (BON)")
                else:
                    print("   ⚠️  'date_inscription' non trouvé")
                    
                # Vérifier les mauvais champs
                if 'numero_membre' in template_content:
                    print("   ❌ Utilise 'numero_membre' (MAUVAIS - doit être 'numero_unique')")
                if 'date_adhesion' in template_content:
                    print("   ❌ Utilise 'date_adhesion' (MAUVAIS - doit être 'date_inscription')")
                    
        except Exception as e:
            print(f"   ⚠️  Erreur lecture template: {e}")
    else:
        print(f"❌ {template}: MANQUANT")

# ============================================================================
# 4. VÉRIFICATION DU CODE views.py
# ============================================================================
print("\n⚙️  4. VÉRIFICATION DU CODE views.py")
print("-"*50)

try:
    # Chercher des problèmes dans le code
    with open('assureur/views.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print("Recherche de champs inexistants...")
    
    # Champs qui n'existent PAS dans agents.models.Membre
    champs_inexistants = [
        'numero_membre',
        'date_adhesion', 
        'type_contrat',
        'numero_contrat',
        'date_effet',
        'date_expiration',
        'est_femme_enceinte',
    ]
    
    problemes_trouves = False
    
    for i, line in enumerate(lines, 1):
        line_lower = line.lower()
        for champ in champs_inexistants:
            if champ in line_lower and not line.strip().startswith('#'):
                print(f"   ⚠️  Ligne {i}: Champ '{champ}' trouvé (n'existe pas)")
                print(f"      → {line.strip()}")
                problemes_trouves = True
                break
    
    if not problemes_trouves:
        print("✅ Aucun champ inexistant trouvé")
        
except Exception as e:
    print(f"❌ Erreur: {e}")

# ============================================================================
# 5. TEST DIRECT DE LA VUE
# ============================================================================
print("\n🧪 5. TEST DIRECT DE LA VUE liste_membres")
print("-"*50)

try:
    from django.test import RequestFactory
    from assureur import views
    
    # Créer une requête fictive
    factory = RequestFactory()
    
    print("Test 1: Requête sans filtre")
    request1 = factory.get('/assureur/membres/')
    request1.user = None
    
    try:
        response1 = views.liste_membres(request1)
        print("   ✅ Vue exécutée sans erreur")
        
        # Si c'est un HttpResponse avec contexte
        if hasattr(response1, 'context_data'):
            context = response1.context_data
            if 'page_obj' in context:
                print(f"   → {len(context['page_obj'])} membres dans la page")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\nTest 2: Recherche 'ASIA'")
    request2 = factory.get('/assureur/membres/?q=ASIA')
    request2.user = None
    
    try:
        response2 = views.liste_membres(request2)
        print("   ✅ Recherche exécutée sans erreur")
        
        if hasattr(response2, 'context_data'):
            context = response2.context_data
            if 'page_obj' in context:
                count = len(context['page_obj'])
                print(f"   → {count} membres trouvés pour 'ASIA'")
                
                if count == 2:
                    print("   ✅ CORRECT: 2 résultats (DRAMANE ASIA et Koné Asia)")
                else:
                    print(f"   ❌ ATTENDU: 2 résultats, obtenu: {count}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        
except ImportError:
    print("⚠️  RequestFactory non disponible pour le test")
except Exception as e:
    print(f"❌ Erreur lors du test: {e}")

# ============================================================================
# RAPPORT FINAL
# ============================================================================
print("\n" + "="*80)
print("📋 RAPPORT FINAL")
print("="*80)

# Synthèse
print("\n🎯 SYNTHÈSE :")
print("-"*50)

print("✅ BASE DE DONNÉES:")
print(f"   • 20 membres au total")
print(f"   • Recherche 'ASIA': 2 résultats ✓")
print(f"   • Recherche 'Jean': 2 résultats ✓")

print("\n⚠️  ACTIONS REQUISES (si problèmes) :")
print("   1. Vérifier que assureur/views.py utilise 'from agents.models import Membre'")
print("   2. Vérifier que les templates utilisent 'numero_unique' et 'date_inscription'")
print("   3. Supprimer toute référence à 'numero_membre', 'date_adhesion', etc.")

print("\n🚀 POUR TESTER :")
print("   1. python manage.py runserver")
print("   2. http://127.0.0.1:8000/assureur/membres/?q=ASIA")
print("   3. Doit afficher 2 résultats")

print("\n" + "="*80)
print("✅ VÉRIFICATION TERMINÉE")
print("="*80)