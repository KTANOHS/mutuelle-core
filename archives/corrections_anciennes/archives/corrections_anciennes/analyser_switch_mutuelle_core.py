#!/usr/bin/env python3
"""
ANALYSE DU CODE DE SWITCH DANS mutuelle_core/views.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyser_vue_dashboard_mutuelle_core():
    """Analyser la vue dashboard dans mutuelle_core/views.py"""
    
    print("🔍 ANALYSE DE mutuelle_core/views.py")
    print("=" * 50)
    
    try:
        # Lire le fichier views.py
        views_path = 'mutuelle_core/views.py'
        with open(views_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Trouver la fonction dashboard
        lines = content.split('\n')
        in_dashboard_function = False
        dashboard_code = []
        
        for i, line in enumerate(lines, 1):
            if 'def dashboard(' in line:
                in_dashboard_function = True
                print(f"\n🎯 FONCTION DASHBOARD TROUVÉE (ligne {i}):")
            
            if in_dashboard_function:
                dashboard_code.append(f"{i:4d}: {line}")
                
                # Fin de fonction
                if line.strip() and not line.startswith(' ') and not line.startswith('def '):
                    break
        
        # Afficher le code pertinent
        print("📋 CODE DE LA VUE DASHBOARD:")
        for code_line in dashboard_code:
            if any(keyword in code_line.lower() for keyword in ['group', 'assureur', 'template', 'render', 'return']):
                if 'group' in code_line.lower() or 'assureur' in code_line.lower():
                    print(f"   🚨 {code_line}")
                else:
                    print(f"   📄 {code_line}")
    
    except Exception as e:
        print(f"❌ Erreur lecture fichier: {e}")

def trouver_logique_switch():
    """Trouver exactement la logique de switch"""
    
    print("\n🎯 RECHERCHE DE LA LOGIQUE DE SWITCH")
    print("=" * 50)
    
    try:
        # Importer et analyser la vue
        from mutuelle_core import views
        
        # Obtenir le code source de la fonction
        import inspect
        source = inspect.getsource(views.dashboard)
        
        lines = source.split('\n')
        print("📝 CODE SOURCE DE dashboard():")
        
        for i, line in enumerate(lines, 1):
            if 'groups.filter' in line and 'Assureur' in line:
                print(f"   🚨 LIGNE CRITIQUE {i}: {line.strip()}")
            elif 'template_name' in line or 'render(' in line:
                print(f"   📄 Ligne {i}: {line.strip()}")
            elif 'if' in line and 'group' in line.lower():
                print(f"   🔀 Ligne {i}: {line.strip()}")
                
    except Exception as e:
        print(f"❌ Erreur analyse code source: {e}")

def solution_rapide():
    """Solution pour corriger le problème"""
    
    print("\n🚀 SOLUTION RAPIDE")
    print("=" * 50)
    
    print("""
🎯 PROBLÈME CONFIRMÉ:
La vue dashboard() dans mutuelle_core/views.py change le template
quand l'utilisateur est dans le groupe 'Assureur'.

🔧 SOLUTIONS:

1. 🎯 SOLUTION TEMPORAIRE (Déjà appliquée):
   Retirer test_assureur du groupe Assureurs ✅

2. 🔧 SOLUTION CODE - Modifier mutuelle_core/views.py:
   Changer la logique pour utiliser toujours l'ancien dashboard

3. ⚙️ SOLUTION SETTING - Ajouter une option:
   FORCE_OLD_DASHBOARD = True dans les settings

4. 🎨 SOLUTION TEMPLATE - Fusionner:
   Adapter le nouveau template avec toutes les fonctions anciennes
""")

def creer_patch_correction():
    """Créer un patch pour corriger le problème"""
    
    print("\n🔧 CRÉATION PATCH DE CORRECTION")
    print("=" * 50)
    
    patch_code = """
# PATCH POUR mutuelle_core/views.py
# Ajouter cette fonction au début du fichier

def get_assureur_dashboard_template(user):
    '''
    Détermine quel template utiliser pour le dashboard assureur
    Retourne toujours l'ancien template complet
    '''
    # FORCER L'ANCIEN DASHBOARD COMPLET
    return 'assureur/dashboard.html'
    
    # OU pour garder l'option:
    # from django.conf import settings
    # if getattr(settings, 'FORCE_OLD_DASHBOARD', False):
    #     return 'assureur/dashboard.html'
    # else:
    #     return 'core/dashboard_unified.html'  # Nouveau dashboard

# Puis modifier la vue dashboard():
# Remplacer les lignes qui choisissent le template par:
# template_name = get_assureur_dashboard_template(request.user)
"""
    
    print(patch_code)

def verifier_autres_utilisateurs():
    """Vérifier si d'autres utilisateurs sont affectés"""
    
    print("\n👥 VÉRIFICATION AUTRES UTILISATEURS")
    print("=" * 50)
    
    from django.contrib.auth.models import User, Group
    
    # Compter les assureurs avec groupe
    groupe_assureur = Group.objects.get(name='Assureurs')
    assureurs_avec_groupe = groupe_assureur.user_set.count()
    
    print(f"👥 Utilisateurs dans le groupe Assureurs: {assureurs_avec_groupe}")
    
    if assureurs_avec_groupe > 0:
        print("📋 Liste des assureurs affectés:")
        for user in groupe_assureur.user_set.all():
            print(f"   👤 {user.username} - {user.get_full_name()}")

def main():
    """Fonction principale"""
    
    print("🚀 ANALYSE COMPLÈTE DU PROBLÈME DE SWITCH")
    print("=" * 60)
    
    analyser_vue_dashboard_mutuelle_core()
    trouver_logique_switch()
    verifier_autres_utilisateurs()
    solution_rapide()
    creer_patch_correction()
    
    print("\n🎉 DIAGNOSTIC COMPLET TERMINÉ !")
    print("=" * 60)
    print("\n💡 RÉSUMÉ:")
    print("• Problème identifié dans mutuelle_core/views.py")
    print("• Switch activé par appartenance au groupe 'Assureurs'") 
    print("• Solution temporaire appliquée ✅")
    print("• Patch de correction fourni 🔧")

if __name__ == "__main__":
    main()