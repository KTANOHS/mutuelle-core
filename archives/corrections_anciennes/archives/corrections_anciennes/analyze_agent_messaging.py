#!/usr/bin/env python3
"""
ANALYSE SPÉCIFIQUE DE LA MESSAGERIE AGENT
"""

import os
import django
from pathlib import Path
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

BASE_DIR = Path(__file__).parent

class AgentMessagingAnalyzer:
    def __init__(self):
        self.results = {
            'templates': {},
            'urls': {},
            'views': {},
            'models': {},
            'issues': []
        }
    
    def run_agent_messaging_analysis(self):
        """Exécute l'analyse complète de la messagerie agent"""
        print("🔍 ANALYSE DE LA MESSAGERIE AGENT...")
        print("=" * 50)
        
        self.analyze_agent_templates()
        self.analyze_agent_urls()
        self.analyze_agent_views()
        self.analyze_agent_models()
        self.check_agent_dashboard_integration()
        self.check_agent_sidebar_integration()
        self.test_agent_messaging_urls()
        
        self.generate_agent_messaging_report()
    
    def analyze_agent_templates(self):
        """Analyse les templates liés à l'agent"""
        print("\n📁 ANALYSE DES TEMPLATES AGENT...")
        
        agent_templates = [
            'agents/dashboard.html',
            'agents/base_agent.html',
            'communication/messagerie_agent.html',
            'includes/sidebar.html'  # Sidebar agent
        ]
        
        for template_path in agent_templates:
            template_file = BASE_DIR / 'templates' / template_path
            
            if not template_file.exists():
                self.results['issues'].append(f"❌ TEMPLATE_MANQUANT: {template_path}")
                continue
            
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analysis = {
                'exists': True,
                'size': len(content),
                'messaging_elements': self.count_messaging_elements(content),
                'issues': self.analyze_template_issues(content, template_path)
            }
            
            self.results['templates'][template_path] = analysis
            
            print(f"   📄 {template_path}: {analysis['messaging_elements']} éléments messagerie")
    
    def count_messaging_elements(self, content):
        """Compte les éléments de messagerie dans un template"""
        elements = {
            'url_messagerie_agent': content.count('communication:messagerie_agent'),
            'url_nouveau_message': content.count('communication:nouveau_message'),
            'messaging_cards': len(re.findall(r'messagerie|Messagerie', content, re.IGNORECASE)),
            'message_buttons': len(re.findall(r'btn.*message|message.*btn', content, re.IGNORECASE)),
            'notification_badges': len(re.findall(r'badge.*message|message.*badge', content, re.IGNORECASE)),
        }
        return elements
    
    def analyze_template_issues(self, content, template_path):
        """Analyse les problèmes spécifiques dans un template"""
        issues = []
        
        # Vérifications spécifiques par template
        if 'agents/dashboard.html' in template_path:
            if 'communication:messagerie_agent' not in content:
                issues.append("LIEN_MESSAGERIE_MANQUANT_DASHBOARD")
            if 'col-xl-3 col-md-6 mb-4' in content and 'Messagerie' not in content:
                issues.append("CARTE_STAT_MESSAGERIE_MANQUANTE")
        
        elif 'includes/sidebar.html' in template_path:
            if 'communication:messagerie_agent' not in content:
                issues.append("LIEN_SIDEBAR_MANQUANT")
        
        elif 'communication/messagerie_agent.html' in template_path:
            if '{% url' not in content and 'href="/communication/' not in content:
                issues.append("INTERFACE_MESSAGERIE_INCOMPLETE")
        
        # Vérifications générales
        if '{% load static %}' not in content and 'static' in content:
            issues.append("LOAD_STATIC_MANQUANT")
        
        if '{{%' in content or '%}}' in content:
            issues.append("SYNTAXE_DOUBLE_ACCOLADES")
        
        return issues
    
    def analyze_agent_urls(self):
        """Analyse les URLs de messagerie agent"""
        print("\n🔗 ANALYSE DES URLs AGENT...")
        
        try:
            from django.urls import reverse, get_resolver
            from communication import urls as communication_urls
            
            # URLs spécifiques à vérifier
            agent_urls_to_check = [
                'communication:messagerie_agent',
                'communication:nouveau_message',
                'communication:message_detail',
                'communication:envoyer_message',
                'communication:liste_messages',
            ]
            
            for url_name in agent_urls_to_check:
                try:
                    url = reverse(url_name)
                    self.results['urls'][url_name] = {
                        'exists': True,
                        'url': url
                    }
                    print(f"   ✅ {url_name}: {url}")
                except Exception as e:
                    self.results['urls'][url_name] = {
                        'exists': False,
                        'error': str(e)
                    }
                    self.results['issues'].append(f"❌ URL_MANQUANTE: {url_name} - {e}")
                    print(f"   ❌ {url_name}: NON TROUVÉE")
        
        except Exception as e:
            self.results['issues'].append(f"❌ ERREUR_ANALYSE_URLS: {e}")
    
    def analyze_agent_views(self):
        """Analyse les vues de messagerie agent"""
        print("\n👁️ ANALYSE DES VUES AGENT...")
        
        try:
            # Vérifier si les vues existent dans communication/views.py
            views_file = BASE_DIR / 'communication' / 'views.py'
            if views_file.exists():
                with open(views_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Chercher les vues spécifiques agent
                agent_views = [
                    'messagerie_agent',
                    'MessageAgentListView',
                    'MessageAgentCreateView',
                    'message_agent'
                ]
                
                for view_name in agent_views:
                    if view_name in content:
                        print(f"   ✅ Vue trouvée: {view_name}")
                    else:
                        print(f"   ❌ Vue non trouvée: {view_name}")
                        self.results['issues'].append(f"VUE_MANQUANTE: {view_name}")
            
            else:
                self.results['issues'].append("FICHIER_VIEWS_MANQUANT: communication/views.py")
        
        except Exception as e:
            self.results['issues'].append(f"ERREUR_ANALYSE_VUES: {e}")
    
    def analyze_agent_models(self):
        """Analyse les modèles de messagerie"""
        print("\n🗄️ ANALYSE DES MODÈLES MESSAGERIE...")
        
        try:
            from communication.models import Message, Conversation
            
            # Vérifier l'accès aux modèles
            model_info = {
                'Message': {
                    'fields': [f.name for f in Message._meta.fields],
                    'count': Message.objects.count()
                },
                'Conversation': {
                    'fields': [f.name for f in Conversation._meta.fields],
                    'count': Conversation.objects.count()
                }
            }
            
            self.results['models'] = model_info
            print(f"   ✅ Modèle Message: {model_info['Message']['count']} messages")
            print(f"   ✅ Modèle Conversation: {model_info['Conversation']['count']} conversations")
        
        except Exception as e:
            self.results['issues'].append(f"ERREUR_MODELES: {e}")
            print(f"   ❌ Erreur modèles: {e}")
    
    def check_agent_dashboard_integration(self):
        """Vérifie l'intégration dans le dashboard agent"""
        print("\n📊 VÉRIFICATION DASHBOARD AGENT...")
        
        dashboard_file = BASE_DIR / 'templates' / 'agents' / 'dashboard.html'
        
        if not dashboard_file.exists():
            self.results['issues'].append("DASHBOARD_AGENT_MANQUANT")
            return
        
        with open(dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifications spécifiques
        checks = {
            'Carte statistique messagerie': 'col-xl-3 col-md-6 mb-4' in content and 'Messagerie' in content,
            'Lien messagerie présent': 'communication:messagerie_agent' in content,
            'Bouton accès rapide': 'btn.*messagerie|messagerie.*btn' in content.lower(),
            'Section messagerie visible': 'messagerie|Messagerie' in content
        }
        
        for check_name, check_result in checks.items():
            if check_result:
                print(f"   ✅ {check_name}")
            else:
                print(f"   ❌ {check_name}")
                self.results['issues'].append(f"DASHBOARD_{check_name.upper().replace(' ', '_')}_MANQUANT")
    
    def check_agent_sidebar_integration(self):
        """Vérifie l'intégration dans la sidebar agent"""
        print("\n📁 VÉRIFICATION SIDEBAR AGENT...")
        
        sidebar_files = [
            'includes/sidebar.html',
            'agents/base_agent.html'
        ]
        
        for sidebar_path in sidebar_files:
            sidebar_file = BASE_DIR / 'templates' / sidebar_path
            
            if not sidebar_file.exists():
                continue
            
            with open(sidebar_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'communication:messagerie_agent' in content:
                print(f"   ✅ Lien présent dans {sidebar_path}")
            else:
                print(f"   ❌ Lien manquant dans {sidebar_path}")
                self.results['issues'].append(f"SIDEBAR_LIEN_MANQUANT: {sidebar_path}")
    
    def test_agent_messaging_urls(self):
        """Teste l'accès aux URLs de messagerie agent"""
        print("\n🌐 TEST D'ACCÈS AUX URLs...")
        
        try:
            from django.test import Client
            from django.contrib.auth import get_user_model
            from django.contrib.auth.models import Group
            
            client = Client()
            User = get_user_model()
            
            # Créer un utilisateur test agent si nécessaire
            try:
                agent_user = User.objects.filter(groups__name='Agent').first()
                if not agent_user:
                    print("   ⚠️  Aucun agent trouvé, création d'un test...")
                    # Créer un agent test
                    agent_user = User.objects.create_user(
                        username='test_agent',
                        email='agent@test.com',
                        password='testpass123'
                    )
                    agent_group, created = Group.objects.get_or_create(name='Agent')
                    agent_user.groups.add(agent_group)
                
                # Tester la connexion
                login_success = client.login(username='test_agent', password='testpass123')
                if login_success:
                    print("   ✅ Connexion agent réussie")
                    
                    # Tester l'accès à la messagerie
                    try:
                        response = client.get(reverse('communication:messagerie_agent'))
                        status = "✅" if response.status_code == 200 else "❌"
                        print(f"   {status} Messagerie agent: HTTP {response.status_code}")
                        
                        if response.status_code != 200:
                            self.results['issues'].append(f"URL_MESSAGERIE_ERREUR: HTTP {response.status_code}")
                    
                    except Exception as e:
                        print(f"   ❌ Erreur accès messagerie: {e}")
                        self.results['issues'].append(f"ERREUR_ACCES_MESSAGERIE: {e}")
                
                else:
                    print("   ❌ Échec connexion agent")
                    self.results['issues'].append("ECHEC_CONNEXION_AGENT_TEST")
            
            except Exception as e:
                print(f"   ❌ Erreur création test: {e}")
                self.results['issues'].append(f"ERREUR_TEST_UTILISATEUR: {e}")
        
        except Exception as e:
            print(f"   ❌ Erreur test client: {e}")
    
    def generate_agent_messaging_report(self):
        """Génère un rapport détaillé"""
        print("\n" + "=" * 60)
        print("📊 RAPPORT D'ANALYSE MESSAGERIE AGENT")
        print("=" * 60)
        
        # Résumé
        total_issues = len(self.results['issues'])
        template_issues = sum(len(t['issues']) for t in self.results['templates'].values())
        url_issues = sum(1 for u in self.results['urls'].values() if not u['exists'])
        
        print(f"\n🎯 RÉSUMÉ:")
        print(f"   📁 Templates analysés: {len(self.results['templates'])}")
        print(f"   🔗 URLs vérifiées: {len(self.results['urls'])}")
        print(f"   🚨 Problèmes détectés: {total_issues}")
        
        # Détails par catégorie
        if self.results['templates']:
            print(f"\n📁 TEMPLATES:")
            for template, analysis in self.results['templates'].items():
                status = "✅" if not analysis['issues'] else "❌"
                elements = analysis['messaging_elements']
                print(f"   {status} {template}")
                print(f"      Éléments: {elements['url_messagerie_agent']} URLs, {elements['messaging_cards']} cartes")
                if analysis['issues']:
                    for issue in analysis['issues']:
                        print(f"      ❌ {issue}")
        
        if self.results['urls']:
            print(f"\n🔗 URLs:")
            for url_name, info in self.results['urls'].items():
                status = "✅" if info['exists'] else "❌"
                url_display = info.get('url', 'NON TROUVÉE')
                print(f"   {status} {url_name}: {url_display}")
        
        # Problèmes critiques
        if self.results['issues']:
            print(f"\n🚨 PROBLÈMES CRITIQUES ({total_issues}):")
            for issue in self.results['issues']:
                print(f"   {issue}")
        
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS:")
        
        if any('LIEN_MESSAGERIE_MANQUANT' in issue for issue in self.results['issues']):
            print("   1. Ajouter les liens messagerie dans le dashboard agent")
        
        if any('URL_MANQUANTE' in issue for issue in self.results['issues']):
            print("   2. Vérifier les URLs dans communication/urls.py")
        
        if any('VUE_MANQUANTE' in issue for issue in self.results['issues']):
            print("   3. Implémenter les vues manquantes dans communication/views.py")
        
        if any('DASHBOARD' in issue for issue in self.results['issues']):
            print("   4. Corriger l'intégration dashboard agent")
        
        print(f"\n🔧 PROCHAINES ÉTAPES:")
        print("   1. Exécutez ce script pour voir les problèmes spécifiques")
        print("   2. Corrigez les problèmes identifiés")
        print("   3. Testez: http://localhost:8000/communication/agent/messagerie/")
        print("   4. Vérifiez le dashboard agent")
        
        # Sauvegarde du rapport
        self.save_agent_report()
    
    def save_agent_report(self):
        """Sauvegarde le rapport dans un fichier"""
        report_file = BASE_DIR / 'ANALYSE_MESSAGERIE_AGENT.md'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# RAPPORT D'ANALYSE MESSAGERIE AGENT\n\n")
            
            f.write("## 📊 RÉSUMÉ\n\n")
            f.write(f"- Templates analysés: {len(self.results['templates'])}\n")
            f.write(f"- URLs vérifiées: {len(self.results['urls'])}\n")
            f.write(f"- Problèmes détectés: {len(self.results['issues'])}\n\n")
            
            if self.results['issues']:
                f.write("## 🚨 PROBLÈMES\n\n")
                for issue in self.results['issues']:
                    f.write(f"- {issue}\n")
            
            f.write("\n## 💡 SOLUTIONS\n\n")
            f.write("1. Vérifier communication/urls.py - URLs agent\n")
            f.write("2. Vérifier communication/views.py - Vues agent\n")
            f.write("3. Vérifier templates/agents/dashboard.html - Intégration\n")
            f.write("4. Vérifier templates/includes/sidebar.html - Lien navigation\n")
        
        print(f"\n📄 Rapport détaillé sauvegardé: {report_file}")

def main():
    analyzer = AgentMessagingAnalyzer()
    analyzer.run_agent_messaging_analysis()

if __name__ == "__main__":
    main()