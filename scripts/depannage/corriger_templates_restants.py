# corriger_templates_restants.py
import os

def corriger_templates_restants():
    print("🔧 CORRECTION DES TEMPLATES RESTANTS")
    print("=" * 50)
    
    templates_a_corriger = [
        '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/agents/creer_bon_soin.html',
        '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/agents/error.html'
    ]
    
    for template_path in templates_a_corriger:
        if not os.path.exists(template_path):
            print(f"⚠️  Template non trouvé: {template_path}")
            continue
            
        with open(template_path, 'r') as f:
            content = f.read()
        
        # Compter les occurrences avant
        avant = content.count('tableau_de_bord_agent')
        
        # Remplacer
        nouveau_content = content.replace(
            "{% url 'agents:tableau_de_bord_agent' %}", 
            "{% url 'agents:dashboard' %}"
        )
        nouveau_content = nouveau_content.replace(
            '{% url "agents:tableau_de_bord_agent" %}', 
            '{% url "agents:dashboard" %}'
        )
        
        # Compter les occurrences après
        apres = nouveau_content.count('tableau_de_bord_agent')
        
        if content != nouveau_content:
            with open(template_path, 'w') as f:
                f.write(nouveau_content)
            print(f"✅ {template_path}")
            print(f"   📊 {avant} → {apres} occurrence(s)")
        else:
            print(f"⚠️  Aucun changement: {template_path}")

def verifier_correction_templates():
    print("\n🔍 VÉRIFICATION APRÈS CORRECTION")
    print("=" * 40)
    
    templates_a_verifier = [
        '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/agents/base_agent.html',
        '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/agents/creer_bon_soin.html',
        '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/agents/error.html',
        '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/agents/dashboard.html'
    ]
    
    tous_corriges = True
    
    for template_path in templates_a_verifier:
        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                content = f.read()
            
            occurrences = content.count('tableau_de_bord_agent')
            if occurrences == 0:
                print(f"✅ {os.path.basename(template_path)}: Aucune occurrence")
            else:
                print(f"❌ {os.path.basename(template_path)}: {occurrences} occurrence(s)")
                tous_corriges = False
        else:
            print(f"⚠️  {template_path}: Non trouvé")
    
    return tous_corriges

if __name__ == "__main__":
    # Corriger les templates restants
    corriger_templates_restants()
    
    # Vérifier la correction
    tous_corriges = verifier_correction_templates()
    
    if tous_corriges:
        print("\n🎉 TOUS LES TEMPLATES SONT CORRIGÉS !")
        print("\n✅ Redémarrez le serveur et testez:")
        print("   python manage.py runserver")
        print("   http://localhost:8000/agents/tableau-de-bord/")
    else:
        print("\n❌ Il reste des templates à corriger manuellement")