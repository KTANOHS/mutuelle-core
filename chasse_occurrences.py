# chasse_occurrences.py
import os
import re

def trouver_occurrences_tableau_bord_agent():
    print("🔍 CHASSE AUX OCCURRENCES DE 'tableau_de_bord_agent'")
    print("=" * 60)
    
    dossier_projet = '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet'
    occurrences_trouvees = []
    
    # Extensions à vérifier
    extensions = ['.html', '.py', '.txt', '.md']
    
    for root, dirs, files in os.walk(dossier_projet):
        # Ignorer certains dossiers
        if 'venv' in root or '__pycache__' in root or '.git' in root:
            continue
            
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'tableau_de_bord_agent' in content:
                            # Compter les occurrences
                            count = content.count('tableau_de_bord_agent')
                            occurrences_trouvees.append({
                                'fichier': file_path,
                                'occurrences': count,
                                'lignes': []
                            })
                            
                            # Trouver les lignes spécifiques
                            lines = content.split('\n')
                            for i, line in enumerate(lines, 1):
                                if 'tableau_de_bord_agent' in line:
                                    occurrences_trouvees[-1]['lignes'].append({
                                        'numero': i,
                                        'contenu': line.strip()
                                    })
                except Exception as e:
                    print(f"⚠️  Erreur lecture {file_path}: {e}")
    
    return occurrences_trouvees

def afficher_resultats(occurrences):
    if not occurrences:
        print("✅ AUCUNE occurrence de 'tableau_de_bord_agent' trouvée !")
        return
    
    print(f"❌ {len(occurrences)} fichier(s) contiennent 'tableau_de_bord_agent':")
    print("-" * 60)
    
    for occ in occurrences:
        print(f"\n📁 {occ['fichier']}")
        print(f"   📊 {occ['occurrences']} occurrence(s)")
        
        for ligne in occ['lignes']:
            print(f"   📍 Ligne {ligne['numero']}: {ligne['contenu'][:100]}...")

def corriger_occurrences(occurrences):
    print("\n🔧 CORRECTION AUTOMATIQUE")
    print("=" * 60)
    
    corrections_effectuees = 0
    
    for occ in occurrences:
        file_path = occ['fichier']
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remplacer selon le type de fichier
            if file_path.endswith('.html'):
                # Template Django
                nouveau_content = content.replace(
                    "{% url 'tableau_de_bord_agent' %}", 
                    "{% url 'agents:dashboard' %}"
                )
                nouveau_content = nouveau_content.replace(
                    '{% url "tableau_de_bord_agent" %}', 
                    '{% url "agents:dashboard" %}'
                )
            elif file_path.endswith('.py'):
                # Code Python - reverse()
                nouveau_content = content.replace(
                    "reverse('tableau_de_bord_agent')", 
                    "reverse('agents:dashboard')"
                )
                nouveau_content = nouveau_content.replace(
                    'reverse("tableau_de_bord_agent")', 
                    'reverse("agents:dashboard")'
                )
                # Code Python - get_absolute_url ou autres
                nouveau_content = nouveau_content.replace(
                    "'tableau_de_bord_agent'", 
                    "'agents:dashboard'"
                )
                nouveau_content = nouveau_content.replace(
                    '"tableau_de_bord_agent"', 
                    '"agents:dashboard"'
                )
            else:
                # Autres fichiers
                nouveau_content = content.replace(
                    'tableau_de_bord_agent', 
                    'agents:dashboard'
                )
            
            if content != nouveau_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(nouveau_content)
                corrections_effectuees += 1
                print(f"✅ Corrigé: {file_path}")
            else:
                print(f"⚠️  Aucun changement: {file_path}")
                
        except Exception as e:
            print(f"❌ Erreur correction {file_path}: {e}")
    
    return corrections_effectuees

def main():
    # 1. Trouver les occurrences
    occurrences = trouver_occurrences_tableau_bord_agent()
    
    # 2. Afficher les résultats
    afficher_resultats(occurrences)
    
    if occurrences:
        # 3. Proposer la correction
        print(f"\n💡 {len(occurrences)} fichier(s) à corriger.")
        reponse = input("Voulez-vous corriger automatiquement ? (o/N): ")
        
        if reponse.lower() in ['o', 'oui', 'y', 'yes']:
            corrections = corriger_occurrences(occurrences)
            print(f"\n🎉 {corrections} correction(s) effectuée(s) !")
            
            # Vérifier après correction
            print("\n🔍 VÉRIFICATION APRÈS CORRECTION:")
            occurrences_restantes = trouver_occurrences_tableau_bord_agent()
            if not occurrences_restantes:
                print("✅ TOUTES les occurrences ont été corrigées !")
            else:
                print("❌ Il reste des occurrences non corrigées:")
                afficher_resultats(occurrences_restantes)
        else:
            print("\n🔧 Correction manuelle nécessaire.")
            print("Remplacez 'tableau_de_bord_agent' par 'agents:dashboard' dans les fichiers listés.")
    else:
        print("\n🎉 Le problème devrait être résolu !")

if __name__ == "__main__":
    main()