import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import Agent
from members.models import Membre
from django.contrib.auth.models import User

def corriger_recherche_membres():
    """Corriger la vue de recherche des membres"""
    print("🔧 CORRECTION DE LA RECHERCHE MEMBRES")
    print("=====================================")
    
    # Vérifier les membres existants
    membres = Membre.objects.all()
    print(f"👤 Membres en base: {membres.count()}")
    
    for membre in membres:
        print(f"  - {membre.nom} {membre.prenom} (ID: {membre.id}, Numéro: {membre.numero_unique})")
    
    # Test de recherche simple
    from django.db.models import Q
    
    print("\n🔍 TEST DE RECHERCHE DIRECTE:")
    resultats = Membre.objects.filter(
        Q(nom__icontains='John') | 
        Q(prenom__icontains='John') |
        Q(numero_unique__icontains='MEM')
    )
    print(f"✅ Recherche 'John': {resultats.count()} résultat(s)")
    
    return True

if __name__ == "__main__":
    corriger_recherche_membres()