#!/usr/bin/env python3
"""
SCRIPT DE CORRECTION COMPLÈTE - TEMPLATE BASE_AGENT
"""

import os
import re

def corriger_template_base_agent():
    """Corrige toutes les références dans base_agent.html"""
    template_path = 'templates/agents/base_agent.html'
    
    print("🔧 CORRECTION DU TEMPLATE BASE_AGENT.HTML")
    print("=" * 50)
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Compter les occurrences avant correction
        count_tableau_de_bord = content.count("agents:tableau_de_bord")
        count_condition = content.count("url_name == 'tableau_de_bord'")
        
        print(f"📊 Avant correction:")
        print(f"   - Références à 'agents:tableau_de_bord': {count_tableau_de_bord}")
        print(f"   - Conditions 'tableau_de_bord': {count_condition}")
        
        # Appliquer les corrections
        content = content.replace("{% url 'agents:tableau_de_bord' %}", "{% url 'agents:tableau_de_bord_agent' %}")
        content = content.replace("url_name == 'tableau_de_bord'", "url_name == 'tableau_de_bord_agent'")
        
        # Compter après correction
        count_tableau_de_bord_after = content.count("agents:tableau_de_bord")
        count_tableau_de_bord_agent_after = content.count("agents:tableau_de_bord_agent")
        
        print(f"📊 Après correction:")
        print(f"   - Références à 'agents:tableau_de_bord': {count_tableau_de_bord_after}")
        print(f"   - Références à 'agents:tableau_de_bord_agent': {count_tableau_de_bord_agent_after}")
        
        # Sauvegarder les corrections
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Template base_agent.html corrigé avec succès!")
        
        return count_tableau_de_bord_after == 0
        
    except Exception as e:
        print(f"❌ Erreur correction template: {e}")
        return False

def verifier_correction_appliquee():
    """Vérifie que la correction a été appliquée"""
    print("\n🔍 VÉRIFICATION DE LA CORRECTION")
    print("=" * 30)
    
    try:
        with open('templates/agents/base_agent.html', 'r') as f:
            content = f.read()
        
        # Vérifier la ligne problématique
        if "{% url 'agents:tableau_de_bord_agent' %}" in content:
            print("✅ Correction appliquée: agents:tableau_de_bord_agent")
        else:
            print("❌ Correction NON appliquée")
            
        if "agents:tableau_de_bord" in content:
            print("❌ Référence incorrecte toujours présente: agents:tableau_de_bord")
            return False
        else:
            print("✅ Aucune référence incorrecte trouvée")
            return True
            
    except Exception as e:
        print(f"❌ Erreur vérification: {e}")
        return False

def main():
    print("🎯 CORRECTION COMPLÈTE DU PROBLÈME NO_REVERSE_MATCH")
    print("=" * 60)
    
    # 1. Corriger le template
    success = corriger_template_base_agent()
    
    # 2. Vérifier la correction
    if success:
        verification = verifier_correction_appliquee()
        
        if verification:
            print("\n🎉 TOUTES LES CORRECTIONS ONT ÉTÉ APPLIQUÉES!")
            print("\n🚀 PROCHAINES ÉTAPES:")
            print("   1. Le serveur va redémarrer automatiquement")
            print("   2. Testez: http://127.0.0.1:8000/agents/verification-cotisations/")
            print("   3. Testez: http://127.0.0.1:8000/agents/tableau-de-bord/")
        else:
            print("\n🚨 IL RESTE DES PROBLÈMES - Vérifiez manuellement le template")
    else:
        print("\n🚨 LA CORRECTION A ÉCHOUÉ")

if __name__ == "__main__":
    main()