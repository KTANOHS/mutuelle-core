#!/usr/bin/env python
import os
import sys

def fix_validation_script():
    """Corriger le script final_validation.py pour passer les arguments aux URLs"""
    
    file_path = 'final_validation.py'
    
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        print("🔍 RECHERCHE DE LA SECTION DE TEST DES URLs...")
        
        # Trouver la section où les URLs sont testées
        start_marker = "🌐 TEST COMPLET DES URLs:"
        end_marker = "📊 URLs:"
        
        start_pos = content.find(start_marker)
        end_pos = content.find(end_marker, start_pos)
        
        if start_pos == -1 or end_pos == -1:
            print("❌ Impossible de trouver la section des URLs dans final_validation.py")
            return False
        
        # Extraire la section des URLs
        urls_section = content[start_pos:end_pos]
        
        # Vérifier si la correction est déjà appliquée
        if "args=[1]" in urls_section:
            print("✅ La correction est déjà appliquée")
            return True
        
        print("🔧 APPLICATION DE LA CORRECTION...")
        
        # Remplacer les appels reverse pour les URLs avec paramètres
        old_code = """        try:
            url = reverse(url_name)
            print(f"   ✅ {url_name:45} -> {url}")
            working_urls += 1"""
        
        new_code = """        try:
            # Gestion des URLs avec paramètres
            if url_name in ['agents:creer_bon_soin_membre', 'agents:confirmation_bon_soin']:
                url = reverse(url_name, args=[1])  # Argument factice pour le test
            else:
                url = reverse(url_name)
            print(f"   ✅ {url_name:45} -> {url}")
            working_urls += 1"""
        
        if old_code in content:
            content = content.replace(old_code, new_code)
            
            # Écrire le fichier corrigé
            with open(file_path, 'w') as file:
                file.write(content)
            
            print("✅ final_validation.py corrigé avec succès!")
            print("🔧 Changements appliqués:")
            print("   - ✅ Ajout de la gestion des arguments pour URLs paramétrées")
            print("   - ✅ Utilisation d'arguments factices (1) pour les tests")
            return True
        else:
            print("❌ Impossible de trouver le code à remplacer")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        return False

def create_alternative_solution():
    """Créer une version alternative si la correction directe échoue"""
    
    alternative_content = '''#!/usr/bin/env python
"""
SCRIPT DE VALIDATION CORRIGÉ - VERSION AVEC GESTION DES ARGUMENTS
Test complet du module agents avec support des URLs paramétrées
"""

import os
import sys
import django
from django.urls import reverse, NoReverseMatch

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("🎯 VALIDATION FINALE DU MODULE AGENTS - VERSION CORRIGÉE")
    print("=" * 50)
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

def test_agents_urls():
    """Tester toutes les URLs du module agents avec gestion des arguments"""
    
    print("🌐 TEST COMPLET DES URLs AVEC ARGUMENTS:")
    print("-" * 50)
    
    # Liste de toutes les URLs agents à tester
    agents_urls = [
        # Tableau de bord
        'agents:dashboard',
        'agents:verification_cotisations',
        'agents:rapport_performance',
        
        # Gestion membres
        'agents:creer_membre',
        'agents:liste_membres',
        
        # Bons de soin
        'agents:creer_bon_soin',
        'agents:creer_bon_soin_membre',  # Nécessite membre_id
        'agents:confirmation_bon_soin',  # Nécessite bon_id
        'agents:historique_bons',
        
        # APIs
        'agents:recherche_membres_api',
        'agents:verifier_cotisation_api',
        'agents:test_simple_api',
        'agents:api_recherche_membres_bon_soin',
        
        # Communication
        'agents:communication',
        'agents:liste_messages',
        'agents:liste_notifications',
        'agents:envoyer_message',
    ]
    
    working_urls = 0
    total_urls = len(agents_urls)
    
    for url_name in agents_urls:
        try:
            # Gestion des URLs avec paramètres
            if url_name == 'agents:creer_bon_soin_membre':
                url = reverse(url_name, args=[1])  # membre_id = 1
            elif url_name == 'agents:confirmation_bon_soin':
                url = reverse(url_name, args=[1])  # bon_id = 1
            else:
                url = reverse(url_name)
            
            print(f"   ✅ {url_name:45} -> {url}")
            working_urls += 1
            
        except NoReverseMatch as e:
            print(f"   ❌ {url_name:45} -> NON TROUVÉE: {e}")
        except Exception as e:
            print(f"   ❌ {url_name:45} -> ERREUR: {e}")
    
    print(f"\\n📊 URLs: {working_urls}/{total_urls} fonctionnelles")
    
    # Calcul du score
    score = (working_urls / total_urls) * 100 if total_urls > 0 else 0
    print(f"\\n🎯 SCORE FINAL: {score:.1f}%")
    
    if score == 100:
        print("   🎉 EXCELLENT! Module agents complètement fonctionnel")
    elif score >= 80:
        print("   ✅ TRÈS BON! Module agents fonctionnel")
    elif score >= 60:
        print("   ⚠️  ACCEPTABLE! Module agents avec quelques problèmes")
    else:
        print("   ❌ CRITIQUE! Module agents nécessite des corrections")
    
    return score

if __name__ == "__main__":
    test_agents_urls()
'''

    file_path = 'validation_corrigee.py'
    
    try:
        with open(file_path, 'w') as file:
            file.write(alternative_content)
        
        print(f"✅ Script de validation alternatif créé: {file_path}")
        print("💡 Exécutez-le avec: python validation_corrigee.py")
        return True
        
    except Exception as e:
        print(f"❌ Erreur création script alternatif: {e}")
        return False

if __name__ == "__main__":
    print("🔄 CORRECTION DU TEST DE VALIDATION")
    print("=" * 50)
    
    print("1️⃣  Tentative de correction de final_validation.py...")
    if fix_validation_script():
        print("\n🎯 CORRECTION RÉUSSIE!")
        print("💡 Relancez la validation:")
        print("   python final_validation.py")
    else:
        print("\n⚠️  Correction directe échouée, création d'une solution alternative...")
        if create_alternative_solution():
            print("\n🎯 SOLUTION ALTERNATIVE CRÉÉE!")
            print("💡 Exécutez la validation corrigée:")
            print("   python validation_corrigee.py")
        else:
            print("\n❌ Toutes les tentatives de correction ont échoué")