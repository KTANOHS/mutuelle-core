import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

django.setup()

from django.apps import apps

def diagnostic_modeles():
    print("🔍 DIAGNOSTIC DES MODÈLES")
    print("=" * 50)
    
    # 1. Modèle Membre
    print("1. 📋 MODÈLE MEMBRE:")
    try:
        Membre = apps.get_model('membres', 'Membre')
        print("   ✅ Modèle Membre trouvé")
        print("   📝 Champs disponibles:")
        for field in Membre._meta.get_fields():
            print(f"      🎯 {field.name} ({field.__class__.__name__})")
    except LookupError:
        print("   ❌ Modèle Membre non trouvé")
    
    # 2. Modèle MaladieChronique
    print("\n2. 🩺 MODÈLE MALADIE CHRONIQUE:")
    try:
        MaladieChronique = apps.get_model('medecin', 'MaladieChronique')
        print("   ✅ Modèle MaladieChronique trouvé")
        print("   📝 Champs disponibles:")
        for field in MaladieChronique._meta.get_fields():
            print(f"      🎯 {field.name} ({field.__class__.__name__})")
    except LookupError:
        print("   ❌ Modèle MaladieChronique non trouvé")
    
    # 3. Vérifier la base de données
    print("\n3. 🗄️ ÉTAT DE LA BASE DE DONNÉES:")
    from django.db import connection
    
    with connection.cursor() as cursor:
        # Tables membres
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%membre%';")
        tables_membres = cursor.fetchall()
        print(f"   📊 Tables membres: {[t[0] for t in tables_membres]}")
        
        # Tables medecin
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%maladie%';")
        tables_maladies = cursor.fetchall()
        print(f"   📊 Tables maladies: {[t[0] for t in tables_maladies]}")
    
    # 4. Compter les enregistrements existants
    print("\n4. 📊 DONNÉES EXISTANTES:")
    try:
        Membre = apps.get_model('membres', 'Membre')
        count_membres = Membre.objects.count()
        print(f"   👥 Membres: {count_membres}")
    except:
        print("   👥 Membres: Modèle non accessible")
    
    try:
        MaladieChronique = apps.get_model('medecin', 'MaladieChronique')
        count_maladies = MaladieChronique.objects.count()
        print(f"   🩺 Maladies chroniques: {count_maladies}")
    except:
        print("   🩺 Maladies chroniques: Modèle non accessible")

diagnostic_modeles()