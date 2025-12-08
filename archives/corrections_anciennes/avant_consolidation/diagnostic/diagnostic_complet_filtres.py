import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    from django.test import Client
    from membres.models import Membre
    from medecin.models import MaladieChronique
    
    def diagnostic_complet_filtres():
        print("🔍 DIAGNOSTIC COMPLET DES FILTRES")
        print("=" * 60)
        
        # 1. Vérifier les données disponibles
        print("1. 📊 DONNÉES DISPONIBLES:")
        patients_count = Membre.objects.count()
        maladies_count = MaladieChronique.objects.count()
        
        print(f"   👥 Patients dans la base: {patients_count}")
        if patients_count > 0:
            patients = Membre.objects.all()[:3]
            for p in patients:
                print(f"      - {p.get_full_name()} (ID: {p.id})")
        
        print(f"   🩺 Maladies chroniques: {maladies_count}")
        if maladies_count > 0:
            maladies = MaladieChronique.objects.all()[:3]
            for m in maladies:
                print(f"      - {m.nom} (ID: {m.id})")
        
        # 2. Test de la page
        client = Client()
        
        print("\n2. 🔑 Connexion...")
        if not client.login(username='medecin_test', password='password123'):
            print("   ❌ Échec connexion")
            return
        
        print("   ✅ Connecté")
        
        # 3. Test de la page
        print("\n3. 🚀 Test page création accompagnement...")
        response = client.get('/medecin/suivi-chronique/accompagnements/creer/')
        
        print(f"   📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            print(f"   📏 Taille page: {len(content)} caractères")
            
            # 4. Vérification du contexte
            print("\n4. 📋 CONTEXTE FOURNI:")
            if hasattr(response, 'context'):
                context = response.context
                print(f"   ✅ Contexte disponible")
                print(f"   👥 Patients dans contexte: {len(context.get('patients', []))}")
                print(f"   🩺 Maladies dans contexte: {len(context.get('maladies', []))}")
            else:
                print("   ❌ Aucun contexte disponible")
            
            # 5. Vérification des éléments HTML
            print("\n5. 🎯 ÉLÉMENTS HTML:")
            elements = [
                ("Formulaire principal", '<form' in content),
                ("Champ recherche patient", 'patientSearch' in content),
                ("Champ recherche maladie", 'maladieSearch' in content),
                ("Select patient", 'patient_id' in content),
                ("Select maladie", 'maladie' in content),
                ("JavaScript", '<script>' in content),
                ("Fonction filterPatients", 'filterPatients()' in content),
                ("Fonction filterMaladies", 'filterMaladies()' in content),
            ]
            
            for element, present in elements:
                status = "✅" if present else "❌"
                print(f"   {status} {element}")
            
            # 6. Vérification des données dans le HTML
            print("\n6. 📄 DONNÉES DANS LE HTML:")
            import re
            
            # Compter les options patients
            patient_options = re.findall(r'<option value="\d+"', content)
            print(f"   👥 Options patients: {len(patient_options) - 1}")  # -1 pour l'option vide
            
            # Compter les options maladies
            maladie_options = re.findall(r'<option value="\d+"', content)
            print(f"   🩺 Options maladies: {len(maladie_options) - 1}")  # -1 pour l'option vide
            
            # 7. Vérification JavaScript
            print("\n7. 🛠️ JAVASCRIPT:")
            js_checks = [
                ("Variables globales", 'allPatients = []' in content and 'allMaladies = []' in content),
                ("Initialisation", 'DOMContentLoaded' in content),
                ("Fonctions de filtrage", 'function filterPatients()' in content and 'function filterMaladies()' in content),
                ("Sélection interactive", 'selectPatient(' in content and 'selectMaladie(' in content),
                ("Validation", 'validateForm(' in content),
            ]
            
            for check, present in js_checks:
                status = "✅" if present else "❌"
                print(f"   {status} {check}")
            
            # 8. Vérification CSS
            print("\n8. 🎨 CSS:")
            css_checks = [
                ("Styles recherche", '.search-highlight' in content),
                ("Sections filtres", '.filter-section' in content),
                ("Résultats recherche", '.search-results' in content),
            ]
            
            for check, present in css_checks:
                status = "✅" if present else "❌"
                print(f"   {status} {check}")
                
        else:
            print(f"   ❌ Page inaccessible: {response.status_code}")
            
        # 9. Recommandations
        print("\n9. 💡 RECOMMANDATIONS:")
        
        if patients_count == 0:
            print("   ⚠️  Créer des patients pour tester les filtres")
            print("   💡 Exécutez: python creer_donnees_test_accompagnement.py")
            
        if maladies_count == 0:
            print("   ⚠️  Créer des maladies chroniques pour tester les filtres")
            print("   💡 Exécutez: python creer_donnees_test_accompagnement.py")
            
        if patients_count > 0 and maladies_count > 0:
            print("   ✅ Données suffisantes pour tester les filtres")
            print("   💡 Testez dans le navigateur: http://127.0.0.1:8000/medecin/suivi-chronique/accompagnements/creer/")
    
    diagnostic_complet_filtres()
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()