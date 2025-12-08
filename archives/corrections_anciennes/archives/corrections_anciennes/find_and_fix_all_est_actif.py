# find_and_fix_all_est_actif.py
import os
import re
import django
import sys

project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def trouver_toutes_occurrences_est_actif():
    """Trouve toutes les occurrences de est_actif dans le projet"""
    print("🎯 RECHERCHE DE TOUTES LES OCCURRENCES DE 'est_actif'")
    print("=" * 60)
    
    occurrences = []
    
    # Dossiers à analyser
    dossiers = [
        'agents',
        'membres', 
        'soins',
        'paiements',
        'core',
        'templates'
    ]
    
    for dossier in dossiers:
        dossier_path = os.path.join(project_path, dossier)
        if os.path.exists(dossier_path):
            for root, dirs, files in os.walk(dossier_path):
                for file in files:
                    if file.endswith(('.py', '.html')):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                lines = content.split('\n')
                                for i, line in enumerate(lines):
                                    if 'est_actif' in line:
                                        occurrences.append({
                                            'file': file_path,
                                            'line': i + 1,
                                            'content': line.strip()
                                        })
                        except:
                            pass
    
    print(f"📊 {len(occurrences)} occurrence(s) trouvée(s):")
    for occ in occurrences:
        print(f"   📄 {os.path.basename(occ['file'])}:L{occ['line']}")
        print(f"      {occ['content']}")
    
    return occurrences

def corriger_fichier_agents_views():
    """Corrige spécifiquement agents/views.py"""
    print("\n🎯 CORRECTION DE agents/views.py")
    print("=" * 60)
    
    views_path = os.path.join(project_path, 'agents/views.py')
    
    try:
        with open(views_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Compter les occurrences avant
        avant = content.count('est_actif')
        print(f"Occurrences de 'est_actif' avant correction: {avant}")
        
        if avant > 0:
            # Afficher les lignes problématiques
            lines = content.split('\n')
            print("Lignes problématiques:")
            for i, line in enumerate(lines):
                if 'est_actif' in line:
                    print(f"  Ligne {i+1}: {line.strip()}")
            
            # Remplacer systématiquement
            content = content.replace("est_actif=True", "statut='ACTIF'")
            content = content.replace("est_actif=False", "statut='INACTIF'")
            content = content.replace(".filter(est_actif=", ".filter(statut=")
            content = content.replace("membres_actifs = Membre.objects.filter(est_actif=True)", "membres_actifs = Membre.objects.filter(statut='ACTIF')")
            content = content.replace("Membre.objects.filter(est_actif=True)", "Membre.objects.filter(statut='ACTIF')")
            
            # Remplacer les occurrences restantes
            content = re.sub(r'est_actif\s*=\s*True', "statut='ACTIF'", content)
            content = re.sub(r'est_actif\s*=\s*False', "statut='INACTIF'", content)
            
            # Compter après correction
            apres = content.count('est_actif')
            print(f"Occurrences de 'est_actif' après correction: {apres}")
            
            if apres == 0:
                print("✅ Toutes les occurrences corrigées!")
            else:
                print(f"⚠️  Il reste {apres} occurrence(s)")
                # Afficher les lignes restantes
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'est_actif' in line:
                        print(f"  Ligne {i+1} restante: {line.strip()}")
            
            # Sauvegarder
            with open(views_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ Fichier agents/views.py sauvegardé")
        else:
            print("ℹ️ Aucune occurrence trouvée dans agents/views.py")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

def corriger_fichier_models():
    """Vérifie et corrige les modèles"""
    print("\n🎯 VÉRIFICATION DES MODÈLES")
    print("=" * 60)
    
    try:
        from membres.models import Membre
        print("✅ Modèle Membre chargé")
        print("   Champs disponibles:", [f.name for f in Membre._meta.fields if 'statut' in f.name or 'actif' in f.name])
    except Exception as e:
        print(f"❌ Erreur modèle Membre: {e}")

def creer_patch_urgence():
    """Crée un patch d'urgence si la correction ne fonctionne pas"""
    print("\n🚨 CRÉATION D'UN PATCH D'URGENCE")
    print("=" * 60)
    
    patch_content = '''# PATCH URGENCE - Correction champ est_actif
# Ajoutez ce code au début de agents/views.py

import sys
from membres.models import Membre

# Monkey patch pour intercepter les appels à est_actif
_original_filter = Membre.objects.filter

def _patched_filter(**kwargs):
    if 'est_actif' in kwargs:
        value = kwargs.pop('est_actif')
        kwargs['statut'] = 'ACTIF' if value else 'INACTIF'
    return _original_filter(**kwargs)

Membre.objects.filter = _patched_filter

print("✅ Patch urgence appliqué - est_actif redirigé vers statut")
'''
    
    patch_path = os.path.join(project_path, 'urgence_patch.py')
    try:
        with open(patch_path, 'w', encoding='utf-8') as f:
            f.write(patch_content)
        print(f"✅ Patch créé: {patch_path}")
        print("💡 Ajoutez 'from .urgence_patch import *' au début de agents/views.py")
    except Exception as e:
        print(f"❌ Erreur création patch: {e}")

def verifier_et_corriger_template():
    """Vérifie les templates aussi"""
    print("\n🎯 VÉRIFICATION DES TEMPLATES")
    print("=" * 60)
    
    templates_path = os.path.join(project_path, 'templates/agents')
    
    if os.path.exists(templates_path):
        for root, dirs, files in os.walk(templates_path):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        if 'est_actif' in content:
                            print(f"❌ Template avec est_actif: {file}")
                            # Corriger le template
                            content = content.replace('est_actif', 'statut')
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(content)
                            print(f"✅ Template corrigé: {file}")
                    except:
                        pass

if __name__ == "__main__":
    # 1. Trouver toutes les occurrences
    occurrences = trouver_toutes_occurrences_est_actif()
    
    # 2. Corriger agents/views.py
    corriger_fichier_agents_views()
    
    # 3. Vérifier les modèles
    corriger_fichier_models()
    
    # 4. Vérifier les templates
    verifier_et_corriger_template()
    
    # 5. Créer un patch d'urgence
    creer_patch_urgence()
    
    print(f"\n🎉 CORRECTIONS TERMINÉES!")
    print("🚀 Redémarrez et testez:")
    print("   python manage.py runserver")
    print("   http://127.0.0.1:8000/agents/bons-soin/creer/")