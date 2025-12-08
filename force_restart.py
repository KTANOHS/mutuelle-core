#!/usr/bin/env python3
"""
Redémarrage forcé complet du système Django
"""

import os
import signal
import subprocess
from pathlib import Path

def force_restart_django():
    print("🔄 REDÉMARRAGE FORCÉ DJANGO")
    print("=" * 50)
    
    # 1. Tuer tous les processus Django
    print("1. 🔫 ARRÊT DES PROCESSUS DJANGO...")
    try:
        # Trouver les PIDs Django
        result = subprocess.run(
            "ps aux | grep -i 'manage.py runserver' | grep -v grep | awk '{print $2}'",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    os.kill(int(pid), signal.SIGKILL)
                    print(f"   ✅ Processus {pid} terminé")
        else:
            print("   ℹ️ Aucun processus Django trouvé")
            
    except Exception as e:
        print(f"   ❌ Erreur arrêt processus: {e}")
    
    # 2. Vider tous les caches
    print("\n2. 🗑️ VIDAGE DES CACHES...")
    cache_dirs = [
        "__pycache__",
        "*/__pycache__",
        "*.pyc",
        "*.pyo",
    ]
    
    for pattern in cache_dirs:
        for path in Path(".").rglob(pattern):
            try:
                if path.is_dir():
                    import shutil
                    shutil.rmtree(path)
                else:
                    path.unlink()
                print(f"   ✅ Supprimé: {path}")
            except Exception as e:
                print(f"   ❌ Erreur suppression {path}: {e}")
    
    # 3. Recréer la structure agents
    print("\n3. 🏗️ RECRÉATION STRUCTURE AGENTS...")
    agents_dirs = [
        "templates/agents",
        "templates/agents/partials", 
        "agents",
    ]
    
    for dir_path in agents_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Créé: {dir_path}")
    
    # 4. Créer un dashboard minimal de diagnostic
    print("\n4. 📄 CRÉATION DASHBOARD DIAGNOSTIC...")
    diagnostic_dashboard = """<!DOCTYPE html>
<html>
<head>
    <title>🚨 DIAGNOSTIC AGENT</title>
    <style>
        body { 
            background: linear-gradient(135deg, #ff6b6b, #4ecdc4);
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
        }
        .alert {
            background: rgba(255,255,255,0.2);
            padding: 20px;
            border-radius: 10px;
            margin: 20px auto;
            max-width: 600px;
        }
    </style>
</head>
<body>
    <h1>🔍 DIAGNOSTIC ESPACE AGENT</h1>
    
    <div class="alert">
        <h2>STATUT: TEMPLATES MANQUANTS</h2>
        <p>Le dossier templates/agents a été supprimé mais l'accès persiste.</p>
        <p>Ceci est un dashboard de diagnostic créé le {{ timestamp }}</p>
    </div>
    
    <div class="alert">
        <h3>INFORMATIONS SYSTÈME:</h3>
        <p><strong>URL actuelle:</strong> <span id="current-url"></span></p>
        <p><strong>User Agent:</strong> <span id="user-agent"></span></p>
        <p><strong>Timestamp:</strong> <span id="timestamp"></span></p>
    </div>
    
    <script>
        document.getElementById('current-url').textContent = window.location.href;
        document.getElementById('user-agent').textContent = navigator.userAgent;
        document.getElementById('timestamp').textContent = new Date().toISOString();
    </script>
</body>
</html>
"""
    
    dashboard_path = Path("templates/agents/dashboard.html")
    dashboard_path.write_text(diagnostic_dashboard)
    print(f"   ✅ Dashboard diagnostic créé: {dashboard_path}")
    
    # 5. Redémarrer le serveur
    print("\n5. 🚀 REDÉMARRAGE SERVEUR...")
    print("   Commande: python manage.py runserver --noreload")
    
    # Démarrer en arrière-plan
    subprocess.Popen([
        "python", "manage.py", "runserver", "--noreload"
    ])
    
    print("\n🎉 REDÉMARRAGE TERMINÉ!")
    print("📋 Testez: http://127.0.0.1:8000/agents/")

if __name__ == "__main__":
    force_restart_django()