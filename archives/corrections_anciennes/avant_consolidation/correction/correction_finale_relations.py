# correction_finale_relations.py
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
from django.apps import apps
from django.utils import timezone

def print_section(title):
    print(f"\n{'='*80}")
    print(f"🔧 {title}")
    print(f"{'='*80}")

def debug_relation_problems():
    """Debug les problèmes de relations"""
    print_section("DEBUG DES PROBLÈMES DE RELATIONS")
    
    User = get_user_model()
    
    # Vérifier chaque utilisateur problématique
    problem_users = [
        ('test_medecin', 'medecin'),
        ('docteur_kouame', 'medecin'),
        ('test_membre', 'membre'),
        ('alia', 'assureur'),
        ('test_assureur', 'assureur')
    ]
    
    for username, relation_name in problem_users:
        try:
            user = User.objects.get(username=username)
            has_relation = hasattr(user, relation_name)
            
            print(f"\n🔍 {username} ({relation_name}):")
            print(f"   Relation existe: {has_relation}")
            
            if has_relation:
                obj = getattr(user, relation_name)
                print(f"   Objet: {obj}")
                print(f"   ID: {obj.id}")
            else:
                print(f"   ❌ Aucune relation {relation_name}")
                
                # Vérifier si l'objet existe mais n'est pas lié
                try:
                    model_class = apps.get_model(relation_name, relation_name.capitalize())
                    obj_exists = model_class.objects.filter(user=user).exists()
                    print(f"   Objet existe dans la table: {obj_exists}")
                    
                    if obj_exists:
                        obj = model_class.objects.get(user=user)
                        print(f"   ⚠️  Objet trouvé mais non accessible: {obj}")
                except Exception as e:
                    print(f"   Erreur vérification: {e}")
                    
        except User.DoesNotExist:
            print(f"❌ Utilisateur {username} non trouvé")
        except Exception as e:
            print(f"💥 Erreur debug {username}: {e}")

def fix_medecin_relations():
    """Corrige les relations Medecin problématiques"""
    print_section("CORRECTION DES RELATIONS MÉDECIN")
    
    User = get_user_model()
    
    try:
        from medecin.models import Medecin, SpecialiteMedicale, EtablissementMedical
        
        # Vérifier et créer les dépendances
        specialite_default, _ = SpecialiteMedicale.objects.get_or_create(
            nom="Médecine Générale",
            defaults={'description': "Spécialité par défaut"}
        )
        
        etablissement_default, _ = EtablissementMedical.objects.get_or_create(
            nom="Centre Médical Principal",
            defaults={
                'adresse': "Adresse par défaut",
                'telephone': "0102030405",
                'type_etablissement': "CENTRE"
            }
        )
        
        medecin_users = User.objects.filter(groups__name='Medecin')
        fixed_count = 0
        
        for user in medecin_users:
            # Vérifier si un objet Medecin existe déjà pour cet utilisateur
            existing_medecin = Medecin.objects.filter(user=user).first()
            
            if existing_medecin:
                print(f"✅ {user.username}: Medecin existe déjà - {existing_medecin}")
                # Forcer la relation
                user.medecin = existing_medecin
                fixed_count += 1
            else:
                print(f"🔧 Création Medecin pour {user.username}")
                try:
                    medecin = Medecin.objects.create(
                        user=user,
                        numero_ordre=f"ORD{user.id:04d}",
                        specialite=specialite_default,
                        etablissement=etablissement_default,
                        telephone_pro="0102030405",
                        email_pro=user.email or f"medecin{user.id}@example.com",
                        annees_experience=5,
                        tarif_consultation=5000.00,
                        actif=True,
                        disponible=True,
                        date_inscription=timezone.now(),
                        date_derniere_modif=timezone.now(),
                        horaires_travail={},
                        diplome_verifie=False
                    )
                    print(f"   ✅ Médecin créé: {medecin}")
                    fixed_count += 1
                except Exception as e:
                    print(f"   ❌ Erreur création: {e}")
        
        return fixed_count
        
    except Exception as e:
        print(f"❌ Erreur correction Medecin: {e}")
        return 0

def fix_membre_relations():
    """Corrige les relations Membre problématiques"""
    print_section("CORRECTION DES RELATIONS MEMBRE")
    
    User = get_user_model()
    
    try:
        from membres.models import Membre
        
        membre_users = User.objects.filter(groups__name='Membre')
        fixed_count = 0
        
        for user in membre_users:
            # Vérifier si un objet Membre existe déjà
            existing_membre = Membre.objects.filter(user=user).first()
            
            if existing_membre:
                print(f"✅ {user.username}: Membre existe déjà - {existing_membre}")
                user.membre = existing_membre
                fixed_count += 1
            else:
                print(f"🔧 Création Membre pour {user.username}")
                try:
                    membre = Membre.objects.create(
                        user=user,
                        numero_unique=f"MEM{user.id:04d}",
                        nom=user.last_name or user.username,
                        prenom=user.first_name or user.username,
                        telephone="0102030405",
                        numero_urgence="0102030406",
                        date_inscription=timezone.now(),
                        statut="AC",
                        categorie="ST",
                        cmu_option=False,
                        adresse="Adresse par défaut",
                        email=user.email or f"membre{user.id}@example.com",
                        profession="Non spécifié",
                        type_piece_identite="CNI",
                        statut_documents="EN_ATTENTE"
                    )
                    print(f"   ✅ Membre créé: {membre}")
                    fixed_count += 1
                except Exception as e:
                    print(f"   ❌ Erreur création: {e}")
        
        return fixed_count
        
    except Exception as e:
        print(f"❌ Erreur correction Membre: {e}")
        return 0

def fix_assureur_relations():
    """Corrige les relations Assureur problématiques"""
    print_section("CORRECTION DES RELATIONS ASSUREUR")
    
    User = get_user_model()
    
    try:
        from assureur.models import Assureur
        
        assureur_users = User.objects.filter(groups__name='Assureur')
        fixed_count = 0
        
        for user in assureur_users:
            # Vérifier si un objet Assureur existe déjà
            existing_assureur = Assureur.objects.filter(user=user).first()
            
            if existing_assureur:
                print(f"✅ {user.username}: Assureur existe déjà - {existing_assureur}")
                user.assureur = existing_assureur
                fixed_count += 1
            else:
                print(f"🔧 Création Assureur pour {user.username}")
                try:
                    assureur = Assureur.objects.create(
                        user=user,
                        numero_employe=f"ASS{user.id:03d}",
                        departement="Gestion des sinistres",
                        date_embauche=date.today(),
                        est_actif=True,
                        created_at=timezone.now(),
                        updated_at=timezone.now()
                    )
                    print(f"   ✅ Assureur créé: {assureur}")
                    fixed_count += 1
                except Exception as e:
                    print(f"   ❌ Erreur création: {e}")
        
        return fixed_count
        
    except Exception as e:
        print(f"❌ Erreur correction Assureur: {e}")
        return 0

def verify_final_relations():
    """Vérification finale après corrections"""
    print_section("VÉRIFICATION FINALE APRÈS CORRECTIONS")
    
    User = get_user_model()
    
    roles = [
        ('Medecin', 'medecin'),
        ('Membre', 'membre'),
        ('Agents', 'agent'),
        ('Pharmacien', 'pharmacien'),
        ('Assureur', 'assureur')
    ]
    
    all_good = True
    
    for group_name, relation in roles:
        users = User.objects.filter(groups__name=group_name)
        with_relation = sum(1 for user in users if hasattr(user, relation))
        
        status = "✅" if with_relation == len(users) else "❌"
        print(f"{status} {group_name}: {with_relation}/{len(users)} avec relation")
        
        if with_relation != len(users):
            all_good = False
            # Afficher les utilisateurs sans relation
            users_without = [user.username for user in users if not hasattr(user, relation)]
            print(f"   ❌ Sans relation: {', '.join(users_without)}")
    
    return all_good

def test_redirection_simulation():
    """Simule la redirection pour tous les utilisateurs"""
    print_section("SIMULATION DE REDIRECTION")
    
    User = get_user_model()
    
    print("🧪 Test de la logique de redirection:")
    
    # Tous les utilisateurs avec leurs groupes
    users = User.objects.filter(
        groups__name__in=['Medecin', 'Membre', 'Agents', 'Pharmacien', 'Assureur']
    )
    
    for user in users:
        groups = [g.name for g in user.groups.all()]
        print(f"\n🔍 {user.username} - Groupes: {', '.join(groups)}")
        
        # Vérifier les relations
        relations = {
            'medecin': '/medecin/dashboard/',
            'membre': '/membres/dashboard/',
            'agent': '/agents/dashboard/',
            'pharmacien': '/pharmacien/dashboard/',
            'assureur': '/assureur/dashboard/'
        }
        
        redirected = False
        for relation, url in relations.items():
            if hasattr(user, relation):
                print(f"   ✅ Relation {relation}: OUI")
                print(f"   🎯 Redirection: {url}")
                redirected = True
                break
        
        if not redirected:
            print(f"   ⚠️  Aucune relation spécifique")
            # Redirection par groupe
            if 'Medecin' in groups:
                print(f"   🎯 Redirection par groupe: /medecin/dashboard/")
            elif 'Membre' in groups:
                print(f"   🎯 Redirection par groupe: /membres/dashboard/")
            elif 'Agents' in groups:
                print(f"   🎯 Redirection par groupe: /agents/dashboard/")
            elif 'Pharmacien' in groups:
                print(f"   🎯 Redirection par groupe: /pharmacien/dashboard/")
            elif 'Assureur' in groups:
                print(f"   🎯 Redirection par groupe: /assureur/dashboard/")
            else:
                print(f"   🎯 Redirection par défaut: /generic-dashboard/")

def main():
    """Fonction principale"""
    print("🚀 CORRECTION FINALE DES RELATIONS")
    print("📋 Résolution des problèmes restants")
    
    try:
        # Étape 1: Debug des problèmes
        debug_relation_problems()
        
        # Étape 2: Corriger les relations problématiques
        fixed_count = 0
        fixed_count += fix_medecin_relations()
        fixed_count += fix_membre_relations()
        fixed_count += fix_assureur_relations()
        
        # Étape 3: Vérification finale
        all_good = verify_final_relations()
        
        # Étape 4: Simulation de redirection
        test_redirection_simulation()
        
        print_section("RÉSULTAT FINAL")
        print(f"✅ {fixed_count} problèmes corrigés")
        
        if all_good:
            print("🎉 TOUTES LES RELATIONS SONT MAINTENANT FONCTIONNELLES !")
            print("\n🎯 Vous pouvez maintenant:")
            print("   1. Redémarrer le serveur Django")
            print("   2. Tester la connexion avec test_medecin")
            print("   3. Vérifier la redirection vers /medecin/dashboard/")
        else:
            print("⚠️  Il reste des problèmes - consultez les logs ci-dessus")
            
    except Exception as e:
        print(f"💥 Erreur critique: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()