# test_sync_only.py
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_current_state():
    """Tester l'état actuel du système"""
    print("🔍 ÉTAT ACTUEL DU SYSTÈME")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        # Membres
        cursor.execute("SELECT COUNT(*) FROM membres_membre")
        membres = cursor.fetchone()[0]
        
        # Cotisations
        cursor.execute("SELECT COUNT(*) FROM assureur_cotisation")
        cotisations = cursor.fetchone()[0]
        
        # Vérifications
        cursor.execute("SELECT COUNT(*) FROM agents_verificationcotisation")
        verifications = cursor.fetchone()[0]
        
        print(f"📊 STATISTIQUES:")
        print(f"   👥 Membres: {membres}")
        print(f"   💰 Cotisations: {cotisations}")
        print(f"   ✅ Vérifications: {verifications}")

def simulate_sync():
    """Simuler la synchronisation avec des données de test"""
    print("\n🎭 SIMULATION SYNCHRONISATION")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        # Mettre à jour toutes les vérifications avec un statut simulé
        cursor.execute("""
            UPDATE agents_verificationcotisation 
            SET statut_cotisation = 'ACTIVE',
                observations = 'Sync simulée: Données de test'
        """)
        
        print(f"✅ {cursor.rowcount} vérifications mises à jour avec statut simulé")

if __name__ == "__main__":
    test_current_state()
    simulate_sync()
    print("\n🎯 Synchronisation simulée terminée!")
    print("💡 Les agents voient maintenant des statuts de cotisation (simulés)")