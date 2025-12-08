# diagnostic_membres.py
import os
import sys
import django
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from django.db import connection
from django.contrib.auth.models import User
from django.apps import apps

print("🔍 DIAGNOSTIC APPROFONDI - SYSTÈME MEMBRES")
print("=" * 60)

def investiguer_modele_membre():
    """Investigue pourquoi le modèle Membre n'est pas accessible"""
    print("1. 🔎 Investigation du modèle Membre...")
    
    # Vérifier si le modèle existe dans les apps
    try:
        modele_membre = apps.get_model('membres', 'Membre')
        print("   ✅ Modèle Membre trouvé dans les apps Django")
        
        # Compter les membres
        try:
            count = modele_membre.objects.count()
            print(f"   👤 Membres dans la base: {count}")
            
            if count == 0:
                print("   ⚠️  AUCUN MEMBRE - Base vide ou problème de création")
                return False, count
            else:
                print("   ✅ Membres présents - Problème d'import résolu")
                return True, count
                
        except Exception as e:
            print(f"   ❌ Erreur comptage membres: {e}")
            return False, 0
            
    except LookupError:
        print("   ❌ Modèle Membre non trouvé dans les apps")
        return False, 0

def verifier_structure_tables():
    """Vérifie la structure des tables en base"""
    print("\n2. 🗃️  Structure des tables en base...")
    
    with connection.cursor() as cursor:
        # Lister toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"   📊 Tables trouvées: {len(tables)}")
        
        # Chercher les tables liées aux membres
        tables_membres = [t for t in tables if 'membre' in t.lower()]
        if tables_membres:
            print(f"   ✅ Tables membres: {', '.join(tables_membres)}")
            
            # Compter les enregistrements dans chaque table membre
            for table in tables_membres:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"      📈 {table}: {count} enregistrements")
                except Exception as e:
                    print(f"      ❌ Erreur lecture {table}: {e}")
        else:
            print("   ❌ Aucune table membre trouvée")

def verifier_relations_utilisateurs():
    """Vérifie les relations entre User et Membre"""
    print("\n3. 🔗 Relations Utilisateurs-Membres...")
    
    try:
        # Vérifier si des Users pourraient être des membres
        total_users = User.objects.count()
        print(f"   👥 Utilisateurs totaux: {total_users}")
        
        # Users sans staff/admin
        users_normaux = User.objects.filter(is_staff=False, is_superuser=False)
        print(f"   👤 Utilisateurs normaux (potentiels membres): {users_normaux.count()}")
        
        # Vérifier les profils étendus
        try:
            from membres.models import Membre
            membres_avec_user = Membre.objects.filter(user__isnull=False)
            print(f"   🔗 Membres avec user associé: {membres_avec_user.count()}")
        except:
            print("   ⚠️  Impossible de vérifier les associations")
            
    except Exception as e:
        print(f"   ❌ Erreur analyse relations: {e}")

def creer_membre_test():
    """Crée un membre de test si la base est vide"""
    print("\n4. 🧪 Test de création d'un membre...")
    
    try:
        from membres.models import Membre
        
        if Membre.objects.count() == 0:
            print("   🆕 Tentative de création d'un membre test...")
            
            # Créer un user test d'abord
            try:
                user_test = User.objects.create_user(
                    username='test_membre',
                    email='test@membre.com',
                    password='test123',
                    first_name='Test',
                    last_name='Membre'
                )
                
                # Créer le membre associé
                membre_test = Membre.objects.create(
                    user=user_test,
                    numero_membre='TEST001',
                    telephone='0102030405'
                )
                
                print("   ✅ Membre test créé avec succès!")
                print(f"   📝 User: {user_test.username}, Membre: {membre_test.numero_membre}")
                
                # Nettoyer le test
                membre_test.delete()
                user_test.delete()
                print("   🧹 Membre test nettoyé")
                
            except Exception as e:
                print(f"   ❌ Erreur création membre test: {e}")
        else:
            print("   ✅ Des membres existent déjà")
            
    except Exception as e:
        print(f"   ❌ Impossible de créer membre test: {e}")

# Exécution des investigations
print("🎯 LANCEMENT DES INVESTIGATIONS...")
print("=" * 60)

membre_ok, count_membres = investiguer_modele_membre()
verifier_structure_tables()
verifier_relations_utilisateurs()

if count_membres == 0:
    creer_membre_test()

print("\n" + "=" * 60)
print("📋 SYNTHÈSE DU DIAGNOSTIC MEMBRES")
print("=" * 60)

if membre_ok and count_membres > 0:
    print("🎉 SYSTÈME MEMBRES OPÉRATIONNEL")
    print(f"✅ {count_membres} membres trouvés dans la base")
else:
    print("🚨 PROBLÈME AVEC LE SYSTÈME MEMBRES")
    print("💡 Actions recommandées:")
    print("   1. Vérifier les migrations: python manage.py migrate")
    print("   2. Vérifier membres/models.py")
    print("   3. Créer des membres via l'interface admin")

print("=" * 60)