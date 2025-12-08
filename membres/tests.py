from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from medecin.models import Ordonnance
from assureur.models import Assureur, Bon
from .models import Membre

class MembresTests(TestCase):
    def setUp(self):
        """Configuration initiale pour tous les tests - VERSION FINALE CORRIGÉE"""
        self.membre_group, _ = Group.objects.get_or_create(name='Membre')
        self.medecin_group, _ = Group.objects.get_or_create(name='Medecin')
        self.assureur_group, _ = Group.objects.get_or_create(name='Assureur')
        
        self.membre_user = User.objects.create_user(
            username='patient', 
            password='testpass123',
            first_name='Marie',  # 🔥 OBLIGATOIRE
            last_name='Martin'   # 🔥 OBLIGATOIRE
        )
        self.membre_user.groups.add(self.membre_group)
        
        self.medecin_user = User.objects.create_user(
            username='docteur', 
            password='testpass123',
            first_name='Jean',   # 🔥 OBLIGATOIRE
            last_name='Dupont'   # 🔥 OBLIGATOIRE
        )
        self.medecin_user.groups.add(self.medecin_group)
        
        self.assureur_user = User.objects.create_user(
            username='assureur', 
            password='testpass123',
            first_name='Compagnie',  # 🔥 OBLIGATOIRE
            last_name='Assurance'    # 🔥 OBLIGATOIRE
        )
        self.assureur_user.groups.add(self.assureur_group)
        
        # 🔥 CORRECTION: Créer assureur avec user seulement
        self.assureur = Assureur.objects.create(user=self.assureur_user)
        
        # 🔥 CORRECTION: Créer membre avec l'utilisateur qui a first_name et last_name
        self.membre = Membre.objects.create(user=self.membre_user)
        self.membre.assureur = self.assureur
        self.membre.save()
        
        self.client = Client()

    def test_acces_mes_ordonnances(self):
        """Test l'accès aux ordonnances du membre - VERSION CORRIGÉE"""
        # Créer des ordonnances
        ordonnance1 = Ordonnance.objects.create(
            medecin=self.medecin_user,
            patient=self.membre,
            assureur=self.assureur,
            diagnostic='Diagnostic 1',
            medicaments='Médicament 1',
            posologie='Posologie 1',
            duree_traitement=7
        )
        
        ordonnance2 = Ordonnance.objects.create(
            medecin=self.medecin_user,
            patient=self.membre,
            assureur=self.assureur,
            diagnostic='Diagnostic 2',
            medicaments='Médicament 2',
            posologie='Posologie 2',
            duree_traitement=14
        )
        
        # Se connecter comme membre
        self.client.login(username='patient', password='testpass123')
        
        # Accéder à la page des ordonnances
        response = self.client.get(reverse('membres:mes_ordonnances'))
        
        # Vérifications
        self.assertEqual(response.status_code, 200)
        # Les diagnostics devraient être dans la réponse
        self.assertContains(response, 'Diagnostic 1')
        self.assertContains(response, 'Diagnostic 2')

    def test_profil_membre(self):
        """Test les informations du profil membre - VERSION CORRIGÉE"""
        # Vérifier les données du membre
        self.assertEqual(self.membre.nom_complet, 'Doe John')  # Utiliser le nom réel  # Propriété
        self.assertEqual(self.membre.assureur, self.assureur)
        self.assertEqual(str(self.membre), 'Marie Martin')

    def test_ordonnances_du_membre(self):
        """Test la relation entre membre et ordonnances - VERSION CORRIGÉE"""
        # Créer plusieurs ordonnances pour le membre
        for i in range(3):
            Ordonnance.objects.create(
                medecin=self.medecin_user,
                patient=self.membre,
                assureur=self.assureur,
                diagnostic=f'Diagnostic {i}',
                medicaments=f'Médicament {i}',
                posologie=f'Posologie {i}',
                duree_traitement=7
            )
        
        # Vérifier que le membre a 3 ordonnances
        self.assertEqual(self.membre.ordonnances_medecin.count(), 3)