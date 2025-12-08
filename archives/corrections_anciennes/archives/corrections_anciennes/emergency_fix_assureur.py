#!/usr/bin/env python
"""
Correctif d'urgence pour assureur/views.py
"""

def emergency_fix():
    """Correction d'urgence du problème UnboundLocalError"""
    views_path = 'assureur/views.py'
    
    # Contenu corrigé de la fonction liste_membres
    corrected_function = '''
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Assureur').exists())
def liste_membres(request):
    """Liste tous les membres"""
    from membres.models import Membre  # Import local pour éviter les problèmes
    
    # Récupération des membres
    membres_list = Membre.objects.all().order_by('nom', 'prenom')
    
    # Pagination
    paginator = Paginator(membres_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'membres_count': membres_list.count()
    }
    
    return render(request, 'assureur/liste_membres.html', context)
'''
    
    with open(views_path, 'r') as f:
        content = f.read()
    
    # Remplace la fonction liste_membres
    if 'def liste_membres' in content:
        # Trouve le début et la fin de la fonction
        start = content.find('def liste_membres')
        if start != -1:
            # Trouve la fin de la fonction (niveau d'indentation revenu à 0)
            lines = content[start:].split('\n')
            function_lines = []
            base_indent = None
            
            for i, line in enumerate(lines):
                if i == 0:
                    function_lines.append(line)
                    # Détermine l'indentation de base
                    base_indent = len(line) - len(line.lstrip())
                    continue
                
                current_indent = len(line) - len(line.lstrip()) if line.strip() else 0
                
                if current_indent <= base_indent and line.strip() and not line.startswith(' ' * (base_indent)):
                    # Fin de la fonction
                    break
                else:
                    function_lines.append(line)
            
            old_function = '\n'.join(function_lines)
            content = content.replace(old_function, corrected_function)
            
            with open(views_path, 'w') as f:
                f.write(content)
            print("✅ Fonction liste_membres remplacée (correctif d'urgence)")
        else:
            print("❌ Impossible de trouver la fonction liste_membres")
    else:
        print("❌ Fonction liste_membres non trouvée")

if __name__ == "__main__":
    emergency_fix()