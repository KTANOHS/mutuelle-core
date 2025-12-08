import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    from django.contrib.auth.models import User
    from medecin.models import Medecin, SpecialiteMedicale, BonSoin
    
    def verification_donnees():
        print("📊 VÉRIFICATION DES DONNÉES")
        print("=" * 40)
        
        # 1. Médecins
        print("1. 🩺 Médecins dans le système:")
        medecins = Medecin.objects.all()
        for medecin in medecins:
            print(f"   👤 {medecin} (User: {medecin.user.username})")
        
        # 2. Spécialités
        print("\n2. 📚 Spécialités médicales:")
        specialites = SpecialiteMedicale.objects.all()
        for spec in specialites:
            print(f"   🎯 {spec.nom} - {spec.description}")
        
        # 3. Bons de soin
        print("\n3. 📋 Bons de soin:")
        bons = BonSoin.objects.all()[:5]  # Premiers 5 seulement
        for bon in bons:
            print(f"   📄 {bon.numero_bon} - {bon.membre} - Statut: {bon.statut}")
        
        print(f"\n📈 Total bons dans le système: {BonSoin.objects.count()}")
        
        # 4. Vérifier les bons assignés au médecin de test
        try:
            medecin_test = Medecin.objects.get(user__username='medecin_test')
            bons_medecin = BonSoin.objects.filter(medecin_destinataire=medecin_test)
            print(f"\n4. 🎯 Bons assignés au médecin test: {bons_medecin.count()}")
            
            for bon in bons_medecin:
                print(f"   📋 {bon.numero_bon} - {bon.membre} - {bon.statut}")
                
        except Medecin.DoesNotExist:
            print("\n4. ❌ Médecin test non trouvé")
    
    verification_donnees()
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()