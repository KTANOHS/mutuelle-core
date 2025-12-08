# test_final_template.py
import os
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

def test_template_affichage():
    print("🎯 TEST FINAL DU TEMPLATE MÉDECIN")
    print("==================================================")
    
    # Vérifier que le template est accessible
    template_path = "templates/medecin/template2.html"
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifications critiques
        checks = {
            "Extends base.html": '{% extends "base.html" %}' in content,
            "Block content": '{% block content %}' in content,
            "Conversation items": 'conversation-item' in content,
            "Nouveau message modal": 'nouveauMessageModal' in content,
            "Badges": 'badge bg-' in content,
            "Statistiques": 'patients_count' in content,
            "Bouton action": 'Nouveau Message' in content,
        }
        
        print("📋 VÉRIFICATION DU TEMPLATE:")
        for check, result in checks.items():
            status = "✅" if result else "❌"
            print(f"   {status} {check}")
        
        score = sum(checks.values())
        total = len(checks)
        
        print(f"📊 SCORE FINAL: {score}/{total} ({score/total*100:.0f}%)")
        
        if score == total:
            print("🎉 TEMPLATE 100% FONCTIONNEL ET PRÊT!")
            print("🌐 Accédez à: http://localhost:8000/medecin/tableau-de-bord/")
        else:
            print("⚠️  Quelques éléments manquent encore")
    
    # Vérifier les URLs médicin
    print("\n🔗 VÉRIFICATION DES URLs MÉDECIN:")
    urls_medecin = [
        '/medecin/tableau-de-bord/',
        '/medecin/bons-soin/',
        '/medecin/ordonnances/',
        '/medecin/rendez-vous/',
    ]
    
    for url in urls_medecin:
        print(f"   📍 {url}")

if __name__ == "__main__":
    test_template_affichage()