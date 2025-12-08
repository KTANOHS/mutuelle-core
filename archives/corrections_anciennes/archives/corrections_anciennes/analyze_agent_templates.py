#!/usr/bin/env python3
"""
Analyse détaillée du contenu des templates agent
"""

from pathlib import Path
import re

class AgentTemplatesAnalyzer:
    def __init__(self, agents_dir="templates/agents"):
        self.agents_dir = Path(agents_dir)
        
    def analyze_all_templates(self):
        """Analyser tous les templates agent"""
        results = {}
        
        for file_path in self.agents_dir.rglob("*.html"):
            if file_path.name.endswith('.backup') or 'backup' in file_path.name:
                continue
                
            relative_path = file_path.relative_to(self.agents_dir)
            results[str(relative_path)] = self.analyze_template(file_path)
            
        return results
    
    def analyze_template(self, file_path):
        """Analyser un template spécifique"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            analysis = {
                'size': file_path.stat().st_size,
                'lines': len(content.splitlines()),
                'extends': self.find_extends(content),
                'includes': self.find_includes(content),
                'blocks': self.find_blocks(content),
                'urls': self.find_urls(content),
                'variables': self.find_template_variables(content),
                'issues': self.check_issues(content, file_path.name)
            }
            
            return analysis
            
        except Exception as e:
            return {'error': str(e)}
    
    def find_extends(self, content):
        """Trouver les templates étendus"""
        extends = re.findall(r'\{%\s*extends\s+[\'"]([^\'"]+)[\'"]\s*%\}', content)
        return extends
    
    def find_includes(self, content):
        """Trouver les templates inclus"""
        includes = re.findall(r'\{%\s*include\s+[\'"]([^\'"]+)[\'"]\s*%\}', content)
        return includes
    
    def find_blocks(self, content):
        """Trouver les blocks Django"""
        blocks = re.findall(r'\{%\s*block\s+(\w+)\s*%\}', content)
        return blocks
    
    def find_urls(self, content):
        """Trouver les URLs Django"""
        urls = re.findall(r'\{%\s*url\s+[\'"]([^\'"]+)[\'"]\s*%\}', content)
        return urls
    
    def find_template_variables(self, content):
        """Trouver les variables de template"""
        variables = re.findall(r'\{\{\s*([\w\.]+)\s*\}\}', content)
        return list(set(variables))  # Retirer les doublons
    
    def check_issues(self, content, filename):
        """Vérifier les problèmes potentiels"""
        issues = []
        
        # Vérifier la taille
        if len(content) < 100:
            issues.append("Template très court, potentiellement vide")
        
        # Vérifier les URLs manquantes
        if 'url ' in content and not re.findall(r'\{%\s*url\s+', content):
            issues.append("URLs potentiellement mal formatées")
        
        # Vérifier les variables non échappées
        if '{{' in content and '}}' not in content:
            issues.append("Variables de template potentiellement mal fermées")
            
        return issues

def main():
    analyzer = AgentTemplatesAnalyzer()
    
    print("🔍 ANALYSE DÉTAILLÉE DES TEMPLATES AGENT")
    print("=" * 60)
    
    results = analyzer.analyze_all_templates()
    
    for template_path, analysis in results.items():
        if 'error' in analysis:
            print(f"\n❌ {template_path}: ERREUR - {analysis['error']}")
            continue
            
        print(f"\n📄 {template_path}")
        print(f"   📏 Taille: {analysis['size']} bytes, Lignes: {analysis['lines']}")
        
        if analysis['extends']:
            print(f"   🔗 Étend: {', '.join(analysis['extends'])}")
        
        if analysis['includes']:
            print(f"   📎 Inclut: {', '.join(analysis['includes'])}")
        
        if analysis['blocks']:
            print(f"   🧱 Blocks: {', '.join(analysis['blocks'])}")
        
        if analysis['urls']:
            print(f"   🌐 URLs: {', '.join(analysis['urls'][:5])}{'...' if len(analysis['urls']) > 5 else ''}")
        
        if analysis['variables']:
            print(f"   📊 Variables: {', '.join(analysis['variables'][:5])}{'...' if len(analysis['variables']) > 5 else ''}")
        
        if analysis['issues']:
            print(f"   ⚠️  Problèmes: {', '.join(analysis['issues'])}")

if __name__ == "__main__":
    main()