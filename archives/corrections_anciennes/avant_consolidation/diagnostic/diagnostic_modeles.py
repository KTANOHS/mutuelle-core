import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    print("🔍 DIAGNOSTIC DES MODÈLES:")
    print("=" * 40)
    
    # Lister tous les modèles disponibles dans membres
    from django.apps import apps
    from membres import models as membres_models
    
    print("📦 Modèles dans membres.models:")
    for name in dir(membres_models):
        obj = getattr(membres_models, name)
        if hasattr(obj, '_meta') and hasattr(obj._meta, 'app_label'):
            if obj._meta.app_label == 'membres':
                print(f"   ✅ {name}")
    
    print("\n📋 Tous les modèles de l'application 'membres':")
    app_models = apps.get_app_config('membres').get_models()
    for model in app_models:
        print(f"   📝 {model.__name__}")
        
    # Vérifier les tables en base de données
    print("\n🗄️ Tables en base de données:")
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            if 'membres' in table[0] or 'medecin' in table[0]:
                print(f"   📊 {table[0]}")
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()