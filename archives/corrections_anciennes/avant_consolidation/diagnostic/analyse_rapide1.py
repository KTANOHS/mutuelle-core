# analyse_rapide.py
import os
import django
from django.apps import apps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyse_rapide():
    print("🔍 ANALYSE RAPIDE DE L'EXISTANT")
    print("=" * 50)
    
    # Vérification des modèles clés
    modeles = ['Membre', 'Cotisation', 'Paiement', 'Bon', 'Soin']
    
    for modele in modeles:
        try:
            obj = apps.get_model('assureur', modele)
            count = obj.objects.count()
            print(f"✅ {modele}: {count} enregistrements")
        except:
            print(f"❌ {modele}: Modèle non trouvé")
    
    # Vérification Membre détaillée
    try:
        Membre = apps.get_model('assureur', 'Membre')
        if Membre.objects.exists():
            membre = Membre.objects.first()
            print(f"\n📋 EXEMPLE MEMBRE:")
            print(f"   • Nom: {membre.nom} {membre.prenom}")
            print(f"   • Contrat: {membre.type_contrat}")
            print(f"   • Couverture: {membre.taux_couverture}%")
            print(f"   • Statut: {membre.statut}")
    except:
        pass

if __name__ == "__main__":
    analyse_rapide()