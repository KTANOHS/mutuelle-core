# analyze_core.py
import os
import sys
import inspect
import django
from pathlib import Path

# Configuration Django
project_path = '/Users/koffitanohsoualiho/Documents/projet'
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    DJANGO_AVAILABLE = True
except Exception as e:
    print(f"❌ Impossible de configurer Django: {e}")
    DJANGO_AVAILABLE = False

class CoreAnalyzer:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.core_path = self.project_path / 'mutuelle_core'
        
    def analyze_structure(self):
        """Analyse la structure du projet core"""
        print("📁 ANALYSE STRUCTURE CORE")
        print("=" * 60)
        
        if not self.core_path.exists():
            print(f"❌ Dossier core non trouvé: {self.core_path}")
            return False
            
        print(f"📍 Chemin core: {self.core_path}")
        
        # Lister les fichiers principaux
        core_files = list(self.core_path.glob('*.py'))
        print(f"\n📄 Fichiers principaux:")
        for file in core_files:
            if file.name != '__init__.py':
                size = file.stat().st_size
                print(f"   - {file.name} ({size} octets)")
        
        return True

    def analyze_urls(self):
        """Analyse complète des URLs"""
        print("\n\n🔗 ANALYSE DES URLs")
        print("=" * 60)
        
        urls_file = self.core_path / 'urls.py'
        if not urls_file.exists():
            print(f"❌ Fichier urls.py non trouvé: {urls_file}")
            return
            
        print(f"📍 Analyse de: {urls_file}")
        
        try:
            # Importer et analyser les URLs
            from mutuelle_core import urls
            from django.urls import get_resolver
            
            resolver = get_resolver()
            url_patterns = []
            
            def extract_patterns(patterns, prefix="", depth=0):
                for pattern in patterns:
                    if hasattr(pattern, 'pattern'):
                        # Django 2.0+
                        if hasattr(pattern, 'url_patterns'):
                            # Include
                            print(f"{'  ' * depth}📁 {pattern.pattern} [include]")
                            extract_patterns(pattern.url_patterns, prefix, depth + 1)
                        else:
                            # Pattern simple
                            callback = getattr(pattern, 'callback', None)
                            if callback:
                                callback_name = getattr(callback, '__name__', 'Unknown')
                                callback_module = getattr(callback, '__module__', 'Unknown')
                                url_name = getattr(pattern, 'name', 'Sans nom')
                                
                                url_info = {
                                    'pattern': str(pattern.pattern),
                                    'callback': f"{callback_module}.{callback_name}",
                                    'name': url_name
                                }
                                url_patterns.append(url_info)
                                
                                status = "✅" if callback_name != 'view' else "⚠️"
                                print(f"{'  ' * depth}{status} {pattern.pattern} -> {callback_name} [name: {url_name}]")
            
            print("\n📋 Liste des URLs:")
            extract_patterns(resolver.url_patterns)
            
            # Analyse des URLs problématiques
            print(f"\n🔍 URLs POTENTIELLEMENT PROBLÉMATIQUES:")
            problematic_urls = []
            for url in url_patterns:
                if 'redirect-after-login' in url['pattern']:
                    problematic_urls.append(url)
                if url['callback'] == 'mutuelle_core.views.view':
                    problematic_urls.append(url)
                    
            for url in problematic_urls:
                print(f"   ⚠️  {url['pattern']} -> {url['callback']} [name: {url['name']}]")
                
            return url_patterns
            
        except Exception as e:
            print(f"❌ Erreur analyse URLs: {e}")
            import traceback
            traceback.print_exc()

    def analyze_views(self):
        """Analyse complète des views"""
        print("\n\n👁️ ANALYSE DES VIEWS")
        print("=" * 60)
        
        views_file = self.core_path / 'views.py'
        if not views_file.exists():
            print(f"❌ Fichier views.py non trouvé: {views_file}")
            return
            
        print(f"📍 Analyse de: {views_file}")
        
        try:
            with open(views_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Compter les lignes et fonctions
            lines = content.split('\n')
            functions = []
            classes = []
            
            current_function = None
            for i, line in enumerate(lines, 1):
                line_stripped = line.strip()
                
                # Détection des fonctions
                if line_stripped.startswith('def '):
                    func_name = line_stripped[4:].split('(')[0]
                    functions.append({'name': func_name, 'line': i, 'type': 'function'})
                    current_function = func_name
                    
                # Détection des classes
                elif line_stripped.startswith('class '):
                    class_name = line_stripped[6:].split('(')[0].split(':')[0]
                    classes.append({'name': class_name, 'line': i, 'type': 'class'})
                    
                # Détection des décorateurs importants
                elif '@' in line_stripped and current_function:
                    if 'login_required' in line_stripped:
                        for func in functions:
                            if func['name'] == current_function:
                                func['decorator'] = 'login_required'
                    elif 'assureur_required' in line_stripped:
                        for func in functions:
                            if func['name'] == current_function:
                                func['decorator'] = 'assureur_required'
            
            print(f"📊 Statistiques:")
            print(f"   - Lignes de code: {len(lines)}")
            print(f"   - Fonctions: {len(functions)}")
            print(f"   - Classes: {len(classes)}")
            
            print(f"\n📋 Liste des views:")
            for func in functions:
                decorator_info = f" [{func.get('decorator', '')}]" if func.get('decorator') else ""
                print(f"   📍 {func['name']}{decorator_info} (ligne {func['line']})")
            
            # Views critiques
            print(f"\n🎯 VIEWS CRITIQUES:")
            critical_views = ['redirect_to_user_dashboard', 'assureur_dashboard', 'home', 'view']
            for func in functions:
                if func['name'] in critical_views:
                    status = "✅" if func.get('decorator') else "⚠️"
                    print(f"   {status} {func['name']} {func.get('decorator', 'SANS DÉCORATEUR')}")
                    
            return functions
            
        except Exception as e:
            print(f"❌ Erreur analyse views: {e}")

    def analyze_utils(self):
        """Analyse complète des utilitaires"""
        print("\n\n🛠️ ANALYSE DES UTILITAIRES")
        print("=" * 60)
        
        utils_file = self.core_path / 'utils.py'
        if not utils_file.exists():
            print(f"❌ Fichier utils.py non trouvé: {utils_file}")
            return
            
        print(f"📍 Analyse de: {utils_file}")
        
        try:
            with open(utils_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Analyser les fonctions utilitaires
            import re
            
            # Trouver toutes les fonctions
            function_pattern = r'def (\w+)\(.*?\):'
            functions = re.findall(function_pattern, content)
            
            # Trouver les décorateurs
            decorator_pattern = r'@(\w+)\s+def (\w+)'
            decorators = re.findall(decorator_pattern, content)
            
            # Trouver les constantes
            constant_pattern = r'^([A-Z_]+)\s*='
            constants = re.findall(constant_pattern, content, re.MULTILINE)
            
            print(f"📊 Statistiques utils:")
            print(f"   - Fonctions: {len(functions)}")
            print(f"   - Décorateurs: {len(decorators)}")
            print(f"   - Constantes: {len(constants)}")
            
            print(f"\n📋 Fonctions utilitaires:")
            for func in functions:
                # Vérifier si c'est une fonction critique
                if 'redirect' in func.lower() or 'group' in func.lower() or 'permission' in func.lower():
                    print(f"   🎯 {func} (FONCTION CRITIQUE)")
                else:
                    print(f"   📍 {func}")
            
            print(f"\n🎯 DÉCORATEURS:")
            for decorator, func in decorators:
                print(f"   @{decorator} -> {func}")
                
            print(f"\n🔣 CONSTANTES:")
            for constant in constants[:10]:  # Premières 10 constantes
                print(f"   {constant}")
                
            # Analyse spécifique des fonctions de redirection
            print(f"\n🔍 ANALYSE FONCTIONS REDIRECTION:")
            redirect_functions = [f for f in functions if 'redirect' in f.lower()]
            for func in redirect_functions:
                print(f"   📍 {func}")
                
                # Extraire le code de la fonction
                func_pattern = rf'def {func}\(.*?\):.*?(?=def|\Z)'
                func_match = re.search(func_pattern, content, re.DOTALL)
                if func_match:
                    func_code = func_match.group(0)
                    lines = func_code.split('\n')
                    print(f"      📝 {len(lines)} lignes")
                    
                    # Vérifier les problèmes potentiels
                    if 'dashboard' in func_code and 'redirect-after-login' in func_code:
                        print("      ⚠️  POTENTIELLE BOUCLE: Redirection vers dashboard ET redirect-after-login")
                    
        except Exception as e:
            print(f"❌ Erreur analyse utils: {e}")

    def analyze_models(self):
        """Analyse rapide des modèles"""
        print("\n\n🗄️ ANALYSE RAPIDE DES MODÈLES")
        print("=" * 60)
        
        models_file = self.core_path / 'models.py'
        if not models_file.exists():
            print(f"❌ Fichier models.py non trouvé: {models_file}")
            return
            
        try:
            with open(models_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Compter les modèles
            class_pattern = r'class (\w+)\(.*Model.*\):'
            models = re.findall(class_pattern, content)
            
            print(f"📊 Modèles trouvés: {len(models)}")
            for model in models:
                print(f"   📍 {model}")
                
        except Exception as e:
            print(f"❌ Erreur analyse modèles: {e}")

    def analyze_problems(self):
        """Analyse des problèmes potentiels"""
        print("\n\n🚨 ANALYSE DES PROBLÈMES POTENTIELS")
        print("=" * 60)
        
        problems = []
        
        # 1. Vérifier la vue 'view' générique
        try:
            from mutuelle_core import views
            if hasattr(views, 'view'):
                problems.append("⚠️  Vue 'view' générique détectée - peut causer des conflits")
        except:
            pass
            
        # 2. Vérifier les URLs en double
        urls = self.analyze_urls()
        if urls:
            url_patterns = [url['pattern'] for url in urls]
            duplicates = set([x for x in url_patterns if url_patterns.count(x) > 1])
            if duplicates:
                problems.append(f"⚠️  URLs en double: {duplicates}")
                
        # 3. Vérifier les fonctions de redirection
        utils_file = self.core_path / 'utils.py'
        if utils_file.exists():
            with open(utils_file, 'r') as f:
                content = f.read()
                if 'redirect-after-login' in content and 'dashboard' in content:
                    problems.append("⚠️  Potentielle boucle dans les fonctions de redirection")
        
        # 4. Afficher les problèmes
        if problems:
            for problem in problems:
                print(f"   {problem}")
        else:
            print("   ✅ Aucun problème critique détecté")

    def generate_report(self):
        """Génère un rapport complet"""
        print("\n\n📊 RAPPORT COMPLET - MUTUELLE CORE")
        print("=" * 60)
        
        if not self.analyze_structure():
            return
            
        self.analyze_urls()
        self.analyze_views() 
        self.analyze_utils()
        self.analyze_models()
        self.analyze_problems()
        
        print("\n" + "=" * 60)
        print("🎯 RECOMMANDATIONS")
        print("=" * 60)
        
        recommendations = [
            "✅ Vérifier que toutes les views critiques ont les bons décorateurs",
            "✅ S'assurer qu'il n'y a pas de boucles dans les redirections", 
            "✅ Tester chaque type d'utilisateur (assureur, medecin, etc.)",
            "✅ Vérifier les groupes et permissions des utilisateurs",
            "✅ S'assurer que tous les templates existent"
        ]
        
        for rec in recommendations:
            print(f"   {rec}")

def quick_analysis():
    """Analyse rapide sans Django"""
    print("⚡ ANALYSE RAPIDE SANS DJANGO")
    print("=" * 60)
    
    project_path = Path('/Users/koffitanohsoualiho/Documents/projet')
    core_path = project_path / 'mutuelle_core'
    
    if not core_path.exists():
        print("❌ Dossier core non trouvé")
        return
        
    # Analyse des fichiers
    files_to_check = ['urls.py', 'views.py', 'utils.py', 'models.py']
    
    for file_name in files_to_check:
        file_path = core_path / file_name
        if file_path.exists():
            size = file_path.stat().st_size
            lines = len(file_path.read_text().split('\n'))
            print(f"📄 {file_name}: {size} octets, {lines} lignes")
        else:
            print(f"❌ {file_name}: NON TROUVÉ")

if __name__ == "__main__":
    if DJANGO_AVAILABLE:
        analyzer = CoreAnalyzer(project_path)
        analyzer.generate_report()
    else:
        quick_analysis()
    
    print("\n" + "=" * 60)
    print("🔧 POUR RÉSOUDRE LES PROBLÈMES IDENTIFIÉS:")
    print("=" * 60)
    print("1. Exécutez: python fix_user_groups.py")
    print("2. Exécutez: python fix_redirect_view_groups.py") 
    print("3. Testez avec: python final_assureur_test.py")