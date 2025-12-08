# diagnostic_projet.py
import os
import sys
import traceback
from pathlib import Path

def trouver_projet_django():
    """Trouver le répertoire du projet Django actuel"""
    repertoire_actuel = Path.cwd()
    
    # Chercher manage.py
    for dirpath, dirnames, filenames in os.walk(repertoire_actuel):
        if 'manage.py' in filenames:
            projet_dir = Path(dirpath)
            print(f"✅ Projet Django trouvé: {projet_dir}")
            return projet_dir
    
    # Si non trouvé, chercher dans les répertoires parents
    parent = repertoire_actuel.parent
    for _ in range(5):  # Chercher sur 5 niveaux max
        manage_py = parent / 'manage.py'
        if manage_py.exists():
            print(f"✅ Projet Django trouvé (dans parent): {parent}")
            return parent
        parent = parent.parent
    
    print("❌ Projet Django non trouvé")
    return None

def analyser_views_problematique(projet_dir):
    """Analyser le fichier views.py problématique"""
    print("\n" + "=" * 60)
    print("🔍 ANALYSE DU FICHIER VIEWS.PY")
    print("=" * 60)
    
    # Fichiers à analyser (par ordre de priorité)
    fichiers_possibles = [
        projet_dir / 'mutuelle_core' / 'views.py',
        projet_dir / 'core' / 'views.py',
        projet_dir / 'apps' / 'core' / 'views.py',
        projet_dir / 'mutuelle_core' / 'views.py',
    ]
    
    fichier_trouve = None
    for fichier in fichiers_possibles:
        if fichier.exists():
            fichier_trouve = fichier
            print(f"✅ Fichier trouvé: {fichier}")
            break
    
    if not fichier_trouve:
        # Chercher récursivement
        print("\n🔎 Recherche récursive de views.py...")
        for root, dirs, files in os.walk(projet_dir):
            if 'views.py' in files:
                # Vérifier si c'est probablement le bon
                chemin = Path(root) / 'views.py'
                contenu = chemin.read_text(encoding='utf-8', errors='ignore')
                if 'def home' in contenu or 'NameError' in contenu or 'html' in contenu:
                    print(f"✅ Fichier potentiel trouvé: {chemin}")
                    fichier_trouve = chemin
                    break
    
    if not fichier_trouve:
        print("❌ Aucun fichier views.py pertinent trouvé")
        return
    
    # Analyser le fichier
    try:
        with open(fichier_trouve, 'r', encoding='utf-8') as f:
            lignes = f.readlines()
        
        print(f"\n📊 Informations sur le fichier:")
        print(f"   • Nombre de lignes: {len(lignes)}")
        print(f"   • Taille: {os.path.getsize(fichier_trouve)} octets")
        
        # Afficher la zone autour de la ligne 254
        print(f"\n📝 ZONE DE L'ERREUR (ligne 254):")
        
        debut = max(240, 0)
        fin = min(270, len(lignes))
        
        for i in range(debut, fin):
            numero_ligne = i + 1
            prefix = ">>>" if numero_ligne == 254 else "   "
            print(f"{prefix} {numero_ligne:3}: {lignes[i].rstrip()}")
        
        # Analyse spécifique de la ligne 254
        if len(lignes) >= 254:
            ligne_254 = lignes[253].strip()
            print(f"\n🔍 Analyse de la ligne 254:")
            print(f"   Contenu: {ligne_254}")
            
            # Chercher des problèmes
            problemes = []
            
            if 'html' in ligne_254:
                if 'html.' in ligne_254:
                    problemes.append("Utilisation de 'html.' sans import")
                elif 'html' in ligne_254.split() and not ('import html' in ligne_254 or 'from html' in ligne_254):
                    problemes.append("Variable 'html' non définie")
            
            if 'html' in ligne_254 and 'escape' in ligne_254:
                problemes.append("Utilisation probable de html.escape() sans import")
            
            if problemes:
                print(f"\n⚠️  Problèmes détectés:")
                for probleme in problemes:
                    print(f"   • {probleme}")
        
        # Vérifier les imports
        print(f"\n📦 IMPORTS DANS LE FICHIER:")
        imports = []
        for i, ligne in enumerate(lignes):
            if ligne.strip().startswith(('import', 'from')) and i < 100:  # Premières 100 lignes
                imports.append(ligne.rstrip())
        
        if imports:
            for imp in imports:
                print(f"   {imp}")
        else:
            print("   Aucun import trouvé")
        
        # Vérifier si 'html' est importé
        html_importe = any('html' in imp.lower() for imp in imports)
        print(f"\n🔎 Import 'html' présent: {'✅ OUI' if html_importe else '❌ NON'}")
        
        # Chercher toutes les utilisations de 'html' dans le fichier
        print(f"\n🔎 TOUTES LES UTILISATIONS DE 'html' DANS LE FICHIER:")
        utilisations_html = []
        for i, ligne in enumerate(lignes):
            if 'html' in ligne.lower():
                utilisations_html.append((i+1, ligne.strip()))
        
        if utilisations_html:
            for ligne_num, contenu in utilisations_html[:10]:  # Limiter à 10 premières
                print(f"   Ligne {ligne_num:3}: {contenu}")
            if len(utilisations_html) > 10:
                print(f"   ... et {len(utilisations_html) - 10} autres")
        else:
            print("   Aucune utilisation de 'html' trouvée")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        traceback.print_exc()

def corriger_erreur_html():
    """Générer la correction pour l'erreur 'html'"""
    print("\n" + "=" * 60)
    print("💡 CORRECTION DE L'ERREUR")
    print("=" * 60)
    
    correction = '''
# SOLUTION 1: AJOUTER LES IMPORTS MANQUANTS
# ----------------------------------------------------
# Au début de votre fichier views.py (avec les autres imports), ajoutez:

from django.utils.html import escape, format_html, mark_safe


# SOLUTION 2: CORRIGER LES UTILISATIONS DE html
# ----------------------------------------------------
# Dans votre code, remplacez:

# ❌ MAUVAIS (cause l'erreur):
# texte = html.escape(texte_utilisateur)
# message = html.format('<strong>{}</strong>', texte)
# variable = html  # si vous utilisez 'html' comme variable

# ✅ CORRECT:
# texte = escape(texte_utilisateur)
# message = format_html('<strong>{}</strong>', texte)
# variable_html = ...  # utilisez un nom différent


# SOLUTION 3: EXEMPLE DE VUE CORRIGÉE
# ----------------------------------------------------
def home(request):
    """Vue d'accueil - Version corrigée"""
    # Imports (déjà en haut du fichier, mais si besoin ici)
    from django.utils.html import escape, format_html
    
    # Récupérer des données
    user_input = request.GET.get('input', '')
    
    # Échapper le HTML pour la sécurité
    safe_input = escape(user_input) if user_input else ""
    
    # Formater du HTML de manière sécurisée
    if request.user.is_authenticated:
        welcome = format_html(
            '<span class="text-success">Bonjour, <strong>{}</strong></span>',
            escape(request.user.get_full_name() or request.user.username)
        )
    else:
        welcome = "Bienvenue visiteur"
    
    context = {
        'title': 'Accueil',
        'welcome_message': welcome,
        'safe_input': safe_input,
    }
    
    return render(request, 'home.html', context)


# SOLUTION 4: VÉRIFICATION RAPIDE
# ----------------------------------------------------
# 1. Ouvrez votre fichier mutuelle_core/views.py
# 2. Cherchez la ligne 254
# 3. Vérifiez comment 'html' est utilisé
# 4. Ajoutez l'import manquant
# 5. Corrigez l'utilisation
# 6. Redémarrez le serveur: python manage.py runserver
'''
    
    print(correction)

def diagnostic_complet():
    """Exécuter un diagnostic complet"""
    print("🔍 DIAGNOSTIC DJANGO - ERREUR 'html'")
    print("=" * 60)
    
    # Trouver le projet
    projet = trouver_projet_django()
    if not projet:
        return
    
    # Analyser le fichier problématique
    analyser_views_problematique(projet)
    
    # Proposer une correction
    corriger_erreur_html()
    
    # Instructions supplémentaires
    print("\n" + "=" * 60)
    print("🚀 PROCÉDURE DE RÉSOLUTION")
    print("=" * 60)
    
    instructions = '''
ÉTAPE PAR ÉTAPE :

1. LOCALISEZ LE FICHIER :
   cd /Users/koffitanohsoualiho/Documents/P\ FINALE\ AVANT\ SYNCHRO/pf\ erreur/projet\ 21.49.30
   ls -la mutuelle_core/views.py

2. OUVREZ LE FICHIER :
   nano mutuelle_core/views.py
   # ou utilisez votre éditeur préféré

3. ALLEZ À LA LIGNE 254 :
   - Dans vim/nano: tapez "254G"
   - Dans VS Code: Ctrl+G puis 254
   - Dans PyCharm: Ctrl+G puis 254

4. ANALYSEZ LA LIGNE :
   Identifiez comment 'html' est utilisé.

5. CORRIGEZ :
   Option A: Ajoutez l'import manquant en haut
   Option B: Remplacez html.xxx par escape()/format_html()
   Option C: Si 'html' est une variable, renommez-la

6. TESTEZ :
   python manage.py runserver
   Ouvrez http://127.0.0.1:8000/

7. SI L'ERREUR PERSISTE :
   - Vérifiez qu'il n'y a pas d'autres utilisations de 'html'
   - Cherchez "html." dans tout le fichier
   - Redémarrez complètement le serveur
'''
    
    print(instructions)

if __name__ == "__main__":
    diagnostic_complet()