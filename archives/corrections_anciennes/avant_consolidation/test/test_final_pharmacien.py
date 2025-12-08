#!/usr/bin/env python
"""
TEST FINAL - INTERFACE PHARMACIEN COMPLÈTE
"""
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_final():
    """Test final complet de l'interface pharmacien"""
    print("🚀 TEST FINAL - INTERFACE PHARMACIEN COMPLÈTE")
    print("=" * 60)
    
    # 1. Vérifier tous les templates
    print("1. 📄 VÉRIFICATION DES TEMPLATES:")
    templates_essentiels = [
        ('base_pharmacien.html', 'Template de base'),
        ('liste_ordonnances.html', 'Template des ordonnances'),
        ('_navbar_pharmacien.html', 'Navigation'),
        ('_sidebar_pharmacien.html', 'Sidebar'),
        ('_sidebar_mobile.html', 'Sidebar mobile'),
    ]
    
    for template, description in templates_essentiels:
        path = BASE_DIR / 'templates' / 'pharmacien' / template
        if path.exists():
            size = path.stat().st_size
            status = "✅" if size > 100 else "⚠️"
            print(f"   {status} {template}: {description} ({size} octets)")
        else:
            print(f"   ❌ {template}: {description} - MANQUANT")
    
    # 2. Vérifier le contenu du template liste_ordonnances
    print("\n2. 🔍 ANALYSE DU TEMPLATE liste_ordonnances.html:")
    liste_path = BASE_DIR / 'templates' / 'pharmacien' / 'liste_ordonnances.html'
    if liste_path.exists():
        with open(liste_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = [
            ('{% extends', 'Héritage du template de base'),
            ('{% block content', 'Block content défini'),
            ('ordonnances', 'Variable ordonnances utilisée'),
            ('{% for', 'Boucle for présente'),
            ('{% empty', 'Section empty présente'),
            ('MED-ORD-001', 'Données de test incluses'),
        ]
        
        for check, description in checks:
            if check in content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description}")
    else:
        print("   ❌ Template liste_ordonnances.html non trouvé")
    
    # 3. Vérifier les données SQL
    print("\n3. 📊 VÉRIFICATION DES DONNÉES:")
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            # Vérifier la vue
            cursor.execute("SELECT COUNT(*) FROM pharmacien_ordonnances_view")
            count_vue = cursor.fetchone()[0]
            print(f"   ✅ Vue SQL: {count_vue} ordonnances")
            
            # Vérifier le contenu
            if count_vue > 0:
                cursor.execute("""
                    SELECT ordonnance_id, numero, patient_nom, patient_prenom, medicaments 
                    FROM pharmacien_ordonnances_view 
                    LIMIT 3
                """)
                ordonnances = cursor.fetchall()
                print("   📋 Contenu de la vue:")
                for ord in ordonnances:
                    print(f"      💊 #{ord[0]}: {ord[1]} - {ord[3]} {ord[2]} - {ord[4]}")
            else:
                print("   ❌ Vue SQL vide")
                
    except Exception as e:
        print(f"   ❌ Erreur données SQL: {e}")
    
    # 4. Tester la vue Django
    print("\n4. 🔧 TEST DE LA VUE DJANGO:")
    try:
        from pharmacien.views import liste_ordonnances_attente
        from django.test import RequestFactory
        from django.contrib.auth.models import User
        
        factory = RequestFactory()
        request = factory.get('/pharmacien/ordonnances/')
        request.user = User.objects.filter(username='GLORIA1').first()
        
        if request.user:
            print(f"   ✅ Utilisateur de test: {request.user.username}")
            
            # Appeler la vue
            response = liste_ordonnances_attente(request)
            print(f"   ✅ Vue exécutée - Status: {response.status_code}")
            
            # Analyser la réponse
            if hasattr(response, 'template_name'):
                print(f"   ✅ Template utilisé: {response.template_name}")
            
            if hasattr(response, 'context_data'):
                context = response.context_data
                print(f"   📊 Contexte disponible: {list(context.keys())}")
                
                if 'ordonnances' in context:
                    ordonnances = context['ordonnances']
                    print(f"   💊 Ordonnances dans contexte: {len(ordonnances)}")
                else:
                    print("   ❌ 'ordonnances' pas dans le contexte")
            else:
                print("   ℹ️  Pas de contexte_data (peut être normal)")
                
        else:
            print("   ❌ Utilisateur GLORIA1 non trouvé")
            
    except Exception as e:
        print(f"   ❌ Erreur test vue: {e}")
    
    # 5. Recommandations finales
    print("\n5. 🎯 DIAGNOSTIC FINAL:")
    
    # Vérifier le template base
    base_path = BASE_DIR / 'templates' / 'pharmacien' / 'base_pharmacien.html'
    if base_path.exists():
        with open(base_path, 'r', encoding='utf-8') as f:
            base_content = f.read()
        
        if 'liste_ordonnances' in base_content:
            print("   ✅ Le template base référence liste_ordonnances")
        else:
            print("   ℹ️  Le template base ne référence pas spécifiquement liste_ordonnances")
    
    print(f"\n🎉 TEST FINAL TERMINÉ!")
    print("\n🚀 POUR TESTER L'INTERFACE:")
    print("   1. python manage.py runserver")
    print("   2. http://127.0.0.1:8000/pharmacien/ordonnances/")
    print("   3. Connectez-vous avec l'utilisateur pharmacien")

if __name__ == "__main__":
    test_final()