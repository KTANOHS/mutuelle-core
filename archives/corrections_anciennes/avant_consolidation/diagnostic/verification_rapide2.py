# verification_rapide.py
import os
import sys
import django

# Configuration Django
projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("="*70)
print("🔍 VÉRIFICATION RAPIDE - LISTE DES MEMBRES")
print("="*70)

# 1. Vérifier l'import
print("\n1. IMPORT DE MEMBRE DANS assureur/views.py:")
try:
    with open('assureur/views.py', 'r') as f:
        content = f.read()
    
    found = False
    for line in content.split('\n'):
        if 'Membre' in line and 'import' in line:
            print(f"   ✅ Trouvé: {line.strip()}")
            found = True
            if 'agents.models' in line:
                print("      → Utilise agents.models.Membre (20 membres)")
            elif 'assureur.models' in line:
                print("      → Utilise assureur.models.Membre (3 membres)")
    
    if not found:
        print("   ❌ Aucun import de Membre trouvé")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# 2. Vérifier la vue
print("\n2. VUE liste_membres:")
try:
    from django.test import RequestFactory
    from assureur.views import liste_membres
    print("   ✅ Vue importable")
    
    # Vérifier la source
    import inspect
    source = inspect.getsource(liste_membres)
    
    checks = [
        ("order_by", "date_inscription" in source or "date_adhesion" in source),
        ("search", "Q(" in source and "icontains" in source),
        ("pagination", "Paginator" in source),
    ]
    
    for check, passed in checks:
        status = "✅" if passed else "❌"
        print(f"   {status} {check}")
        
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# 3. Tester la recherche
print("\n3. TEST DE RECHERCHE DIRECTE:")
try:
    # Essayer d'abord agents.models
    try:
        from agents.models import Membre
        from django.db.models import Q
        
        search = "ASIA"
        results = Membre.objects.filter(
            Q(nom__icontains=search) | 
            Q(prenom__icontains=search)
        )
        print(f"   agents.models.Membre: {results.count()} résultat(s) pour '{search}'")
        
        if results.count() > 0:
            for m in results:
                print(f"      • {m.nom} {m.prenom} (ID: {m.id}, Numéro: {m.numero_unique})")
    except Exception as e:
        print(f"   agents.models.Membre: Erreur - {e}")
    
    # Essayer assureur.models
    try:
        from assureur.models import Membre as MembreAssureur
        from django.db.models import Q
        
        search = "ASIA"
        results = MembreAssureur.objects.filter(
            Q(nom__icontains=search) | 
            Q(prenom__icontains=search)
        )
        print(f"   assureur.models.Membre: {results.count()} résultat(s) pour '{search}'")
    except Exception as e:
        print(f"   assureur.models.Membre: Erreur - {e}")
        
except Exception as e:
    print(f"   ❌ Erreur globale: {e}")

# 4. Recommandation finale
print("\n" + "="*70)
print("🎯 RECOMMANDATION FINALE:")

try:
    from agents.models import Membre as MembreAgents
    from assureur.models import Membre as MembreAssureur
    
    if MembreAgents.objects.count() > MembreAssureur.objects.count():
        print("   Utilisez 'from agents.models import Membre' dans assureur/views.py")
        print("   Le template doit utiliser 'numero_unique' et 'date_inscription'")
    else:
        print("   Utilisez 'from assureur.models import Membre' dans assureur/views.py")
        print("   Le template doit utiliser 'numero_membre' et 'date_adhesion'")
        
except:
    print("   Impossible de déterminer quel modèle utiliser")

print("\n🚀 ACTION IMMÉDIATE:")
print("   1. Modifiez assureur/views.py pour utiliser le bon import")
print("   2. Modifiez le template pour utiliser les bons champs")
print("   3. Redémarrez le serveur: python manage.py runserver")
print("   4. Testez: http://127.0.0.1:8000/assureur/membres/?q=ASIA")
print("="*70)