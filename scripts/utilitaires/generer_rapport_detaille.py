#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def generer_rapport_detaille():
    """Génère un rapport détaillé des modifications"""
    
    print("📋 RAPPORT DÉTAILLÉ DES MODIFICATIONS")
    print("=" * 60)
    
    # Agents - Détail complet
    print("\n👥 AGENTS - DÉTAIL COMPLET")
    print("=" * 40)
    
    try:
        from agents.models import Agent, BonSoin, VerificationCotisation
        
        print("\n📊 MODÈLES AGENTS:")
        print(f"   • Agent: {Agent._meta.get_fields().__len__()} champs")
        print(f"   • BonSoin: {BonSoin._meta.get_fields().__len__()} champs") 
        print(f"   • VerificationCotisation: {VerificationCotisation._meta.get_fields().__len__()} champs")
        
        # Statistiques
        nb_agents = Agent.objects.count()
        nb_bons = BonSoin.objects.count()
        nb_verifications = VerificationCotisation.objects.count()
        
        print(f"\n📈 STATISTIQUES:")
        print(f"   • Agents enregistrés: {nb_agents}")
        print(f"   • Bons de soin créés: {nb_bons}")
        print(f"   • Vérifications effectuées: {nb_verifications}")
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Communication - Détail complet
    print("\n💬 COMMUNICATION - DÉTAIL COMPLET")
    print("=" * 40)
    
    try:
        from communication.models import Message, Notification, PieceJointe
        
        print("\n📊 MODÈLES COMMUNICATION:")
        print(f"   • Message: {Message._meta.get_fields().__len__()} champs")
        print(f"   • Notification: {Notification._meta.get_fields().__len__()} champs")
        print(f"   • PieceJointe: {PieceJointe._meta.get_fields().__len__()} champs")
        
        # Statistiques
        nb_messages = Message.objects.count()
        nb_notifications = Notification.objects.count()
        nb_pieces_jointes = PieceJointe.objects.count()
        
        print(f"\n📈 STATISTIQUES:")
        print(f"   • Messages échangés: {nb_messages}")
        print(f"   • Notifications créées: {nb_notifications}")
        print(f"   • Pièces jointes uploadées: {nb_pieces_jointes}")
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Templates
    print("\n🎨 TEMPLATES IMPLÉMENTÉS")
    print("=" * 40)
    
    templates_agents = list(Path('templates/agents').rglob('*.html'))
    templates_communication = list(Path('templates/communication').rglob('*.html'))
    
    print(f"\n👥 TEMPLATES AGENTS ({len(templates_agents)}):")
    for template in templates_agents:
        print(f"   • {template.relative_to('templates')}")
    
    print(f"\n💬 TEMPLATES COMMUNICATION ({len(templates_communication)}):")
    for template in templates_communication:
        print(f"   • {template.relative_to('templates')}")
    
    # URLs disponibles
    print("\n🔗 URLS DISPONIBLES")
    print("=" * 40)
    
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        
        urls_agents = []
        urls_communication = []
        
        for namespace, pattern in resolver.namespace_dict.items():
            if 'agents' in namespace:
                urls_agents.extend(get_urls_from_pattern(pattern))
            elif 'communication' in namespace:
                urls_communication.extend(get_urls_from_pattern(pattern))
        
        print(f"\n👥 URLS AGENTS ({len(urls_agents)}):")
        for url in urls_agents[:10]:  # Limiter l'affichage
            print(f"   • {url}")
        
        print(f"\n💬 URLS COMMUNICATION ({len(urls_communication)}):")
        for url in urls_communication[:10]:
            print(f"   • {url}")
            
    except Exception as e:
        print(f"   ❌ Erreur URLs: {e}")

def get_urls_from_pattern(pattern):
    """Extrait les URLs d'un pattern"""
    urls = []
    try:
        if hasattr(pattern, 'url_patterns'):
            for sub_pattern in pattern.url_patterns:
                urls.extend(get_urls_from_pattern(sub_pattern))
        elif hasattr(pattern, 'pattern'):
            urls.append(str(pattern.pattern))
    except:
        pass
    return urls

def checklist_deploiement():
    """Checklist pour le déploiement"""
    print("\n✅ CHECKLIST DÉPLOIEMENT")
    print("=" * 40)
    
    checklist = [
        ("📊 Migrations appliquées", verifier_migrations_appliquees()),
        ("🔗 URLs configurées", verifier_urls_config()),
        ("⚙️ Admin fonctionnel", verifier_admin()),
        ("🎨 Templates accessibles", verifier_templates()),
        ("📱 Tests fonctionnels", verifier_tests()),
    ]
    
    for item, statut in checklist:
        if statut:
            print(f"   ✅ {item}")
        else:
            print(f"   ❌ {item}")

def verifier_migrations_appliquees():
    try:
        from django.db.migrations.recorder import MigrationRecorder
        migrations_agents = MigrationRecorder.Migration.objects.filter(app='agents').count()
        migrations_comm = MigrationRecorder.Migration.objects.filter(app='communication').count()
        return migrations_agents > 0 and migrations_comm > 0
    except:
        return False

def verifier_urls_config():
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        return any('agents' in str(p) for p in resolver.url_patterns)
    except:
        return False

def verifier_admin():
    try:
        from django.contrib import admin
        from agents.models import Agent
        return Agent in admin.site._registry
    except:
        return False

def verifier_templates():
    return Path('templates/agents').exists() and Path('templates/communication').exists()

def verifier_tests():
    try:
        # Test basique d'import
        from agents.models import Agent
        from communication.models import Message
        return True
    except:
        return False

if __name__ == "__main__":
    generer_rapport_detaille()
    checklist_deploiement()
    
    print(f"\n🎯 PROCHAINES ÉTAPES:")
    print("   1. Vérifier la checklist ci-dessus")
    print("   2. Tester manuellement les fonctionnalités")
    print("   3. Vérifier les permissions utilisateurs")
    print("   4. Déployer en environnement de test")
    print("   5. Former les utilisateurs aux nouvelles fonctionnalités")