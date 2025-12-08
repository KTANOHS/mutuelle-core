# resolution_definitive.py
import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur setup Django: {e}")
    sys.exit(1)

from django.contrib.auth import get_user_model
from django.db import connection
from django.core.management import call_command

def print_section(title):
    print(f"\n{'='*80}")
    print(f"🔧 {title}")
    print(f"{'='*80}")

def reset_django_cache():
    """Réinitialise le cache Django et recharge les objets"""
    print_section("RÉINITIALISATION DU CACHE DJANGO")
    
    # Vider le cache
    from django.core.cache import cache
    cache.clear()
    print("✅ Cache Django vidé")
    
    # Recharger les applications
    from django.apps import apps
    apps.models_ready = False
    apps.ready = False
    apps.populate(settings.INSTALLED_APPS)
    print("✅ Applications rechargées")

def check_database_relations():
    """Vérifie les relations directement dans la base de données"""
    print_section("VÉRIFICATION DES RELATIONS EN BASE DE DONNÉES")
    
    User = get_user_model()
    
    # Vérifier chaque table de relation
    relations_to_check = [
        ('medecin_medecin', 'user_id', 'Medecin'),
        ('membres_membre', 'user_id', 'Membre'),
        ('agents_agent', 'user_id', 'Agent'),
        ('pharmacien_pharmacien', 'user_id', 'Pharmacien'),
        ('assureur_assureur', 'user_id', 'Assureur')
    ]
    
    with connection.cursor() as cursor:
        for table, user_field, model_name in relations_to_check:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"📊 {model_name}: {count} enregistrements dans la table")
                
                # Vérifier les utilisateurs avec relations
                cursor.execute(f"""
                    SELECT u.username, {table}.id 
                    FROM {table} 
                    JOIN auth_user u ON {table}.{user_field} = u.id
                """)
                users_with_relations = cursor.fetchall()
                
                if users_with_relations:
                    print(f"   👥 Utilisateurs avec relation:")
                    for username, obj_id in users_with_relations[:5]:
                        print(f"      ✅ {username} -> {model_name} #{obj_id}")
                else:
                    print(f"   ⚠️  Aucune relation trouvée")
                    
            except Exception as e:
                print(f"❌ Erreur vérification {table}: {e}")

def force_relation_refresh():
    """Force le rafraîchissement des relations"""
    print_section("FORCE LE RAFRAÎCHISSEMENT DES RELATIONS")
    
    User = get_user_model()
    
    # Recharger tous les utilisateurs depuis la base
    users = User.objects.filter(
        groups__name__in=['Medecin', 'Membre', 'Agents', 'Pharmacien', 'Assureur']
    )
    
    for user in users:
        print(f"\n🔍 Rechargement de {user.username}:")
        
        # Recharger l'utilisateur depuis la base
        fresh_user = User.objects.get(pk=user.pk)
        
        # Tester chaque relation
        relations = ['medecin', 'membre', 'agent', 'pharmacien', 'assureur']
        for relation in relations:
            try:
                # Vérifier si la relation existe en forçant une requête
                if hasattr(fresh_user, relation):
                    # Forcer l'accès à la relation
                    obj = getattr(fresh_user, relation)
                    print(f"   ✅ {relation}: {obj}")
                else:
                    print(f"   ❌ {relation}: Non accessible")
                    
            except Exception as e:
                print(f"   ⚠️  {relation}: Erreur - {e}")

def recreate_problematic_relations():
    """Recrée les relations problématiques"""
    print_section("RECRÉATION DES RELATIONS PROBLÉMATIQUES")
    
    User = get_user_model()
    
    # Utilisateurs problématiques identifiés
    problem_users = [
        ('test_medecin', 'medecin', 'Medecin'),
        ('docteur_kouame', 'medecin', 'Medecin'),
        ('test_membre', 'membre', 'Membre'),
        ('alia', 'assureur', 'Assureur'),
        ('test_assureur', 'assureur', 'Assureur')
    ]
    
    for username, relation_name, model_name in problem_users:
        try:
            user = User.objects.get(username=username)
            print(f"\n🔧 Traitement de {username} ({model_name})")
            
            # Supprimer l'objet existant problématique
            try:
                model_class = apps.get_model(relation_name, model_name)
                existing_obj = model_class.objects.filter(user=user).first()
                
                if existing_obj:
                    print(f"   🗑️  Suppression de l'objet problématique: {existing_obj}")
                    existing_obj.delete()
                    
                # Recréer l'objet
                print(f"   🔄 Recréation de l'objet...")
                
                if model_name == 'Medecin':
                    from medecin.models import Medecin, SpecialiteMedicale, EtablissementMedical
                    
                    specialite_default = SpecialiteMedicale.objects.first()
                    etablissement_default = EtablissementMedical.objects.first()
                    
                    new_obj = Medecin.objects.create(
                        user=user,
                        numero_ordre=f"ORD{user.id:04d}",
                        specialite=specialite_default,
                        etablissement=etablissement_default,
                        telephone_pro="0102030405",
                        email_pro=user.email or f"medecin{user.id}@example.com",
                        annees_experience=5,
                        tarif_consultation=5000.00
                    )
                    
                elif model_name == 'Membre':
                    from membres.models import Membre
                    
                    new_obj = Membre.objects.create(
                        user=user,
                        numero_unique=f"MEM{user.id:04d}",
                        nom=user.last_name or user.username,
                        prenom=user.first_name or user.username,
                        telephone="0102030405",
                        statut="AC",
                        categorie="ST"
                    )
                    
                elif model_name == 'Assureur':
                    from assureur.models import Assureur
                    
                    new_obj = Assureur.objects.create(
                        user=user,
                        numero_employe=f"ASS{user.id:03d}",
                        departement="Gestion",
                        date_embauche=date.today()
                    )
                
                print(f"   ✅ Nouvel objet créé: {new_obj}")
                
                # Vérifier que la relation est maintenant accessible
                fresh_user = User.objects.get(pk=user.pk)
                if hasattr(fresh_user, relation_name):
                    obj = getattr(fresh_user, relation_name)
                    print(f"   ✅ Relation maintenant accessible: {obj}")
                else:
                    print(f"   ❌ Relation toujours inaccessible")
                    
            except Exception as e:
                print(f"   ❌ Erreur recréation: {e}")
                
        except User.DoesNotExist:
            print(f"❌ Utilisateur {username} non trouvé")

def test_all_relations_final():
    """Test final de toutes les relations"""
    print_section("TEST FINAL DE TOUTES LES RELATIONS")
    
    User = get_user_model()
    
    users = User.objects.filter(
        groups__name__in=['Medecin', 'Membre', 'Agents', 'Pharmacien', 'Assureur']
    )
    
    success_count = 0
    total_count = 0
    
    for user in users:
        total_count += 1
        groups = [g.name for g in user.groups.all()]
        
        relations_ok = []
        relations_problem = []
        
        # Tester chaque relation possible
        for relation in ['medecin', 'membre', 'agent', 'pharmacien', 'assureur']:
            try:
                if hasattr(user, relation):
                    obj = getattr(user, relation)
                    relations_ok.append(relation)
                else:
                    relations_problem.append(relation)
            except:
                relations_problem.append(relation)
        
        if relations_ok:
            success_count += 1
            status = "✅"
        else:
            status = "❌"
        
        print(f"{status} {user.username} [{', '.join(groups)}]:")
        if relations_ok:
            print(f"   Relations OK: {', '.join(relations_ok)}")
        if relations_problem:
            print(f"   Relations KO: {', '.join(relations_problem)}")
    
    print(f"\n📊 RÉSULTAT: {success_count}/{total_count} utilisateurs avec relations fonctionnelles")
    return success_count == total_count

def main():
    """Fonction principale"""
    print("🚀 RÉSOLUTION DÉFINITIVE DES RELATIONS")
    print("📋 Correction des relations OneToOne inaccessibles")
    
    try:
        # Étape 1: Vérifier la base de données
        check_database_relations()
        
        # Étape 2: Réinitialiser le cache
        reset_django_cache()
        
        # Étape 3: Forcer le rafraîchissement
        force_relation_refresh()
        
        # Étape 4: Recréer les relations problématiques
        recreate_problematic_relations()
        
        # Étape 5: Test final
        all_good = test_all_relations_final()
        
        print_section("RÉSULTAT FINAL")
        if all_good:
            print("🎉 TOUTES LES RELATIONS SONT MAINTENANT FONCTIONNELLES !")
            print("\n🎯 Vous pouvez maintenant:")
            print("   1. Redémarrer le serveur Django")
            print("   2. Tester la connexion avec test_medecin")
            print("   3. Vérifier que la redirection fonctionne correctement")
        else:
            print("⚠️  Il reste des problèmes - une solution plus radicale est nécessaire")
            print("💡 Essayez de redémarrer complètement le serveur Django")
            
    except Exception as e:
        print(f"💥 Erreur critique: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()