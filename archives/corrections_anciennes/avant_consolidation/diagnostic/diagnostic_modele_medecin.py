import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    from django.apps import apps
    from medecin.models import Medecin
    
    def diagnostic_modele_medecin():
        print("🔍 DIAGNOSTIC DU MODÈLE MÉDECIN")
        print("=" * 50)
        
        # 1. Obtenir le modèle Medecin
        model = apps.get_model('medecin', 'Medecin')
        
        # 2. Afficher tous les champs du modèle
        print("📋 CHAMPS DU MODÈLE MÉDECIN:")
        for field in model._meta.get_fields():
            print(f"   🎯 {field.name} ({field.__class__.__name__})")
            if hasattr(field, 'related_model') and field.related_model:
                print(f"      → Related to: {field.related_model}")
            if hasattr(field, 'max_length'):
                print(f"      → Max length: {field.max_length}")
        
        # 3. Vérifier s'il y a des médecins existants
        print(f"\n📊 MÉDECINS EXISTANTS: {Medecin.objects.count()}")
        for medecin in Medecin.objects.all()[:5]:  # Premiers 5 seulement
            print(f"   👤 {medecin}")
            # Afficher les attributs disponibles
            attrs = [attr for attr in dir(medecin) if not attr.startswith('_') and not callable(getattr(medecin, attr))]
            print(f"      Attributs: {', '.join(attrs[:10])}...")
        
        # 4. Vérifier la structure via la base de données
        print("\n🗄️ STRUCTURE TABLE MÉDECIN:")
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info(medecin_medecin);")
            columns = cursor.fetchall()
            for col in columns:
                print(f"   📝 {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULLABLE'}")
    
    diagnostic_modele_medecin()
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()