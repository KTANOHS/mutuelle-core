# debug_ordonnance.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from medecin.models import Ordonnance, Medecin
from membres.models import Membre

def debug_ordonnance():
    print("🔍 DÉBOGAGE ORDONNANCE")
    print("=" * 40)
    
    # Vérifier les médecins existants
    medecins = Medecin.objects.all()
    print(f"📊 Médecins trouvés: {medecins.count()}")
    for med in medecins[:3]:
        print(f"  - {med.user.username} ({med.user.get_full_name()})")
    
    # Vérifier les patients
    patients = Membre.objects.all()
    print(f"📊 Patients trouvés: {patients.count()}")
    for pat in patients[:3]:
        print(f"  - {pat.nom} {pat.prenom}")
    
    # Vérifier les ordonnances existantes
    ordonnances = Ordonnance.objects.all()
    print(f"📊 Ordonnances existantes: {ordonnances.count()}")
    for ord in ordonnances[:5]:
        print(f"  - #{ord.numero} pour {ord.patient.nom} par Dr {ord.medecin.last_name}")
    
    # Vérifier la structure du modèle Ordonnance
    print(f"\n🔧 Structure du modèle Ordonnance:")
    fields = Ordonnance._meta.get_fields()
    for field in fields:
        if hasattr(field, 'name'):
            print(f"  - {field.name} ({type(field).__name__})")

if __name__ == "__main__":
    debug_ordonnance()