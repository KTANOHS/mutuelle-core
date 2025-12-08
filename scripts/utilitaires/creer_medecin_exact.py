import os
import django
import sys
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    from django.contrib.auth.models import User
    from medecin.models import Medecin, SpecialiteMedicale, EtablissementMedical
    
    def creer_medecin_exact():
        print("🛠️ CRÉATION MÉDECIN (STRUCTURE EXACTE)")
        print("=" * 50)
        
        # 1. Vérifier/Créer une spécialité médicale
        print("1. 🔍 Vérification spécialité médicale...")
        try:
            specialite = SpecialiteMedicale.objects.get(nom="Généraliste")
            print(f"   ✅ Spécialité trouvée: {specialite}")
        except SpecialiteMedicale.DoesNotExist:
            # Créer la spécialité
            specialite = SpecialiteMedicale.objects.create(
                nom="Généraliste",
                description="Médecine générale"
            )
            print("   ✅ Spécialité 'Généraliste' créée")
        
        # 2. Vérifier/Créer un établissement médical
        print("2. 🏥 Vérification établissement médical...")
        try:
            etablissement = EtablissementMedical.objects.get(nom="Cabinet Test")
            print(f"   ✅ Établissement trouvé: {etablissement}")
        except EtablissementMedical.DoesNotExist:
            # Créer l'établissement
            etablissement = EtablissementMedical.objects.create(
                nom="Cabinet Test",
                type_etablissement="cabinet",
                adresse="123 Rue Test, Ville Test",
                telephone="0123456789",
                email="cabinet@test.com"
            )
            print("   ✅ Établissement 'Cabinet Test' créé")
        
        # 3. Vérifier/Créer l'utilisateur
        print("3. 👤 Vérification utilisateur...")
        try:
            user = User.objects.get(username='medecin_test')
            print("   ✅ Utilisateur medecin_test trouvé")
        except User.DoesNotExist:
            user = User.objects.create_user(
                username='medecin_test',
                email='medecin@test.com',
                password='password123',
                first_name='Docteur',
                last_name='Test'
            )
            print("   ✅ Utilisateur medecin_test créé")
        
        # 4. Vérifier/Créer le médecin AVEC LA BONNE STRUCTURE
        print("4. 🩺 Vérification médecin...")
        try:
            medecin = Medecin.objects.get(user=user)
            print(f"   ✅ Médecin trouvé: {medecin}")
            
        except Medecin.DoesNotExist:
            # Créer le médecin avec tous les champs requis
            medecin = Medecin.objects.create(
                user=user,
                numero_ordre="ORD123456",
                specialite=specialite,
                etablissement=etablissement,
                telephone_pro="0123456789",
                email_pro="medecin.pro@test.com",
                annees_experience=10,
                tarif_consultation=50.00,
                actif=True,
                disponible=True,
                date_inscription=datetime.now(),
                date_derniere_modif=datetime.now(),
                horaires_travail=json.dumps({
                    "lundi": {"debut": "08:00", "fin": "18:00"},
                    "mardi": {"debut": "08:00", "fin": "18:00"},
                    "mercredi": {"debut": "08:00", "fin": "18:00"},
                    "jeudi": {"debut": "08:00", "fin": "18:00"},
                    "vendredi": {"debut": "08:00", "fin": "18:00"}
                }),
                diplome_verifie=True
                # cv_document est optionnel
            )
            print("   ✅ Médecin créé avec succès!")
        
        # 5. Affichage des détails
        print(f"\n5. 📋 DÉTAILS DU MÉDECIN:")
        print(f"   👤 Nom complet: Dr {user.first_name} {user.last_name}")
        print(f"   📧 Email pro: {medecin.email_pro}")
        print(f"   📞 Téléphone pro: {medecin.telephone_pro}")
        print(f"   🎯 Spécialité: {medecin.specialite.nom}")
        print(f"   🏥 Établissement: {medecin.etablissement.nom}")
        print(f"   📜 Numéro d'ordre: {medecin.numero_ordre}")
        print(f"   💰 Tarif consultation: {medecin.tarif_consultation}€")
        print(f"   📅 Années expérience: {medecin.annees_experience}")
        print(f"   ✅ Actif: {medecin.actif}")
        print(f"   🟢 Disponible: {medecin.disponible}")
        
        return user, medecin
    
    user, medecin = creer_medecin_exact()
    
    print("\n🎯 MÉDECIN CRÉÉ AVEC SUCCÈS!")
    print("📋 Prêt pour les tests d'interface")
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()