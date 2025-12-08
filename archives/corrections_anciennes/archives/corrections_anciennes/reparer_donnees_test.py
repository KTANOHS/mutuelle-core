# reparer_donnees_test.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def reparer_donnees():
    """Réparer les données de test"""
    print("🔧 Réparation des données de test...")
    
    from django.contrib.auth.models import User, Group
    from membres.models import Membre
    from medecin.models import Ordonnance, Medecin
    from django.utils import timezone
    
    # 1. Réparer les noms des utilisateurs
    print("1. Réparation des noms utilisateurs...")
    
    # Trouver l'utilisateur patient
    patient_user = User.objects.filter(username='patient').first()
    if patient_user:
        patient_user.first_name = 'John'
        patient_user.last_name = 'Doe'
        patient_user.save()
        print(f"✅ Patient réparé: {patient_user.first_name} {patient_user.last_name}")
    
    # Trouver le membre associé
    membre = Membre.objects.filter(user=patient_user).first()
    if membre:
        print(f"✅ Membre trouvé: {membre.nom_complet}")
    
    # 2. Vérifier les ordonnances
    print("2. Vérification des ordonnances...")
    
    ordonnances = Ordonnance.objects.all()
    print(f"Ordonnances totales: {ordonnances.count()}")
    
    for ord in ordonnances:
        print(f"Ordonnance {ord.id}:")
        print(f"  - Patient: {ord.patient}")
        print(f"  - Diagnostic: {ord.diagnostic}")
        print(f"  - Date: {ord.date_prescription}")
        print(f"  - Est valide: {ord.est_valide}")
        
        # Vérifier que l'ordonnance a une date de prescription
        if not ord.date_prescription:
            ord.date_prescription = timezone.now().date()
            ord.save()
            print(f"  ✅ Date de prescription ajoutée")
    
    # 3. Créer des ordonnances de test si nécessaire
    if ordonnances.count() == 0:
        print("3. Création d'ordonnances de test...")
        
        # Trouver un médecin
        medecin_user = User.objects.filter(groups__name='Médecins').first()
        if medecin_user and hasattr(medecin_user, 'medecin_profile'):
            medecin = medecin_user.medecin_profile
            
            # Créer 3 ordonnances de test
            for i in range(1, 4):
                ordonnance = Ordonnance.objects.create(
                    medecin=medecin,
                    patient=patient_user,
                    diagnostic=f"Diagnostic {i}",
                    date_prescription=timezone.now().date()
                )
                print(f"✅ Ordonnance {i} créée: {ordonnance.diagnostic}")
    
    print("🎉 DONNÉES RÉPARÉES!")

if __name__ == "__main__":
    reparer_donnees()