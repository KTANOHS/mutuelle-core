# diagnostic.py
import os
import sys
import django
from django.urls import reverse, NoReverseMatch
from django.apps import apps
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from membres.models import Membre
from assureur.models import Assureur
from agents.models import Agent
from medecin.models import Medecin

def diagnostic_complet():
    print("=" * 60)
    print("🔍 DIAGNOSTIC COMPLET DU SYSTÈME")
    print("=" * 60)
    
    # 1. Vérification des modèles
    verifier_modeles()
    
    # 2. Vérification des URLs
    verifier_urls()
    
    # 3. Vérification des utilisateurs et permissions
    verifier_utilisateurs()
    
    # 4. Vérification des données
    verifier_donnees()
    
    # 5. Vérification des fonctions utilitaires
    verifier_fonctions_utilitaires()
    
    # 6. Vérification des timezones
    verifier_timezones()

def verifier_modeles():
    print("\n📊 1. VÉRIFICATION DES MODÈLES")
    print("-" * 40)
    
    modeles_essentiels = [
        'membres.Membre',
        'assureur.Assureur', 
        'agents.Agent',
        'medecin.Medecin',
        'assureur.Bon',
        'assureur.Paiement'
    ]
    
    for modele in modeles_essentiels:
        try:
            model = apps.get_model(modele)
            count = model.objects.count()
            print(f"✅ {modele}: {count} enregistrement(s)")
        except LookupError:
            print(f"❌ {modele}: Modèle non trouvé")

def verifier_urls():
    print("\n🌐 2. VÉRIFICATION DES URLs")
    print("-" * 40)
    
    urls_a_verifier = [
        'accueil',
        'connexion',
        'assureur:dashboard',
        'assureur:liste_membres', 
        'assureur:creer_bon',
        'agents:tableau_de_bord',
        'medecin:dashboard',
    ]
    
    for url_name in urls_a_verifier:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name} -> {url}")
        except NoReverseMatch as e:
            print(f"❌ {url_name}: {e}")

def verifier_utilisateurs():
    print("\n👥 3. VÉRIFICATION DES UTILISATEURS")
    print("-" * 40)
    
    User = get_user_model()
    
    # Comptage des utilisateurs
    total_users = User.objects.count()
    print(f"👤 Utilisateurs totaux: {total_users}")
    
    # Vérification des types d'utilisateurs
    try:
        assureurs = Assureur.objects.count()
        agents = Agent.objects.count()
        medecins = Medecin.objects.count()
        
        print(f"🏢 Assureurs: {assureurs}")
        print(f"👨‍💼 Agents: {agents}") 
        print(f"👨‍⚕️ Médecins: {medecins}")
        
        # Test avec un utilisateur spécifique
        test_user = User.objects.filter(username='assureur_test').first()
        if test_user:
            print(f"\n🔍 Test utilisateur 'assureur_test':")
            print(f"   - ID: {test_user.id}")
            print(f"   - Email: {test_user.email}")
            print(f"   - Superuser: {test_user.is_superuser}")
            print(f"   - Staff: {test_user.is_staff}")
            
            # Test des fonctions de permission
            from core.utils import est_assureur, est_agent, est_medecin
            print(f"   - Est assureur: {est_assureur(test_user)}")
            print(f"   - Est agent: {est_agent(test_user)}")
            print(f"   - Est médecin: {est_medecin(test_user)}")
        else:
            print("❌ Utilisateur 'assureur_test' non trouvé")
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des utilisateurs: {e}")

def verifier_donnees():
    print("\n📁 4. VÉRIFICATION DES DONNÉES")
    print("-" * 40)
    
    # Vérification des membres
    try:
        membres = Membre.objects.all()
        print(f"👥 Membres: {membres.count()}")
        
        if membres.exists():
            print("📋 Liste des membres:")
            for membre in membres[:5]:  # Affiche les 5 premiers
                print(f"   - ID: {membre.id}, Nom: {membre.nom}, Assureur: {membre.assureur}")
        else:
            print("⚠️  Aucun membre trouvé dans la base")
            
    except Exception as e:
        print(f"❌ Erreur avec le modèle Membre: {e}")

def verifier_fonctions_utilitaires():
    print("\n⚙️ 5. VÉRIFICATION DES FONCTIONS UTILITAIRES")
    print("-" * 40)
    
    try:
        from core.utils import (
            est_assureur, est_agent, est_medecin, 
            gerer_erreurs, get_user_redirect_url
        )
        
        print("✅ Fonctions utilitaires importées avec succès")
        
        # Test des fonctions avec un utilisateur de test
        User = get_user_model()
        test_user = User.objects.filter(username='assureur_test').first()
        
        if test_user:
            print(f"🧪 Tests avec l'utilisateur '{test_user.username}':")
            print(f"   - est_assureur: {est_assureur(test_user)}")
            print(f"   - est_agent: {est_agent(test_user)}")
            print(f"   - est_medecin: {est_medecin(test_user)}")
            
            # Test de redirection
            redirect_url = get_user_redirect_url(test_user)
            print(f"   - URL de redirection: {redirect_url}")
        else:
            print("⚠️  Utilisateur de test non disponible pour les tests")
            
    except ImportError as e:
        print(f"❌ Erreur d'import des fonctions utilitaires: {e}")
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")

def verifier_timezones():
    print("\n⏰ 6. VÉRIFICATION DES TIMEZONES")
    print("-" * 40)
    
    from django.conf import settings
    from django.utils import timezone
    
    print(f"🕒 TIME_ZONE: {settings.TIME_ZONE}")
    print(f"🔧 USE_TZ: {settings.USE_TZ}")
    print(f"⏰ Timezone actuelle: {timezone.now()}")

def verification_avancee():
    print("\n" + "=" * 60)
    print("🔧 VÉRIFICATIONS AVANCÉES")
    print("=" * 60)
    
    # Vérification des tables de base de données
    print("\n🗄️  VÉRIFICATION DE LA BASE DE DONNÉES")
    print("-" * 40)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📋 Tables trouvées: {len(tables)}")
        
        tables_essentielles = [
            'membres_membre', 'assureur_assureur', 'agents_agent',
            'medecin_medecin', 'auth_user', 'assureur_bon'
        ]
        
        for table in tables_essentielles:
            if table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"✅ {table}: {count} enregistrement(s)")
            else:
                print(f"❌ {table}: Table manquante")

def generer_recommandations():
    print("\n" + "=" * 60)
    print("💡 RECOMMANDATIONS")
    print("=" * 60)
    
    recommendations = [
        "🔧 Vérifiez que tous les namespaces sont corrects dans urls.py",
        "👥 Créez des données de test si aucun membre n'existe",
        "✅ Testez les redirections après connexion", 
        "⏰ Utilisez timezone.now() pour les dates",
        "🐛 Activez le mode debug pour plus de détails sur les erreurs",
        "📚 Consultez les logs pour les erreurs spécifiques"
    ]
    
    for rec in recommendations:
        print(f"• {rec}")

if __name__ == "__main__":
    diagnostic_complet()
    verification_avancee() 
    generer_recommandations()
    
    print("\n🎯 DIAGNOSTIC TERMINÉ - Vérifiez les résultats ci-dessus")