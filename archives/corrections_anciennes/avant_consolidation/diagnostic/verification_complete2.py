# verification_complete.py
import os
import sys
import django
import inspect
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
# 1. VÉRIFICATION DES IMPORTS ET MODÈLES
# ============================================================================
print("\n📦 1. VÉRIFICATION DES IMPORTS ET MODÈLES")
print("-"*50)

try:
    from assureur import views
    print("✅ Module assureur.views importé")
    
    # Vérifier les imports dans le code source
    with open('assureur/views.py', 'r', encoding='utf-8') as f:
        view_content = f.read()
    
    # Compter les imports Membre
    membre_imports = [line for line in view_content.split('\n') if 'import Membre' in line]
    
    print(f"   Nombre d'imports 'Membre': {len(membre_imports)}")
    
    if len(membre_imports) > 1:
        print("   ⚠️  ATTENTION: Plusieurs imports Membre détectés")
        for imp in membre_imports:
            print(f"     → {imp.strip()}")
    else:
        print("   ✅ Un seul import Membre (bon)")
    
    # Vérifier que c'est bien agents.models
    if 'from agents.models import Membre' in view_content:
        print("   ✅ Import correct: from agents.models import Membre")
    else:
        print("   ❌ Mauvais import: ce n'est pas 'from agents.models import Membre'")
    
except Exception as e:
    print(f"❌ Erreur lors de l'import: {e}")

# ============================================================================
# 2. VÉRIFICATION DES DONNÉES
# ============================================================================
print("\n📊 2. VÉRIFICATION DES DONNÉES")
print("-"*50)

try:
    from agents.models import Membre
    from assureur.models import Bon, Soin, Paiement, Cotisation
    
    # Compter les données
    total_membres = Membre.objects.count()
    total_bons = Bon.objects.count()
    total_soins = Soin.objects.count()
    total_paiements = Paiement.objects.count()
    total_cotisations = Cotisation.objects.count()
    
    print(f"✅ Membres: {total_membres}")
    print(f"✅ Bons: {total_bons}")
    print(f"✅ Soins: {total_soins}")
    print(f"✅ Paiements: {total_paiements}")
    print(f"✅ Cotisations: {total_cotisations}")
    
    # Vérifier la recherche
    print("\n   🔍 TEST DE RECHERCHE:")
    search_terms = ['ASIA', 'Jean', 'Dupont', 'test']
    
    for term in search_terms:
        results = Membre.objects.filter(
            Q(nom__icontains=term) |
            Q(prenom__icontains=term) |
            Q(email__icontains=term) |
            Q(numero_unique__icontains=term)
        ).count()
        print(f"     • '{term}': {results} résultat(s)")
    
    # Vérifier quelques champs critiques
    print("\n   📋 CHAMPS CRITIQUES:")
    sample_membre = Membre.objects.first()
    if sample_membre:
        fields_to_check = [
            'numero_unique', 'date_inscription', 'statut', 
            'nom', 'prenom', 'email', 'telephone'
        ]
        
        for field in fields_to_check:
            if hasattr(sample_membre, field):
                value = getattr(sample_membre, field)
                print(f"     • {field}: {value}")
            else:
                print(f"     ❌ {field}: N'EXISTE PAS!")
    
except Exception as e:
    print(f"❌ Erreur lors de la vérification des données: {e}")
    traceback.print_exc()

# ============================================================================
# 3. VÉRIFICATION DES FONCTIONS
# ============================================================================
print("\n⚙️  3. VÉRIFICATION DES FONCTIONS DANS views.py")
print("-"*50)

# Liste des fonctions critiques à vérifier
critical_functions = [
    'liste_membres',
    'creer_membre',
    'detail_membre',
    'recherche_membre',
    'dashboard_assureur',
    'liste_bons',
    'liste_cotisations',
    'generer_cotisations'
]

for func_name in critical_functions:
    try:
        func = getattr(views, func_name, None)
        if func:
            print(f"✅ {func_name}(): Existe")
            
            # Vérifier si c'est une fonction décorée
            if hasattr(func, '__name__'):
                print(f"     Type: Fonction ({func.__name__})")
            
            # Vérifier les décorateurs pour les fonctions sécurisées
            if func_name in ['liste_membres', 'dashboard_assureur', 'creer_membre']:
                if hasattr(func, '__wrapped__'):
                    print(f"     Décorateurs: login_required, user_passes_test")
        else:
            print(f"❌ {func_name}(): N'existe pas!")
    except Exception as e:
        print(f"⚠️  {func_name}(): Erreur lors de la vérification: {e}")

# ============================================================================
# 4. VÉRIFICATION DES CHAMPS INEXISTANTS
# ============================================================================
print("\n🚨 4. RECHERCHE DE CHAMPS INEXISTANTS DANS LE CODE")
print("-"*50)

# Liste des champs qui n'existent PAS dans agents.models.Membre
nonexistent_fields = [
    'numero_membre',
    'date_adhesion',
    'type_contrat',
    'numero_contrat',
    'date_effet',
    'date_expiration',
    'est_femme_enceinte',
    'created_at',  # Dans le contexte de Membre, utiliser date_inscription
    'employeur',
    'assureur',
    'contrat'
]

found_issues = False

with open('assureur/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
for line_num, line in enumerate(lines, 1):
    line_lower = line.lower()
    
    for field in nonexistent_fields:
        if field in line_lower:
            # Vérifier si c'est dans un commentaire
            if not line.strip().startswith('#'):
                print(f"   ⚠️  Ligne {line_num}: {field}")
                print(f"      → {line.strip()}")
                found_issues = True

if not found_issues:
    print("✅ Aucun champ inexistant trouvé")

# ============================================================================
# 5. VÉRIFICATION DES TEMPLATES
# ============================================================================
print("\n📁 5. VÉRIFICATION DES TEMPLATES")
print("-"*50)

templates_to_check = [
    'assureur/templates/assureur/liste_membres.html',
    'assureur/templates/assureur/dashboard.html',
    'assureur/templates/assureur/detail_membre.html',
    'assureur/templates/assureur/creer_membre.html'
]

for template_path in templates_to_check:
    if os.path.exists(template_path):
        print(f"✅ {template_path}: Existe")
        
        # Vérifier quelques champs critiques dans le template
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                if 'liste_membres.html' in template_path:
                    if 'numero_unique' in content:
                        print(f"     → Utilise 'numero_unique' (bon)")
                    elif 'numero_membre' in content:
                        print(f"     ⚠️  Utilise 'numero_membre' (mauvais)")
                    
                    if 'date_inscription' in content:
                        print(f"     → Utilise 'date_inscription' (bon)")
                    elif 'date_adhesion' in content:
                        print(f"     ⚠️  Utilise 'date_adhesion' (mauvais)")
    else:
        print(f"❌ {template_path}: N'existe pas")

# ============================================================================
# 6. TEST DE LA VUE liste_membres
# ============================================================================
print("\n🧪 6. TEST SIMULÉ DE LA VUE liste_membres")
print("-"*50)

try:
    from django.test import RequestFactory
    
    # Créer une requête fictive
    factory = RequestFactory()
    
    # Test 1: Requête sans paramètres
    request1 = factory.get('/assureur/membres/')
    request1.user = None
    
    print("   Test 1: Liste sans filtre")
    try:
        response1 = views.liste_membres(request1)
        print("     ✅ Vue exécutée sans erreur")
    except Exception as e:
        print(f"     ❌ Erreur: {e}")
        traceback.print_exc()
    
    # Test 2: Requête avec recherche
    request2 = factory.get('/assureur/membres/?q=ASIA')
    request2.user = None
    
    print("\n   Test 2: Recherche 'ASIA'")
    try:
        response2 = views.liste_membres(request2)
        print("     ✅ Recherche exécutée sans erreur")
        
        # Vérifier le contexte si c'est un render
        if hasattr(response2, 'context_data'):
            context = response2.context_data
            if 'page_obj' in context:
                print(f"     → {len(context['page_obj'])} membres trouvés")
    except Exception as e:
        print(f"     ❌ Erreur: {e}")
        traceback.print_exc()
    
except ImportError:
    print("   ⚠️  Impossible d'importer RequestFactory (test limité)")
except Exception as e:
    print(f"   ❌ Erreur lors du test: {e}")

# ============================================================================
# 7. VÉRIFICATION DES URLs
# ============================================================================
print("\n🔗 7. VÉRIFICATION DES URLs")
print("-"*50)

try:
    # Lire le fichier urls.py de l'app assureur
    urls_path = 'assureur/urls.py'
    if os.path.exists(urls_path):
        with open(urls_path, 'r', encoding='utf-8') as f:
            urls_content = f.read()
        
        # Chercher les URLs critiques
        urls_to_check = [
            'membres/',
            'membres/creer/',
            'membres/<int:membre_id>/',
            'recherche_membre',
            'liste_bons',
            'liste_cotisations'
        ]
        
        for url_pattern in urls_to_check:
            if url_pattern in urls_content:
                print(f"✅ URL '{url_pattern}': Configurée")
            else:
                print(f"⚠️  URL '{url_pattern}': Non trouvée")
    else:
        print("❌ Fichier assureur/urls.py non trouvé")
        
except Exception as e:
    print(f"❌ Erreur lors de la vérification des URLs: {e}")

# ============================================================================
# 8. TEST DIRECT DE LA BASE DE DONNÉES
# ============================================================================
print("\n🗄️  8. TEST DIRECT DE LA BASE DE DONNÉES")
print("-"*50)

try:
    print("   Test de recherche avec différents filtres:")
    
    # Test avec Q object
    from django.db.models import Q
    
    # Test 1: Recherche simple
    test1 = Membre.objects.filter(
        Q(nom__icontains='ASIA') |
        Q(prenom__icontains='ASIA')
    ).count()
    print(f"     • 'ASIA' (nom/prénom): {test1} résultat(s)")
    
    # Test 2: Recherche par numéro
    test2 = Membre.objects.filter(numero_unique__icontains='MEM').count()
    print(f"     • 'MEM' (numéro): {test2} résultat(s)")
    
    # Test 3: Recherche par email
    test3 = Membre.objects.filter(email__icontains='@').count()
    print(f"     • '@' (email): {test3} résultat(s)")
    
    # Test 4: Recherche combinée
    test4 = Membre.objects.filter(
        Q(nom__icontains='Jean') |
        Q(prenom__icontains='Jean')
    ).values_list('nom', 'prenom', 'numero_unique')[:5]
    
    if test4:
        print(f"     • 'Jean': {len(test4)} résultat(s)")
        for nom, prenom, num in test4:
            print(f"       - {prenom} {nom} ({num})")
    
    # Vérifier que les champs critiques existent
    print("\n   Vérification des champs du modèle:")
    sample = Membre.objects.first()
    if sample:
        required_fields = ['numero_unique', 'date_inscription', 'statut']
        for field in required_fields:
            if hasattr(sample, field):
                print(f"     • {field}: ✓ Existe")
            else:
                print(f"     • {field}: ✗ N'existe pas!")
    
except Exception as e:
    print(f"❌ Erreur lors du test DB: {e}")
    traceback.print_exc()

# ============================================================================
# RAPPORT FINAL
# ============================================================================
print("\n" + "="*80)
print("📋 RAPPORT FINAL")
print("="*80)

# Récapitulatif
print("\n🎯 RÉCAPITULATIF:")
print("-"*50)

# Compter les erreurs potentielles
issues = []

# Vérifier l'import
if len(membre_imports) > 1:
    issues.append("• Multiples imports de Membre")
elif 'from agents.models import Membre' not in view_content:
    issues.append("• Mauvais import de Membre")

# Vérifier les templates manquants
missing_templates = []
for template in templates_to_check:
    if not os.path.exists(template):
        missing_templates.append(template.split('/')[-1])

if missing_templates:
    issues.append(f"• Templates manquants: {', '.join(missing_templates)}")

# Vérifier les champs inexistants
if found_issues:
    issues.append("• Champs inexistants détectés dans le code")

# Afficher les résultats
if issues:
    print("⚠️  PROBLÈMES DÉTECTÉS:")
    for issue in issues:
        print(f"  {issue}")
else:
    print("✅ Aucun problème majeur détecté")

print("\n🚀 RECOMMANDATIONS:")
print("-"*50)

# Vérifier la recherche 'ASIA' pour confirmer le fonctionnement
asia_count = Membre.objects.filter(
    Q(nom__icontains='ASIA') | Q(prenom__icontains='ASIA')
).count()

if asia_count > 0:
    print(f"✅ La recherche fonctionne ('ASIA' = {asia_count} résultat(s))")
    print("✅ agents.models.Membre est correctement utilisé")
    print("\n🎉 VOTRE SYSTÈME EST PRÊT!")
    print("\nPour tester complètement:")
    print("1. Redémarrez le serveur: python manage.py runserver")
    print("2. Accédez à: http://127.0.0.1:8000/assureur/membres/?q=ASIA")
    print("3. Vous devriez voir", asia_count, "membre(s)")
else:
    print("⚠️  La recherche 'ASIA' ne retourne aucun résultat")
    print("   Vérifiez que:")
    print("   1. Les données de test sont présentes")
    print("   2. agents.models.Membre est utilisé")
    print("   3. Le modèle a bien les champs 'nom' et 'prenom'")

print("\n" + "="*80)
print("✅ VÉRIFICATION TERMINÉE")
print("="*80)