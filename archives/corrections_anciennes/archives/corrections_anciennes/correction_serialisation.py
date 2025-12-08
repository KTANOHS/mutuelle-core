#!/usr/bin/env python3
"""
CORRECTION URGENTE - ERREUR JSON SERIALIZATION
"""

import re

def corriger_erreur_serialisation():
    """Corrige l'erreur 'Object of type method is not JSON serializable'"""
    file_path = 'agents/views.py'
    
    print("🔧 CORRECTION ERREUR SÉRIALISATION JSON")
    print("=" * 50)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Rechercher la fonction recherche_membres_api
        start = content.find('def recherche_membres_api')
        if start == -1:
            print("❌ Fonction recherche_membres_api non trouvée")
            return False
        
        end = content.find('def ', start + 1)
        if end == -1:
            end = len(content)
        
        fonction_content = content[start:end]
        
        print("📋 Analyse de la fonction recherche_membres_api...")
        
        # Vérifier les problèmes courants
        problemes = []
        
        # 1. Vérifier les méthodes non appelées (sans parenthèses)
        method_pattern = r"'(\w+)':\s*(\w+(?=,|\}))(?![\(\)])"
        matches = re.findall(method_pattern, fonction_content)
        
        for champ, valeur in matches:
            if not valeur.startswith("membre.") and valeur not in ['id', 'nom', 'prenom', 'numero_unique', 'telephone', 'statut']:
                problemes.append(f"Champ '{champ}' utilise '{valeur}' (méthode non appelée)")
        
        if problemes:
            print("❌ Problèmes détectés:")
            for p in problemes:
                print(f"   - {p}")
            
            # Remplacer la fonction entière par une version corrigée
            nouvelle_fonction = '''
@login_required
def recherche_membres_api(request):
    """API pour la recherche de membres - VERSION CORRIGÉE"""
    try:
        query = request.GET.get('q', '').strip()
        
        logger.info(f"Recherche membres API appelée avec query: '{query}'")
        
        if len(query) < 2:
            return JsonResponse({'membres': []})
        
        # Import sécurisé
        from membres.models import Membre
        from django.db.models import Q
        from django.http import JsonResponse
        
        # Recherche dans la base de données
        membres = Membre.objects.filter(
            Q(nom__icontains=query) |
            Q(prenom__icontains=query) |
            Q(numero_unique__icontains=query) |
            Q(telephone__icontains=query)
        )[:10]
        
        logger.info(f"Nombre de membres trouvés: {len(membres)}")
        
        # Construction des résultats avec valeurs SÉRIALISABLES
        results = []
        for membre in membres:
            # ✅ CORRECTION: Utiliser getattr() pour éviter les méthodes
            results.append({
                'id': getattr(membre, 'id', None),
                'nom': getattr(membre, 'nom', ''),
                'prenom': getattr(membre, 'prenom', ''),
                'numero_unique': getattr(membre, 'numero_unique', ''),
                'telephone': getattr(membre, 'telephone', ''),
                'statut': getattr(membre, 'statut', '')
            })
        
        logger.info(f"Recherche réussie: {len(results)} résultats")
        return JsonResponse({'membres': results})
        
    except Exception as e:
        logger.error(f"Erreur critique recherche membres: {e}")
        return JsonResponse({
            'membres': [], 
            'error': 'Erreur technique lors de la recherche'
        }, status=500)
'''
            
            # Remplacer l'ancienne fonction par la nouvelle
            content = content[:start] + nouvelle_fonction + content[end:]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Fonction recherche_membres_api remplacée par version corrigée")
            return True
        else:
            print("✅ Aucun problème de sérialisation détecté")
            return True
            
    except Exception as e:
        print(f"❌ Erreur correction: {e}")
        return False

def verifier_imports():
    """Vérifie que tous les imports nécessaires sont présents"""
    file_path = 'agents/views.py'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        imports_necessaires = [
            'from django.http import JsonResponse',
            'from django.db.models import Q',
            'from membres.models import Membre'
        ]
        
        print("\n🔍 VÉRIFICATION DES IMPORTS")
        print("-" * 30)
        
        for imp in imports_necessaires:
            if imp in content:
                print(f"✅ {imp}")
            else:
                print(f"❌ {imp} - MANQUANT")
                # Ajouter l'import manquant
                if 'from django.' in imp:
                    # Ajouter après les autres imports Django
                    pattern = r'(from django\.\w+ import)'
                    match = re.search(pattern, content)
                    if match:
                        pos = match.start()
                        content = content[:pos] + imp + '\n' + content[pos:]
                        print(f"   ➕ Import ajouté")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"❌ Erreur vérification imports: {e}")

def main():
    print("🎯 CORRECTION URGENTE - ERREUR SÉRIALISATION JSON")
    print("=" * 60)
    
    # 1. Corriger l'erreur de sérialisation
    success = corriger_erreur_serialisation()
    
    # 2. Vérifier les imports
    verifier_imports()
    
    if success:
        print("\n🎉 CORRECTION APPLIQUÉE AVEC SUCCÈS!")
        print("\n🚀 PROCHAINES ÉTAPES:")
        print("1. Le serveur va redémarrer automatiquement")
        print("2. Testez la recherche avec: 'test', 'gloria', 'me'")
        print("3. Vérifiez que plus d'erreur 500")
    else:
        print("\n🚨 LA CORRECTION A ÉCHOUÉ - Intervention manuelle nécessaire")

if __name__ == "__main__":
    main()