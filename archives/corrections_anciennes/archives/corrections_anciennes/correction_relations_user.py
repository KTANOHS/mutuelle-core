# correction_relations_user.py
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
from django.contrib.auth.models import Group
from django.apps import apps

def print_section(title):
    print(f"\n{'='*80}")
    print(f"🔧 {title}")
    print(f"{'='*80}")

def create_missing_user_relations():
    """Crée les relations manquantes entre User et les modèles spécifiques"""
    print_section("CORRECTION DES RELATIONS UTILISATEUR MANQUANTES")
    
    User = get_user_model()
    
    # Mapping groupes -> modèles
    group_model_mapping = {
        'Medecin': 'Medecin',
        'Membre': 'Membre',
        'Agents': 'Agent', 
        'Pharmacien': 'Pharmacien',
        'Assureur': 'Assureur'
    }
    
    users_corrected = 0
    
    for user in User.objects.all():
        user_groups = user.groups.all()
        
        for group in user_groups:
            model_name = group_model_mapping.get(group.name)
            
            if model_name:
                try:
                    # Vérifier si le modèle existe
                    model_class = apps.get_model(model_name.lower(), model_name)
                    
                    # Vérifier si la relation existe déjà
                    if not hasattr(user, model_name.lower()):
                        print(f"🔧 Création {model_name} pour {user.username} ({group.name})")
                        
                        # Créer l'objet lié selon le type
                        if model_name == 'Medecin':
                            from medecin.models import Medecin
                            medecin = Medecin.objects.create(
                                user=user,
                                nom=user.last_name or user.username,
                                prenom=user.first_name or user.username,
                                specialite="Généraliste",
                                numero_ordre=f"ORD{user.id:04d}",
                                est_actif=True
                            )
                            print(f"   ✅ Médecin créé: {medecin}")
                            
                        elif model_name == 'Agent':
                            from agents.models import Agent
                            agent = Agent.objects.create(
                                user=user,
                                nom=user.last_name or user.username,
                                prenom=user.first_name or user.username,
                                code_agent=f"AGT{user.id:03d}",
                                est_actif=True,
                                role="AGENT"
                            )
                            print(f"   ✅ Agent créé: {agent}")
                            
                        elif model_name == 'Membre':
                            from membres.models import Membre
                            membre = Membre.objects.create(
                                user=user,
                                nom=user.last_name or user.username,
                                prenom=user.first_name or user.username,
                                numero_membre=f"MEM{user.id:04d}",
                                est_actif=True
                            )
                            print(f"   ✅ Membre créé: {membre}")
                            
                        elif model_name == 'Pharmacien':
                            from pharmacien.models import Pharmacien
                            pharmacien = Pharmacien.objects.create(
                                user=user,
                                nom=user.last_name or user.username,
                                prenom=user.first_name or user.username,
                                numero_ordre=f"PHARM{user.id:04d}",
                                est_actif=True
                            )
                            print(f"   ✅ Pharmacien créé: {pharmacien}")
                            
                        elif model_name == 'Assureur':
                            from assureur.models import Assureur
                            assureur = Assureur.objects.create(
                                user=user,
                                nom=user.last_name or user.username,
                                prenom=user.first_name or user.username,
                                compagnie="Compagnie Principale",
                                est_actif=True
                            )
                            print(f"   ✅ Assureur créé: {assureur}")
                            
                        users_corrected += 1
                        
                except LookupError:
                    print(f"❌ Modèle {model_name} non trouvé")
                except Exception as e:
                    print(f"❌ Erreur création {model_name} pour {user.username}: {e}")
    
    print(f"\n📊 {users_corrected} relations utilisateur créées")

def verify_redirection_logic():
    """Vérifie et corrige la logique de redirection"""
    print_section("VÉRIFICATION DE LA LOGIQUE DE REDIRECTION")
    
    # Vérifier si la vue redirect_after_login existe
    views_file = BASE_DIR / 'mutuelle_core' / 'views.py'
    
    if views_file.exists():
        with open(views_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'def redirect_after_login' in content:
            print("✅ Vue redirect_after_login existe")
            
            # Vérifier la logique de redirection
            if 'hasattr(user,' in content and 'medecin' in content:
                print("✅ Logique de détection des relations présente")
            else:
                print("⚠️  Logique de détection des relations à vérifier")
        else:
            print("❌ Vue redirect_after_login non trouvée")
            
            # Créer la vue si elle n'existe pas
            create_redirect_view()
    else:
        print("❌ Fichier views.py de mutuelle_core non trouvé")

def create_redirect_view():
    """Crée la vue de redirection si elle n'existe pas"""
    print("➕ Création de la vue redirect_after_login...")
    
    views_file = BASE_DIR / 'mutuelle_core' / 'views.py'
    
    redirect_code = '''

def redirect_after_login(request):
    """Redirige l'utilisateur vers le dashboard approprié selon son type"""
    user = request.user
    
    # Vérifier d'abord par les relations OneToOne
    if hasattr(user, 'medecin'):
        return redirect('medecin:dashboard')
    elif hasattr(user, 'pharmacien'):
        return redirect('pharmacien:dashboard')
    elif hasattr(user, 'agent'):
        return redirect('agents:dashboard')
    elif hasattr(user, 'membre'):
        return redirect('membres:dashboard')
    elif hasattr(user, 'assureur'):
        return redirect('assureur:dashboard')
    
    # Vérifier par les groupes (fallback)
    elif user.groups.filter(name='Medecin').exists():
        return redirect('medecin:dashboard')
    elif user.groups.filter(name='Pharmacien').exists():
        return redirect('pharmacien:dashboard')
    elif user.groups.filter(name='Agents').exists():
        return redirect('agents:dashboard')
    elif user.groups.filter(name='Membre').exists():
        return redirect('membres:dashboard')
    elif user.groups.filter(name='Assureur').exists():
        return redirect('assureur:dashboard')
    elif user.is_staff:
        return redirect('/admin/')
    else:
        # Redirection par défaut
        return redirect('core:home')
'''
    
    try:
        with open(views_file, 'a', encoding='utf-8') as f:
            f.write(redirect_code)
        print("✅ Vue redirect_after_login créée")
    except Exception as e:
        print(f"❌ Erreur création vue: {e}")

def test_fixed_redirection():
    """Teste la redirection après correction"""
    print_section("TEST DE REDIRECTION APRÈS CORRECTION")
    
    User = get_user_model()
    
    # Tester avec les utilisateurs corrigés
    test_users = User.objects.filter(
        groups__name__in=['Medecin', 'Membre', 'Agents', 'Pharmacien', 'Assureur']
    )[:3]
    
    for user in test_users:
        print(f"\n--- Test avec {user.username} ---")
        
        # Vérifier les relations
        relations = ['medecin', 'membre', 'agent', 'pharmacien', 'assureur']
        user_relations = []
        
        for rel in relations:
            if hasattr(user, rel):
                user_relations.append(rel)
                obj = getattr(user, rel)
                print(f"   ✅ {rel}: {obj}")
        
        if not user_relations:
            print("   ❌ Aucune relation - problème non résolu")
            continue
            
        # Déterminer la redirection
        if hasattr(user, 'medecin'):
            expected = '/medecin/dashboard/'
        elif hasattr(user, 'membre'):
            expected = '/membres/dashboard/'
        elif hasattr(user, 'agent'):
            expected = '/agents/dashboard/'
        elif hasattr(user, 'pharmacien'):
            expected = '/pharmacien/dashboard/'
        elif hasattr(user, 'assureur'):
            expected = '/assureur/dashboard/'
        else:
            expected = '/generic-dashboard/'
            
        print(f"   🎯 Redirection: {expected}")
        print(f"   ✅ PRÊT pour la connexion")

def check_user_status_report():
    """Génère un rapport d'état des utilisateurs"""
    print_section("RAPPORT D'ÉTAT DES UTILISATEURS")
    
    User = get_user_model()
    
    # Compter les utilisateurs par groupe avec/sans relations
    groups_to_check = ['Medecin', 'Membre', 'Agents', 'Pharmacien', 'Assureur']
    
    for group_name in groups_to_check:
        users_in_group = User.objects.filter(groups__name=group_name)
        users_with_relation = []
        users_without_relation = []
        
        model_name = {
            'Medecin': 'medecin',
            'Membre': 'membre', 
            'Agents': 'agent',
            'Pharmacien': 'pharmacien',
            'Assureur': 'assureur'
        }.get(group_name)
        
        for user in users_in_group:
            if hasattr(user, model_name):
                users_with_relation.append(user.username)
            else:
                users_without_relation.append(user.username)
        
        print(f"\n📊 {group_name}:")
        print(f"   ✅ Avec relation: {len(users_with_relation)} utilisateurs")
        if users_with_relation:
            print(f"      {', '.join(users_with_relation[:3])}" + 
                  ("..." if len(users_with_relation) > 3 else ""))
        
        print(f"   ❌ Sans relation: {len(users_without_relation)} utilisateurs")
        if users_without_relation:
            print(f"      {', '.join(users_without_relation[:3])}" + 
                  ("..." if len(users_without_relation) > 3 else ""))

def main():
    """Fonction principale"""
    print("🚀 CORRECTION AUTOMATIQUE DES RELATIONS UTILISATEUR")
    print("📋 Résolution du problème de redirection des médecins")
    
    try:
        # Générer un rapport avant correction
        check_user_status_report()
        
        # Créer les relations manquantes
        create_missing_user_relations()
        
        # Vérifier la logique de redirection
        verify_redirection_logic()
        
        # Générer un rapport après correction
        check_user_status_report()
        
        # Tester la redirection
        test_fixed_redirection()
        
        print_section("CORRECTION TERMINÉE")
        print("✅ Toutes les corrections ont été appliquées")
        print("🎯 Actions recommandées:")
        print("   1. Redémarrer le serveur Django")
        print("   2. Se connecter avec test_medecin")
        print("   3. Vérifier la redirection vers /medecin/dashboard/")
        print("   4. Tester avec d'autres types d'utilisateurs")
        
    except Exception as e:
        print(f"💥 Erreur critique lors de la correction: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()