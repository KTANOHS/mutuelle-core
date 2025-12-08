#!/usr/bin/env python
"""
DIAGNOSTIC FINAL - POURQUOI LES ORDONNANCES N'APPARAISSENT PAS ?
"""
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostic_complet():
    """Diagnostic complet du problème"""
    print("🚀 DIAGNOSTIC FINAL - INTERFACE PHARMACIEN")
    print("=" * 60)
    
    # 1. Vérifier l'état des templates
    print("1. 📄 ÉTAT DES TEMPLATES:")
    templates = [
        'base_pharmacien.html',
        'liste_ordonnances.html', 
        '_navbar_pharmacien.html',
        '_sidebar_pharmacien.html',
        '_sidebar_mobile.html'
    ]
    
    for template in templates:
        path = BASE_DIR / 'templates' / 'pharmacien' / template
        if path.exists():
            size = path.stat().st_size
            status = "✅" if size > 100 else "⚠️"
            print(f"   {status} {template} ({size} octets)")
        else:
            print(f"   ❌ {template} MANQUANT")
    
    # 2. Analyser le contenu de liste_ordonnances.html
    print("\n2. 🔍 ANALYSE liste_ordonnances.html:")
    liste_path = BASE_DIR / 'templates' / 'pharmacien' / 'liste_ordonnances.html'
    
    if liste_path.exists():
        with open(liste_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifications critiques
        checks = [
            ('{% extends', 'Héritage base_pharmacien.html'),
            ('{% block content', 'Block content défini'),
            ('ordonnances', 'Variable ordonnances utilisée'),
            ('{% for ordonnance in ordonnances', 'Boucle for correcte'),
            ('{{ ordonnance.numero', 'Affichage numéro ordonnance'),
            ('{{ ordonnance.patient_nom', 'Affichage patient'),
            ('{% empty %}', 'Section empty présente'),
            ('Aucune ordonnance', 'Message si vide'),
        ]
        
        for check, description in checks:
            if check in content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description}")
        
        # Vérifier si c'est la version avec données forcées
        if 'MODE URGENCE' in content or 'MED-ORD-001' in content:
            print("   🔥 TEMPLATE AVEC DONNÉES FORCÉES")
        else:
            print("   📝 TEMPLATE DYNAMIQUE (dépend de la vue)")
    
    # 3. Tester la vue Django en profondeur
    print("\n3. 🔧 TEST PROFOND DE LA VUE:")
    try:
        from pharmacien.views import liste_ordonnances_attente
        from django.test import RequestFactory
        from django.contrib.auth.models import User
        import inspect
        
        # Afficher le code source de la vue
        print("   📝 Code de la vue liste_ordonnances_attente:")
        source = inspect.getsource(liste_ordonnances_attente)
        for line in source.split('\n')[:15]:  # Premières 15 lignes
            print(f"      {line}")
        
        # Tester l'exécution
        factory = RequestFactory()
        request = factory.get('/pharmacien/ordonnances/')
        request.user = User.objects.filter(username='GLORIA1').first()
        
        if request.user:
            print(f"   👤 Utilisateur: {request.user.username}")
            
            # Exécuter la vue
            response = liste_ordonnances_attente(request)
            print(f"   📊 Status: {response.status_code}")
            
            # Analyser la réponse
            if hasattr(response, 'context_data'):
                context = response.context_data
                print(f"   🎯 Contexte: {list(context.keys())}")
                
                if 'ordonnances' in context:
                    ordonnances = context['ordonnances']
                    print(f"   💊 Ordonnances: {len(ordonnances)} éléments")
                    
                    # Afficher les détails des premières ordonnances
                    for i, ord in enumerate(ordonnances[:2]):
                        print(f"      {i+1}. {getattr(ord, 'numero', 'N/A')}")
                else:
                    print("   ❌ 'ordonnances' manquant dans le contexte")
            else:
                print("   ℹ️  Pas de contexte_data (TemplateResponse)")
                
        else:
            print("   ❌ Utilisateur GLORIA1 non trouvé")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # 4. Vérifier les données SQL directement
    print("\n4. 🗄️  DONNÉES SQL DIRECTES:")
    from django.db import connection
    
    try:
        with connection.cursor() as cursor:
            # Vérifier la vue
            cursor.execute("SELECT COUNT(*) FROM pharmacien_ordonnances_view")
            count = cursor.fetchone()[0]
            print(f"   ✅ Vue SQL: {count} ordonnances")
            
            if count > 0:
                cursor.execute("""
                    SELECT ordonnance_id, numero, patient_nom, patient_prenom, medicaments,
                           medecin_nom, medecin_prenom, date_prescription
                    FROM pharmacien_ordonnances_view 
                    LIMIT 3
                """)
                print("   📋 Contenu détaillé:")
                for row in cursor.fetchall():
                    print(f"      💊 #{row[0]}: {row[1]}")
                    print(f"         Patient: {row[3]} {row[2]}")
                    print(f"         Médecin: Dr. {row[6]} {row[5]}")
                    print(f"         Médicaments: {row[4]}")
                    print(f"         Date: {row[7]}")
                    print()
            else:
                print("   ❌ Vue SQL vide")
                
    except Exception as e:
        print(f"   ❌ Erreur SQL: {e}")
    
    # 5. Diagnostic final
    print("\n5. 🎯 DIAGNOSTIC FINAL:")
    
    # Vérifier si le template a des données codées
    if liste_path.exists():
        with open(liste_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'MED-ORD-001' in content and 'Marie Dupont' in content:
            print("   ✅ Le template a des données codées en dur")
            print("   🚀 Les ordonnances DEVRAIENT apparaître")
        else:
            print("   ❌ Le template n'a pas de données codées")
            print("   💡 Il dépend de la vue Django pour les données")
    
    print(f"\n🔧 SOLUTIONS POSSIBLES:")
    print("   1. Si template a données codées → Doit apparaître")
    print("   2. Si template dynamique → Vérifier la vue Django")
    print("   3. Si erreur 500 → Voir logs serveur")
    print("   4. Si page blanche → Problème template")
    print("   5. Si 'Aucune ordonnance' → Données manquantes")

if __name__ == "__main__":
    diagnostic_complet()