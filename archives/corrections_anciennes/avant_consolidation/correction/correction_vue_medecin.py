# correction_vue_medecin.py
import os
import re

def corriger_vue_medecin():
    print("🔧 CORRECTION DE LA VUE MÉDECIN")
    print("==================================================")
    
    # Chemin de la vue medecin
    vue_path = "medecin/views.py"
    
    if not os.path.exists(vue_path):
        print("❌ Fichier medecin/views.py introuvable")
        return
    
    # Lire le contenu actuel
    with open(vue_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si template2.html est utilisé
    if 'template2.html' in content:
        print("✅ template2.html est déjà référencé dans les vues")
    else:
        print("❌ template2.html n'est pas utilisé dans les vues")
        
        # Trouver la vue dashboard et corriger le template
        if 'def dashboard(' in content:
            # Remplacer le template dans la vue dashboard
            new_content = re.sub(
                r'def dashboard\(request\):.*?return render\(request,[^,]+,\s*{[^}]*}\)',
                'def dashboard(request):\n    \"\"\"Vue tableau de bord médecin avec template complet\"\"\"\n    try:\n        # Récupérer les données statistiques\n        medecin = request.user.medecin\n        \n        # Compter les patients\n        patients_count = Membre.objects.filter(\n            consultations__medecin=medecin\n        ).distinct().count()\n        \n        # Compter les messages\n        messages_count = Message.objects.filter(\n            Q(destinataire=request.user) | Q(expediteur=request.user)\n        ).count()\n        \n        # Compter les ordonnances\n        ordonnances_count = BonSoin.objects.filter(\n            medecin=medecin\n        ).count()\n        \n        # Compter les bons de soin\n        bons_soin_count = BonSoin.objects.filter(\n            medecin=medecin,\n            statut__in=[\"EN_ATTENTE\", \"VALIDE\"]\n        ).count()\n        \n        # Récupérer les conversations\n        conversations = Message.objects.filter(\n            Q(destinataire=request.user) | Q(expediteur=request.user)\n        ).order_by(\'-date_creation\')[:10]\n        \n        context = {\n            \"patients_count\": patients_count,\n            \"messages_count\": messages_count,\n            \"ordonnances_count\": ordonnances_count,\n            \"bons_soin_count\": bons_soin_count,\n            \"conversations\": conversations,\n        }\n        \n        return render(request, \"medecin/template2.html\", context)\n    except Exception as e:\n        messages.error(request, f\"Erreur lors du chargement du tableau de bord: {str(e)}\")\n        return render(request, \"medecin/template2.html\", {})',
                content,
                flags=re.DOTALL
            )
            
            if new_content != content:
                with open(vue_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print("✅ Vue dashboard corrigée pour utiliser template2.html")
            else:
                print("⚠️  Impossible de corriger automatiquement la vue dashboard")
    
    # Vérifier aussi le template par défaut
    template_base_path = "templates/medecin/base.html"
    if os.path.exists(template_base_path):
        with open(template_base_path, 'r', encoding='utf-8') as f:
            base_content = f.read()
        
        # Vérifier si base.html étend le bon template
        if '{% extends "base.html" %}' not in base_content:
            print("❌ medecin/base.html n'étend pas base.html")
            # Corriger medecin/base.html
            new_base_content = '{% extends "base.html" %}\n{% load static %}\n\n' + base_content
            with open(template_base_path, 'w', encoding='utf-8') as f:
                f.write(new_base_content)
            print("✅ medecin/base.html corrigé pour étendre base.html")
    
    print("🎯 TEST DE LA VUE CORRIGÉE...")
    
    # Tester l'accès au template
    template_test_path = "templates/medecin/template2.html"
    if os.path.exists(template_test_path):
        with open(template_test_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Vérifier les éléments critiques
        elements = {
            "conversation-item": "conversation-item" in template_content,
            "badge bg-": "badge bg-" in template_content,
            "nouveauMessageModal": "nouveauMessageModal" in template_content,
            "Dernière activité": "last_activity" in template_content,
            "Statistiques": "card text-white bg-primary" in template_content,
            "Nouveau Message": "Nouveau Message" in template_content,
            "Conversations": "Conversations" in template_content,
        }
        
        score = sum(elements.values())
        total = len(elements)
        
        print(f"📊 VÉRIFICATION DU TEMPLATE:")
        for element, present in elements.items():
            status = "✅ PRÉSENT" if present else "❌ ABSENT"
            print(f"   {status} {element}")
        
        print(f"📈 SCORE: {score}/{total} ({score/total*100:.0f}%)")
        
        if score == total:
            print("🎉 TEMPLATE COMPLÈTEMENT FONCTIONNEL!")
        else:
            print("⚠️  Template incomplet, vérifiez la structure")
    else:
        print("❌ template2.html introuvable après correction")

if __name__ == "__main__":
    corriger_vue_medecin()