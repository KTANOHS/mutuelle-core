# generation_automatique.py
import os
import django
import sys
import schedule
import time
from datetime import datetime, timedelta

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from assureur.models import Cotisation, Membre
import re

def generer_cotisations_mois():
    """Génère automatiquement les cotisations du mois précédent"""
    try:
        # Date du mois précédent
        aujourdhui = datetime.now()
        if aujourdhui.month == 1:
            mois_precedent = aujourdhui.replace(year=aujourdhui.year-1, month=12)
        else:
            mois_precedent = aujourdhui.replace(month=aujourdhui.month-1)
        
        periode = mois_precedent.strftime("%Y-%m")
        
        print(f"🔧 Début de la génération automatique pour {periode}")
        
        # Vérifier si déjà généré
        if Cotisation.objects.filter(periode=periode).exists():
            print(f"ℹ️ Cotisations déjà existantes pour {periode}")
            return
        
        # Connexion
        client = Client()
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            print("❌ Aucun superutilisateur trouvé")
            return
        
        client.login(username=user.username, password='admin123')
        
        # Récupérer CSRF
        response = client.get('/assureur/cotisations/generer/')
        if response.status_code != 200:
            print(f"❌ Page génération inaccessible: {response.status_code}")
            return
        
        content = response.content.decode('utf-8')
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', content)
        if not csrf_match:
            print("❌ Token CSRF non trouvé")
            return
        
        csrf_token = csrf_match.group(1)
        
        # Génération
        response = client.post('/assureur/cotisations/generer/', {
            'periode': periode,
            'csrfmiddlewaretoken': csrf_token
        })
        
        if response.status_code == 302:
            nouvelles = Cotisation.objects.filter(periode=periode).count()
            print(f"✅ Génération réussie: {nouvelles} cotisations créées pour {periode}")
        else:
            print(f"❌ Échec de génération: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")

def test_generation_immediate():
    """Test immédiat de la fonction de génération"""
    print("🧪 TEST DE GÉNÉRATION IMMÉDIATE")
    print("="*50)
    
    # Générer pour le mois précédent
    generer_cotisations_mois()
    
    # Vérifier
    cotisations = Cotisation.objects.all()
    print(f"\n📊 RÉCAPITULATIF FINAL:")
    print(f"   Total cotisations: {cotisations.count()}")
    
    periodes = cotisations.values('periode').annotate(
        count=Count('id'),
        total=Sum('montant')
    ).order_by('periode')
    
    for p in periodes:
        print(f"   {p['periode']}: {p['count']} cotisations, {p['total']:,.0f} FCFA")
    
    total_general = sum(c.montant for c in cotisations if c.montant)
    print(f"   💰 TOTAL GÉNÉRAL: {total_general:,.0f} FCFA")
    
    print("\n" + "="*50)
    print("TEST TERMINÉ ✅")

if __name__ == "__main__":
    # Pour planifier une exécution mensuelle (décommentez si nécessaire)
    # schedule.every().month.do(generer_cotisations_mois)
    
    # Exécution immédiate pour test
    from django.db.models import Count, Sum
    test_generation_immediate()
    
    # Pour la planification (décommentez en production)
    # print("\n⏰ Planificateur démarré. Exécution mensuelle programmée.")
    # while True:
    #     schedule.run_pending()
    #     time.sleep(3600)  # Vérifie toutes les heures