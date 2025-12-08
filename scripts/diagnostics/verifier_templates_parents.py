# verifier_templates_parents.py
import os
import re

def verifier_templates_parents():
    print("🔍 VÉRIFICATION DES TEMPLATES PARENTS")
    print("=" * 50)
    
    templates_dir = '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates'
    problemes = []
    
    # Templates à vérifier
    templates_importants = [
        'agents/base_agent.html',
        'base.html',
        'base_dashboard.html',  # Si existe
        'includes/navigation.html'  # Si existe
    ]
    
    for template in templates_importants:
        template_path = os.path.join(templates_dir, template)
        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                content = f.read()
                
            if 'tableau_de_bord_agent' in content:
                problemes.append({
                    'template': template,
                    'occurrences': content.count('tableau_de_bord_agent')
                })
                print(f"❌ {template}: {content.count('tableau_de_bord_agent')} occurrence(s)")
            else:
                print(f"✅ {template}: Aucune occurrence")
        else:
            print(f"⚠️  {template}: Non trouvé")
    
    return problemes

def corriger_template_parent(template_path):
    """Corrige un template parent spécifique"""
    with open(template_path, 'r') as f:
        content = f.read()
    
    # Remplacer les occurrences
    nouveau_content = content.replace(
        "{% url 'tableau_de_bord_agent' %}", 
        "{% url 'agents:dashboard' %}"
    )
    nouveau_content = nouveau_content.replace(
        '{% url "tableau_de_bord_agent" %}', 
        '{% url "agents:dashboard" %}'
    )
    
    with open(template_path, 'w') as f:
        f.write(nouveau_content)
    
    print(f"✅ {template_path} corrigé")

if __name__ == "__main__":
    problemes = verifier_templates_parents()
    
    if problemes:
        print(f"\n🔧 {len(problemes)} template(s) parent(s) à corriger")
        for probleme in problemes:
            template_path = os.path.join(
                '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates',
                probleme['template']
            )
            corriger_template_parent(template_path)
    else:
        print("\n🎉 Aucun problème dans les templates parents !")