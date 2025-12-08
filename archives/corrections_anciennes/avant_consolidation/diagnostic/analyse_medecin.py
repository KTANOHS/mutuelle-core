#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT D'ANALYSE COMPLÈTE - MODULE MEDECIN
Version Python compatible avec tous les environnements
"""

import os
import sys
import re
import subprocess
from pathlib import Path

class MedecinAnalyzer:
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.medecin_dir = self.project_dir / "medecin"
        self.templates_dir = self.medecin_dir / "templates" / "medecin"
        
    def print_header(self, title):
        print(f"\n{'='*50}")
        print(f"🔍 {title}")
        print(f"{'='*50}")
    
    def analyze_structure(self):
        """Analyse la structure du module medecin"""
        self.print_header("STRUCTURE DU MODULE MEDECIN")
        
        if not self.medecin_dir.exists():
            print("❌ Dossier medecin introuvable")
            return False
            
        print("✅ Dossier medecin trouvé")
        print("\n📁 Structure:")
        for item in self.medecin_dir.rglob("*"):
            if "__pycache__" not in str(item) and not item.name.endswith(".pyc"):
                rel_path = item.relative_to(self.medecin_dir)
                prefix = "  " * (len(rel_path.parents) - 1)
                if item.is_dir():
                    print(f"{prefix}📁 {rel_path}/")
                else:
                    print(f"{prefix}📄 {rel_path}")
        return True
    
    def analyze_models(self):
        """Analyse le fichier models.py"""
        self.print_header("ANALYSE DES MODÈLES")
        
        models_file = self.medecin_dir / "models.py"
        if not models_file.exists():
            print("❌ models.py introuvable")
            return
            
        print("✅ models.py trouvé")
        
        # Compter les lignes
        with open(models_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            print(f"📊 Lignes de code: {len(lines)}")
            
        # Trouver les classes de modèles
        class_pattern = r"^class (\w+)(?:\(|:)"
        classes = re.findall(class_pattern, content, re.MULTILINE)
        print(f"\n🏷️  Classes de modèles trouvées ({len(classes)}):")
        for class_name in classes[:10]:  # Afficher les 10 premières
            print(f"   • {class_name}")
            
        # Vérifier les imports
        import_pattern = r"^(from|import) .*"
        imports = re.findall(import_pattern, content, re.MULTILINE)
        print(f"\n🔄 Imports trouvés ({len(imports)}):")
        for imp in imports[:5]:
            print(f"   {imp}")
    
    def analyze_views(self):
        """Analyse le fichier views.py"""
        self.print_header("ANALYSE DES VUES")
        
        views_file = self.medecin_dir / "views.py"
        if not views_file.exists():
            print("❌ views.py introuvable")
            return
            
        print("✅ views.py trouvé")
        
        with open(views_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            print(f"📊 Lignes de code: {len(lines)}")
            
        # Trouver les fonctions de vues
        function_pattern = r"^def (\w+)\("
        functions = re.findall(function_pattern, content, re.MULTILINE)
        print(f"\n👁️  Fonctions de vues trouvées ({len(functions)}):")
        for func in functions[:15]:
            print(f"   • {func}()")
            
        # Vérifier les décorateurs
        decorator_pattern = r"^@(\w+)"
        decorators = re.findall(decorator_pattern, content, re.MULTILINE)
        print(f"\n🎀 Décorateurs utilisés:")
        decorator_count = {}
        for decorator in decorators:
            decorator_count[decorator] = decorator_count.get(decorator, 0) + 1
            
        for decorator, count in decorator_count.items():
            print(f"   • @{decorator}: {count} fois")
            
        # Test de syntaxe
        try:
            compile(content, 'views.py', 'exec')
            print("✅ Syntaxe Python valide")
        except SyntaxError as e:
            print(f"❌ Erreur de syntaxe: {e}")
    
    def analyze_urls(self):
        """Analyse le fichier urls.py"""
        self.print_header("ANALYSE DES URLS")
        
        urls_file = self.medecin_dir / "urls.py"
        if not urls_file.exists():
            print("❌ urls.py introuvable")
            return
            
        print("✅ urls.py trouvé")
        
        with open(urls_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Trouver les patterns d'URL
        url_pattern = r"path\(['\"]([^'\"]+)['\"],\s*([^,]+),\s*name=['\"]([^'\"]+)['\"]\)"
        urls = re.findall(url_pattern, content)
        
        print(f"\n🔗 URLs définies ({len(urls)}):")
        for url_pattern, view, name in urls[:20]:
            print(f"   • {url_pattern} → {view} (name: '{name}')")
            
        # Vérifier les imports problématiques
        if "views_suivi_chronique" in content:
            print("\n🚨 PROBLÈME CRITIQUE: 'views_suivi_chronique' trouvé dans urls.py")
            print("   Cette importation n'existe pas et doit être remplacée par 'views'")
            
        # Test d'import
        try:
            # Ajouter le projet au path Python
            sys.path.insert(0, str(self.project_dir))
            from medecin import urls
            print("✅ URLs importées avec succès")
        except Exception as e:
            print(f"❌ Erreur d'import des URLs: {e}")
    
    def analyze_templates(self):
        """Analyse des templates"""
        self.print_header("ANALYSE DES TEMPLATES")
        
        if not self.templates_dir.exists():
            print("❌ Dossier templates/medecin introuvable")
            return
            
        templates = list(self.templates_dir.rglob("*.html"))
        print(f"✅ {len(templates)} templates trouvés")
        
        # Templates critiques
        critical_templates = [
            "dashboard.html", "mes_rendez_vous.html", 
            "liste_bons.html", "creer_ordonnance.html",
            "detail_bon.html", "detail_consultation.html"
        ]
        
        print("\n🎯 Templates critiques:")
        for template in critical_templates:
            template_path = self.templates_dir / template
            if template_path.exists():
                print(f"   ✅ {template}")
            else:
                print(f"   ❌ {template} - MANQUANT")
    
    def check_imports(self):
        """Vérifie les imports entre modules"""
        self.print_header("VÉRIFICATION DES IMPORTS")
        
        try:
            sys.path.insert(0, str(self.project_dir))
            
            modules_to_check = ['medecin.models', 'medecin.views', 'medecin.urls']
            for module_name in modules_to_check:
                try:
                    __import__(module_name)
                    print(f"✅ {module_name} - Import réussi")
                except ImportError as e:
                    print(f"❌ {module_name} - Erreur: {e}")
                    
        except Exception as e:
            print(f"❌ Erreur lors de la vérification des imports: {e}")
    
    def generate_report(self):
        """Génère un rapport complet"""
        self.print_header("RAPPORT COMPLET - MODULE MEDECIN")
        
        # Collecter les statistiques
        stats = {
            'models': 0,
            'views': 0,
            'urls': 0,
            'templates': 0
        }
        
        # Compter les modèles
        models_file = self.medecin_dir / "models.py"
        if models_file.exists():
            with open(models_file, 'r') as f:
                content = f.read()
                stats['models'] = len(re.findall(r"^class (\w+)", content, re.MULTILINE))
        
        # Compter les vues
        views_file = self.medecin_dir / "views.py"
        if views_file.exists():
            with open(views_file, 'r') as f:
                content = f.read()
                stats['views'] = len(re.findall(r"^def (\w+)\(", content, re.MULTILINE))
        
        # Compter les URLs
        urls_file = self.medecin_dir / "urls.py"
        if urls_file.exists():
            with open(urls_file, 'r') as f:
                content = f.read()
                stats['urls'] = len(re.findall(r"path\(", content))
        
        # Compter les templates
        if self.templates_dir.exists():
            stats['templates'] = len(list(self.templates_dir.rglob("*.html")))
        
        print("📊 STATISTIQUES DU MODULE:")
        print(f"   • Modèles: {stats['models']}")
        print(f"   • Vues: {stats['views']}")
        print(f"   • URLs: {stats['urls']}")
        print(f"   • Templates: {stats['templates']}")
        
        # Vérifications critiques
        print("\n🔍 POINTS DE CONTRÔLE CRITIQUES:")
        
        # Vérifier les vues principales
        critical_views = ['dashboard_medecin', 'liste_bons', 'mes_rendez_vous', 'creer_ordonnance']
        views_file = self.medecin_dir / "views.py"
        if views_file.exists():
            with open(views_file, 'r') as f:
                views_content = f.read()
                for view in critical_views:
                    if f"def {view}" in views_content:
                        print(f"   ✅ Vue '{view}' trouvée")
                    else:
                        print(f"   ❌ Vue '{view}' MANQUANTE")
        
        # Vérifier les URLs principales
        critical_urls = ['dashboard', 'liste_bons', 'mes_rendez_vous']
        urls_file = self.medecin_dir / "urls.py"
        if urls_file.exists():
            with open(urls_file, 'r') as f:
                urls_content = f.read()
                for url in critical_urls:
                    if f"name='{url}'" in urls_content:
                        print(f"   ✅ URL '{url}' trouvée")
                    else:
                        print(f"   ❌ URL '{url}' MANQUANTE")
        
        # Test final
        print("\n🧪 TEST FINAL:")
        try:
            sys.path.insert(0, str(self.project_dir))
            from medecin import models, views, urls
            print("✅ ✅ ✅ MODULE MEDECIN FONCTIONNEL ✅ ✅ ✅")
        except Exception as e:
            print(f"❌ ❌ ❌ ERREUR CRITIQUE: {e} ❌ ❌ ❌")
    
    def run_complete_analysis(self):
        """Exécute l'analyse complète"""
        print("🔍 DÉMARRAGE DE L'ANALYSE COMPLÈTE DU MODULE MEDECIN")
        print("=" * 60)
        
        if not self.analyze_structure():
            return
            
        self.analyze_models()
        self.analyze_views()
        self.analyze_urls()
        self.analyze_templates()
        self.check_imports()
        self.generate_report()
        
        print("\n" + "=" * 60)
        print("🎉 ANALYSE TERMINÉE")

def main():
    """Fonction principale"""
    project_dir = "/Users/koffitanohsoualiho/Documents/sup/projet 21.49.30"
    
    if not os.path.exists(project_dir):
        print(f"❌ Le dossier du projet n'existe pas: {project_dir}")
        sys.exit(1)
    
    analyzer = MedecinAnalyzer(project_dir)
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()