#!/usr/bin/env python3
"""
VÉRIFICATION FINALE - Test complet après correction
"""

import requests
import time
import sys

def test_dashboard_access():
    """Test l'accès au dashboard après correction"""
    
    print("🧪 TEST DU DASHBOARD APRÈS CORRECTION")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    dashboard_url = f"{base_url}/agents/tableau-de-bord/"
    
    try:
        print(f"🔗 Test de l'URL: {dashboard_url}")
        
        # Faire une requête GET
        response = requests.get(dashboard_url, timeout=10)
        
        print(f"📊 Statut HTTP: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCÈS: La page charge correctement !")
            
            # Vérifier le contenu de la réponse
            if "Taux conformité" in response.text:
                print("✅ Le contenu 'Taux conformité' est présent")
            
            if "stats.pourcentage_conformite" in response.text:
                print("❌ ATTENTION: La variable template est visible dans le HTML")
            else:
                print("✅ La variable template est correctement rendue")
            
            # Vérifier l'absence d'erreurs
            if "TemplateSyntaxError" in response.text:
                print("🚨 ERREUR: TemplateSyntaxError toujours présente !")
                return False
            else:
                print("✅ Aucune TemplateSyntaxError détectée")
                return True
                
        elif response.status_code == 302:
            print("⚠️  Redirection détectée - Vérifiez la connexion")
            return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
            
    except requests.ConnectionError:
        print("❌ Impossible de se connecter au serveur")
        print("💡 Assurez-vous que le serveur tourne: python manage.py runserver")
        return False
    except requests.Timeout:
        print("❌ Timeout - Le serveur ne répond pas")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def verifier_template_final():
    """Vérification finale du template corrigé"""
    
    print("\n🔍 VÉRIFICATION DU TEMPLATE CORRIGÉ")
    print("=" * 50)
    
    template_path = 'templates/agents/dashboard.html'
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier que l'ancienne syntaxe est absente
        anciennes_syntaxes = [
            r'\(\s*\(\s*stats\.membres_a_jour\s*/\s*stats\.membres_actifs\s*\)\s*\*\s*100\s*\)\s*\|\s*floatformat:0',
            r'\|\s*\(\(.*\*.*100\)',
            r'stats\.membres_a_jour.*stats\.membres_actifs.*floatformat'
        ]
        
        erreurs_trouvees = False
        for pattern in anciennes_syntaxes:
            import re
            if re.search(pattern, content):
                print(f"🚨 ANCIENNE SYNTAXE TROUVÉE: {pattern}")
                erreurs_trouvees = True
        
        if not erreurs_trouvees:
            print("✅ Aucune ancienne syntaxe problématique")
        
        # Vérifier que la nouvelle syntaxe est présente
        if 'stats.pourcentage_conformite' in content:
            print("✅ Nouvelle syntaxe 'stats.pourcentage_conformite' présente")
            
            # Compter les occurrences
            count = content.count('stats.pourcentage_conformite')
            print(f"📊 Occurrences de 'stats.pourcentage_conformite': {count}")
        else:
            print("❌ Nouvelle syntaxe absente !")
            erreurs_trouvees = True
        
        # Vérifier la section spécifique
        if 'Taux conformité' in content:
            print("✅ Section 'Taux conformité' trouvée")
            
            # Extraire la section pour vérification
            start = content.find('Taux conformité')
            end = content.find('</div>', start) + 6
            section = content[start:end]
            
            if 'stats.pourcentage_conformite' in section:
                print("✅ Correction appliquée dans la section Taux conformité")
            else:
                print("❌ Correction NON appliquée dans la section Taux conformité")
                erreurs_trouvees = True
        else:
            print("❌ Section 'Taux conformité' non trouvée")
            erreurs_trouvees = True
        
        return not erreurs_trouvees
        
    except FileNotFoundError:
        print(f"❌ Template non trouvé: {template_path}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def vider_cache_complet():
    """Vider tout le cache Django"""
    
    print("\n🗑️  NETTOYAGE COMPLET DU CACHE")
    print("=" * 50)
    
    import os
    import glob
    
    # Supprimer les caches
    cache_dirs = [
        '__pycache__',
        'agents/__pycache__',
        'templates/__pycache__',
        'membres/__pycache__',
        'core/__pycache__',
        'soins/__pycache__',
        'paiements/__pycache__',
        'medecin/__pycache__',
        'pharmacien/__pycache__',
        'assureur/__pycache__'
    ]
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            os.system(f'rm -rf {cache_dir}')
            print(f"✅ Cache supprimé: {cache_dir}")
    
    # Supprimer les fichiers .pyc
    pyc_files = glob.glob('**/*.pyc', recursive=True)
    for pyc_file in pyc_files:
        os.remove(pyc_file)
        print(f"✅ Fichier .pyc supprimé: {pyc_file}")
    
    print(f"📊 Total fichiers .pyc supprimés: {len(pyc_files)}")

if __name__ == "__main__":
    print("🎯 VÉRIFICATION FINALE APRÈS CORRECTION")
    print("=" * 60)
    
    # 1. Vérifier le template
    template_ok = verifier_template_final()
    
    # 2. Vider le cache (au cas où)
    vider_cache_complet()
    
    # 3. Tester l'accès (si le serveur tourne)
    print("\n🌐 TEST D'ACCÈS AU DASHBOARD")
    print("=" * 50)
    print("💡 Assurez-vous que le serveur tourne dans un autre terminal")
    print("   Commande: python manage.py runserver")
    print("")
    
    input("Appuyez sur Entrée quand le serveur est démarré...")
    
    access_ok = test_dashboard_access()
    
    # 4. Résumé final
    print("\n📊 RAPPORT FINAL")
    print("=" * 50)
    
    if template_ok and access_ok:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ Template corrigé avec succès")
        print("✅ Dashboard accessible sans erreur")
        print("")
        print("🚀 Votre application fonctionne maintenant correctement !")
    else:
        print("❌ PROBLEMES RÉSIDUELS")
        if not template_ok:
            print("   - Le template n'est pas complètement corrigé")
        if not access_ok:
            print("   - L'accès au dashboard échoue")
        print("")
        print("🔧 Vérifiez manuellement le template et redémarrez le serveur")