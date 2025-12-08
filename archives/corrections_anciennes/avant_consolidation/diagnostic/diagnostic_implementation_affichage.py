# diagnostic_implementation_affichage.py
import os
import sys
import django
from pathlib import Path
from datetime import datetime

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

print("🔍 DIAGNOSTIC IMPLÉMENTATION AFFICHAGE_UNIFIE")
print("=" * 60)

class DiagnosticImplementation:
    def __init__(self):
        self.rapport = {
            'timestamp': datetime.now().isoformat(),
            'tests': [],
            'erreurs': [],
            'recommandations': []
        }
    
    def verifier_import_affichage_unifie(self):
        """Vérifie que le module affichage_unifie est importable"""
        print("\n1. 📦 VÉRIFICATION IMPORT AFFICHAGE_UNIFIE...")
        
        try:
            from affichage_unifie import afficher_fiche_cotisation_unifiee, determiner_statut_cotisation
            self.rapport['tests'].append({
                'test': 'Import affichage_unifie',
                'statut': '✅ SUCCÈS',
                'details': 'Module importé avec succès'
            })
            print("   ✅ Module affichage_unifie importé avec succès")
            return True
        except ImportError as e:
            self.rapport['erreurs'].append({
                'test': 'Import affichage_unifie',
                'erreur': f'Import impossible: {e}',
                'severite': 'CRITIQUE'
            })
            print(f"   ❌ ERREUR: Impossible d'importer affichage_unifie: {e}")
            return False
    
    def verifier_fonctions_disponibles(self):
        """Vérifie que les fonctions nécessaires sont disponibles"""
        print("\n2. 🔧 VÉRIFICATION FONCTIONS DISPONIBLES...")
        
        try:
            from affichage_unifie import afficher_fiche_cotisation_unifiee, determiner_statut_cotisation
            
            # Test de la fonction principale
            test_result = afficher_fiche_cotisation_unifiee(None, None, None)
            
            self.rapport['tests'].append({
                'test': 'Fonction afficher_fiche_cotisation_unifiee',
                'statut': '✅ SUCCÈS',
                'details': 'Fonction exécutée avec succès'
            })
            print("   ✅ Fonction afficher_fiche_cotisation_unifiee opérationnelle")
            
            # Test de la fonction de détermination de statut
            statut, icone, classe = determiner_statut_cotisation(None)
            
            self.rapport['tests'].append({
                'test': 'Fonction determiner_statut_cotisation',
                'statut': '✅ SUCCÈS',
                'details': f'Retour: {statut}, {icone}, {classe}'
            })
            print("   ✅ Fonction determiner_statut_cotisation opérationnelle")
            
            return True
            
        except Exception as e:
            self.rapport['erreurs'].append({
                'test': 'Fonctions affichage_unifie',
                'erreur': f'Erreur exécution: {e}',
                'severite': 'CRITIQUE'
            })
            print(f"   ❌ ERREUR: Fonctions non opérationnelles: {e}")
            return False
    
    def verifier_integration_views(self):
        """Vérifie l'intégration dans agents/views.py"""
        print("\n3. 📁 VÉRIFICATION INTÉGRATION VIEWS.PY...")
        
        views_path = Path('agents/views.py')
        
        if not views_path.exists():
            self.rapport['erreurs'].append({
                'test': 'Fichier views.py',
                'erreur': 'Fichier agents/views.py non trouvé',
                'severite': 'CRITIQUE'
            })
            print("   ❌ Fichier agents/views.py non trouvé")
            return False
        
        try:
            with open(views_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier l'import
            if 'from affichage_unifie import' in content:
                self.rapport['tests'].append({
                    'test': 'Import dans views.py',
                    'statut': '✅ SUCCÈS',
                    'details': 'Import détecté dans views.py'
                })
                print("   ✅ Import affichage_unifie détecté dans views.py")
            else:
                self.rapport['erreurs'].append({
                    'test': 'Import dans views.py',
                    'erreur': 'Import non trouvé dans views.py',
                    'severite': 'CRITIQUE'
                })
                print("   ❌ Import affichage_unifie NON TROUVÉ dans views.py")
            
            # Vérifier la vue afficher_fiche_cotisation_unifiee_view
            if 'def afficher_fiche_cotisation_unifiee_view' in content:
                self.rapport['tests'].append({
                    'test': 'Vue afficher_fiche_cotisation_unifiee_view',
                    'statut': '✅ SUCCÈS',
                    'details': 'Vue détectée dans views.py'
                })
                print("   ✅ Vue afficher_fiche_cotisation_unifiee_view détectée")
            else:
                self.rapport['erreurs'].append({
                    'test': 'Vue affichage unifié',
                    'erreur': 'Vue afficher_fiche_cotisation_unifiee_view non trouvée',
                    'severite': 'CRITIQUE'
                })
                print("   ❌ Vue afficher_fiche_cotisation_unifiee_view NON TROUVÉE")
            
            return True
            
        except Exception as e:
            self.rapport['erreurs'].append({
                'test': 'Lecture views.py',
                'erreur': f'Erreur lecture: {e}',
                'severite': 'CRITIQUE'
            })
            print(f"   ❌ Erreur lecture views.py: {e}")
            return False
    
    def verifier_urls_configuration(self):
        """Vérifie la configuration des URLs"""
        print("\n4. 🌐 VÉRIFICATION CONFIGURATION URLs...")
        
        urls_path = Path('agents/urls.py')
        
        if not urls_path.exists():
            self.rapport['erreurs'].append({
                'test': 'Fichier urls.py',
                'erreur': 'Fichier agents/urls.py non trouvé',
                'severite': 'CRITIQUE'
            })
            print("   ❌ Fichier agents/urls.py non trouvé")
            return False
        
        try:
            with open(urls_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier l'URL pour l'affichage unifié
            if 'fiche-cotisation-unifiee' in content:
                self.rapport['tests'].append({
                    'test': 'URL affichage unifié',
                    'statut': '✅ SUCCÈS',
                    'details': 'URL fiche-cotisation-unifiee détectée'
                })
                print("   ✅ URL fiche-cotisation-unifiee détectée dans urls.py")
            else:
                self.rapport['erreurs'].append({
                    'test': 'URL affichage unifié',
                    'erreur': 'URL fiche-cotisation-unifiee non trouvée',
                    'severite': 'MOYENNE'
                })
                print("   ❌ URL fiche-cotisation-unifiee NON TROUVÉE dans urls.py")
            
            return True
            
        except Exception as e:
            self.rapport['erreurs'].append({
                'test': 'Lecture urls.py',
                'erreur': f'Erreur lecture: {e}',
                'severite': 'CRITIQUE'
            })
            print(f"   ❌ Erreur lecture urls.py: {e}")
            return False
    
    def verifier_template_existe(self):
        """Vérifie que le template existe"""
        print("\n5. 📋 VÉRIFICATION TEMPLATE...")
        
        template_path = Path('agents/templates/agents/fiche_cotisation_unifiee.html')
        
        if template_path.exists():
            self.rapport['tests'].append({
                'test': 'Template fiche_cotisation_unifiee.html',
                'statut': '✅ SUCCÈS',
                'details': 'Template trouvé'
            })
            print("   ✅ Template fiche_cotisation_unifiee.html trouvé")
            return True
        else:
            self.rapport['erreurs'].append({
                'test': 'Template affichage unifié',
                'erreur': 'Template fiche_cotisation_unifiee.html non trouvé',
                'severite': 'MOYENNE'
            })
            print("   ❌ Template fiche_cotisation_unifiee.html NON TROUVÉ")
            return False
    
    def tester_fonctionnalite_complete(self):
        """Teste la fonctionnalité complète avec des données réelles"""
        print("\n6. 🧪 TEST FONCTIONNALITÉ COMPLÈTE...")
        
        try:
            from membres.models import Membre
            from agents.models import VerificationCotisation
            from membres.models import Cotisation
            from affichage_unifie import afficher_fiche_cotisation_unifiee
            
            # Récupérer un membre de test
            membre_test = Membre.objects.first()
            
            if not membre_test:
                self.rapport['erreurs'].append({
                    'test': 'Données test',
                    'erreur': 'Aucun membre trouvé pour le test',
                    'severite': 'MOYENNE'
                })
                print("   ⚠️  Aucun membre trouvé pour le test")
                return False
            
            # Récupérer vérification et cotisation
            verification = VerificationCotisation.objects.filter(membre=membre_test).first()
            cotisation = Cotisation.objects.filter(membre=membre_test).first()
            
            # Générer l'affichage unifié
            fiche = afficher_fiche_cotisation_unifiee(membre_test, verification, cotisation)
            
            self.rapport['tests'].append({
                'test': 'Génération fiche réelle',
                'statut': '✅ SUCCÈS',
                'details': f'Fiche générée pour {membre_test.nom_complet}'
            })
            print(f"   ✅ Fiche générée avec succès pour {membre_test.nom_complet}")
            
            # Afficher un extrait de la fiche
            print(f"   📄 Extrait fiche:\n{fiche[:200]}...")
            
            return True
            
        except Exception as e:
            self.rapport['erreurs'].append({
                'test': 'Test fonctionnalité complète',
                'erreur': f'Erreur test: {e}',
                'severite': 'CRITIQUE'
            })
            print(f"   ❌ Erreur test fonctionnalité: {e}")
            return False
    
    def verifier_acces_url(self):
        """Vérifie l'accès à l'URL via le navigateur"""
        print("\n7. 🌐 VÉRIFICATION ACCÈS URL...")
        
        try:
            from django.test import Client
            from django.contrib.auth.models import User
            
            # Créer un client de test
            client = Client()
            
            # Tenter de se connecter (simuler un agent)
            user = User.objects.filter(is_staff=True).first()
            if user:
                client.force_login(user)
                
                # Tester l'accès à l'URL
                response = client.get('/agents/fiche-cotisation-unifiee/1/')
                
                if response.status_code == 200:
                    self.rapport['tests'].append({
                        'test': 'Accès URL',
                        'statut': '✅ SUCCÈS',
                        'details': 'URL accessible avec statut 200'
                    })
                    print("   ✅ URL /agents/fiche-cotisation-unifiee/1/ accessible")
                elif response.status_code == 404:
                    self.rapport['tests'].append({
                        'test': 'Accès URL',
                        'statut': '🟡 ATTENTION',
                        'details': 'URL accessible mais membre 1 non trouvé'
                    })
                    print("   🟡 URL accessible mais membre 1 non trouvé (statut 404)")
                else:
                    self.rapport['erreurs'].append({
                        'test': 'Accès URL',
                        'erreur': f'Statut HTTP: {response.status_code}',
                        'severite': 'MOYENNE'
                    })
                    print(f"   ❌ Erreur accès URL: statut {response.status_code}")
            else:
                self.rapport['erreurs'].append({
                    'test': 'Accès URL',
                    'erreur': 'Aucun utilisateur staff trouvé pour le test',
                    'severite': 'MOYENNE'
                })
                print("   ⚠️  Aucun utilisateur staff trouvé pour tester l'accès")
                
        except Exception as e:
            self.rapport['erreurs'].append({
                'test': 'Test accès URL',
                'erreur': f'Erreur test accès: {e}',
                'severite': 'MOYENNE'
            })
            print(f"   ❌ Erreur test accès URL: {e}")
    
    def generer_rapport_complet(self):
        """Génère un rapport complet du diagnostic"""
        print("\n" + "="*60)
        print("📊 RAPPORT DIAGNOSTIC IMPLÉMENTATION")
        print("="*60)
        
        # Résumé
        total_tests = len(self.rapport['tests'])
        total_erreurs = len(self.rapport['erreurs'])
        tests_reussis = sum(1 for test in self.rapport['tests'] if test['statut'] == '✅ SUCCÈS')
        
        print(f"\n📈 STATISTIQUES:")
        print(f"   • Tests réalisés: {total_tests}")
        print(f"   • Tests réussis: {tests_reussis}")
        print(f"   • Erreurs détectées: {total_erreurs}")
        print(f"   • Taux de succès: {(tests_reussis/total_tests)*100:.1f}%" if total_tests > 0 else "N/A")
        
        # Détails des tests
        print(f"\n✅ TESTS RÉUSSIS:")
        for test in self.rapport['tests']:
            if test['statut'] == '✅ SUCCÈS':
                print(f"   • {test['test']}: {test['details']}")
        
        # Erreurs critiques
        erreurs_critiques = [e for e in self.rapport['erreurs'] if e['severite'] == 'CRITIQUE']
        if erreurs_critiques:
            print(f"\n🔴 ERREURS CRITIQUES:")
            for erreur in erreurs_critiques:
                print(f"   • {erreur['test']}: {erreur['erreur']}")
        
        # Erreurs moyennes
        erreurs_moyennes = [e for e in self.rapport['erreurs'] if e['severite'] == 'MOYENNE']
        if erreurs_moyennes:
            print(f"\n🟡 ERREURS MOYENNES:")
            for erreur in erreurs_moyennes:
                print(f"   • {erreur['test']}: {erreur['erreur']}")
        
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS:")
        
        if total_erreurs == 0:
            print("   ✅ L'implémentation est COMPLÈTEMENT FONCTIONNELLE!")
            print("   🚀 Vous pouvez maintenant utiliser l'affichage unifié")
        else:
            if any('Import' in e['test'] for e in self.rapport['erreurs']):
                print("   🔧 Corriger l'import de affichage_unifie dans views.py")
            
            if any('Vue' in e['test'] for e in self.rapport['erreurs']):
                print("   🔧 Ajouter la vue afficher_fiche_cotisation_unifiee_view dans views.py")
            
            if any('URL' in e['test'] for e in self.rapport['erreurs']):
                print("   🔧 Configurer l'URL dans agents/urls.py")
            
            if any('Template' in e['test'] for e in self.rapport['erreurs']):
                print("   🔧 Créer le template fiche_cotisation_unifiee.html")
        
        print(f"\n🎯 PROCHAINES ÉTAPES:")
        print("   1. Accéder à: http://127.0.0.1:8000/agents/fiche-cotisation-unifiee/1/")
        print("   2. Tester avec différents membres")
        print("   3. Intégrer dans l'interface de recherche existante")
        
        print("\n" + "="*60)
    
    def executer_diagnostic_complet(self):
        """Exécute le diagnostic complet"""
        print("🎯 LANCEMENT DIAGNOSTIC COMPLET...")
        
        try:
            self.verifier_import_affichage_unifie()
            self.verifier_fonctions_disponibles()
            self.verifier_integration_views()
            self.verifier_urls_configuration()
            self.verifier_template_existe()
            self.tester_fonctionnalite_complete()
            self.verifier_acces_url()
            self.generer_rapport_complet()
            
            print("✅ DIAGNOSTIC TERMINÉ")
            
        except Exception as e:
            print(f"❌ Erreur lors du diagnostic: {e}")

# Exécution
if __name__ == "__main__":
    diagnostic = DiagnosticImplementation()
    diagnostic.executer_diagnostic_complet()