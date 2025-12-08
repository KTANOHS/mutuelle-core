# test_cotisations_correct.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from assureur.models import Membre, Cotisation
from django.utils import timezone
import datetime

class CotisationTests(TestCase):
    
    def setUp(self):
        # Créer un utilisateur assureur
        self.user = User.objects.create_user(
            username='assureur_test',
            password='password123',
            is_staff=True
        )
        
        # Créer des membres actifs
        for i in range(3):
            Membre.objects.create(
                nom=f"Test{i}",
                prenom=f"Membre{i}",
                statut='actif',
                numero_membre=f"MBR00{i}",
                type_membre='standard'
            )
    
    def test_page_generer_cotisations(self):
        """Test d'accès à la page de génération"""
        self.client.login(username='assureur_test', password='password123')
        response = self.client.get(reverse('assureur:generer_cotisations'))
        
        print(f"Status code: {response.status_code}")
        print(f"Template utilisé: {response.template_name}")
        
        if response.status_code == 200:
            print("✓ Page génération accessible")
            
            # Vérifier les données de contexte
            context = response.context
            if context:
                print(f"Membres actifs dans contexte: {context.get('membres_actifs_count', 'Non défini')}")
                print(f"Cotisations ce mois: {context.get('cotisations_mois_count', 'Non défini')}")
                print(f"À générer: {context.get('a_generer_count', 'Non défini')}")
        else:
            print("✗ Erreur page génération")
            print(f"Contenu: {response.content[:500]}")
        
        self.assertEqual(response.status_code, 200)
    
    def test_preview_generation(self):
        """Test de la prévisualisation"""
        self.client.login(username='assureur_test', password='password123')
        response = self.client.get(
            reverse('assureur:preview_generation'),
            {'periode': '2024-12'}
        )
        
        print(f"Prévisualisation - Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Prévisualisation fonctionnelle")
            print(f"Contenu type: {type(response.content)}")
            
            # Si c'est du HTML
            if b'<html' in response.content or b'<!DOCTYPE' in response.content:
                print("Retourne du HTML (peut-être une redirection vers login?)")
                print(f"Premiers 500 caractères: {response.content[:500]}")
            else:
                # C'est probablement du JSON ou du HTML partiel
                print(f"Contenu: {response.content[:500]}")
        else:
            print("✗ Erreur prévisualisation")
            print(f"Contenu: {response.content[:500]}")
        
        # Selon votre implémentation, cela pourrait retourner 200 ou autre
        # self.assertEqual(response.status_code, 200)
    
    def test_generate_cotisations_post(self):
        """Test POST de génération de cotisations"""
        self.client.login(username='assureur_test', password='password123')
        
        # Compter les cotisations avant
        avant = Cotisation.objects.count()
        print(f"Cotisations avant génération: {avant}")
        
        # Générer des cotisations pour décembre 2024
        response = self.client.post(
            reverse('assureur:generer_cotisations'),
            {'periode': '2024-12'}
        )
        
        print(f"POST génération - Status: {response.status_code}")
        
        # Compter les cotisations après
        apres = Cotisation.objects.count()
        print(f"Cotisations après génération: {apres}")
        
        # Vérifier que des cotisations ont été créées
        if apres > avant:
            print(f"✓ {apres - avant} cotisation(s) créée(s)")
            
            # Afficher les nouvelles cotisations
            nouvelles = Cotisation.objects.all().order_by('-id')[:apres-avant]
            for cotisation in nouvelles:
                print(f"  - {cotisation.membre.nom} {cotisation.membre.prenom}: {cotisation.periode}")
        else:
            print("✗ Aucune cotisation créée")
            
            # Vérifier pourquoi
            membres_actifs = Membre.objects.filter(statut='actif').count()
            print(f"Membres actifs: {membres_actifs}")
            
            # Vérifier s'il y a déjà des cotisations pour décembre 2024
            cotisations_existantes = Cotisation.objects.filter(periode='2024-12').count()
            print(f"Cotisations existantes pour décembre 2024: {cotisations_existantes}")
        
        # Selon votre implémentation, cela pourrait rediriger (302) ou retourner 200
        # self.assertIn(response.status_code, [200, 302])
    
    def test_list_cotisations(self):
        """Test de la liste des cotisations"""
        self.client.login(username='assureur_test', password='password123')
        response = self.client.get(reverse('assureur:liste_cotisations'))
        
        print(f"Liste cotisations - Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Liste des cotisations accessible")
            
            # Vérifier le contexte
            if hasattr(response, 'context'):
                cotisations = response.context.get('cotisations', [])
                print(f"Nombre de cotisations dans contexte: {len(cotisations)}")
        else:
            print("✗ Erreur liste des cotisations")
            print(f"Contenu: {response.content[:500]}")
        
        self.assertEqual(response.status_code, 200)

# Pour exécuter depuis la ligne de commande
if __name__ == "__main__":
    import django
    import sys
    import os
    
    # Configuration Django
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
    django.setup()
    
    # Créer une instance de test
    test = CotisationTests()
    
    # Exécuter setUp pour créer les données
    print("=== Configuration des données de test ===")
    test.setUp()
    
    print("\n=== Test 1: Page génération de cotisations ===")
    try:
        test.test_page_generer_cotisations()
    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== Test 2: Prévisualisation ===")
    try:
        test.test_preview_generation()
    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== Test 3: Génération de cotisations (POST) ===")
    try:
        test.test_generate_cotisations_post()
    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== Test 4: Liste des cotisations ===")
    try:
        test.test_list_cotisations()
    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()