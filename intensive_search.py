#!/usr/bin/env python3
"""
Recherche intensive de tous les fichiers agents
"""

import os
import subprocess
from pathlib import Path

def intensive_agent_search():
    print("🔍 RECHERCHE INTENSIVE DES FICHIERS AGENTS")
    print("=" * 60)
    
    # Recherche dans tout le système
    search_patterns = [
        "*agent*",
        "*dashboard*", 
        "*agents*",
        "*/agents/*"
    ]
    
    print("1. 📁 RECHERCHE DANS TOUT LE PROJET:")
    project_root = Path(".")
    
    # Recherche récursive de tous les fichiers HTML
    html_files = list(project_root.rglob("*.html"))
    agent_related = []
    
    for file_path in html_files:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        if any(keyword in content.lower() for keyword in ['agent', 'dashboard', 'espace agent']):
            agent_related.append(file_path)
            print(f"   📄 {file_path} (contient 'agent')")
    
    print(f"\n📊 {len(agent_related)} fichiers liés aux agents trouvés")
    
    # Vérifier les dossiers cachés
    print("\n2. 🔍 RECHERCHE DES DOSSIERS CACHÉS:")
    hidden_dirs = [d for d in project_root.iterdir() if d.name.startswith('.') and d.is_dir()]
    for hidden_dir in hidden_dirs:
        print(f"   📁 {hidden_dir}")
        # Chercher dans les dossiers cachés
        for html_file in hidden_dir.rglob("*.html"):
            print(f"      📄 {html_file}")

def check_django_template_loaders():
    """Vérifier la configuration des template loaders Django"""
    print(f"\n3. ⚙️ CONFIGURATION DJANGO TEMPLATES:")
    
    try:
        import django
        from django.conf import settings
        
        if not settings.configured:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
            django.setup()
        
        template_dirs = getattr(settings, 'TEMPLATES', [])
        for config in template_dirs:
            if 'DIRS' in config:
                print(f"   📂 Dirs: {config['DIRS']}")
            if 'APP_DIRS' in config:
                print(f"   📱 APP_DIRS: {config['APP_DIRS']}")
                
    except Exception as e:
        print(f"   ❌ Erreur configuration: {e}")

def check_system_temp_files():
    """Vérifier les fichiers temporaires système"""
    print(f"\n4. 🗑️ FICHIERS TEMPORAIRES SYSTÈME:")
    
    temp_dirs = [
        "/tmp",
        "/var/tmp", 
        os.path.expanduser("~/tmp"),
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Downloads")
    ]
    
    for temp_dir in temp_dirs:
        if Path(temp_dir).exists():
            print(f"   🔍 Scan de {temp_dir}")
            try:
                # Chercher des fichiers agents
                for pattern in ["*agent*", "*dashboard*"]:
                    for file_path in Path(temp_dir).rglob(pattern):
                        if file_path.suffix in ['.html', '.py']:
                            print(f"      📄 {file_path}")
            except Exception as e:
                print(f"      ❌ Erreur scan: {e}")

def check_process_and_cache():
    """Vérifier les processus et caches en cours"""
    print(f"\n5. 🔄 PROCESSUS ET CACHES:")
    
    try:
        # Vérifier les processus Django
        result = subprocess.run(
            "ps aux | grep -i django", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        if result.stdout:
            print("   🖥️ Processus Django trouvés:")
            for line in result.stdout.split('\n'):
                if 'python' in line and 'manage.py' in line:
                    print(f"      🔧 {line}")
        
        # Vérifier le cache mémoire
        result = subprocess.run(
            "lsof | grep -i template", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        if result.stdout:
            print("   📝 Fichiers templates ouverts:")
            for line in result.stdout.split('\n')[:3]:
                print(f"      📄 {line}")
                
    except Exception as e:
        print(f"   ❌ Erreur processus: {e}")

def create_emergency_block():
    """Créer un bloc d'urgence pour empêcher l'accès"""
    print(f"\n6. 🚨 CRÉATION BLOC D'URGENCE:")
    
    # Créer un view de secours
    emergency_view = """
# agents/views_emergency.py
from django.http import HttpResponse
from django.shortcuts import render

def emergency_dashboard(request):
    return HttpResponse('''
    <html>
    <head><title>MAINTENANCE AGENT</title></head>
    <body style="background: red; color: white; text-align: center; padding: 50px;">
        <h1>🚨 ESPACE AGENT EN MAINTENANCE</h1>
        <p>L'espace agent est temporairement indisponible.</p>
        <p>Raison: Templates manquants</p>
        <p>Veuillez contacter l'administrateur.</p>
    </body>
    </html>
    ''', status=503)
"""
    
    emergency_path = Path("agents/views_emergency.py")
    emergency_path.parent.mkdir(exist_ok=True)
    emergency_path.write_text(emergency_view)
    print(f"   ✅ View d'urgence créée: {emergency_path}")

if __name__ == "__main__":
    intensive_agent_search()
    check_django_template_loaders()
    check_system_temp_files()
    check_process_and_cache()
    create_emergency_block()