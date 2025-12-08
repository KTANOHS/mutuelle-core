# test_ordonnance_flow.py
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_real_ordonnance_flow():
    """Tester le flux réel ordonnance médecin → pharmacien"""
    print("🧪 TEST RÉEL FLUX ORDONNANCE")
    print("=" * 50)
    
    try:
        # 1. Créer une ordonnance médecin
        from medecin.models import Ordonnance as OrdonnanceMedecin
        from membres.models import Membre
        
        # Prendre un membre existant
        membre = Membre.objects.first()
        
        # Créer ordonnance médecin
        ordonnance_medecin = OrdonnanceMedecin.objects.create(
            membre=membre,
            date_prescription=timezone.now().date(),
            diagnostic="Test diagnostic",
            instructions="Prendre 3 fois par jour",
            duree_traitement=7,
            renouvelable=False
        )
        print(f"✅ Ordonnance médecin créée: ID {ordonnance_medecin.id}")
        
        # 2. Vérifier si elle est visible par pharmacien
        from pharmacien.models import Ordonnance as OrdonnancePharmacien
        
        try:
            # Vérifier si une version pharmacien existe
            ordonnance_pharmacien = OrdonnancePharmacien.objects.filter(
                ordonnance_medecin=ordonnance_medecin
            ).first()
            
            if ordonnance_pharmacien:
                print(f"✅ Ordonnance visible par pharmacien: ID {ordonnance_pharmacien.id}")
            else:
                print("❌ Ordonnance NON visible par pharmacien")
                print("💡 Le partage automatique ne fonctionne pas")
                
        except Exception as e:
            print(f"❌ Erreur vérification pharmacien: {e}")
            
    except Exception as e:
        print(f"❌ Erreur test flux: {e}")

def check_manual_sharing():
    """Vérifier le partage manuel si automatique échoue"""
    print("\n🔧 VÉRIFICATION PARTAGE MANUEL")
    print("=" * 50)
    
    from django.db import connection
    
    with connection.cursor() as cursor:
        # Vérifier s'il existe un mécanisme de partage manuel
        try:
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' 
                AND (name LIKE '%partage%' OR name LIKE '%share%')
            """)
            tables_partage = cursor.fetchall()
            
            if tables_partage:
                print("✅ Tables de partage détectées:")
                for table in tables_partage:
                    print(f"   📋 {table[0]}")
            else:
                print("❌ Aucun système de partage détecté")
                
        except Exception as e:
            print(f"❌ Erreur recherche partage: {e}")

if __name__ == "__main__":
    test_real_ordonnance_flow()
    check_manual_sharing()
    print("\n🎯 POUR TESTER EN CONDITIONS RÉELLES:")
    print("   1. 👨‍⚕️ Connectez-vous comme médecin")
    print("   2. 📝 Créez une ordonnance pour un membre")
    print("   3. 💊 Connectez-vous comme pharmacien") 
    print("   4. 🔍 Vérifiez si l'ordonnance est visible")