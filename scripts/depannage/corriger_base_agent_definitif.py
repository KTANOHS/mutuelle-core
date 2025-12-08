# corriger_base_agent_definitif.py
import os

def corriger_base_agent_definitif():
    template_path = '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/agents/base_agent.html'
    
    print("🔧 CORRECTION DÉFINITIVE DE base_agent.html")
    print("=" * 50)
    
    if not os.path.exists(template_path):
        print("❌ Template base_agent.html non trouvé")
        return False
    
    # Lire le contenu
    with open(template_path, 'r') as f:
        content = f.read()
    
    print(f"📊 Occurrences avant: {content.count('tableau_de_bord_agent')}")
    
    # CORRECTION 1: Remplacer l'URL dans le href
    content = content.replace(
        'href="{% url \'agents:tableau_de_bord_agent\' %}"',
        'href="{% url \'agents:dashboard\' %}"'
    )
    
    # CORRECTION 2: Remplacer l'URL avec guillemets doubles
    content = content.replace(
        'href="{% url "agents:tableau_de_bord_agent" %}"',
        'href="{% url "agents:dashboard" %}"'
    )
    
    # CORRECTION 3: Remplacer la condition active
    content = content.replace(
        "request.resolver_match.url_name == 'tableau_de_bord_agent'",
        "request.resolver_match.url_name == 'dashboard'"
    )
    
    # CORRECTION 4: Remplacer toute occurrence restante
    content = content.replace(
        "tableau_de_bord_agent",
        "dashboard"
    )
    
    # Écrire le contenu corrigé
    with open(template_path, 'w') as f:
        f.write(content)
    
    # Vérifier
    with open(template_path, 'r') as f:
        new_content = f.read()
    
    print(f"📊 Occurrences après: {new_content.count('tableau_de_bord_agent')}")
    
    if new_content.count('tableau_de_bord_agent') == 0:
        print("✅ base_agent.html corrigé avec succès !")
        return True
    else:
        print("❌ Il reste des occurrences non corrigées")
        return False

def afficher_lignes_problematiques():
    template_path = '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/agents/base_agent.html'
    
    print("\n🔍 LIGNES PROBLÉMATIQUES:")
    print("-" * 30)
    
    with open(template_path, 'r') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, 1):
        if 'tableau_de_bord_agent' in line:
            print(f"Ligne {i}: {line.strip()}")

def verifier_correction_complete():
    print("\n✅ VÉRIFICATION FINALE")
    print("=" * 30)
    
    templates = [
        '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/agents/base_agent.html',
        '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/agents/dashboard.html',
        '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/agents/creer_bon_soin.html',
        '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/agents/error.html'
    ]
    
    tous_corriges = True
    
    for template in templates:
        if os.path.exists(template):
            with open(template, 'r') as f:
                content = f.read()
            
            count = content.count('tableau_de_bord_agent')
            if count == 0:
                print(f"✅ {os.path.basename(template)}: OK")
            else:
                print(f"❌ {os.path.basename(template)}: {count} occurrence(s)")
                tous_corriges = False
        else:
            print(f"⚠️  {os.path.basename(template)}: Non trouvé")
    
    return tous_corriges

if __name__ == "__main__":
    # Afficher les lignes problématiques avant correction
    afficher_lignes_problematiques()
    
    # Corriger
    succes = corriger_base_agent_definitif()
    
    if succes:
        # Vérification finale
        tous_corriges = verifier_correction_complete()
        
        if tous_corriges:
            print("\n🎉 TOUS LES TEMPLATES SONT CORRIGÉS !")
            print("\n🚀 Redémarrez le serveur et testez:")
            print("   python manage.py runserver")
            print("   http://localhost:8000/agents/tableau-de-bord/")
        else:
            print("\n❌ Il reste des templates à corriger")
    else:
        print("\n❌ La correction a échoué")