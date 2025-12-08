#!/usr/bin/env python
"""
Script de diagnostic pour l'application Assureur
Exécution: python manage.py shell < diagnostic_assureur.py
ou: python diagnostic_assureur.py
"""

import os
import sys
import django
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

from django.contrib.auth.models import User
from django.db import models
from assureur.models import Assureur, Membre, Cotisation, BonPriseEnCharge
from django.urls import reverse, NoReverseMatch
from django.test import Client

class DiagnosticAssureur:
    """Classe de diagnostic pour l'application Assureur"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success = []
        self.test_user = None
        
    def print_header(self, title):
        """Affiche un en-tête de section"""
        print(f"\n{'='*60}")
        print(f" {title}")
        print(f"{'='*60}")
    
    def check_model(self, model_class, model_name):
        """Vérifie si un modèle existe et a des données"""
        self.print_header(f"Vérification du modèle: {model_name}")
        
        try:
            # Vérifier si la table existe
            table_name = model_class._meta.db_table
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                
            print(f"✅ Table {table_name} existe")
            print(f"   Nombre d'enregistrements: {count}")
            
            # Vérifier les champs du modèle
            fields = [f.name for f in model_class._meta.fields]
            print(f"   Champs: {', '.join(fields[:5])}...")
            
            return True
        except Exception as e:
            self.errors.append(f"Modèle {model_name}: {str(e)}")
            print(f"❌ Erreur avec le modèle {model_name}: {e}")
            return False
    
    def check_assureur_relations(self):
        """Vérifie les relations entre les modèles"""
        self.print_header("Vérification des relations")
        
        try:
            # Vérifier User -> Assureur
            print("\n1. Relation User -> Assureur:")
            users_with_assureur = User.objects.filter(assureur__isnull=False).count()
            print(f"   Users avec profil assureur: {users_with_assureur}")
            
            # Vérifier Assureur -> Membre
            print("\n2. Relation Assureur -> Membre:")
            assureurs = Assureur.objects.all()[:3]  # Prendre 3 assureurs
            for a in assureurs:
                membres_count = Membre.objects.filter(assureur=a).count()
                print(f"   Assureur '{a.nom}': {membres_count} membres")
                
            # Vérifier Membre -> Cotisation
            print("\n3. Relation Membre -> Cotisation:")
            membres = Membre.objects.all()[:3]
            for m in membres:
                cotisations_count = Cotisation.objects.filter(membre=m).count()
                print(f"   Membre '{m.nom}': {cotisations_count} cotisations")
                
            return True
        except Exception as e:
            self.errors.append(f"Relations: {str(e)}")
            print(f"❌ Erreur relations: {e}")
            return False
    
    def check_dashboard_view(self):
        """Vérifie la vue dashboard"""
        self.print_header("Test de la vue Dashboard")
        
        try:
            # Créer un utilisateur de test
            test_user, created = User.objects.get_or_create(
                username='test_assureur',
                defaults={'email': 'test@assureur.com', 'is_active': True}
            )
            
            if created:
                test_user.set_password('test123')
                test_user.save()
                print("✅ Utilisateur de test créé")
            else:
                print("⚠️  Utilisateur de test existe déjà")
            
            # Créer ou récupérer l'assureur de test
            assureur, created = Assureur.objects.get_or_create(
                user=test_user,
                defaults={'nom': 'Assureur Test', 'email': 'test@assureur.com'}
            )
            
            # Créer des données de test
            self.create_test_data(assureur)
            
            # Tester l'accès au dashboard
            client = Client()
            
            # Tester sans authentification
            print("\n1. Test sans authentification:")
            response = client.get(reverse('assureur:dashboard'))
            print(f"   Code: {response.status_code} (attendu: 302 redirect)")
            
            # Tester avec authentification
            print("\n2. Test avec authentification:")
            client.force_login(test_user)
            response = client.get(reverse('assureur:dashboard'))
            print(f"   Code: {response.status_code} (attendu: 200)")
            
            if response.status_code == 200:
                print("✅ Dashboard accessible")
                
                # Vérifier le contenu du contexte
                context = response.context
                print("\n3. Vérification du contexte:")
                
                if 'assureur' in context:
                    print(f"   ✅ 'assureur' dans contexte: {context['assureur']}")
                else:
                    self.errors.append("'assureur' manquant dans contexte")
                    print("   ❌ 'assureur' manquant dans contexte")
                
                if 'stats' in context:
                    print(f"   ✅ 'stats' dans contexte: {len(context['stats'])} statistiques")
                else:
                    self.errors.append("'stats' manquant dans contexte")
                    print("   ❌ 'stats' manquant dans contexte")
            else:
                self.errors.append(f"Dashboard retourne {response.status_code}")
                
            # Nettoyer les données de test
            self.cleanup_test_data(test_user)
            
            return True
        except NoReverseMatch as e:
            self.errors.append(f"URL dashboard: {str(e)}")
            print(f"❌ URL dashboard non trouvée: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Dashboard test: {str(e)}")
            print(f"❌ Erreur dashboard: {e}")
            return False
    
    def create_test_data(self, assureur):
        """Crée des données de test pour l'assureur"""
        print("\nCréation des données de test...")
        
        # Créer quelques membres
        for i in range(3):
            membre, created = Membre.objects.get_or_create(
                assureur=assureur,
                nom=f"Membre Test {i}",
                defaults={
                    'prenom': f"Prénom {i}",
                    'email': f"membre{i}@test.com",
                    'statut': 'actif'
                }
            )
            if created:
                print(f"   ✅ Membre {membre.nom} créé")
                
                # Créer des cotisations
                cotisation = Cotisation.objects.create(
                    membre=membre,
                    montant=10000 + (i * 5000),
                    statut='payee' if i % 2 == 0 else 'en_retard',
                    date_echeance=datetime.now()
                )
                print(f"   ✅ Cotisation {cotisation.montant} FCFA créée")
    
    def cleanup_test_data(self, test_user):
        """Nettoie les données de test"""
        print("\nNettoyage des données de test...")
        
        try:
            # Supprimer l'assureur de test
            Assureur.objects.filter(user=test_user).delete()
            print("   ✅ Assureur de test supprimé")
            
            # Supprimer l'utilisateur de test
            test_user.delete()
            print("   ✅ Utilisateur de test supprimé")
        except Exception as e:
            print(f"   ⚠️  Erreur nettoyage: {e}")
    
    def check_templates(self):
        """Vérifie les templates"""
        self.print_header("Vérification des templates")
        
        templates_to_check = [
            'assureur/base_assureur.html',
            'assureur/dashboard.html',
            'assureur/liste_bons.html',
            'assureur/liste_cotisations.html',
        ]
        
        from django.template.loader import get_template
        
        for template_path in templates_to_check:
            try:
                template = get_template(template_path)
                print(f"✅ Template {template_path} trouvé")
            except Exception as e:
                self.errors.append(f"Template {template_path}: {str(e)}")
                print(f"❌ Template {template_path} non trouvé: {e}")
    
    def check_urls(self):
        """Vérifie les URLs"""
        self.print_header("Vérification des URLs")
        
        urls_to_check = [
            ('assureur:dashboard', {}),
            ('assureur:liste_bons', {}),
            ('assureur:liste_cotisations', {}),
            ('assureur:liste_membres', {}),
        ]
        
        for url_name, kwargs in urls_to_check:
            try:
                path = reverse(url_name, kwargs=kwargs)
                print(f"✅ URL {url_name}: {path}")
            except NoReverseMatch as e:
                self.errors.append(f"URL {url_name}: {str(e)}")
                print(f"❌ URL {url_name} non trouvée: {e}")
            except Exception as e:
                self.errors.append(f"URL {url_name}: {str(e)}")
                print(f"❌ Erreur URL {url_name}: {e}")
    
    def check_database_queries(self):
        """Vérifie les requêtes de statistiques"""
        self.print_header("Test des requêtes statistiques")
        
        try:
            from django.db.models import Count, Sum, Q
            from django.utils import timezone
            
            today = timezone.now()
            debut_mois = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            # Simuler les requêtes du dashboard
            print("\n1. Test requêtes membres:")
            try:
                membres_count = Membre.objects.count()
                print(f"   Total membres: {membres_count}")
            except Exception as e:
                print(f"   ❌ Erreur membres: {e}")
            
            print("\n2. Test requêtes cotisations:")
            try:
                cotisations = Cotisation.objects.filter(
                    date_echeance__month=today.month,
                    date_echeance__year=today.year
                ).aggregate(
                    total=Count('id'),
                    payees=Count('id', filter=Q(statut='payee')),
                    montant_total=Sum('montant', filter=Q(statut='payee'))
                )
                print(f"   Résultat: {cotisations}")
            except Exception as e:
                print(f"   ❌ Erreur cotisations: {e}")
            
            print("\n3. Test requêtes bons:")
            try:
                bons = BonPriseEnCharge.objects.aggregate(
                    total=Count('id'),
                    en_attente=Count('id', filter=Q(statut='en_attente')),
                    valides=Count('id', filter=Q(statut='valide'))
                )
                print(f"   Résultat: {bons}")
            except Exception as e:
                print(f"   ❌ Erreur bons: {e}")
                
            return True
        except Exception as e:
            self.errors.append(f"Requêtes: {str(e)}")
            print(f"❌ Erreur requêtes: {e}")
            return False
    
    def run_all_checks(self):
        """Exécute tous les diagnostics"""
        print("🚀 LANCEMENT DU DIAGNOSTIC ASSUREUR")
        print("="*60)
        
        # 1. Vérifier les modèles
        models_to_check = [
            (Assureur, "Assureur"),
            (Membre, "Membre"),
            (Cotisation, "Cotisation"),
            (BonPriseEnCharge, "BonPriseEnCharge"),
        ]
        
        for model_class, model_name in models_to_check:
            self.check_model(model_class, model_name)
        
        # 2. Vérifier les relations
        self.check_assureur_relations()
        
        # 3. Vérifier les URLs
        self.check_urls()
        
        # 4. Vérifier les templates
        self.check_templates()
        
        # 5. Vérifier les requêtes
        self.check_database_queries()
        
        # 6. Tester la vue dashboard
        self.check_dashboard_view()
        
        # Afficher le résumé
        self.print_summary()
    
    def print_summary(self):
        """Affiche le résumé du diagnostic"""
        self.print_header("RÉSUMÉ DU DIAGNOSTIC")
        
        print(f"\n🔍 {len(self.success)} tests réussis")
        print(f"⚠️  {len(self.warnings)} avertissements")
        print(f"❌ {len(self.errors)} erreurs critiques\n")
        
        if self.errors:
            print("ERREURS CRITIQUES:")
            for error in self.errors:
                print(f"  • {error}")
            print(f"\n🔥 CORRECTIONS REQUISES:")
            
            if any("'assureur' manquant" in e for e in self.errors):
                print("""
  1. Vérifiez que votre vue passe 'assureur' dans le contexte:
     context = {
         'assureur': assureur,  # ← Ajoutez cette ligne
         'stats': stats,
         ...
     }
                """)
            
            if any("URL" in e and "non trouvée" in e for e in self.errors):
                print("""
  2. Vérifiez vos URLs dans urls.py:
     - assureur:dashboard
     - assureur:liste_bons
     - assureur:liste_cotisations
                """)
            
            if any("Template" in e for e in self.errors):
                print("""
  3. Vérifiez vos templates dans templates/assureur/
     - base_assureur.html
     - dashboard.html
     - liste_bons.html
     - liste_cotisations.html
                """)
        
        if not self.errors and not self.warnings:
            print("🎉 TOUT EST FONCTIONNEL !")
            print("   L'application assureur est prête à être utilisée.")
        elif self.errors:
            print("\n🔧 Exécutez les corrections ci-dessus avant de continuer.")
        else:
            print("⚠️  Vérifiez les avertissements mais l'application devrait fonctionner.")

if __name__ == "__main__":
    print("🔧 Diagnostic de l'application Assureur")
    print("Version: 1.0")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    diagnostic = DiagnosticAssureur()
    diagnostic.run_all_checks()