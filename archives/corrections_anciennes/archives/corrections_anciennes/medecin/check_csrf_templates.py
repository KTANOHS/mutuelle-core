# medecin/check_csrf_templates.py
import os
import re

def verifier_csrf_templates():
    """Vérifie tous les templates pour les tokens CSRF"""
    
    print("🔍 VÉRIFICATION CSRF DANS LES TEMPLATES")
    print("=" * 60)
    
    templates_dir = 'medecin/templates'
    
    if not os.path.exists(templates_dir):
        print(f"❌ Répertoire non trouvé: {templates_dir}")
        return
    
    problemes = {}
    
    for fichier in os.listdir(templates_dir):
        if fichier.endswith('.html'):
            chemin = os.path.join(templates_dir, fichier)
            
            with open(chemin, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Trouver tous les formulaires POST
            forms_post = re.findall(r'<form[^>]*method=["\']post["\'][^>]*>', content, re.IGNORECASE)
            
            forms_sans_csrf = []
            
            for form in forms_post:
                # Extraire plus de contexte autour du formulaire
                form_start = content.find(form)
                form_end = content.find('</form>', form_start)
                form_content = content[form_start:form_end] if form_end != -1 else content[form_start:form_start+500]
                
                if '{% csrf_token %}' not in form_content:
                    forms_sans_csrf.append(form[:100] + '...')
            
            if forms_sans_csrf:
                problemes[fichier] = forms_sans_csrf
                print(f"❌ {fichier}: {len(forms_sans_csrf)} formulaire(s) sans CSRF")
                for form in forms_sans_csrf[:2]:  # Montrer max 2 exemples
                    print(f"   └─ {form}")
            else:
                if forms_post:
                    print(f"✅ {fichier}: {len(forms_post)} formulaire(s) avec CSRF")
                else:
                    print(f"ℹ️  {fichier}: Aucun formulaire POST")
    
    if problemes:
        print(f"\n🚨 {len(problemes)} TEMPLATES AVEC PROBLÈMES CSRF:")
        for template, forms in problemes.items():
            print(f"   - {template}: {len(forms)} formulaire(s) sans CSRF")
        
        print(f"\n💡 CORRECTIONS REQUISES:")
        print("   Ajoutez {% csrf_token %} dans chaque formulaire POST:")
        print("   <form method=\"post\">")
        print("       {% csrf_token %}  <!-- ⬅️ AJOUTER CETTE LIGNE -->")
        print("       ... autres champs ...")
        print("   </form>")
    else:
        print(f"\n🎉 TOUS LES TEMPLATES ONT LES CSRF TOKENS!")

# Exécution:
# python manage.py shell
# >>> from medecin.check_csrf_templates import verifier_csrf_templates
# >>> verifier_csrf_templates()