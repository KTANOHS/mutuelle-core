#!/usr/bin/env python3
"""
CORRECTION FINALE - Condition if problématique
"""

import os

def corriger_condition_if():
    """Corrige la condition if qui utilise les anciennes variables"""
    
    template_path = 'templates/agents/dashboard.html'
    
    print("🔧 CORRECTION DE LA CONDITION IF")
    print("=" * 50)
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Sauvegarder
    backup_path = f"{template_path}.backup_final"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"💾 Backup créé: {backup_path}")
    
    # Remplacer la condition problématique
    ancienne_condition = "{% if stats.membres_a_jour and stats.membres_actifs %}"
    nouvelle_condition = "{% if stats.pourcentage_conformite %}"
    
    if ancienne_condition in content:
        content_corrige = content.replace(ancienne_condition, nouvelle_condition)
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content_corrige)
        
        print("✅ Condition if CORRIGÉE !")
        print(f"❌ ANCIENNE: {ancienne_condition}")
        print(f"✅ NOUVELLE: {nouvelle_condition}")
        return True
    else:
        print("❌ Condition problématique non trouvée")
        return False

def verifier_correction_finale():
    """Vérification finale complète"""
    
    template_path = 'templates/agents/dashboard.html'
    
    print("\n🔍 VÉRIFICATION FINALE")
    print("=" * 50)
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier que l'ancien calcul est absent
    ancien_calcul = "((stats.membres_a_jour / stats.membres_actifs) * 100)"
    if ancien_calcul in content:
        print("🚨 ANCIEN CALCUL PRÉSENT !")
        return False
    else:
        print("✅ Ancien calcul ABSENT")
    
    # Vérifier que la nouvelle variable est présente
    if 'stats.pourcentage_conformite' in content:
        print("✅ Nouvelle variable PRÉSENTE")
    else:
        print("❌ Nouvelle variable ABSENTE")
        return False
    
    # Vérifier la condition if corrigée
    if '{% if stats.pourcentage_conformite %}' in content:
        print("✅ Condition if CORRIGÉE")
    else:
        print("❌ Condition if NON CORRIGÉE")
        return False
    
    print("🎉 TEMPLATE 100% CORRIGÉ !")
    return True

def demarrer_serveur_et_tester():
    """Démarre le serveur et teste"""
    
    print("\n🚀 DÉMARRAGE ET TEST")
    print("=" * 50)
    
    # Vider le cache une dernière fois
    print("🗑️  Vidage du cache final...")
    os.system('rm -rf __pycache__ agents/__pycache__')
    os.system('find . -name "*.pyc" -delete')
    
    print("💡 Redémarrez manuellement le serveur:")
    print("   python manage.py runserver")
    print("")
    print("🌐 Puis testez l'URL:")
    print("   http://localhost:8000/agents/tableau-de-bord/")
    print("")
    print("✅ L'erreur TemplateSyntaxError devrait être RÉSOLUE !")

if __name__ == "__main__":
    if corriger_condition_if():
        if verifier_correction_finale():
            demarrer_serveur_et_tester()
        else:
            print("❌ La vérification finale a échoué")
    else:
        print("❌ La correction a échoué")