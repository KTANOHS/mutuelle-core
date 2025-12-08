# quick_sync.py
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def sync_now():
    """Synchroniser immédiatement les vérifications"""
    print("🔄 SYNCHRONISATION IMMÉDIATE")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        # Synchroniser la vérification pour le membre ID 1
        cursor.execute("""
            UPDATE agents_verificationcotisation 
            SET statut_cotisation = 'ACTIVE',
                observations = 'Sync: SQLITE-MANUAL-001'
            WHERE membre_id = 1
        """)
        print(f"✅ Vérification synchronisée pour membre_id 1")
        
        # Vérifier
        cursor.execute("""
            SELECT m.prenom, m.nom, c.reference, c.statut, v.statut_cotisation
            FROM membres_membre m
            JOIN assureur_cotisation c ON m.id = c.membre_id
            LEFT JOIN agents_verificationcotisation v ON m.id = v.membre_id
            WHERE m.id = 1
        """)
        result = cursor.fetchone()
        if result:
            prenom, nom, ref, statut_cot, statut_verif = result
            print(f"📋 RÉSULTAT SYNCHRO:")
            print(f"   👤 {prenom} {nom}")
            print(f"   💰 {ref} - {statut_cot}")
            print(f"   ✅ Vérification: {statut_verif}")

def check_all_verifications():
    """Vérifier toutes les vérifications"""
    print("\n🔍 ÉTAT DES VÉRIFICATIONS")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT m.prenom, m.nom, v.statut_cotisation, v.observations
            FROM agents_verificationcotisation v
            JOIN membres_membre m ON v.membre_id = m.id
            LIMIT 5
        """)
        print("📋 5 premières vérifications:")
        for prenom, nom, statut, obs in cursor.fetchall():
            print(f"   👤 {prenom} {nom}: {statut}")

if __name__ == "__main__":
    sync_now()
    check_all_verifications()
    print("\n🎉 PRÊT PLE TEST !")