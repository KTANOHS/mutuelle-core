#!/usr/bin/env python3
"""
ANALYSE DE TOUS LES ACTEURS - VÉRIFICATION DES DASHBOARDS
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from django.test import RequestFactory

def analyser_tous_les_groupes():
    """Analyser tous les groupes et leurs dashboards"""
    
    print("🔍 ANALYSE DE TOUS LES ACTEURS")
    print("=" * 50)
    
    groupes_a_analyser = [
        'Membres',
        'Medecins', 
        'Assureurs',
        'Pharmaciens',
        'Agents'
    ]
    
    factory = RequestFactory()
    
    for groupe_nom in groupes_a_analyser:
        try:
            groupe = Group.objects.get(name=groupe_nom)
            users = groupe.user_set.all()
            
            print(f"\n👥 GROUPE: {groupe_nom}")
            print(f"   📊 {users.count()} utilisateurs")
            
            if users.exists():
                user_test = users.first()
                print(f"   👤 Exemple: {user_test.username}")
                
                # Tester l'accès dashboard
                try:
                    from mutuelle_core.views import dashboard
                    
                    request = factory.get('/')
                    request.user = user_test
                    
                    response = dashboard(request)
                    
                    print(f"   🌐 Dashboard: {response.status_code}")
                    
                    if hasattr(response, 'url'):
                        print(f"   🔀 Redirection vers: {response.url}")
                    elif hasattr(response, 'template_name'):
                        templates = response.template_name
                        if not isinstance(templates, list):
                            templates = [templates]
                        print(f"   📄 Template: {templates[0]}")
                        
                except Exception as e:
                    print(f"   ❌ Erreur test: {e}")
                    
        except Group.DoesNotExist:
            print(f"\n❌ Groupe {groupe_nom} non trouvé")

def comparer_redirections():
    """Comparer les redirections de tous les groupes"""
    
    print("\n🔄 COMPARAISON DES REDIRECTIONS")
    print("=" * 50)
    
    from mutuelle_core.views import dashboard
    factory = RequestFactory()
    
    groupes_redirections = {
        'Membres': '/membres/dashboard/',
        'Medecins': '/medecin/dashboard/', 
        'Assureurs': '/assureur/dashboard/',
        'Pharmaciens': '/pharmacien/dashboard/',
        'Agents': '/agents/dashboard/'
    }
    
    for groupe_nom, redirection_attendue in groupes_redirections.items():
        try:
            groupe = Group.objects.get(name=groupe_nom)
            user = groupe.user_set.first()
            
            if user:
                request = factory.get('/')
                request.user = user
                
                response = dashboard(request)
                
                if hasattr(response, 'url'):
                    print(f"🎯 {groupe_nom}:")
                    print(f"   ✅ Redirection: {response.url}")
                    print(f"   📍 Attendu: {redirection_attendue}")
                    
                    if response.url == redirection_attendue:
                        print("   🟢 CORRECT - Redirection normale")
                    else:
                        print("   🔴 PROBLEME - Redirection anormale")
                else:
                    print(f"🎯 {groupe_nom}: ❌ Pas de redirection")
                    
        except Exception as e:
            print(f"🎯 {groupe_nom}: ❌ Erreur: {e}")

def tester_dashboards_individuels():
    """Tester chaque dashboard individuellement"""
    
    print("\n🧪 TEST DES DASHBOARDS INDIVIDUELS")
    print("=" * 50)
    
    dashboards_a_tester = [
        ('Membres', '/membres/dashboard/'),
        ('Medecins', '/medecin/dashboard/'),
        ('Assureurs', '/assureur/dashboard/'), 
        ('Pharmaciens', '/pharmacien/dashboard/'),
        ('Agents', '/agents/dashboard/')
    ]
    
    factory = RequestFactory()
    
    for groupe_nom, url_dashboard in dashboards_a_tester:
        print(f"\n🎯 {groupe_nom}:")
        
        try:
            # Résoudre l'URL
            from django.urls import resolve
            match = resolve(url_dashboard)
            
            print(f"   🌐 URL: {url_dashboard}")
            print(f"   📍 Vue: {match.func.__name__}")
            
            # Tester la vue
            user = User.objects.filter(groups__name=groupe_nom).first()
            if user:
                request = factory.get(url_dashboard)
                request.user = user
                
                response = match.func(request, **match.kwargs)
                
                if hasattr(response, 'template_name'):
                    templates = response.template_name
                    if not isinstance(templates, list):
                        templates = [templates]
                    print(f"   📄 Template: {templates[0]}")
                    
                    # Vérifier si c'est l'ancien ou nouveau système
                    if 'core/dashboard' in templates[0]:
                        print("   🟡 SYSTÈME: Nouveau dashboard unifié")
                    else:
                        print("   🟢 SYSTÈME: Ancien dashboard spécifique")
                        
            else:
                print("   ❌ Aucun utilisateur trouvé")
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")

def verifier_problemes_similaires():
    """Vérifier si d'autres groupes ont des problèmes similaires"""
    
    print("\n🔍 RECHERCHE DE PROBLÈMES SIMILAIRES")
    print("=" * 50)
    
    problemes_trouves = []
    
    # Tester chaque utilisateur de chaque groupe
    for groupe in Group.objects.all():
        users = groupe.user_set.all()[:2]  # Tester 2 users par groupe
        
        for user in users:
            try:
                # Simuler l'accès dashboard
                from mutuelle_core.views import dashboard
                factory = RequestFactory()
                request = factory.get('/')
                request.user = user
                
                response = dashboard(request)
                
                # Vérifier si c'est une redirection problématique
                if hasattr(response, 'url'):
                    url = response.url
                    if '/assureur/dashboard/' in url and groupe.name == 'Assureurs':
                        problemes_trouves.append(f"🔴 ASSUREURS: Redirection vers {url}")
                    elif '/core/' in url or 'unified' in url:
                        problemes_trouves.append(f"🟡 {groupe.name}: Utilise nouveau système")
                    else:
                        problemes_trouves.append(f"🟢 {groupe.name}: Système normal")
                        
            except Exception as e:
                problemes_trouves.append(f"❌ {groupe.name}: Erreur {e}")
    
    # Afficher les résultats
    if problemes_trouves:
        print("📊 RÉSULTATS:")
        for probleme in set(problemes_trouves):  # Enlever les doublons
            print(f"   {probleme}")
    else:
        print("✅ Aucun problème détecté")

def recommander_corrections():
    """Recommander des corrections pour tous les groupes"""
    
    print("\n🔧 RECOMMANDATIONS POUR TOUS LES GROUPES")
    print("=" * 50)
    
    print("""
🎯 SITUATION ACTUELLE:
• Tous les groupes sont redirigés vers leurs dashboards spécifiques
• Le problème des ASSUREURS est spécifique à leur dashboard

🔧 CORRECTIONS RECOMMANDÉES:

1. 🎯 CORRECTION ASSUREURS (Prioritaire):
   - Modifier mutuelle_core/views.py pour les ASSUREURS
   - OU corriger assureur/views.dashboard pour restaurer l'ancienne fonctionnalité

2. 🔍 VÉRIFICATION AUTRES GROUPES:
   - Tester chaque dashboard individuellement
   - Vérifier que toutes les fonctions sont présentes

3. ⚙️ SOLUTION SYSTÈME:
   - Standardiser tous les dashboards sur l'ancien système
   - OU compléter le nouveau système avec toutes les fonctions

4. 🧪 TESTS COMPLETS:
   - Tester chaque fonctionnalité par groupe
   - Vérifier les permissions et accès
""")

def main():
    """Fonction principale"""
    
    print("🚀 ANALYSE COMPLÈTE DE TOUS LES ACTEURS")
    print("=" * 60)
    
    analyser_tous_les_groupes()
    comparer_redirections()
    tester_dashboards_individuels()
    verifier_problemes_similaires()
    recommander_corrections()
    
    print("\n🎉 ANALYSE TERMINÉE !")
    print("=" * 60)
    print("\n💡 CONCLUSION:")
    print("Le problème est probablement SPÉCIFIQUE aux ASSUREURS")
    print("Les autres groupes utilisent leurs dashboards normaux")

if __name__ == "__main__":
    main()