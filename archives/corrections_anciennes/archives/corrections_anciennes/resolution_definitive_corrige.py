# resolution_definitive_corrige.py
import os
import sys
import django
from pathlib import Path
from datetime import date, datetime

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
from django.core.cache import cache
from django.apps import apps
from django.conf import settings

def print_section(title):
    print(f"\n{'='*80}")
    print(f"🔧 {title}")
    print(f"{'='*80}")

def reset_django_cache():
    """Réinitialise le cache Django et recharge les objets"""
    print_section("RÉINITIALISATION DU CACHE DJANGO")
    
    # Vider le cache
    cache.clear()
    print("✅ Cache Django vidé")
    
    # Recharger les applications
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

def fix_specific_problems():
    """Corrige les problèmes spécifiques identifiés"""
    print_section("CORRECTION DES PROBLÈMES SPÉCIFIQUES")
    
    User = get_user_model()
    
    # Les utilisateurs problématiques identifiés
    problem_cases = [
        ('test_medecin', 'Medecin'),
        ('docteur_kouame', 'Medecin'),
        ('test_membre', 'Membre'), 
        ('alia', 'Assureur'),
        ('test_assureur', 'Assureur')
    ]
    
    for username, expected_model in problem_cases:
        try:
            user = User.objects.get(username=username)
            print(f"\n🔧 Traitement de {username} (devrait avoir {expected_model})")
            
            # Vérifier l'état actuel
            relation_name = expected_model.lower()
            has_relation = hasattr(user, relation_name)
            
            if has_relation:
                obj = getattr(user, relation_name)
                print(f"   ✅ Relation existe: {obj}")
            else:
                print(f"   ❌ Relation manquante")
                
                # Vérifier dans la base de données
                try:
                    model_class = apps.get_model(relation_name, expected_model)
                    db_obj = model_class.objects.filter(user=user).first()
                    
                    if db_obj:
                        print(f"   ⚠️  Objet existe en base: {db_obj}")
                        print(f"   🔄 Tentative de réparation...")
                        
                        # Essayer de supprimer et recréer
                        db_obj.delete()
                        
                        # Recréer l'objet
                        if expected_model == 'Medecin':
                            from medecin.models import Medecin, SpecialiteMedicale, EtablissementMedical
                            specialite = SpecialiteMedicale.objects.first()
                            etablissement = EtablissementMedical.objects.first()
                            
                            new_obj = Medecin.objects.create(
                                user=user,
                                numero_ordre=f"ORD{user.id:04d}",
                                specialite=specialite,
                                etablissement=etablissement,
                                telephone_pro="0102030405",
                                email_pro=user.email or f"{username}@example.com",
                                annees_experience=5,
                                tarif_consultation=5000.00
                            )
                            
                        elif expected_model == 'Membre':
                            from membres.models import Membre
                            new_obj = Membre.objects.create(
                                user=user,
                                numero_unique=f"MEM{user.id:04d}",
                                nom=user.last_name or username,
                                prenom=user.first_name or username,
                                telephone="0102030405",
                                statut="AC",
                                categorie="ST"
                            )
                            
                        elif expected_model == 'Assureur':
                            from assureur.models import Assureur
                            new_obj = Assureur.objects.create(
                                user=user,
                                numero_employe=f"ASS{user.id:03d}",
                                departement="Gestion",
                                date_embauche=date.today()
                            )
                        
                        print(f"   ✅ Nouvel objet créé: {new_obj}")
                        
                        # Vérifier que ça marche maintenant
                        fresh_user = User.objects.get(pk=user.pk)
                        if hasattr(fresh_user, relation_name):
                            final_obj = getattr(fresh_user, relation_name)
                            print(f"   ✅ Relation maintenant accessible: {final_obj}")
                        else:
                            print(f"   ❌ Relation toujours inaccessible")
                            
                    else:
                        print(f"   ❌ Aucun objet trouvé en base")
                        
                except Exception as e:
                    print(f"   💥 Erreur réparation: {e}")
                    
        except User.DoesNotExist:
            print(f"❌ Utilisateur {username} non trouvé")

def test_redirection_logic():
    """Teste la logique de redirection qui sera utilisée"""
    print_section("TEST DE LA LOGIQUE DE REDIRECTION")
    
    User = get_user_model()
    
    # Simuler la logique de redirect_after_login
    def simulate_redirect(user):
        """Simule la logique de redirection"""
        # Vérifier d'abord par les relations OneToOne
        if hasattr(user, 'medecin'):
            return '/medecin/dashboard/'
        elif hasattr(user, 'pharmacien'):
            return '/pharmacien/dashboard/'
        elif hasattr(user, 'agent'):
            return '/agents/dashboard/'
        elif hasattr(user, 'membre'):
            return '/membres/dashboard/'
        elif hasattr(user, 'assureur'):
            return '/assureur/dashboard/'
        
        # Fallback par groupes
        elif user.groups.filter(name='Medecin').exists():
            return '/medecin/dashboard/'
        elif user.groups.filter(name='Pharmacien').exists():
            return '/pharmacien/dashboard/'
        elif user.groups.filter(name='Agents').exists():
            return '/agents/dashboard/'
        elif user.groups.filter(name='Membre').exists():
            return '/membres/dashboard/'
        elif user.groups.filter(name='Assureur').exists():
            return '/assureur/dashboard/'
        else:
            return '/generic-dashboard/'
    
    # Tester avec tous les utilisateurs
    users = User.objects.filter(
        groups__name__in=['Medecin', 'Membre', 'Agents', 'Pharmacien', 'Assureur']
    )
    
    print("🧪 Simulation des redirections:")
    
    for user in users:
        groups = [g.name for g in user.groups.all()]
        redirect_url = simulate_redirect(user)
        
        # Vérifier les relations
        relations_status = []
        for rel in ['medecin', 'membre', 'agent', 'pharmacien', 'assureur']:
            if hasattr(user, rel):
                relations_status.append(f"✅{rel}")
            else:
                relations_status.append(f"❌{rel}")
        
        print(f"\n🔍 {user.username} [{', '.join(groups)}]")
        print(f"   Relations: {', '.join(relations_status)}")
        print(f"   🎯 Redirection: {redirect_url}")

def final_verification():
    """Vérification finale"""
    print_section("VÉRIFICATION FINALE")
    
    User = get_user_model()
    
    # Compter les succès/échecs
    stats = {
        'Medecin': {'total': 0, 'with_relation': 0},
        'Membre': {'total': 0, 'with_relation': 0},
        'Agents': {'total': 0, 'with_relation': 0},
        'Pharmacien': {'total': 0, 'with_relation': 0},
        'Assureur': {'total': 0, 'with_relation': 0}
    }
    
    users = User.objects.filter(
        groups__name__in=['Medecin', 'Membre', 'Agents', 'Pharmacien', 'Assureur']
    )
    
    for user in users:
        for group in user.groups.all():
            group_name = group.name
            if group_name in stats:
                stats[group_name]['total'] += 1
                
                relation_name = group_name.lower() if group_name != 'Agents' else 'agent'
                if hasattr(user, relation_name):
                    stats[group_name]['with_relation'] += 1
    
    # Afficher les résultats
    all_good = True
    for group_name, data in stats.items():
        total = data['total']
        with_rel = data['with_relation']
        
        status = "✅" if with_rel == total else "❌"
        print(f"{status} {group_name}: {with_rel}/{total} avec relation")
        
        if with_rel != total:
            all_good = False
    
    return all_good

def main():
    """Fonction principale"""
    print("🚀 RÉSOLUTION DÉFINITIVE DES RELATIONS - VERSION CORRIGÉE")
    print("📋 Correction des relations OneToOne inaccessibles")
    
    try:
        # Étape 1: Vérifier la base de données
        check_database_relations()
        
        # Étape 2: Réinitialiser le cache
        reset_django_cache()
        
        # Étape 3: Forcer le rafraîchissement
        force_relation_refresh()
        
        # Étape 4: Corriger les problèmes spécifiques
        fix_specific_problems()
        
        # Étape 5: Tester la redirection
        test_redirection_logic()
        
        # Étape 6: Vérification finale
        all_good = final_verification()
        
        print_section("RÉSULTAT FINAL")
        if all_good:
            print("🎉 TOUTES LES RELATIONS SONT MAINTENANT FONCTIONNELLES !")
            print("\n🎯 Vous pouvez maintenant:")
            print("   1. Redémarrer le serveur Django")
            print("   2. Tester la connexion avec test_medecin")
            print("   3. Vérifier que la redirection fonctionne correctement")
        else:
            print("⚠️  Il reste des problèmes")
            print("💡 Essayez la solution radicale ou redémarrez le serveur")
            
    except Exception as e:
        print(f"💥 Erreur critique: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()