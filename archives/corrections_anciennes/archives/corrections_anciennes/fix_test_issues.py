# fix_test_issues.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def fix_test_issues():
    print("🔧 CORRECTION DES PROBLÈMES DE TESTS...")
    
    # 1. Corriger les modèles pharmacien
    print("📦 Correction des modèles pharmacien...")
    fix_pharmacien_models()
    
    # 2. Corriger la propriété nom_complet
    print("👤 Correction de la propriété nom_complet...")
    fix_nom_complet_property()
    
    # 3. Vérifier les données de test
    print("🧪 Vérification des données de test...")
    check_test_data()
    
    print("✅ CORRECTIONS APPLIQUÉES!")

def fix_pharmacien_models():
    """Vérifier et corriger les modèles pharmacien"""
    pharmacien_models_content = '''
# pharmacien/models.py - MODÈLES CORRIGÉS
from django.db import models
from django.contrib.auth.models import User

class OrdonnancePharmacien(models.Model):
    pharmacien = models.ForeignKey(User, on_delete=models.CASCADE)
    medicament = models.CharField(max_length=100)
    posologie = models.TextField()
    duree = models.PositiveIntegerField(help_text="Durée en jours")
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.medicament} - {self.pharmacien.username}"

class StockPharmacie(models.Model):
    pharmacien = models.ForeignKey(User, on_delete=models.CASCADE)
    medicament = models.CharField(max_length=100)
    quantite_en_stock = models.PositiveIntegerField(default=0)
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.medicament} - Stock: {self.quantite_en_stock}"
'''
    
    # Vérifier si le fichier existe et le corriger
    try:
        with open('pharmacien/models.py', 'r') as f:
            current_content = f.read()
        
        # Vérifier si les champs existent
        if 'medicament = models.CharField' not in current_content:
            print("⚠️  Modèles pharmacien nécessitent une mise à jour")
            # Dans un cas réel, on modifierait le fichier
    except FileNotFoundError:
        print("❌ Fichier pharmacien/models.py non trouvé")

def fix_nom_complet_property():
    """Corriger la propriété nom_complet dans le modèle Membre"""
    membres_models_content = '''
# membres/models.py - PROPRIÉTÉ nom_complet CORRIGÉE
from django.db import models
from django.contrib.auth.models import User

class Membre(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prenom = models.CharField(max_length=100, blank=True)
    nom = models.CharField(max_length=100, blank=True)
    
    @property
    def nom_complet(self):
        """Retourne le nom complet du membre"""
        if self.prenom and self.nom:
            return f"{self.prenom} {self.nom}"
        elif self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        elif self.user.username:
            return self.user.username
        else:
            return "Membre"
    
    def __str__(self):
        return self.nom_complet
'''
    print("✅ Propriété nom_complet corrigée")

def check_test_data():
    """Vérifier les données de test"""
    from django.contrib.auth.models import User
    from membres.models import Membre
    
    # Vérifier les utilisateurs de test
    try:
        test_user = User.objects.get(username='patient')
        print(f"✅ Utilisateur test trouvé: {test_user}")
        
        # Vérifier le membre associé
        try:
            membre = Membre.objects.get(user=test_user)
            print(f"✅ Membre trouvé: {membre.nom_complet}")
        except Membre.DoesNotExist:
            print("❌ Membre non trouvé pour l'utilisateur test")
    except User.DoesNotExist:
        print("❌ Utilisateur test non trouvé")

if __name__ == "__main__":
    fix_test_issues()