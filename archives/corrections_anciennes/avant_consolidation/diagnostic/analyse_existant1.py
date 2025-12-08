#!/usr/bin/env python
"""
ANALYSE DU TEMPLATE ET VUE EXISTANTS
"""
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyser_template_existant():
    """Analyse le template liste_ordonnances.html existant"""
    print("🔍 ANALYSE DU TEMPLATE EXISTANT")
    print("=" * 50)
    
    template_path = BASE_DIR / 'templates' / 'pharmacien' / 'liste_ordonnances.html'
    
    if template_path.exists():
        print(f"✅ Template trouvé: {template_path}")
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print("\n📝 CONTENU DU TEMPLATE (premières 50 lignes):")
            print("=" * 40)
            
            lines = content.split('\n')
            for i, line in enumerate(lines[:50]):
                print(f"{i+1:3d}: {line}")
            
            # Analyse critique
            print("\n🔍 ANALYSE CRITIQUE:")
            
            # Vérifier l'extension
            if '{% extends' in content:
                print("✅ Template étend un base")
            else:
                print("❌ Template n'étend pas de base")
            
            # Vérifier la variable ordonnances
            if 'ordonnances' in content:
                print("✅ Variable 'ordonnances' trouvée")
            else:
                print("❌ Variable 'ordonnances' NON trouvée")
                
            # Vérifier la boucle
            if '{% for' in content and 'ordonnance' in content:
                print("✅ Boucle for détectée")
            else:
                print("❌ Aucune boucle for")
                
            # Vérifier empty
            if '{% empty %}' in content:
                print("✅ Section empty présente")
            else:
                print("❌ Section empty absente")
                
        except Exception as e:
            print(f"❌ Erreur lecture template: {e}")
    else:
        print(f"❌ Template non trouvé: {template_path}")

def analyser_vue_existante():
    """Analyse la vue Django existante"""
    print("\n📋 ANALYSE DE LA VUE EXISTANTE")
    print("=" * 40)
    
    try:
        views_path = BASE_DIR / 'pharmacien' / 'views.py'
        
        if views_path.exists():
            with open(views_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print("📝 CODE DE LA VUE liste_ordonnances_attente:")
            print("-" * 40)
            
            # Extraire la fonction
            if 'def liste_ordonnances_attente' in content:
                start = content.find('def liste_ordonnances_attente')
                end = content.find('def ', start + 1)
                if end == -1:
                    end = len(content)
                
                fonction = content[start:end]
                for line in fonction.split('\n'):
                    print(f"   {line}")
                
                # Analyse
                if 'Ordonnance.objects.filter' in fonction:
                    print("\n🔍 La vue utilise Ordonnance.objects.filter()")
                elif 'pharmacien_ordonnances_view' in fonction:
                    print("\n🔍 La vue utilise pharmacien_ordonnances_view")
                else:
                    print("\n🔍 Source des données non identifiée")
                    
            else:
                print("❌ Fonction liste_ordonnances_attente non trouvée")
                
        else:
            print("❌ Fichier views.py non trouvé")
            
    except Exception as e:
        print(f"❌ Erreur analyse vue: {e}")

def tester_vue_actuelle():
    """Teste la vue actuelle"""
    print("\n🧪 TEST DE LA VUE ACTUELLE")
    print("=" * 40)
    
    try:
        from pharmacien.views import liste_ordonnances_attente
        from django.test import RequestFactory
        from django.contrib.auth.models import User
        
        # Créer une requête
        factory = RequestFactory()
        request = factory.get('/pharmacien/ordonnances/')
        request.user = User.objects.filter(username='GLORIA1').first()
        
        if request.user:
            print(f"✅ Utilisateur de test: {request.user.username}")
            
            # Appeler la vue
            response = liste_ordonnances_attente(request)
            print(f"✅ Vue exécutée - Status: {response.status_code}")
            
            # Analyser la réponse
            if hasattr(response, 'context_data'):
                context = response.context_data
                print(f"📊 Contexte: {list(context.keys())}")
                
                if 'ordonnances' in context:
                    ordonnances = context['ordonnances']
                    print(f"💊 Ordonnances dans contexte: {len(ordonnances)}")
                    
                    for i, ord in enumerate(ordonnances[:3]):
                        print(f"   {i+1}. {getattr(ord, 'numero', 'N/A')}")
                else:
                    print("❌ 'ordonnances' pas dans le contexte")
            else:
                print("ℹ️  Pas de contexte_data disponible")
                
        else:
            print("❌ Utilisateur GLORIA1 non trouvé")
            
    except Exception as e:
        print(f"❌ Erreur test vue: {e}")

def verifier_donnees_sql():
    """Vérifie les données directement en SQL"""
    print("\n🗄️  VÉRIFICATION DONNÉES SQL")
    print("=" * 40)
    
    from django.db import connection
    
    try:
        with connection.cursor() as cursor:
            # Vérifier la vue
            cursor.execute("SELECT COUNT(*) FROM pharmacien_ordonnances_view")
            count_vue = cursor.fetchone()[0]
            print(f"✅ Vue SQL: {count_vue} ordonnances")
            
            if count_vue > 0:
                cursor.execute("SELECT ordonnance_id, numero, patient_nom, medicaments FROM pharmacien_ordonnances_view LIMIT 3")
                for row in cursor.fetchall():
                    print(f"   💊 #{row[0]}: {row[1]} - {row[2]} - {row[3]}")
                    
            # Vérifier la table medecin_ordonnance
            cursor.execute("SELECT COUNT(*) FROM medecin_ordonnance")
            count_table = cursor.fetchone()[0]
            print(f"✅ Table medecin_ordonnance: {count_table} ordonnances")
            
    except Exception as e:
        print(f"❌ Erreur SQL: {e}")

def main():
    """Fonction principale"""
    print("🚀 ANALYSE COMPLÈTE - TEMPLATE ET VUE EXISTANTS")
    print("=" * 60)
    
    analyser_template_existant()
    analyser_vue_existante()
    tester_vue_actuelle()
    verifier_donnees_sql()
    
    print(f"\n🎯 DIAGNOSTIC TERMINÉ")

if __name__ == "__main__":
    sys.exit(main())