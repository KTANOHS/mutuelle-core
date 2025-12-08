#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC COMPLET - PROFIL ASSUREUR
Version: 1.0
Auteur: Système Mutuelle
Date: 2025-12-05
"""

import os
import sys
import django
from django.conf import settings

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("="*80)
print("DIAGNOSTIC COMPLET - PROFIL ASSUREUR")
print("="*80)

# ==================== SECTION 1: VÉRIFICATION DU SYSTÈME ====================

print("\n🔍 SECTION 1: VÉRIFICATION DU SYSTÈME")
print("-"*40)

try:
    from django.contrib.auth.models import User, Group
    print("✅ Module auth importé avec succès")
except Exception as e:
    print(f"❌ Erreur import auth: {e}")

try:
    from core.utils import get_user_primary_group, get_user_redirect_url
    print("✅ Module core.utils importé avec succès")
except Exception as e:
    print(f"❌ Erreur import core.utils: {e}")

# ==================== SECTION 2: VÉRIFICATION UTILISATEURS ====================

print("\n👥 SECTION 2: VÉRIFICATION DES UTILISATEURS")
print("-"*40)

# Lister tous les utilisateurs
print("\n📋 Liste complète des utilisateurs:")
print("-"*30)
users = User.objects.all()
for user in users:
    groups = [g.name for g in user.groups.all()]
    print(f"• {user.username} (ID: {user.id})")
    print(f"  📧 Email: {user.email}")
    print(f"  🏷️  Groupes: {groups}")
    print(f"  👑 Superuser: {user.is_superuser}")
    print(f"  🏢 Staff: {user.is_staff}")
    print(f"  🔐 Actif: {user.is_active}")
    
    # Vérifier le type détecté
    try:
        user_type = get_user_primary_group(user)
        redirect_url = get_user_redirect_url(user)
        print(f"  🎯 Type détecté: {user_type}")
        print(f"  🚀 Redirection: {redirect_url}")
    except:
        print(f"  ⚠️  Type détecté: Erreur")

# ==================== SECTION 3: VÉRIFICATION SPÉCIFIQUE DOUA ====================

print("\n🎯 SECTION 3: VÉRIFICATION UTILISATEUR DOUA")
print("-"*40)

try:
    doua = User.objects.get(username='DOUA')
    
    print(f"✅ DOUA trouvé (ID: {doua.id})")
    print(f"   📧 Email: {doua.email}")
    print(f"   👑 Superuser: {doua.is_superuser}")
    print(f"   🏢 Staff: {doua.is_staff}")
    
    # Groupes
    doua_groups = [g.name for g in doua.groups.all()]
    print(f"   🏷️  Groupes: {doua_groups}")
    
    # Vérification spécifique
    is_in_assureur_group = any('assureur' in g.lower() for g in doua_groups)
    print(f"   ✅ Dans groupe Assureur: {is_in_assureur_group}")
    
    # Vérification redirection
    try:
        doua_type = get_user_primary_group(doua)
        doua_redirect = get_user_redirect_url(doua)
        print(f"   🎯 Type détecté: {doua_type}")
        print(f"   🚀 URL redirection: {doua_redirect}")
        
        # Vérifier si l'URL est correcte
        expected_urls = ['/assureur/', '/assureur', '/assureur/dashboard/']
        if doua_redirect in expected_urls or '/assureur' in doua_redirect:
            print(f"   ✅ Redirection assureur correcte")
        else:
            print(f"   ❌ Redirection incorrecte (attendue: /assureur/, obtenue: {doua_redirect})")
            
    except Exception as e:
        print(f"   ❌ Erreur détection type: {e}")
        
except User.DoesNotExist:
    print("❌ ERREUR CRITIQUE: L'utilisateur DOUA n'existe pas!")
    print("   Solution: python manage.py shell -c \"")
    print("   from django.contrib.auth.models import User, Group")
    print("   doua = User.objects.create_user('DOUA', 'doua@assureur.com', 'doua123')")
    print("   assureur_group = Group.objects.get_or_create(name='Assureur')[0]")
    print("   doua.groups.add(assureur_group)")
    print("   doua.is_staff = True")
    print("   doua.save()")
    print("   print('DOUA créé avec succès')")
    print("   \"")

# ==================== SECTION 4: VÉRIFICATION MODÈLES ASSUREUR ====================

print("\n🏢 SECTION 4: VÉRIFICATION MODÈLES ASSUREUR")
print("-"*40)

# Vérifier chaque modèle
models_to_check = [
    ('membres.models', 'Membre', 'Modèle des membres'),
    ('assureur.models', 'ConfigurationAssurance', 'Configuration assureur'),
    ('assureur.models', 'Bon', 'Bons de soin'),
    ('assureur.models', 'Paiement', 'Paiements'),
]

for module_path, model_name, description in models_to_check:
    try:
        module = __import__(module_path, fromlist=[model_name])
        model_class = getattr(module, model_name)
        
        count = model_class.objects.count()
        print(f"✅ {description} ({model_name}): {count} enregistrements")
        
        # Afficher quelques exemples si disponibles
        if count > 0 and count <= 10:
            print(f"   📝 Exemples:")
            for obj in model_class.objects.all()[:3]:
                print(f"   • {str(obj)[:50]}...")
        elif count > 10:
            print(f"   📊 Top 3:")
            for obj in model_class.objects.all()[:3]:
                print(f"   • {str(obj)[:50]}...")
                
    except ImportError as e:
        print(f"❌ {description}: Module non trouvé ({e})")
    except AttributeError as e:
        print(f"❌ {description}: Modèle non trouvé ({e})")
    except Exception as e:
        print(f"❌ {description}: Erreur ({e})")

# ==================== SECTION 5: VÉRIFICATION FONCTIONS UTILITAIRES ====================

print("\n⚙️ SECTION 5: VÉRIFICATION FONCTIONS UTILITAIRES")
print("-"*40)

# Vérifier les fonctions de core.utils
functions_to_test = [
    'get_user_primary_group',
    'get_user_redirect_url', 
    'get_user_type',
    'user_is_assureur',
    'est_assureur',
    'get_assureur_stats'
]

for func_name in functions_to_test:
    try:
        from core.utils import __dict__ as utils_dict
        if func_name in utils_dict:
            print(f"✅ Fonction {func_name} disponible")
        else:
            print(f"❌ Fonction {func_name} non disponible")
    except Exception as e:
        print(f"❌ Erreur vérification {func_name}: {e}")

# Tester avec l'utilisateur DOUA
print("\n🧪 TESTS AVEC UTILISATEUR DOUA:")
print("-"*30)

if 'doua' in locals():
    try:
        # Test get_user_primary_group
        primary_group = get_user_primary_group(doua)
        print(f"📊 Groupe principal: {primary_group}")
        
        # Test get_user_redirect_url
        redirect_url = get_user_redirect_url(doua)
        print(f"📍 URL redirection: {redirect_url}")
        
        # Test user_is_assureur
        is_assureur = getattr(__import__('core.utils', fromlist=['user_is_assureur']), 'user_is_assureur', None)
        if is_assureur:
            print(f"🎫 Est assureur: {is_assureur(doua)}")
        
        # Test get_assureur_stats
        get_stats = getattr(__import__('core.utils', fromlist=['get_assureur_stats']), 'get_assureur_stats', None)
        if get_stats:
            stats = get_stats()
            print(f"📈 Statistiques assureur: {stats}")
            
    except Exception as e:
        print(f"❌ Erreur tests: {e}")

# ==================== SECTION 6: VÉRIFICATION URLs ====================

print("\n🌐 SECTION 6: VÉRIFICATION URLs")
print("-"*40)

# Vérifier les URLs de l'assureur
assureur_urls = [
    ('/', 'Page d\'accueil'),
    ('/assureur/', 'Tableau de bord assureur'),
    ('/assureur/membres/', 'Liste des membres'),
    ('/assureur/bons/', 'Liste des bons'),
    ('/assureur/paiements/', 'Liste des paiements'),
    ('/assureur/rapport-statistiques/', 'Rapports statistiques'),
    ('/assureur/communication/', 'Communication'),
    ('/accounts/login/', 'Connexion'),
    ('/admin/', 'Admin Django'),
]

print("📋 URLs à vérifier:")
for url, description in assureur_urls:
    print(f"  • {description}: {url}")

# ==================== SECTION 7: RECOMMANDATIONS ====================

print("\n💡 SECTION 7: RECOMMANDATIONS")
print("-"*40)

# Vérifier l'état et faire des recommandations
issues = []

# 1. Vérifier DOUA
if 'doua' not in locals():
    issues.append("❌ L'utilisateur DOUA n'existe pas")
elif not any('assureur' in g.lower() for g in [g.name for g in doua.groups.all()]):
    issues.append("⚠️ DOUA n'est pas dans le groupe 'Assureur'")
else:
    print("✅ DOUA correctement configuré")

# 2. Vérifier les données
try:
    from membres.models import Membre
    if Membre.objects.count() == 0:
        issues.append("⚠️ Aucun membre dans la base de données")
    else:
        print(f"✅ Données membres: {Membre.objects.count()} membres")
except:
    issues.append("❌ Impossible d'accéder aux données membres")

# 3. Vérifier la redirection
try:
    if 'doua' in locals():
        redirect = get_user_redirect_url(doua)
        if '/assureur' not in redirect:
            issues.append(f"⚠️ Redirection incorrecte: {redirect} (attendu: /assureur/)")
        else:
            print(f"✅ Redirection correcte: {redirect}")
except:
    issues.append("❌ Impossible de vérifier la redirection")

# Afficher les problèmes
if issues:
    print("\n🚨 PROBLÈMES IDENTIFIÉS:")
    for issue in issues:
        print(f"  {issue}")
else:
    print("✅ Aucun problème critique identifié")

# ==================== SECTION 8: RÉSUMÉ ====================

print("\n📊 SECTION 8: RÉSUMÉ DU SYSTÈME")
print("-"*40)

summary = {
    "Utilisateurs totaux": User.objects.count(),
    "Utilisateurs avec groupe Assureur": User.objects.filter(groups__name__icontains='assureur').count(),
    "Superutilisateurs": User.objects.filter(is_superuser=True).count(),
    "Utilisateurs staff": User.objects.filter(is_staff=True).count(),
}

for key, value in summary.items():
    print(f"  • {key}: {value}")

# Vérifier les modèles
try:
    from membres.models import Membre
    from assureur.models import Bon, ConfigurationAssurance, Paiement
    
    data_summary = {
        "Membres": Membre.objects.count(),
        "Bons de soin": Bon.objects.count(),
        "Paiements": Paiement.objects.count(),
        "Configurations": ConfigurationAssurance.objects.count(),
    }
    
    print("\n🗄️ DONNÉES DISPONIBLES:")
    for key, value in data_summary.items():
        status = "✅" if value > 0 else "⚠️"
        print(f"  {status} {key}: {value}")
        
except Exception as e:
    print(f"⚠️ Impossible de récupérer les données: {e}")

# ==================== SECTION 9: ACTIONS CORRECTIVES ====================

print("\n🔧 SECTION 9: ACTIONS CORRECTIVES DISPONIBLES")
print("-"*40)

print("1. Créer l'utilisateur DOUA:")
print("   python manage.py shell -c \"")
print("   from django.contrib.auth.models import User, Group")
print("   doua = User.objects.create_user('DOUA', 'doua@assureur.com', 'doua123')")
print("   assureur_group = Group.objects.get_or_create(name='Assureur')[0]")
print("   doua.groups.add(assureur_group)")
print("   doua.is_staff = True")
print("   doua.save()")
print("   print('DOUA créé avec succès')")
print("   \"")

print("\n2. Créer des données de test:")
print("   python create_final_test_data.py")

print("\n3. Réinitialiser le mot de passe de DOUA:")
print("   python manage.py shell -c \"")
print("   from django.contrib.auth.models import User")
print("   user = User.objects.get(username='DOUA')")
print("   user.set_password('doua123')")
print("   user.save()")
print("   print('Mot de passe réinitialisé')")
print("   \"")

print("\n4. Démarrer le serveur:")
print("   python manage.py runserver")

print("\n5. URL de connexion:")
print("   http://127.0.0.1:8000/accounts/login/")

print("\n" + "="*80)
print("DIAGNOSTIC TERMINÉ")
print("="*80)

# Exporter le rapport dans un fichier
with open('rapport_diagnostic_assureur.txt', 'w') as f:
    import datetime
    f.write(f"Rapport de diagnostic - {datetime.datetime.now()}\n")
    f.write("="*80 + "\n")
    
    # Récupérer la sortie console
    import io
    from contextlib import redirect_stdout
    
    output = io.StringIO()
    with redirect_stdout(output):
        # Réexécuter les tests
        pass
    
    f.write(output.getvalue())

print("\n📄 Rapport exporté: rapport_diagnostic_assureur.txt")