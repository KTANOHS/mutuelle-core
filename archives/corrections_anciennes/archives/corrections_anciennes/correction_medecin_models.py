#!/usr/bin/env python
"""
CORRECTION URGENTE - medecin/models.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

def corriger_medecin_models():
    """Corrige le fichier medecin/models.py"""
    print("🔧 CORRECTION URGENTE - medecin/models.py")
    print("=" * 60)
    
    file_path = 'medecin/models.py'
    
    if not os.path.exists(file_path):
        print(f"❌ Fichier {file_path} non trouvé")
        return False
    
    try:
        # Lire le contenu actuel
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Vérifier si la correction est déjà présente
        if "return date.today() <= date_expiration" in content:
            print("✅ La correction est_valide est déjà présente")
            return True
        
        # Remplacer la méthode est_valide problématique
        old_method = """@property
def est_valide(self):
    \"\"\"Vérifie si l'ordonnance est encore valide (30 jours)\"\"\"
    if not self.date_prescription:
        return False
    
    date_expiration = self.date_prescription + timedelta(days=30)
    return timezone.now().date() <= date_expiration"""
        
        new_method = """@property
def est_valide(self):
    \"\"\"Vérifie si l'ordonnance est encore valide (30 jours) - VERSION CORRIGÉE\"\"\"
    if not self.date_prescription:
        return False
    
    # ✅ CORRECTION: Gérer à la fois les dates et les datetimes
    if hasattr(self.date_prescription, 'date'):
        # C'est un datetime, on extrait la date
        date_prescription_date = self.date_prescription.date()
    else:
        # C'est déjà une date
        date_prescription_date = self.date_prescription
        
    date_expiration = date_prescription_date + timedelta(days=30)
    
    # ✅ CORRECTION: Utiliser date.today() pour éviter l'erreur de comparaison
    return date.today() <= date_expiration"""
        
        if old_method in content:
            content = content.replace(old_method, new_method)
            print("✅ Méthode est_valide corrigée")
        else:
            print("⚠️  Méthode est_valide non trouvée dans le format attendu")
            # Essayer une autre approche
            if "timezone.now().date() <= date_expiration" in content:
                content = content.replace(
                    "timezone.now().date() <= date_expiration", 
                    "date.today() <= date_expiration"
                )
                print("✅ Correction alternative appliquée")
            else:
                print("❌ Impossible de trouver le code à corriger")
                return False
        
        # Sauvegarder le fichier corrigé
        with open(file_path, 'w') as f:
            f.write(content)
        
        print("✅ Fichier medecin/models.py corrigé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        return False

def tester_correction():
    """Teste la correction appliquée"""
    print("\n🔍 TEST DE LA CORRECTION:")
    
    try:
        from medecin.models import Ordonnance
        from django.contrib.auth.models import User
        from datetime import date, timedelta
        
        # Créer une ordonnance de test
        user, created = User.objects.get_or_create(
            username='test_correction_medecin',
            defaults={'first_name': 'Test', 'last_name': 'Correction'}
        )
        
        ordonnance = Ordonnance(
            patient=user,
            diagnostic="Test correction",
            date_prescription=date.today(),  # Utiliser date au lieu de datetime
            medecin_prescripteur="Dr Test"
        )
        
        # Tester la méthode est_valide
        est_valide = ordonnance.est_valide
        print(f"✅ Test est_valide: {est_valide}")
        
        # Nettoyer
        if created:
            user.delete()
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    success = corriger_medecin_models()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ CORRECTION APPLIQUÉE - Testons maintenant...")
        tester_correction()
        
        print("\n🎯 EXÉCUTEZ MAINTENANT:")
        print("python manage.py test medecin.tests.MedecinTests.test_ordonnance_est_valide --settings=mutuelle_core.settings")