#!/usr/bin/env python3
"""
SCRIPT D'ANALYSE ET CORRECTION NameError: 'GroupeCommunication' is not defined
Diagnostique et résout les problèmes d'import dans communication/models.py
"""

import os
import re
import sys
from pathlib import Path

class CommunicationAnalyzer:
    def __init__(self):
        self.communication_path = Path('communication')
        self.models_file = self.communication_path / 'models.py'
        self.admin_file = self.communication_path / 'admin.py'
        self.problemes = []
        self.solutions = []
    
    def analyser_structure_fichiers(self):
        """Analyse la structure des fichiers"""
        print("📁 ANALYSE DE LA STRUCTURE DES FICHIERS")
        print("=" * 45)
        
        # Vérifier l'existence des fichiers
        if not self.models_file.exists():
            self.problemes.append("❌ models.py n'existe pas")
            return False
        else:
            print("✅ models.py trouvé")
        
        if not self.admin_file.exists():
            self.problemes.append("❌ admin.py n'existe pas")
            return False
        else:
            print("✅ admin.py trouvé")
        
        return True
    
    def analyser_models_py(self):
        """Analyse détaillée de models.py"""
        print(f"\n🔬 ANALYSE DÉTAILLÉE DE models.py")
        print("=" * 35)
        
        try:
            with open(self.models_file, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Vérifier la présence des classes
            classes_trouvees = re.findall(r'class (\w+)\(models\.Model\):', contenu)
            print(f"🏗️  Classes trouvées dans models.py: {len(classes_trouvees)}")
            
            for classe in classes_trouvees:
                print(f"  • {classe}")
            
            # Vérifier spécifiquement GroupeCommunication
            if 'GroupeCommunication' in classes_trouvees:
                print("✅ GroupeCommunication trouvé dans models.py")
            else:
                self.problemes.append("❌ GroupeCommunication NON TROUVÉ dans models.py")
            
            # Vérifier MessageGroupe
            if 'MessageGroupe' in classes_trouvees:
                print("✅ MessageGroupe trouvé dans models.py")
            else:
                self.problemes.append("❌ MessageGroupe NON TROUVÉ dans models.py")
            
            # Vérifier les imports
            imports_essentiels = [
                'from django.db import models',
                'from django.contrib.auth.models import User',
                'from django.utils import timezone'
            ]
            
            print("\n📥 VÉRIFICATION DES IMPORTS:")
            for imp in imports_essentiels:
                if imp in contenu:
                    print(f"  ✅ {imp}")
                else:
                    print(f"  ❌ {imp} MANQUANT")
            
            return classes_trouvees
            
        except Exception as e:
            self.problemes.append(f"❌ Erreur lecture models.py: {e}")
            return []
    
    def analyser_admin_py(self):
        """Analyse détaillée de admin.py"""
        print(f"\n⚙️  ANALYSE DÉTAILLÉE DE admin.py")
        print("=" * 35)
        
        try:
            with open(self.admin_file, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Vérifier l'import des modèles
            imports_match = re.findall(r'from \.models import ([\w\s,]+)', contenu)
            if imports_match:
                modeles_importes = [m.strip() for m in imports_match[0].split(',')]
                print(f"📥 Modèles importés dans admin.py:")
                for modele in modeles_importes:
                    print(f"  • {modele}")
                
                # Vérifier GroupeCommunication
                if 'GroupeCommunication' in modeles_importes:
                    print("✅ GroupeCommunication importé dans admin.py")
                else:
                    self.problemes.append("❌ GroupeCommunication NON IMPORTÉ dans admin.py")
                    self.solutions.append("Ajouter GroupeCommunication dans l'import de admin.py")
                
                # Vérifier MessageGroupe
                if 'MessageGroupe' in modeles_importes:
                    print("✅ MessageGroupe importé dans admin.py")
                else:
                    self.problemes.append("❌ MessageGroupe NON IMPORTÉ dans admin.py")
                    self.solutions.append("Ajouter MessageGroupe dans l'import de admin.py")
            
            # Vérifier les décorateurs @admin.register
            registres = re.findall(r'@admin\.register\((\w+)\)', contenu)
            print(f"\n🎯 Modèles enregistrés avec @admin.register:")
            for registre in registres:
                print(f"  • {registre}")
            
            # Vérifier GroupeCommunication
            if 'GroupeCommunication' in registres:
                print("✅ GroupeCommunication enregistré avec @admin.register")
            else:
                self.problemes.append("❌ GroupeCommunication NON ENREGISTRÉ avec @admin.register")
            
            if 'MessageGroupe' in registres:
                print("✅ MessageGroupe enregistré avec @admin.register")
            else:
                self.problemes.append("❌ MessageGroupe NON ENREGISTRÉ avec @admin.register")
            
        except Exception as e:
            self.problemes.append(f"❌ Erreur lecture admin.py: {e}")
    
    def verifier_syntaxe_python(self):
        """Vérifie la syntaxe Python des fichiers"""
        print(f"\n🐍 VÉRIFICATION SYNTAXE PYTHON")
        print("=" * 30)
        
        try:
            # Vérifier models.py
            compile(open(self.models_file).read(), str(self.models_file), 'exec')
            print("✅ models.py - Syntaxe Python valide")
        except SyntaxError as e:
            self.problemes.append(f"❌ Erreur syntaxe models.py: {e}")
        
        try:
            # Vérifier admin.py
            compile(open(self.admin_file).read(), str(self.admin_file), 'exec')
            print("✅ admin.py - Syntaxe Python valide")
        except SyntaxError as e:
            self.problemes.append(f"❌ Erreur syntaxe admin.py: {e}")
    
    def diagnostiquer_probleme_import(self):
        """Diagnostique le problème d'import spécifique"""
        print(f"\n🔍 DIAGNOSTIC DU PROBLÈME D'IMPORT")
        print("=" * 40)
        
        # Scénarios possibles
        scenarios = [
            "1. GroupeCommunication n'est pas défini dans models.py",
            "2. GroupeCommunication est défini mais non importé dans admin.py", 
            "3. Erreur de syntaxe dans models.py empêchant l'import",
            "4. Problème d'ordre des imports dans admin.py",
            "5. Fichier models.py corrompu ou incomplet"
        ]
        
        print("Scénarios possibles:")
        for scenario in scenarios:
            print(f"  • {scenario}")
    
    def corriger_automatiquement(self):
        """Corrige automatiquement les problèmes détectés"""
        print(f"\n🔧 CORRECTION AUTOMATIQUE")
        print("=" * 25)
        
        if not self.problemes:
            print("✅ Aucun problème à corriger")
            return
        
        # Correction 1: Vérifier et corriger admin.py
        try:
            with open(self.admin_file, 'r', encoding='utf-8') as f:
                contenu_admin = f.read()
            
            # Vérifier l'import
            import_correct = "from .models import Message, Conversation, PieceJointe, Notification, GroupeCommunication, MessageGroupe"
            
            # Trouver et remplacer l'import incorrect
            pattern_import = r'from \.models import [\w\s,]+'
            import_actuel = re.search(pattern_import, contenu_admin)
            
            if import_actuel:
                if import_actuel.group(0) != import_correct:
                    contenu_admin_corrige = contenu_admin.replace(import_actuel.group(0), import_correct)
                    
                    # Sauvegarder backup
                    backup_file = self.communication_path / 'admin_backup.py'
                    with open(backup_file, 'w', encoding='utf-8') as f:
                        f.write(contenu_admin)
                    
                    # Écrire la version corrigée
                    with open(self.admin_file, 'w', encoding='utf-8') as f:
                        f.write(contenu_admin_corrige)
                    
                    print("✅ admin.py corrigé - Import mis à jour")
                    print(f"📦 Backup sauvegardé: {backup_file.name}")
                else:
                    print("✅ Import dans admin.py déjà correct")
            else:
                print("❌ Impossible de trouver l'import dans admin.py")
                
        except Exception as e:
            print(f"❌ Erreur lors de la correction admin.py: {e}")
    
    def verifier_correction(self):
        """Vérifie que la correction a fonctionné"""
        print(f"\n✅ VÉRIFICATION DE LA CORRECTION")
        print("=" * 35)
        
        try:
            # Test d'import simple
            exec(open(self.models_file).read())
            print("✅ models.py - Import test réussi")
            
            # Test d'import admin
            exec(open(self.admin_file).read())
            print("✅ admin.py - Import test réussi")
            
            # Test spécifique GroupeCommunication
            code_test = """
from communication.models import GroupeCommunication, MessageGroupe
print("✅ GroupeCommunication importé avec succès")
print("✅ MessageGroupe importé avec succès")
"""
            exec(code_test)
            
        except NameError as e:
            if 'GroupeCommunication' in str(e):
                print("❌ GroupeCommunication toujours non défini")
                self.problemes.append("GroupeCommunication non résolu après correction")
            else:
                print(f"❌ Autre erreur: {e}")
        except Exception as e:
            print(f"❌ Erreur lors de la vérification: {e}")
    
    def generer_rapport(self):
        """Génère un rapport complet"""
        print(f"\n📊 RAPPORT D'ANALYSE COMPLET")
        print("=" * 40)
        
        if self.problemes:
            print("🚨 PROBLÈMES IDENTIFIÉS:")
            for i, probleme in enumerate(self.problemes, 1):
                print(f"  {i}. {probleme}")
        else:
            print("✅ AUCUN PROBLÈME IDENTIFIÉ")
        
        if self.solutions:
            print("\n💡 SOLUTIONS RECOMMANDÉES:")
            for i, solution in enumerate(self.solutions, 1):
                print(f"  {i}. {solution}")
        
        # Recommandations finales
        print("\n🎯 ACTIONS IMMÉDIATES:")
        print("  1. Vérifier que models.py contient bien GroupeCommunication")
        print("  2. Vérifier l'import dans admin.py inclut GroupeCommunication")
        print("  3. Exécuter 'python manage.py check' pour confirmer")
        print("  4. Créer les migrations si nécessaire")
    
    def executer_analyse_complete(self):
        """Exécute l'analyse complète"""
        print("🚀 DÉBUT DE L'ANALYSE NameError: 'GroupeCommunication'")
        print("=" * 55)
        
        if not self.analyser_structure_fichiers():
            return
        
        classes_models = self.analyser_models_py()
        self.analyser_admin_py()
        self.verifier_syntaxe_python()
        self.diagnostiquer_probleme_import()
        
        # Appliquer correction si nécessaire
        if self.problemes:
            print(f"\n💡 {len(self.problemes)} problème(s) détecté(s)")
            reponse = input("Appliquer la correction automatique? (o/N): ").strip().lower()
            if reponse in ['o', 'oui', 'y', 'yes']:
                self.corriger_automatiquement()
                self.verifier_correction()
        
        self.generer_rapport()

if __name__ == '__main__':
    analyzer = CommunicationAnalyzer()
    analyzer.executer_analyse_complete()