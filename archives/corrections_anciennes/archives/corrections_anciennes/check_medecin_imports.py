#!/usr/bin/env python
"""
VÉRIFICATION ET CORRECTION DES IMPORTS DANS MEDECIN/VIEWS.PY
"""
import os

def check_medecin_imports():
    print("🔍 VÉRIFICATION DES IMPORTS DANS MEDECIN/VIEWS.PY")
    print("=" * 60)
    
    medecin_views_file = 'medecin/views.py'
    
    if not os.path.exists(medecin_views_file):
        print("❌ medecin/views.py n'existe pas")
        return False
    
    with open(medecin_views_file, 'r') as f:
        content = f.read()
    
    # Vérifier les imports nécessaires
    required_imports = [
        'from django.shortcuts import render',
        'from django.contrib.auth.decorators import login_required',
        'from core.utils import get_dashboard_context'
    ]
    
    missing_imports = []
    
    for import_stmt in required_imports:
        if import_stmt not in content:
            missing_imports.append(import_stmt)
            print(f"❌ Import manquant: {import_stmt}")
        else:
            print(f"✅ Import présent: {import_stmt}")
    
    # Vérifier les fonctions nécessaires
    required_functions = ['liste_bons', 'creer_ordonnance', 'dashboard']
    missing_functions = []
    
    for func in required_functions:
        if f"def {func}(" not in content:
            missing_functions.append(func)
            print(f"❌ Fonction manquante: {func}")
        else:
            print(f"✅ Fonction présente: {func}")
    
    return missing_imports, missing_functions

def fix_medecin_views():
    print("\n🔧 CORRECTION DE MEDECIN/VIEWS.PY")
    print("=" * 50)
    
    medecin_views_file = 'medecin/views.py'
    
    # Lire le contenu actuel
    with open(medecin_views_file, 'r') as f:
        content = f.read()
    
    # Ajouter les imports manquants
    imports_to_add = '''from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.utils import get_dashboard_context
'''
    
    # Vérifier si les imports de base sont présents
    if 'from django.shortcuts import render' not in content:
        # Ajouter au début du fichier
        lines = content.split('\n')
        lines.insert(0, imports_to_add)
        content = '\n'.join(lines)
    
    # Ajouter les fonctions manquantes si nécessaire
    missing_functions_code = '''

@login_required
def liste_bons(request):
    """Liste des bons de soin"""
    from soins.models import BonSoin
    
    context = get_dashboard_context(request.user)
    
    if hasattr(request.user, 'medecin'):
        context['bons'] = BonSoin.objects.filter(medecin=request.user.medecin)[:20]
    else:
        context['bons'] = BonSoin.objects.all()[:20]
    
    return render(request, 'medecin/liste_bons.html', context)

@login_required
def creer_ordonnance(request):
    """Créer une ordonnance"""
    context = get_dashboard_context(request.user)
    
    return render(request, 'medecin/creer_ordonnance.html', context)

@login_required
def dashboard(request):
    """Dashboard Médecin"""
    context = get_dashboard_context(request.user)
    
    # Ajouter des données spécifiques
    try:
        if hasattr(request.user, 'medecin'):
            context['medecin_profile'] = request.user.medecin
    except:
        pass
    
    return render(request, 'medecin/dashboard.html', context)
'''
    
    # Ajouter les fonctions manquantes
    if 'def liste_bons(' not in content:
        content += missing_functions_code
    
    # Écrire le fichier corrigé
    with open(medecin_views_file, 'w') as f:
        f.write(content)
    
    print("✅ medecin/views.py corrigé avec succès!")
    return True

def main():
    print("🚀 VÉRIFICATION ET CORRECTION DES IMPORTS")
    print("=" * 60)
    
    # Vérifier l'état actuel
    missing_imports, missing_functions = check_medecin_imports()
    
    if missing_imports or missing_functions:
        print(f"\n❌ Problèmes détectés:")
        print(f"   - {len(missing_imports)} imports manquants")
        print(f"   - {len(missing_functions)} fonctions manquantes")
        
        # Corriger automatiquement
        fix_success = fix_medecin_views()
        
        if fix_success:
            print("\n✅ Vérification après correction:")
            check_medecin_imports()
    else:
        print("\n🎉 Tous les imports et fonctions sont présents!")
    
    print("\n" + "=" * 60)
    print("💡 EXÉCUTEZ MAINTENANT: python manage.py check")

if __name__ == "__main__":
    main()