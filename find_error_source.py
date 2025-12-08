# find_error_source.py
import os
import sys
import django
import traceback
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

django.setup()

print("🔍 RECHERCHE DE LA SOURCE DE L'ERREUR 'Membre matching query does not exist'")
print("="*50)

from assureur.views import dashboard_assureur
from django.test import RequestFactory
from django.contrib.auth.models import User
from assureur.models import Assureur

# Créer une requête de test
factory = RequestFactory()

# Trouver un utilisateur assureur
try:
    # Essayer de trouver un assureur existant
    assureur = Assureur.objects.first()
    if assureur:
        user = assureur.user
        print(f"✅ Utilisateur trouvé: {user.username}")
        
        # Simuler une requête
        request = factory.get('/assureur/')
        request.user = user
        
        print("\n🎯 Test de la vue dashboard_assureur...")
        try:
            response = dashboard_assureur(request)
            print(f"✅ Vue exécutée avec succès, statut: {response.status_code}")
        except Exception as e:
            print(f"❌ Erreur lors de l'exécution: {e}")
            print("\n📋 Trace complète:")
            traceback.print_exc()
            
            # Analyser l'erreur plus en détail
            if "Membre matching query does not exist" in str(e):
                print("\n🔍 ERREUR SPÉCIFIQUE TROUVÉE: Membre non trouvé")
                print("   Cela se produit généralement quand:")
                print("   1. Un objet référence un membre_id qui n'existe plus")
                print("   2. Une requête .get() échoue")
                print("   3. Un select_related() sur un membre supprimé")
                
    else:
        print("❌ Aucun assureur trouvé dans la base")
        
except Exception as e:
    print(f"❌ Erreur générale: {e}")
    traceback.print_exc()

print("\n" + "="*50)
print("📊 VÉRIFICATION DES DONNÉES PROBLÉMATIQUES")
print("="*50)

from django.db import connection
from django.db.models import ForeignKey

# Vérifier toutes les relations ForeignKey vers Membre
print("\n1. Vérification des relations ForeignKey cassées...")

# Liste de tous les modèles avec ForeignKey vers Membre
from django.apps import apps

models_to_check = []
for model in apps.get_app_config('assureur').get_models():
    for field in model._meta.get_fields():
        if isinstance(field, ForeignKey) and field.related_model:
            if field.related_model.__name__ == 'Membre':
                models_to_check.append((model, field.name))

for model, field_name in models_to_check:
    print(f"\n   {model.__name__}.{field_name}:")
    
    # Compter les objets avec des valeurs non-null
    total = model.objects.exclude(**{f"{field_name}__isnull": True}).count()
    print(f"     Total avec {field_name} non-null: {total}")
    
    # Vérifier les IDs qui ne correspondent à aucun membre
    with connection.cursor() as cursor:
        table_name = model._meta.db_table
        column_name = field_name + "_id"
        
        # Vérifier si la colonne existe
        cursor.execute(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='{table_name}' AND column_name='{column_name}'
        """)
        
        if cursor.fetchone():
            # Trouver les IDs qui ne sont pas dans la table Membre
            cursor.execute(f"""
                SELECT DISTINCT a.{column_name}
                FROM {table_name} a
                LEFT JOIN assureur_membre b ON a.{column_name} = b.id
                WHERE a.{column_name} IS NOT NULL AND b.id IS NULL
            """)
            
            bad_ids = cursor.fetchall()
            if bad_ids:
                print(f"     ⚠️  {len(bad_ids)} IDs de membres manquants trouvés:")
                for bad_id in bad_ids[:5]:  # Limiter l'affichage
                    print(f"        - {bad_id[0]}")
                if len(bad_ids) > 5:
                    print(f"        ... et {len(bad_ids)-5} autres")
            else:
                print(f"     ✅ Tous les IDs de membres existent")

print("\n" + "="*50)
print("🎯 RECOMMANDATIONS")
print("="*50)

print("\nSi l'erreur persiste, essayez ces solutions:")

print("\n1. VÉRIFIER LES MIGRATIONS:")
print("   python manage.py makemigrations assureur")
print("   python manage.py migrate assureur")

print("\n2. RÉINITIALISER LES DONNÉES DE TEST:")
print("   python manage.py flush")
print("   (Attention: cela supprime toutes les données)")

print("\n3. CRÉER UN NOUVEL ASSUREUR ET MEMBRE:")
print("""
from django.contrib.auth.models import User
from assureur.models import Assureur, Membre

# Créer un nouvel utilisateur
user = User.objects.create_user('test2', 'test2@example.com', 'password123')

# Créer un assureur
assureur = Assureur.objects.create(user=user, nom='Test Assureur 2')

# Créer un membre
membre = Membre.objects.create(
    numero_membre='MEMTEST001',
    nom='Dupont',
    prenom='Jean',
    email='jean@example.com',
    telephone='0123456789',
    statut='actif'
)

print(f"Nouvel assureur: {assureur.id}")
print(f"Nouveau membre: {membre.id}")
""")

print("\n4. TESTER LA VUE AVEC LE NOUVEL UTILISATEUR")
print("   Connectez-vous avec le nouvel utilisateur 'test2'")