import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    from django.contrib.auth.models import User
    from medecin.models import Medecin, SpecialiteMedicale, EtablissementMedical
    
    def verification_donnees_exacte():
        print("📊 VÉRIFICATION DES DONNÉES EXACTES")
        print("=" * 50)
        
        # 1. Vérifier le médecin de test
        print("1. 🧪 MÉDECIN DE TEST:")
        try:
            medecin_test = Medecin.objects.get(user__username='medecin_test')
            print(f"   ✅ Trouvé: {medecin_test}")
            print(f"   👤 User: {medecin_test.user.username}")
            print(f"   📧 Email pro: {medecin_test.email_pro}")
            print(f"   📞 Téléphone: {medecin_test.telephone_pro}")
            print(f"   🎯 Spécialité: {medecin_test.specialite.nom}")
            print(f"   🏥 Établissement: {medecin_test.etablissement.nom}")
            print(f"   ✅ Actif: {medecin_test.actif}")
            print(f"   🟢 Disponible: {medecin_test.disponible}")
            
        except Medecin.DoesNotExist:
            print("   ❌ Médecin test non trouvé")
            return False
        
        # 2. Vérifier les spécialités
        print("\n2. 📚 SPÉCIALITÉS MÉDICALES:")
        specialites = SpecialiteMedicale.objects.all()
        for spec in specialites:
            count = Medecin.objects.filter(specialite=spec).count()
            print(f"   🎯 {spec.nom}: {count} médecin(s)")
        
        # 3. Vérifier les établissements
        print("\n3. 🏥 ÉTABLISSEMENTS MÉDICAUX:")
        etablissements = EtablissementMedical.objects.all()
        for etab in etablissements:
            count = Medecin.objects.filter(etablissement=etab).count()
            print(f"   🏥 {etab.nom} ({etab.type_etablissement}): {count} médecin(s)")
        
        # 4. Statistiques générales
        print("\n4. 📈 STATISTIQUES:")
        print(f"   👨‍⚕️  Total médecins: {Medecin.objects.count()}")
        print(f"   ✅ Médecins actifs: {Medecin.objects.filter(actif=True).count()}")
        print(f"   🟢 Médecins disponibles: {Medecin.objects.filter(disponible=True).count()}")
        
        return True
    
    success = verification_donnees_exacte()
    
    if success:
        print("\n🎉 TOUTES LES DONNÉES SONT CORRECTES!")
    else:
        print("\n❌ PROBLEME AVEC LES DONNÉES")
        
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()