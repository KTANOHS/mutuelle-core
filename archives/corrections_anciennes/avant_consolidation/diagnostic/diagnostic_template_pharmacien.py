#!/usr/bin/env python
"""
DIAGNOSTIC TEMPLATE PHARMACIEN - Pourquoi aucune ordonnance n'apparaît
"""
import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostic_complet():
    """Diagnostic complet du template pharmacien"""
    print("🔍 DIAGNOSTIC TEMPLATE PHARMACIEN")
    print("=" * 60)
    
    # 1. Vérifier la vue Django
    diagnostic_vue()
    
    # 2. Vérifier le template
    diagnostic_template()
    
    # 3. Vérifier les données
    diagnostic_donnees()
    
    # 4. Vérifier les URLs
    diagnostic_urls()

def diagnostic_vue():
    """Diagnostic de la vue Django"""
    print("\n📋 1. DIAGNOSTIC VUE DJANGO")
    
    try:
        # Essayer d'importer la vue pharmacien
        from pharmacien import views
        
        # Vérifier si la vue ordonnances existe
        if hasattr(views, 'ordonnances_pharmacien'):
            print("✅ Vue 'ordonnances_pharmacien' trouvée")
            
            # Analyser ce que renvoie la vue
            from django.test import RequestFactory
            from django.contrib.auth.models import User
            
            # Créer une requête simulée
            factory = RequestFactory()
            request = factory.get('/pharmacien/ordonnances/')
            
            # Simuler un utilisateur pharmacien
            pharmacien_user = User.objects.filter(groups__name='Pharmacien').first()
            if pharmacien_user:
                request.user = pharmacien_user
                
                # Essayer d'appeler la vue
                try:
                    response = views.ordonnances_pharmacien(request)
                    print(f"✅ Vue exécutée - Status: {response.status_code}")
                    
                    # Vérifier le contexte
                    if hasattr(response, 'context_data'):
                        print(f"📊 Contexte: {response.context_data}")
                    else:
                        print("ℹ️  Pas de contexte disponible (peut être normal)")
                        
                except Exception as e:
                    print(f"❌ Erreur exécution vue: {e}")
            else:
                print("⚠️  Aucun utilisateur pharmacien trouvé")
        else:
            print("❌ Vue 'ordonnances_pharmacien' non trouvée")
            
    except Exception as e:
        print(f"❌ Erreur import views: {e}")

def diagnostic_template():
    """Diagnostic du template"""
    print("\n📄 2. DIAGNOSTIC TEMPLATE")
    
    # Chercher le template pharmacien
    templates_paths = [
        BASE_DIR / 'pharmacien' / 'templates' / 'pharmacien',
        BASE_DIR / 'templates' / 'pharmacien',
        BASE_DIR / 'pharmacien' / 'templates',
    ]
    
    for path in templates_paths:
        if path.exists():
            print(f"✅ Dossier template trouvé: {path}")
            
            # Chercher les fichiers template
            for file in path.glob('*.html'):
                print(f"   📄 {file.name}")
                
            # Chercher spécifiquement le template ordonnances
            ordonnances_template = path / 'ordonnances.html'
            if ordonnances_template.exists():
                print(f"✅ Template ordonnances trouvé: {ordonnances_template}")
                
                # Analyser le contenu du template
                try:
                    with open(ordonnances_template, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Vérifications critiques
                    if 'for' in content and 'in' in content:
                        print("✅ Boucle for détectée dans le template")
                    else:
                        print("❌ Aucune boucle for détectée")
                        
                    if 'empty' in content:
                        print("✅ Section 'empty' détectée (pour liste vide)")
                    else:
                        print("❌ Aucune section 'empty' détectée")
                        
                    # Vérifier les variables de contexte
                    variables = ['ordonnances', 'ordonnance', 'ordonnance_list']
                    found_vars = [var for var in variables if var in content]
                    if found_vars:
                        print(f"✅ Variables de contexte: {found_vars}")
                    else:
                        print("❌ Aucune variable d'ordonnance détectée")
                        
                except Exception as e:
                    print(f"❌ Erreur lecture template: {e}")
            else:
                print(f"❌ Template ordonnances.html non trouvé dans {path}")
                
            break
    else:
        print("❌ Aucun dossier template pharmacien trouvé")

def diagnostic_donnees():
    """Diagnostic des données"""
    print("\n📊 3. DIAGNOSTIC DONNÉES")
    
    from django.db import connection
    
    try:
        # Vérifier la vue SQL
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM pharmacien_ordonnances_view")
            count_vue = cursor.fetchone()[0]
            print(f"✅ Vue SQL: {count_vue} ordonnances")
            
            if count_vue > 0:
                cursor.execute("""
                    SELECT ordonnance_id, numero, patient_nom, patient_prenom, medicaments
                    FROM pharmacien_ordonnances_view 
                    LIMIT 3
                """)
                ordonnances = cursor.fetchall()
                print("📋 Ordonnances dans la vue:")
                for ord in ordonnances:
                    print(f"   💊 #{ord[0]}: {ord[1]} - {ord[3]} {ord[2]} - {ord[4]}")
            else:
                print("❌ Aucune ordonnance dans la vue SQL")
                
    except Exception as e:
        print(f"❌ Erreur données: {e}")
    
    # Vérifier l'utilisateur pharmacien connecté
    try:
        from django.contrib.auth.models import User, Group
        pharmacien_group = Group.objects.filter(name='Pharmacien').first()
        if pharmacien_group:
            pharmaciens = User.objects.filter(groups=pharmacien_group)
            print(f"👥 Utilisateurs pharmaciens: {pharmaciens.count()}")
            
            for user in pharmaciens[:3]:
                print(f"   👤 {user.username} - {user.first_name} {user.last_name}")
        else:
            print("❌ Groupe 'Pharmacien' non trouvé")
            
    except Exception as e:
        print(f"❌ Erreur utilisateurs: {e}")

def diagnostic_urls():
    """Diagnostic des URLs"""
    print("\n🌐 4. DIAGNOSTIC URLS")
    
    try:
        from django.urls import resolve, reverse
        from django.test import RequestFactory
        
        # Vérifier si l'URL est configurée
        try:
            url_match = resolve('/pharmacien/ordonnances/')
            print(f"✅ URL résolue: {url_match}")
            print(f"   Vue: {url_match.func}")
            print(f"   Arguments: {url_match.args}")
            print(f"   Kwargs: {url_match.kwargs}")
        except Exception as e:
            print(f"❌ URL non résolue: {e}")
            
        # Vérifier la configuration URLs
        try:
            from mutuelle_core import urls
            print("✅ Module URLs chargé")
            
            # Vérifier les patterns
            for pattern in urls.urlpatterns:
                if hasattr(pattern, 'pattern'):
                    pattern_str = str(pattern.pattern)
                    if 'pharmacien' in pattern_str:
                        print(f"   🔗 Pattern pharmacien: {pattern_str}")
                        
        except Exception as e:
            print(f"❌ Erreur URLs: {e}")
            
    except Exception as e:
        print(f"❌ Erreur diagnostic URLs: {e}")

def analyser_template_direct():
    """Analyse directe du template"""
    print("\n🔍 5. ANALYSE DIRECTE TEMPLATE")
    
    # Chercher et analyser le template
    template_path = None
    for path in [
        BASE_DIR / 'pharmacien' / 'templates' / 'pharmacien' / 'ordonnances.html',
        BASE_DIR / 'templates' / 'pharmacien' / 'ordonnances.html',
        BASE_DIR / 'pharmacien' / 'templates' / 'ordonnances.html',
    ]:
        if path.exists():
            template_path = path
            break
    
    if template_path:
        print(f"✅ Template trouvé: {template_path}")
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Analyser la structure
            print("\n📝 ANALYSE DU TEMPLATE:")
            
            # Vérifier l'extension
            if '{% extends' in content:
                print("✅ Template étend un base.html")
            else:
                print("❌ Template n'étend pas de base")
            
            # Vérifier le titre
            if '<title>' in content:
                title_start = content.find('<title>') + 7
                title_end = content.find('</title>')
                title = content[title_start:title_end].strip()
                print(f"📌 Titre: {title}")
            
            # Vérifier la boucle des ordonnances
            if 'for' in content and 'in' in content:
                # Extraire la boucle
                for_start = content.find('{% for')
                for_end = content.find('{% endfor %}') + 12
                if for_start != -1 and for_end != -1:
                    boucle = content[for_start:for_end]
                    print(f"🔄 Boucle détectée:")
                    print(f"   {boucle[:100]}...")
                    
                    # Vérifier la variable de boucle
                    if 'ordonnances' in boucle:
                        print("✅ Variable 'ordonnances' utilisée dans la boucle")
                    else:
                        print("❌ Variable 'ordonnances' non trouvée dans la boucle")
            else:
                print("❌ Aucune boucle for détectée")
            
            # Vérifier la section empty
            if '{% empty %}' in content:
                print("✅ Section 'empty' présente (message si liste vide)")
                empty_start = content.find('{% empty %}') + 11
                empty_end = content.find('{% endfor %}')
                empty_content = content[empty_start:empty_end].strip()
                print(f"   Message empty: {empty_content[:100]}...")
            else:
                print("❌ Section 'empty' absente")
                
            # Vérifier l'affichage des données
            variables_affichees = []
            for var in ['numero', 'patient_nom', 'medicaments', 'date_prescription']:
                if var in content:
                    variables_affichees.append(var)
            
            if variables_affichees:
                print(f"✅ Variables affichées: {variables_affichees}")
            else:
                print("❌ Aucune variable d'ordonnance affichée")
                
        except Exception as e:
            print(f"❌ Erreur analyse template: {e}")
    else:
        print("❌ Template ordonnances.html non trouvé")

def main():
    """Fonction principale"""
    print("🚀 DIAGNOSTIC COMPLET - TEMPLATE PHARMACIEN")
    print("=" * 60)
    
    try:
        diagnostic_complet()
        analyser_template_direct()
        
        print(f"\n🎯 RÉCAPITULATIF DU DIAGNOSTIC:")
        print("💡 Prochaines étapes de correction...")
        
    except Exception as e:
        print(f"💥 ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())