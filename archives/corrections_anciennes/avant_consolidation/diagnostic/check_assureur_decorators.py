
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
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Accès réservé aux assureurs.")
            return redirect('/')
    
    return _wrapped_view
'''
        
        with open(decorators_path, 'w') as f:
            f.write(decorator_code)
        print("✅ Décorateur assureur_required créé")
        
else:
    print(f"❌ Fichier non trouvé: {decorators_path}")
    
    # Créer le dossier et le fichier
    assureur_dir = os.path.join(os.getcwd(), 'assureur')
    if not os.path.exists(assureur_dir):
        os.makedirs(assureur_dir)
    
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
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Accès réservé aux assureurs.")
            return redirect('/')
    
    return _wrapped_view
'''
    
    with open(decorators_path, 'w') as f:
        f.write(decorator_code)
    
    print(f"✅ Fichier créé: {decorators_path}")

