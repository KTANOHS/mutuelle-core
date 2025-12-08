# fix_missing_sync.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db import connection

def check_table_structures():
    """Vérifier la structure des tables problématiques"""
    print("🔍 STRUCTURE DES TABLES PROBLÉMATIQUES")
    print("=" * 50)
    
    tables = ['soins_soin', 'medecin_consultation', 'soins_bondesoin']
    
    for table in tables:
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                print(f"\n📋 {table}:")
                for col in columns:
                    print(f"   {col[1]} ({col[2]})")
        except Exception as e:
            print(f"❌ {table}: {e}")

def create_missing_relations():
    """Créer des relations manquantes pour la synchronisation"""
    print("\n🔗 CRÉATION DE RELATIONS TEST")
    print("=" * 50)
    
    # Créer quelques enregistrements de test dans les tables vides
    test_data = [
        ('soins_soin', 'Soin de test pour membre 1', 1),
        ('medecin_consultation', 'Consultation test', 2),
    ]
    
    for table, description, membre_id in test_data:
        try:
            with connection.cursor() as cursor:
                # Vérifier si la table a un champ membre_id
                cursor.execute(f"PRAGMA table_info({table})")
                colonnes = [col[1] for col in cursor.fetchall()]
                
                if 'membre_id' in colonnes:
                    cursor.execute(f"INSERT INTO {table} (description, membre_id) VALUES (?, ?)", 
                                 [description, membre_id])
                    print(f"✅ {table}: Relation créée avec membre_id {membre_id}")
                else:
                    print(f"⚠️  {table}: Pas de champ membre_id")
                    
        except Exception as e:
            print(f"❌ {table}: {e}")

if __name__ == "__main__":
    check_table_structures()
    create_missing_relations()