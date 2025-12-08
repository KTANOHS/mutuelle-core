# redemarrage_intelligent.py
import os
import subprocess
import time

def redemarrage_serveur():
    """
    Redémarre intelligemment le serveur Django
    """
    print("REDÉMARRAGE INTELLIGENT DU SERVEUR")
    print("=" * 50)
    
    # 1. Trouver le processus Django
    print("🔍 Recherche des processus Django...")
    try:
        result = subprocess.run(['pgrep', '-f', 'runserver'], capture_output=True, text=True)
        if result.stdout:
            pids = result.stdout.strip().split('\n')
            print(f"✓ Processus Django trouvés: {', '.join(pids)}")
            
            # Tuer les processus
            for pid in pids:
                subprocess.run(['kill', pid])
                print(f"✓ Processus {pid} arrêté")
            
            time.sleep(2)  # Attendre que les processus soient bien arrêtés
        else:
            print("✓ Aucun processus Django en cours")
    except Exception as e:
        print(f"⚠ Erreur recherche processus: {e}")
    
    # 2. Redémarrer le serveur en arrière-plan
    print("\n🔄 Redémarrage du serveur...")
    try:
        # Démarrer en arrière-plan
        process = subprocess.Popen([
            'python', 'manage.py', 'runserver'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✓ Serveur redémarré en arrière-plan")
        print(f"✓ PID du nouveau processus: {process.pid}")
        
        # Attendre un peu que le serveur soit prêt
        time.sleep(3)
        
    except Exception as e:
        print(f"❌ Erreur redémarrage: {e}")
        print("\n💡 Redémarrage manuel requis:")
        print("   python manage.py runserver")

def test_final_complet():
    """
    Test complet après redémarrage
    """
    print("\n" + "="*50)
    print("TEST FINAL COMPLET")
    print("="*50)
    
    # Attendre un peu plus pour être sûr que le serveur est prêt
    time.sleep(2)
    
    try:
        # Lancer le test
        result = subprocess.run(['python', 'test_final_optimise.py'], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Erreurs:", result.stderr)
    except Exception as e:
        print(f"❌ Impossible d'exécuter le test: {e}")

if __name__ == "__main__":
    redemarrage_serveur()
    test_final_complet()