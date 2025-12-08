# analyze_agents_templates.py
import os
import re
import django
import sys

# Configuration Django
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyser_template(file_path):
    """Analyse un template Django et détecte les erreurs de syntaxe"""
    print(f"\n🔍 ANALYSE de: {file_path}")
    print("=" * 60)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {file_path}")
        return
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Détecter les tags Django non fermés
    errors = []
    
    # Vérifier les blocs if
    if_pattern = r'{%\s*if.*?%}'
    endif_pattern = r'{%\s*endif\s*%}'
    
    if_count = len(re.findall(if_pattern, content))
    endif_count = len(re.findall(endif_pattern, content))
    
    if if_count != endif_count:
        errors.append(f"❌ BALISES IF: {if_count} 'if' vs {endif_count} 'endif'")
    
    # Vérifier les blocs for
    for_pattern = r'{%\s*for.*?%}'
    endfor_pattern = r'{%\s*endfor\s*%}'
    
    for_count = len(re.findall(for_pattern, content))
    endfor_count = len(re.findall(endfor_pattern, content))
    
    if for_count != endfor_count:
        errors.append(f"❌ BALISES FOR: {for_count} 'for' vs {endfor_count} 'endfor'")
    
    # Vérifier les blocs block
    block_pattern = r'{%\s*block.*?%}'
    endblock_pattern = r'{%\s*endblock.*?%}'
    
    block_count = len(re.findall(block_pattern, content))
    endblock_count = len(re.findall(endblock_pattern, content))
    
    if block_count != endblock_count:
        errors.append(f"❌ BALISES BLOCK: {block_count} 'block' vs {endblock_count} 'endblock'")
    
    # Afficher les résultats
    if errors:
        for error in errors:
            print(error)
        
        # Afficher les lignes problématiques
        print(f"\n📋 LIGNES AVEC DES BALISES IF:")
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if '{% if' in line and '{% endif' not in line:
                print(f"   Ligne {i}: {line.strip()}")
        
        print(f"\n📋 LIGNES AVEC DES BALISES ENDIF:")
        for i, line in enumerate(lines, 1):
            if '{% endif' in line:
                print(f"   Ligne {i}: {line.strip()}")
                
    else:
        print("✅ Aucune erreur de balises détectée")

def corriger_template_base_agent():
    """Corrige le template base_agent.html spécifiquement"""
    template_path = os.path.join(project_path, 'templates/agents/base_agent.html')
    
    print(f"\n🎯 CORRECTION DU TEMPLATE: {template_path}")
    print("=" * 60)
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {template_path}")
        return
    except UnicodeDecodeError:
        with open(template_path, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Trouver la section problématique (ligne 161)
    lines = content.split('\n')
    
    print("📝 SECTION PROBLÉMATIQUE (autour de la ligne 161):")
    for i in range(155, 170):  # Afficher les lignes autour de l'erreur
        if i < len(lines):
            marker = ">>> ERREUR ICI <<<" if i == 161 else ""
            print(f"{i:3d}: {lines[i]} {marker}")
    
    # CORRECTION : Le problème est que le tag if n'est pas fermé correctement
    # La structure actuelle est incorrecte
    old_code = """                                        <!-- ✅ CORRIGÉ : Compteur de notifications -->
                                        {% if request.user.notification_set.all %}
                                    {% with unread_count=request.user.notification_set.all|length %}
                                        {% if unread_count > 0 %}
                                            <span class="badge bg-danger float-end">{{ unread_count }}</span>
                                            {% endif %}
                                        {% endwith %}"""
    
    new_code = """                                        <!-- ✅ CORRIGÉ : Compteur de notifications -->
                                        {% with unread_count=request.user.notification_set.unread.count %}
                                            {% if unread_count > 0 %}
                                                <span class="badge bg-danger float-end">{{ unread_count }}</span>
                                            {% endif %}
                                        {% endwith %}"""
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        
        # Sauvegarder la correction
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("\n✅ TEMPLATE CORRIGÉ avec succès!")
        print("🔧 Correction appliquée:")
        print("   - Suppression du double if imbriqué")
        print("   - Utilisation de 'unread.count' pour les notifications non lues")
        print("   - Structure with/if simplifiée")
    else:
        print("\n⚠️  Le code problématique n'a pas été trouvé dans le format attendu")
        print("📋 Essayons une correction manuelle...")
        
        # Correction alternative
        corrected_lines = []
        in_problem_section = False
        problem_fixed = False
        
        for i, line in enumerate(lines):
            if '{% if request.user.notification_set.all %}' in line and not problem_fixed:
                # Remplacer cette ligne par with
                corrected_lines.append(line.replace(
                    '{% if request.user.notification_set.all %}', 
                    '{% with unread_count=request.user.notification_set.unread.count %}'
                ))
                in_problem_section = True
            elif in_problem_section and '{% endwith %}' in line:
                corrected_lines.append('                                        {% endwith %}')
                in_problem_section = False
                problem_fixed = True
            else:
                corrected_lines.append(line)
        
        # Sauvegarder la correction alternative
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(corrected_lines))
        print("✅ CORRECTION ALTERNATIVE APPLIQUÉE!")

def analyser_tous_les_templates_agents():
    """Analyse tous les templates du dossier agents"""
    templates_dir = os.path.join(project_path, 'templates/agents')
    
    print("🔍 ANALYSE COMPLÈTE DES TEMPLATES AGENTS")
    print("=" * 60)
    
    if not os.path.exists(templates_dir):
        print(f"❌ Dossier templates/agents non trouvé: {templates_dir}")
        return
    
    templates = []
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                templates.append(os.path.join(root, file))
    
    print(f"📁 {len(templates)} templates trouvés:")
    for template in templates:
        print(f"   📄 {os.path.basename(template)}")
    
    for template in templates:
        analyser_template(template)

def verifier_structure_notifications():
    """Vérifie si le modèle Notification existe et est correct"""
    print(f"\n🔍 VÉRIFICATION DU MODÈLE NOTIFICATION")
    print("=" * 60)
    
    try:
        from django.apps import apps
        from notifications.models import Notification
        
        print("✅ Modèle Notification trouvé")
        
        # Vérifier les champs
        print("📋 Champs du modèle Notification:")
        for field in Notification._meta.fields:
            print(f"   - {field.name} ({field.get_internal_type()})")
            
    except ImportError:
        print("❌ Modèle Notification non trouvé")
        print("💡 Le template essaie d'accéder à request.user.notification_set")
        print("   mais le modèle Notification n'existe pas ou n'est pas importé")

if __name__ == "__main__":
    print("🎯 SCRIPT D'ANALYSE ET CORRECTION DES TEMPLATES AGENTS")
    print("=" * 60)
    
    # 1. Analyser tous les templates
    analyser_tous_les_templates_agents()
    
    # 2. Corriger le template spécifique qui cause l'erreur
    corriger_template_base_agent()
    
    # 3. Vérifier la structure des notifications
    verifier_structure_notifications()
    
    print(f"\n🎉 ANALYSE TERMINÉE!")
    print("🔧 Redémarrez le serveur et testez le dashboard:")
    print("   python manage.py runserver")
    print("   http://127.0.0.1:8000/agents/dashboard/")