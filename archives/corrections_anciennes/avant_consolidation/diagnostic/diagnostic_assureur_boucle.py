import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from assureur.models import Assureur
from django.urls import reverse, resolve, Resolver404
from django.utils import timezone
import logging

# Configuration logging
logging.basicConfig(level=logging.INFO, format='🔍 %(message)s')
logger = logging.getLogger(__name__)

def diagnostic_complet_assureur():
    print("🔍 DIAGNOSTIC COMPLET ERREUR BOUCLE ASSUREUR")
    print("=" * 60)
    
    # 1. Vérifier l'utilisateur DOUA
    print("\n1. 👤 DIAGNOSTIC UTILISATEUR DOUA")
    print("-" * 40)
    
    try:
        user_doua = User.objects.get(username='DOUA')
        print(f"✅ Utilisateur DOUA trouvé: ID {user_doua.id}")
        print(f"   📧 Email: {user_doua.email}")
        print(f"   👥 Groupes: {[g.name for g in user_doua.groups.all()]}")
        print(f"   🔐 Est actif: {user_doua.is_active}")
        print(f"   🏢 Est staff: {user_doua.is_staff}")
        print(f"   👑 Est superuser: {user_doua.is_superuser}")
    except User.DoesNotExist:
        print("❌ ERREUR CRITIQUE: Utilisateur DOUA non trouvé!")
        return False
    except Exception as e:
        print(f"❌ Erreur recherche DOUA: {e}")
        return False
    
    # 2. Vérifier le profil Assureur
    print("\n2. 🏥 DIAGNOSTIC PROFIL ASSUREUR")
    print("-" * 40)
    
    try:
        assureur = Assureur.objects.filter(user=user_doua).first()
        if assureur:
            print(f"✅ Profil Assureur trouvé: {assureur.numero_employe}")
            print(f"   📋 Département: {assureur.departement}")
            print(f"   📅 Date embauche: {assureur.date_embauche}")
            print(f"   📞 Téléphone: {getattr(assureur, 'telephone', 'Non défini')}")
            print(f"   🟢 Statut: {getattr(assureur, 'statut', 'Non défini')}")
        else:
            print("❌ PROFIL ASSUREUR NON TROUVÉ pour DOUA!")
            print("💡 Création automatique du profil...")
            
            assureur = Assureur.objects.create(
                user=user_doua,
                numero_employe=f"EMP{user_doua.id:04d}",
                departement="gestion",
                date_embauche=timezone.now().date(),
                telephone="+2250100000000",
                email=user_doua.email,
                statut="actif"
            )
            print(f"✅ Profil Assureur créé: {assureur.numero_employe}")
    except Exception as e:
        print(f"❌ Erreur profil Assureur: {e}")
        return False
    
    # 3. Vérifier les groupes et permissions
    print("\n3. 🔐 DIAGNOSTIC GROUPES ET PERMISSIONS")
    print("-" * 40)
    
    try:
        groupe_assureur = Group.objects.filter(name='Assureur').first()
        if groupe_assureur:
            print(f"✅ Groupe 'Assureur' trouvé: {groupe_assureur.id}")
            
            # Vérifier si DOUA est dans le groupe
            if user_doua.groups.filter(name='Assureur').exists():
                print("✅ DOUA est bien dans le groupe Assureur")
            else:
                print("⚠️ DOUA n'est PAS dans le groupe Assureur")
                print("💡 Ajout au groupe...")
                user_doua.groups.add(groupe_assureur)
                print("✅ DOUA ajouté au groupe Assureur")
        else:
            print("❌ Groupe 'Assureur' non trouvé!")
            print("💡 Création du groupe...")
            groupe_assureur = Group.objects.create(name='Assureur')
            user_doua.groups.add(groupe_assureur)
            print("✅ Groupe Assureur créé et DOUA ajouté")
    except Exception as e:
        print(f"❌ Erreur groupes: {e}")
    
    # 4. Vérifier les URLs et vues
    print("\n4. 🌐 DIAGNOSTIC URLs ET VUES")
    print("-" * 40)
    
    urls_a_verifier = [
        'assureur:dashboard',
        'assureur:acces_interdit', 
        'assureur:liste_membres',
        'assureur:liste_bons',
    ]
    
    for url_name in urls_a_verifier:
        try:
            url = reverse(url_name)
            print(f"✅ URL {url_name}: {url}")
        except Exception as e:
            print(f"❌ URL {url_name}: {e}")
    
    # 5. Vérifier la fonction get_assureur_connecte
    print("\n5. 🔧 DIAGNOSTIC FONCTION get_assureur_connecte")
    print("-" * 40)
    
    try:
        from assureur.views import get_assureur_connecte
        
        # Simuler une requête
        class MockRequest:
            def __init__(self, user):
                self.user = user
        
        mock_request = MockRequest(user_doua)
        assureur_connecte = get_assureur_connecte(mock_request)
        
        if assureur_connecte:
            print(f"✅ get_assureur_connecte() retourne: {assureur_connecte}")
            print(f"   📋 Numéro employé: {assureur_connecte.numero_employe}")
        else:
            print("❌ get_assureur_connecte() retourne None")
            print("💡 Problème dans la fonction de détection")
            
    except Exception as e:
        print(f"❌ Erreur get_assureur_connecte: {e}")
    
    # 6. Vérifier le décorateur est_assureur
    print("\n6. 🛡️ DIAGNOSTIC DÉCORATEUR est_assureur")
    print("-" * 40)
    
    try:
        from assureur.views import est_assureur
        
        # Tester le décorateur
        def vue_test(request):
            return "Vue test"
        
        vue_decoree = est_assureur(vue_test)
        print("✅ Décorateur est_assureur chargé avec succès")
        
    except Exception as e:
        print(f"❌ Erreur décorateur est_assureur: {e}")
    
    # 7. Vérifier les templates
    print("\n7. 📄 DIAGNOSTIC TEMPLATES")
    print("-" * 40)
    
    templates_a_verifier = [
        'assureur/dashboard.html',
        'assureur/acces_interdit.html',
        'assureur/base_assureur.html',
    ]
    
    from django.template.loader import get_template
    from django.template import TemplateDoesNotExist
    
    for template in templates_a_verifier:
        try:
            get_template(template)
            print(f"✅ Template {template}: TROUVÉ")
        except TemplateDoesNotExist:
            print(f"❌ Template {template}: NON TROUVÉ")
        except Exception as e:
            print(f"⚠️ Template {template}: {e}")
    
    # 8. Test de connexion simulé
    print("\n8. 🧪 TEST DE CONNEXION SIMULÉ")
    print("-" * 40)
    
    try:
        from django.test import RequestFactory
        from assureur.views import dashboard_assureur
        
        factory = RequestFactory()
        request = factory.get('/assureur/dashboard/')
        request.user = user_doua
        
        print("✅ Simulation de requête créée")
        
        # Essayer d'appeler la vue
        try:
            response = dashboard_assureur(request)
            print(f"✅ Vue dashboard_assureur: Status {response.status_code}")
        except Exception as e:
            print(f"❌ Erreur vue dashboard_assureur: {e}")
            
    except Exception as e:
        print(f"❌ Erreur test simulation: {e}")
    
    # 9. Résumé et recommandations
    print("\n9. 📋 RÉSUMÉ ET RECOMMANDATIONS")
    print("-" * 40)
    
    print("🎯 CAUSES POSSIBLES DE LA BOUCLE:")
    print("   1. ❌ Profil Assureur manquant pour DOUA")
    print("   2. ❌ DOUA pas dans le groupe Assureur") 
    print("   3. ❌ Fonction get_assureur_connecte défaillante")
    print("   4. ❌ Décorateur est_assureur trop restrictif")
    print("   5. ❌ Template dashboard manquant")
    print("   6. ❌ Redirection circulaire dans les vues")
    
    print("\n🚀 SOLUTIONS:")
    print("   1. ✅ Vérifier que le profil Assureur existe")
    print("   2. ✅ Vérifier l'appartenance au groupe")
    print("   3. ✅ Tester get_assureur_connecte avec DOUA")
    print("   4. ✅ Vérifier les templates dans assureur/")
    print("   5. ✅ Examiner les logs Django pour la boucle exacte")
    
    return True

def verifier_boucle_redirection():
    """Vérifie spécifiquement la boucle de redirection"""
    print("\n🔄 DIAGNOSTIC SPÉCIFIQUE BOUCLE REDIRECTION")
    print("-" * 50)
    
    try:
        from assureur.views import dashboard_assureur, acces_interdit
        
        print("✅ Vues chargées:")
        print(f"   - dashboard_assureur: {dashboard_assureur}")
        print(f"   - acces_interdit: {acces_interdit}")
        
        # Vérifier les URLs de redirection
        try:
            url_dashboard = reverse('assureur:dashboard')
            url_acces_interdit = reverse('assureur:acces_interdit')
            print(f"✅ URLs de redirection:")
            print(f"   - Dashboard: {url_dashboard}")
            print(f"   - Accès interdit: {url_acces_interdit}")
        except Exception as e:
            print(f"❌ Erreur URLs: {e}")
            
    except Exception as e:
        print(f"❌ Erreur diagnostic boucle: {e}")

if __name__ == "__main__":
    print("🚀 LANCEMENT DU DIAGNOSTIC ASSUREUR...")
    print("=" * 60)
    
    success = diagnostic_complet_assureur()
    verifier_boucle_redirection()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 DIAGNOSTIC TERMINÉ - Vérifiez les résultats ci-dessus")
        print("💡 Exécutez maintenant: python manage.py runserver")
        print("🌐 Testez: http://127.0.0.1:8000/assureur/dashboard/")
    else:
        print("❌ DIAGNOSTIC ÉCHOUÉ - Corrigez les erreurs critiques")