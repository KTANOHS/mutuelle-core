#!/usr/bin/env python
"""
VÉRIFICATION DE LA VUE CORRIGÉE
"""

import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Django configuré")
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

def verifier_vue_corrigee():
    """Vérifie que la vue a été correctement corrigée"""
    print("🔍 VÉRIFICATION DE LA VUE CORRIGÉE...")
    
    chemin_views = os.path.join(os.path.dirname(__file__), 'assureur', 'views.py')
    
    with open(chemin_views, 'r') as f:
        contenu = f.read()
    
    # Vérifications
    verifications = {
        'JsonResponse importé': 'from django.http import JsonResponse' in contenu or 'from django.http import' in contenu and 'JsonResponse' in contenu,
        'Fonction creer_bon existe': 'def creer_bon(' in contenu,
        'Retourne JsonResponse': 'return JsonResponse(' in contenu,
        'Gestion des exceptions': 'except Exception as e:' in contenu,
        'Gestion méthode non autorisée': 'status=405' in contenu,
    }
    
    print("\n📋 RÉSULTATS DE VÉRIFICATION:")
    for check, result in verifications.items():
        status = "✅" if result else "❌"
        print(f"   {status} {check}")
    
    # Afficher un extrait de la fonction
    print("\n📝 EXTRAIT DE LA FONCTION:")
    lines = contenu.split('\n')
    in_function = False
    function_lines = []
    
    for line in lines:
        if 'def creer_bon(' in line:
            in_function = True
        if in_function:
            function_lines.append(line)
            if line.strip() and not line.startswith(' ') and not line.startswith('\t') and 'def creer_bon(' not in line:
                if len(function_lines) > 1:  # Au moins une ligne après la définition
                    break
    
    for line in function_lines[:10]:  # Afficher les 10 premières lignes
        print(f"   {line}")
    
    if len(function_lines) > 10:
        print("   ...")
    
    return all(verifications.values())

def tester_vue_avec_requests():
    """Teste la vue avec des requêtes HTTP simulées"""
    print("\n🌐 TEST DE LA VUE AVEC REQUÊTES...")
    
    from django.test import RequestFactory
    from assureur.views import creer_bon
    from membres.models import Membre
    import json
    
    # Créer une factory de requêtes
    factory = RequestFactory()
    
    # Récupérer un membre
    membre = Membre.objects.first()
    if not membre:
        print("❌ Aucun membre trouvé")
        return False
    
    print(f"👤 Membre de test: {membre.nom} {membre.prenom}")
    
    # Test 1: Requête POST AJAX valide
    print("\n🧪 Test 1: Requête AJAX valide...")
    data_valide = {
        'type_soin': 'Consultation test',
        'montant_total': '15000',
        'taux_remboursement': '80'
    }
    
    request = factory.post(
        f'/assureur/bons/creer/{membre.numero_unique}/',
        data=json.dumps(data_valide),
        content_type='application/json',
        HTTP_X_REQUESTED_WITH='XMLHttpRequest'
    )
    
    try:
        response = creer_bon(request, membre.numero_unique)
        print(f"   📊 Statut: {response.status_code}")
        if hasattr(response, 'content'):
            print(f"   📦 Contenu: {response.content.decode()}")
        
        if response.status_code == 200:
            print("   ✅ Requête AJAX valide: SUCCÈS")
        else:
            print("   ❌ Requête AJAX valide: ÉCHEC")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False
    
    # Test 2: Requête sans AJAX
    print("\n🧪 Test 2: Requête sans en-tête AJAX...")
    request = factory.post(
        f'/assureur/bons/creer/{membre.numero_unique}/',
        data=json.dumps(data_valide),
        content_type='application/json'
    )
    
    try:
        response = creer_bon(request, membre.numero_unique)
        print(f"   📊 Statut: {response.status_code}")
        if response.status_code == 405:
            print("   ✅ Méthode non autorisée bien gérée")
        else:
            print("   ❌ Gestion méthode non autorisée échouée")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if verifier_vue_corrigee():
        print("\n✅ Vue correctement corrigée!")
        print("\n🎯 Testons maintenant avec des requêtes...")
        tester_vue_avec_requests()
    else:
        print("\n❌ La vue n'est pas correctement corrigée")