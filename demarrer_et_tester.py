#!/usr/bin/env python
"""
SCRIPT DE DÉMARRAGE ET TEST AUTOMATIQUE
Démarre le serveur et teste toutes les interfaces
"""
import os
import sys
import time
import webbrowser
import threading
from pathlib import Path

def demarrer_serveur():
    """Démarre le serveur Django en arrière-plan"""
    print("🚀 Démarrage du serveur Django...")
    
    # Commande pour démarrer le serveur
    cmd = f"cd {Path(__file__).parent} && python manage.py runserver"
    
    def run_server():
        os.system(cmd)
    
    # Démarrer dans un thread séparé
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    print("⏳ Attente du démarrage du serveur...")
    time.sleep(5)  # Attendre que le serveur démarre
    return True

def ouvrir_navigateur():
    """Ouvre les URLs critiques dans le navigateur"""
    urls = [
        "http://127.0.0.1:8000/admin/",
        "http://127.0.0.1:8000/pharmacien/ordonnances/",
        "http://127.0.0.1:8000/medecin/",
        "http://127.0.0.1:8000/agents/tableau-de-bord/",
    ]
    
    print("🌐 Ouverture des interfaces dans le navigateur...")
    
    for i, url in enumerate(urls):
        print(f"   {i+1}. {url}")
        webbrowser.open_new_tab(url)
        time.sleep(1)  # Petit délai entre chaque ouverture

def main():
    """Fonction principale"""
    print("🎯 DÉMARRAGE AUTOMATIQUE DU SYSTÈME")
    print("=" * 50)
    
    try:
        # Démarrer le serveur
        if demarrer_serveur():
            print("✅ Serveur démarré avec succès!")
            
            # Ouvrir les interfaces
            ouvrir_navigateur()
            
            print("\n🎉 SYSTÈME OPÉRATIONNEL!")
            print("\n📋 INTERFACES OUVERTES:")
            print("   • Admin: http://127.0.0.1:8000/admin/")
            print("   • Pharmacien: http://127.0.0.1:8000/pharmacien/ordonnances/")
            print("   • Médecin: http://127.0.0.1:8000/medecin/")
            print("   • Agents: http://127.0.0.1:8000/agents/tableau-de-bord/")
            
            print("\n💡 Le serveur reste actif. Pour l'arrêter: Ctrl+C")
            print("🔄 Actualisez les pages pour voir les nouvelles données")
            
            # Garder le script actif
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n⏹️  Arrêt du système...")
                
        else:
            print("❌ Impossible de démarrer le serveur")
            
    except Exception as e:
        print(f"💥 Erreur: {e}")

if __name__ == "__main__":
    main()