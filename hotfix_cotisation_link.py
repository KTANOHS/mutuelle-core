# hotfix_cotisation_link.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def add_cotisation_to_verification():
    """Ajouter un lien direct entre vérification et cotisation"""
    from agents.models import VerificationCotisation
    from assureur.models import Cotisation
    
    print("🔗 AJOUT LIEN VÉRIFICATION→COTISATION")
    
    for verification in VerificationCotisation.objects.all():
        try:
            # Trouver la cotisation correspondante
            cotisation = Cotisation.objects.filter(membre=verification.membre).first()
            if cotisation:
                # Stocker la référence (solution temporaire)
                verification.observations = f"Cotisation: {cotisation.reference} - Statut: {cotisation.statut}"
                verification.save()
                print(f"✅ Lien ajouté pour {verification.membre.prenom}")
        except Exception as e:
            print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    add_cotisation_to_verification()
    print("🎯 PATCH APPLIQUÉ - Liens temporaires créés")