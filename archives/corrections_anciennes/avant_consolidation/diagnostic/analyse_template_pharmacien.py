#!/usr/bin/env python
"""
ANALYSE DU TEMPLATE PHARMACIEN EXISTANT
"""
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyser_template_liste_ordonnances():
    """Analyse le template liste_ordonnances.html"""
    print("🔍 ANALYSE TEMPLATE liste_ordonnances.html")
    print("=" * 60)
    
    template_path = BASE_DIR / 'templates' / 'pharmacien' / 'liste_ordonnances.html'
    
    if template_path.exists():
        print(f"✅ Template trouvé: {template_path}")
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print("\n📝 CONTENU DU TEMPLATE:")
            print("=" * 40)
            
            # Afficher les premières lignes
            lines = content.split('\n')
            for i, line in enumerate(lines[:50]):  # Premières 50 lignes
                print(f"{i+1:3d}: {line}")
            
            # Analyse spécifique
            print("\n🔍 ANALYSE CRITIQUE:")
            
            # Vérifier la variable de contexte
            if 'ordonnances' in content:
                print("✅ Variable 'ordonnances' trouvée")
            else:
                print("❌ Variable 'ordonnances' NON trouvée")
                
            # Vérifier la boucle
            if '{% for' in content and 'ordonnance' in content:
                print("✅ Boucle for avec variable 'ordonnance' trouvée")
            else:
                print("❌ Boucle for NON trouvée")
                
            # Vérifier la section empty
            if '{% empty %}' in content:
                print("✅ Section 'empty' trouvée")
            else:
                print("❌ Section 'empty' NON trouvée")
                
            # Vérifier l'affichage des données
            variables = ['numero', 'patient_nom', 'medicaments', 'date_prescription']
            for var in variables:
                if var in content:
                    print(f"✅ Variable '{var}' affichée")
                else:
                    print(f"❌ Variable '{var}' NON affichée")
                    
        except Exception as e:
            print(f"❌ Erreur lecture template: {e}")
    else:
        print(f"❌ Template non trouvé: {template_path}")

def analyser_vue_pharmacien():
    """Analyse la vue Django"""
    print("\n📋 ANALYSE DE LA VUE")
    print("=" * 40)
    
    try:
        from pharmacien import views
        
        # Vérifier la fonction liste_ordonnances_attente
        if hasattr(views, 'liste_ordonnances_attente'):
            print("✅ Vue 'liste_ordonnances_attente' trouvée")
            
            import inspect
            source = inspect.getsource(views.liste_ordonnances_attente)
            
            print("\n📝 CODE DE LA VUE:")
            print("-" * 30)
            
            # Afficher le code source
            for line in source.split('\n'):
                print(f"   {line}")
                
            # Vérifications critiques
            if 'pharmacien_ordonnances_view' in source:
                print("\n✅ Vue utilise 'pharmacien_ordonnances_view'")
            else:
                print("\n❌ Vue n'utilise PAS 'pharmacien_ordonnances_view'")
                
            if 'context' in source or 'render' in source:
                print("✅ Vue renvoie un contexte")
            else:
                print("❌ Vue ne renvoie pas de contexte")
                
        else:
            print("❌ Vue 'liste_ordonnances_attente' non trouvée")
            
    except Exception as e:
        print(f"❌ Erreur analyse vue: {e}")

def tester_vue_directement():
    """Teste la vue directement"""
    print("\n🧪 TEST DIRECT DE LA VUE")
    print("=" * 40)
    
    try:
        from pharmacien.views import liste_ordonnances_attente
        from django.test import RequestFactory
        from django.contrib.auth.models import User
        
        # Créer une requête simulée
        factory = RequestFactory()
        request = factory.get('/pharmacien/ordonnances/')
        
        # Utiliser un utilisateur pharmacien existant
        pharmacien_user = User.objects.filter(username='GLORIA1').first()
        if pharmacien_user:
            request.user = pharmacien_user
            
            # Appeler la vue
            response = liste_ordonnances_attente(request)
            
            print(f"✅ Vue exécutée - Status: {response.status_code}")
            
            # Vérifier le contexte
            if hasattr(response, 'context_data'):
                context = response.context_data
                print(f"📊 Contexte disponible: {list(context.keys())}")
                
                if 'ordonnances' in context:
                    ordonnances = context['ordonnances']
                    print(f"💊 Ordonnances dans contexte: {len(ordonnances)}")
                    
                    for i, ord in enumerate(ordonnances[:3]):
                        print(f"   {i+1}. {getattr(ord, 'numero', 'N/A')}")
                else:
                    print("❌ 'ordonnances' non dans le contexte")
            else:
                print("ℹ️  Pas de contexte_data (TemplateResponse)")
                
        else:
            print("❌ Utilisateur GLORIA1 non trouvé")
            
    except Exception as e:
        print(f"❌ Erreur test vue: {e}")

def main():
    """Fonction principale"""
    print("🚀 ANALYSE COMPLÈTE - TEMPLATE PHARMACIEN")
    print("=" * 60)
    
    analyser_template_liste_ordonnances()
    analyser_vue_pharmacien()
    tester_vue_directement()
    
    print(f"\n🎯 DIAGNOSTIC TERMINÉ")

if __name__ == "__main__":
    sys.exit(main())