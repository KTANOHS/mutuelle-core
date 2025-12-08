# fix_ordonnance_display.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def fix_ordonnance_display():
    """Vérifier pourquoi les ordonnances ne s'affichent pas"""
    print("🔍 VÉRIFICATION AFFICHAGE ORDONNANCES...")
    
    try:
        from soins.models import Ordonnance
        from membres.models import Membre
        
        # Vérifier s'il y a des ordonnances
        ordonnances_count = Ordonnance.objects.count()
        print(f"📊 Nombre d'ordonnances en base: {ordonnances_count}")
        
        # Vérifier les données de test
        membre = Membre.objects.first()
        if membre:
            print(f"👤 Membre test: {membre.nom_complet}")
            
        # Vérifier si les ordonnances sont liées au membre
        if membre and hasattr(membre, 'ordonnances'):
            ordonnances_membre = membre.ordonnances.count()
            print(f"📋 Ordonnances du membre: {ordonnances_membre}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    fix_ordonnance_display()