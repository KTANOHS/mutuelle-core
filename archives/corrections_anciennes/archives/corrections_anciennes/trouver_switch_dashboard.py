#!/usr/bin/env python3
"""
TROUVER LA VUE QUI FAIT LE SWITCH DE DASHBOARD
"""

import os
import django
import subprocess

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def trouver_code_switch():
    """Trouver le code qui change le dashboard basé sur les groupes"""
    
    print("🔍 RECHERCHE DU CODE DE SWITCH DASHBOARD")
    print("=" * 50)
    
    # Rechercher dans tout le code
    motifs = [
        'dashboard_unified',
        'generic_dashboard', 
        'assureur/dashboard',
        'user.groups.filter',
        'groups.filter.*assureur',
        'template_name.*assureur',
        'if.*group.*assureur'
    ]
    
    for motif in motifs:
        print(f"\n🎯 Recherche: {motif}")
        try:
            result = subprocess.run([
                'grep', '-r', '-n', '--color=always', motif,
                'assureur/', 'core/', 'mutuelle_core/', '--include=*.py'
            ], capture_output=True, text=True)
            
            if result.stdout:
                lignes = result.stdout.strip().split('\n')
                for ligne in lignes:
                    if ligne:  # Ignorer les lignes vides
                        print(f"   📍 {ligne}")
            else:
                print("   ❌ Aucun résultat")
                
        except Exception as e:
            print(f"   ⚠️  Erreur: {e}")

def analyser_vues_assureur():
    """Analyser les vues de l'app assureur"""
    
    print("\n📁 ANALYSE DES VUES ASSUREUR")
    print("=" * 50)
    
    try:
        # Importer les vues assureur
        from assureur import views
        
        # Lister toutes les vues
        print("🎯 Vues trouvées dans assureur.views:")
        for attr_name in dir(views):
            if not attr_name.startswith('_'):
                attr = getattr(views, attr_name)
                if callable(attr):
                    print(f"   📍 {attr_name}")
                    
    except Exception as e:
        print(f"❌ Erreur import views: {e}")

def tester_vue_dashboard():
    """Tester la vue dashboard directement"""
    
    print("\n🧪 TEST DIRECT DE LA VUE DASHBOARD")
    print("=" * 50)
    
    try:
        from django.test import RequestFactory
        from django.contrib.auth.models import User
        
        # Essayer d'importer différentes vues dashboard
        vues_possibles = [
            'assureur.views.dashboard',
            'core.views.dashboard',
            'core.views.home',
            'mutuelle_core.views.dashboard'
        ]
        
        factory = RequestFactory()
        user_avec_groupe = User.objects.get(username='test_assureur')
        user_sans_groupe = User.objects.get(username='test_assureur')
        
        # Remettre temporairement dans le groupe pour test
        from django.contrib.auth.models import Group
        groupe_assureur = Group.objects.get(name='Assureurs')
        user_avec_groupe.groups.add(groupe_assureur)
        
        for vue_path in vues_possibles:
            try:
                module_path, vue_name = vue_path.rsplit('.', 1)
                module = __import__(module_path, fromlist=[vue_name])
                vue_func = getattr(module, vue_name)
                
                print(f"\n🔍 Test vue: {vue_path}")
                
                # Test avec groupe
                request = factory.get('/')
                request.user = user_avec_groupe
                response_avec = vue_func(request)
                
                # Test sans groupe  
                request.user = user_sans_groupe
                response_sans = vue_func(request)
                
                if hasattr(response_avec, 'template_name'):
                    temp_avec = response_avec.template_name
                    temp_sans = response_sans.template_name
                    
                    print(f"   📄 Avec groupe: {temp_avec}")
                    print(f"   📄 Sans groupe: {temp_sans}")
                    
                    if temp_avec != temp_sans:
                        print("   🎯 ⚠️  SWITCH DÉTECTÉ! Les templates sont différents!")
                    
            except Exception as e:
                print(f"   ❌ Erreur test {vue_path}: {e}")
        
        # Retirer du groupe après test
        user_avec_groupe.groups.remove(groupe_assureur)
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")

def main():
    """Fonction principale"""
    
    print("🚀 IDENTIFICATION DU POINT DE SWITCH DASHBOARD")
    print("=" * 60)
    
    trouver_code_switch()
    analyser_vues_assureur()
    tester_vue_dashboard()
    
    print("\n🎉 RECHERCHE TERMINÉE !")
    print("=" * 60)

if __name__ == "__main__":
    main()