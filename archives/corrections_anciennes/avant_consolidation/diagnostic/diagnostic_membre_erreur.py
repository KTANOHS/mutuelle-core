#!/usr/bin/env python3
"""
SCRIPT DE DIAGNOSTIC - Erreur "Cannot resolve keyword 'membre'"
Usage: python diagnostic_membre_erreur.py
"""

import os
import sys
import django
import re
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

from django.apps import apps
from django.db import models
from django.core.exceptions import FieldDoesNotExist

class DiagnosticMembreErreur:
    """Classe pour diagnostiquer l'erreur 'Cannot resolve keyword membre'"""
    
    def __init__(self):
        self.resultats = {
            'erreurs_trouvees': [],
            'modeles_avec_problemes': [],
            'fichiers_avec_erreurs': [],
            'suggestions_correction': []
        }
    
    def analyser_structure_modeles(self):
        """Analyse la structure des modèles et leurs relations"""
        print("\n" + "="*70)
        print("🔍 ANALYSE STRUCTURELLE DES MODÈLES")
        print("="*70)
        
        # Obtenir tous les modèles
        tous_les_modeles = apps.get_models()
        
        print(f"📊 Modèles trouvés: {len(tous_les_modeles)}")
        
        # Analyser chaque modèle
        for modele in tous_les_modeles:
            print(f"\n🗄️  Modèle: {modele.__name__}")
            print(f"   📍 Application: {modele._meta.app_label}")
            
            # Lister tous les champs
            champs = modele._meta.get_fields()
            champs_noms = [f.name for f in champs if hasattr(f, 'name')]
            
            print(f"   📋 Champs: {', '.join(champs_noms)}")
            
            # Vérifier si le modèle a un champ 'membre'
            if 'membre' in champs_noms:
                print("   ✅ Champ 'membre' trouvé")
            else:
                print("   ❌ Champ 'membre' NON trouvé")
                
                # Chercher des champs similaires
                champs_similaires = [champ for champ in champs_noms 
                                   if 'patient' in champ.lower() or 'user' in champ.lower()]
                if champs_similaires:
                    print(f"   💡 Champs similaires: {champs_similaires}")
    
    def rechercher_occurrences_code(self):
        """Recherche toutes les occurrences de 'membre' dans le code"""
        print("\n" + "="*70)
        print("🔎 RECHERCHE DES OCCURRENCES DANS LE CODE")
        print("="*70)
        
        # Patterns à rechercher
        patterns = [
            r'\.filter\(.*membre.*\)',
            r'\.exclude\(.*membre.*\)',
            r'\.get\(.*membre.*\)',
            r'Soin\.objects\.filter\(.*membre.*\)',
            r'soin\.membre',
            r'filter\(membre=',
            r'filter\(membre__',
        ]
        
        # Dossiers à analyser
        dossiers_analyse = ['assureur', 'soins', 'membres', 'templates']
        
        for dossier in dossiers_analyse:
            chemin_dossier = BASE_DIR / dossier
            if not chemin_dossier.exists():
                continue
                
            print(f"\n📁 Analyse du dossier: {dossier}")
            
            # Analyser les fichiers Python
            for fichier_py in chemin_dossier.rglob('*.py'):
                self.analyser_fichier_python(fichier_py, patterns)
            
            # Analyser les templates HTML
            for fichier_html in chemin_dossier.rglob('*.html'):
                self.analyser_fichier_template(fichier_html)
    
    def analyser_fichier_python(self, fichier, patterns):
        """Analyse un fichier Python pour trouver des références à 'membre'"""
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                contenu = f.read()
                lignes = contenu.split('\n')
            
            erreurs_fichier = []
            
            for numero_ligne, ligne in enumerate(lignes, 1):
                ligne = ligne.strip()
                
                # Vérifier les patterns
                for pattern in patterns:
                    if re.search(pattern, ligne):
                        erreur = {
                            'fichier': str(fichier),
                            'ligne': numero_ligne,
                            'code': ligne,
                            'pattern': pattern,
                            'type': 'python'
                        }
                        erreurs_fichier.append(erreur)
                
                # Vérifier les imports et les querysets spécifiques
                if 'membre' in ligne and ('filter' in ligne or 'objects' in ligne):
                    if not any(mot in ligne for mot in ['#', '"""', "'''"]):  # Ignorer les commentaires
                        erreur = {
                            'fichier': str(fichier),
                            'ligne': numero_ligne,
                            'code': ligne,
                            'pattern': 'membre dans queryset',
                            'type': 'python'
                        }
                        erreurs_fichier.append(erreur)
            
            if erreurs_fichier:
                print(f"   📄 {fichier.name}: {len(erreurs_fichier)} occurrence(s) trouvée(s)")
                for erreur in erreurs_fichier:
                    print(f"      ❌ Ligne {erreur['ligne']}: {erreur['code']}")
                    self.resultats['erreurs_trouvees'].append(erreur)
                    self.resultats['fichiers_avec_erreurs'].append(erreur['fichier'])
                    
        except Exception as e:
            print(f"   ⚠️ Erreur lecture {fichier}: {e}")
    
    def analyser_fichier_template(self, fichier):
        """Analyse un fichier template pour trouver des références à 'membre'"""
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                contenu = f.read()
                lignes = contenu.split('\n')
            
            erreurs_fichier = []
            
            for numero_ligne, ligne in enumerate(lignes, 1):
                ligne = ligne.strip()
                
                # Vérifier les références dans les templates
                if 'membre' in ligne and ('soin.' in ligne or 'bon.' in ligne):
                    if 'soin.membre' in ligne or 'bon.membre' in ligne:
                        erreur = {
                            'fichier': str(fichier),
                            'ligne': numero_ligne,
                            'code': ligne,
                            'pattern': 'soin.membre ou bon.membre',
                            'type': 'template'
                        }
                        erreurs_fichier.append(erreur)
            
            if erreurs_fichier:
                print(f"   📄 {fichier.name}: {len(erreurs_fichier)} occurrence(s) trouvée(s)")
                for erreur in erreurs_fichier:
                    print(f"      ❌ Ligne {erreur['ligne']}: {erreur['code']}")
                    self.resultats['erreurs_trouvees'].append(erreur)
                    self.resultats['fichiers_avec_erreurs'].append(erreur['fichier'])
                    
        except Exception as e:
            print(f"   ⚠️ Erreur lecture {fichier}: {e}")
    
    def analyser_relations_modeles(self):
        """Analyse les relations entre modèles"""
        print("\n" + "="*70)
        print("🔄 ANALYSE DES RELATIONS ENTRE MODÈLES")
        print("="*70)
        
        try:
            from soins.models import Soin
            from membres.models import Membre
            
            print("🔗 Relations identifiées:")
            print(f"   • Soin.patient -> {Soin._meta.get_field('patient').related_model}")
            print(f"   • Membre -> {Membre.__name__}")
            
            # Vérifier si la relation est correcte
            if Soin._meta.get_field('patient').related_model == Membre:
                print("   ✅ Relation Soin.patient → Membre est correcte")
            else:
                print("   ❌ Relation Soin.patient incorrecte")
                
        except Exception as e:
            print(f"   ❌ Erreur analyse relations: {e}")
    
    def generer_suggestions(self):
        """Génère des suggestions de correction basées sur les erreurs trouvées"""
        print("\n" + "="*70)
        print("💡 SUGGESTIONS DE CORRECTION")
        print("="*70)
        
        if not self.resultats['erreurs_trouvees']:
            print("✅ Aucune erreur trouvée - Aucune correction nécessaire")
            return
        
        suggestions = []
        
        for erreur in self.resultats['erreurs_trouvees']:
            if erreur['type'] == 'python':
                if 'Soin.objects.filter' in erreur['code'] and 'membre' in erreur['code']:
                    suggestions.append({
                        'fichier': erreur['fichier'],
                        'ligne': erreur['ligne'],
                        'ancien_code': erreur['code'],
                        'nouveau_code': erreur['code'].replace('membre=', 'patient='),
                        'explication': "Remplacer 'membre' par 'patient' dans le filtre Soin"
                    })
                elif 'soin.membre' in erreur['code']:
                    suggestions.append({
                        'fichier': erreur['fichier'],
                        'ligne': erreur['ligne'],
                        'ancien_code': erreur['code'],
                        'nouveau_code': erreur['code'].replace('soin.membre', 'soin.patient'),
                        'explication': "Remplacer 'soin.membre' par 'soin.patient'"
                    })
        
        # Ajouter des suggestions générales
        suggestions.append({
            'fichier': 'GLOBAL',
            'ligne': 'N/A',
            'ancien_code': 'Soin.objects.filter(membre=...)',
            'nouveau_code': 'Soin.objects.filter(patient=...)',
            'explication': "Le modèle Soin utilise 'patient' au lieu de 'membre'"
        })
        
        suggestions.append({
            'fichier': 'GLOBAL',
            'ligne': 'N/A',
            'ancien_code': 'soin.membre.nom',
            'nouveau_code': 'soin.patient.nom',
            'explication': "Accéder au patient via soin.patient"
        })
        
        # Afficher les suggestions
        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n🔧 Suggestion {i}:")
            print(f"   📍 Fichier: {suggestion['fichier']}")
            if suggestion['ligne'] != 'N/A':
                print(f"   📄 Ligne: {suggestion['ligne']}")
            print(f"   ❌ Avant: {suggestion['ancien_code']}")
            print(f"   ✅ Après: {suggestion['nouveau_code']}")
            print(f"   💡 Explication: {suggestion['explication']}")
        
        self.resultats['suggestions_correction'] = suggestions
    
    def creer_script_correction(self):
        """Crée un script de correction automatique"""
        if not self.resultats['suggestions_correction']:
            return
            
        script_content = """#!/usr/bin/env python3
# SCRIPT DE CORRECTION AUTOMATIQUE - Erreur 'membre'
# Généré automatiquement par diagnostic_membre_erreur.py

import os
import re
import sys
from pathlib import Path

def corriger_erreurs_membre():
    corrections = [
        # Patterns pour Soin.objects.filter
        (r'Soin\\\\.objects\\\\.filter\\\\(.*)membre=', r'Soin.objects.filter\\\\1patient='),
        (r'soin\\\\.membre', r'soin.patient'),
        (r'filter\\\\(membre=', r'filter(patient='),
        (r'filter\\\\(membre__', r'filter(patient__'),
    ]
    
    fichiers_corriges = 0
    
    # Fichiers à corriger basés sur l'analyse
    fichiers_a_corriger = {fichiers}
    
    for fichier_pattern in fichiers_a_corriger:
        for fichier_path in Path('.').rglob(fichier_pattern):
            if fichier_path.exists():
                try:
                    with open(fichier_path, 'r', encoding='utf-8') as f:
                        contenu = f.read()
                    
                    contenu_corrige = contenu
                    for pattern_avant, pattern_apres in corrections:
                        contenu_corrige = re.sub(pattern_avant, pattern_apres, contenu_corrige)
                    
                    if contenu_corrige != contenu:
                        with open(fichier_path, 'w', encoding='utf-8') as f:
                            f.write(contenu_corrige)
                        print(f"✅ Corrections appliquées: {{fichier_path}}")
                        fichiers_corriges += 1
                    else:
                        print(f"✅ Aucune correction nécessaire: {{fichier_path}}")
                        
                except Exception as e:
                    print(f"❌ Erreur correction {{fichier_path}}: {{e}}")
    
    print(f"\\\\n🎯 {{fichiers_corriges}} fichiers corrigés")

if __name__ == "__main__":
    corriger_erreurs_membre()
""".format(fichiers=str(list(set(self.resultats['fichiers_avec_erreurs']))))
        
        with open('correction_automatique_membre.py', 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print(f"\n📄 Script de correction généré: correction_automatique_membre.py")
    
    def generer_rapport(self):
        """Génère un rapport complet"""
        print("\n" + "="*70)
        print("📊 RAPPORT DE DIAGNOSTIC COMPLET")
        print("="*70)
        
        print(f"\n📈 STATISTIQUES:")
        print(f"   • Erreurs trouvées: {len(self.resultats['erreurs_trouvees'])}")
        print(f"   • Fichiers avec erreurs: {len(set(self.resultats['fichiers_avec_erreurs']))}")
        print(f"   • Suggestions de correction: {len(self.resultats['suggestions_correction'])}")
        
        if self.resultats['erreurs_trouvees']:
            print(f"\n❌ ERREURS IDENTIFIÉES:")
            for erreur in self.resultats['erreurs_trouvees']:
                print(f"   • {erreur['fichier']}:L{erreur['ligne']} - {erreur['code'][:50]}...")
        
        print(f"\n🎯 DIAGNOSTIC:")
        if self.resultats['erreurs_trouvees']:
            print("   ❌ L'erreur 'Cannot resolve keyword membre' est confirmée")
            print("   💡 Cause: Utilisation du champ 'membre' qui n'existe pas dans le modèle Soin")
            print("   🔧 Solution: Remplacer 'membre' par 'patient' dans tous les fichiers")
        else:
            print("   ✅ Aucune occurrence problématique trouvée")
            print("   💡 L'erreur peut venir d'une autre source")
    
    def executer_diagnostic_complet(self):
        """Exécute le diagnostic complet"""
        print("🔍 DÉMARRAGE DU DIAGNOSTIC...")
        print("Erreur: Cannot resolve keyword 'membre'")
        print("="*70)
        
        self.analyser_structure_modeles()
        self.analyser_relations_modeles()
        self.rechercher_occurrences_code()
        self.generer_suggestions()
        self.creer_script_correction()
        self.generer_rapport()
        
        return self.resultats

# Exécution du script
if __name__ == "__main__":
    try:
        diagnostic = DiagnosticMembreErreur()
        resultats = diagnostic.executer_diagnostic_complet()
        
        # Code de sortie
        if resultats['erreurs_trouvees']:
            print("\n💥 DIAGNOSTIC TERMINÉ - CORRECTIONS NÉCESSAIRES")
            sys.exit(1)
        else:
            print("\n✅ DIAGNOSTIC TERMINÉ - AUCUNE CORRECTION NÉCESSAIRE")
            sys.exit(0)
            
    except Exception as e:
        print(f"❌ Erreur lors du diagnostic: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)