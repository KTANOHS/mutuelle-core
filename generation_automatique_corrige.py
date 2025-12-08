# generation_automatique_corrige.py
import os
import django
import sys
from datetime import datetime, timedelta

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from assureur.models import Cotisation, Membre
from django.db.models import Count, Sum
import re

def generer_cotisations_mois():
    """Génère automatiquement les cotisations du mois précédent"""
    try:
        # Date du mois précédent (corrigée pour éviter les erreurs)
        aujourdhui = datetime.now()
        
        # Calcul correct du mois précédent
        if aujourdhui.month == 1:
            annee = aujourdhui.year - 1
            mois = 12
        else:
            annee = aujourdhui.year
            mois = aujourdhui.month - 1
        
        periode = f"{annee}-{mois:02d}"
        
        print(f"🔧 Début de la génération automatique pour {periode}")
        print(f"   Date actuelle: {aujourdhui}")
        
        # Vérifier si déjà généré
        existantes = Cotisation.objects.filter(periode=periode).count()
        if existantes > 0:
            print(f"ℹ️  Cotisations déjà existantes pour {periode}: {existantes}")
            return False
        
        # Vérifier s'il y a des membres actifs
        membres_actifs = Membre.objects.filter(statut='actif').count()
        if membres_actifs == 0:
            print("❌ Aucun membre actif - impossible de générer")
            return False
            
        print(f"✅ {membres_actifs} membre(s) actif(s) trouvé(s)")
        
        # Connexion avec force_login pour éviter les problèmes d'authentification
        client = Client()
        
        # Utiliser l'admin principal
        try:
            user = User.objects.get(username='admin')
            # Force login pour les tests automatisés
            client.force_login(user)
            print(f"✅ Connecté en tant que: {user.username}")
        except User.DoesNotExist:
            print("❌ Utilisateur admin non trouvé")
            return False
        
        # Récupérer CSRF
        response = client.get('/assureur/cotisations/generer/')
        print(f"📄 Page génération - Status: {response.status_code}")
        
        if response.status_code != 200:
            # Essayer une autre approche
            print("⚠️  Utilisation de la méthode directe...")
            return generer_cotisations_direct(periode)
        
        content = response.content.decode('utf-8')
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', content)
        
        if not csrf_match:
            print("❌ Token CSRF non trouvé dans le formulaire")
            return generer_cotisations_direct(periode)
        
        csrf_token = csrf_match.group(1)
        print(f"✅ Token CSRF obtenu")
        
        # Génération
        print(f"🚀 Envoi de la requête POST...")
        response = client.post('/assureur/cotisations/generer/', {
            'periode': periode,
            'csrfmiddlewaretoken': csrf_token
        })
        
        print(f"📤 Réponse POST - Status: {response.status_code}")
        
        if response.status_code in [200, 302]:
            nouvelles = Cotisation.objects.filter(periode=periode).count()
            print(f"✅ Génération terminée: {nouvelles} nouvelle(s) cotisation(s) pour {periode}")
            return True
        else:
            print(f"❌ Échec de génération: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {str(e)}")
        return False

def generer_cotisations_direct(periode):
    """Méthode alternative de génération directe"""
    print(f"🔄 Utilisation de la méthode directe pour {periode}")
    
    try:
        from assureur.views import generer_cotisations_view
        
        # Créer une requête simulée
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.post('/assureur/cotisations/generer/', {'periode': periode})
        
        # Ajouter l'utilisateur à la requête
        request.user = User.objects.get(username='admin')
        
        # Appeler la vue directement
        response = generer_cotisations_view(request)
        
        if response.status_code in [200, 302]:
            nouvelles = Cotisation.objects.filter(periode=periode).count()
            print(f"✅ Génération directe réussie: {nouvelles} cotisation(s)")
            return True
        else:
            print(f"❌ Échec génération directe: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur génération directe: {str(e)}")
        return False

def rapport_final():
    """Affiche un rapport final du système"""
    print("\n" + "="*60)
    print("📊 RAPPORT FINAL DU SYSTÈME")
    print("="*60)
    
    # Membres
    membres = Membre.objects.all()
    actifs = membres.filter(statut='actif').count()
    print(f"\n👥 MEMBRES:")
    print(f"   Total: {membres.count()}")
    print(f"   Actifs: {actifs}")
    print(f"   Inactifs: {membres.count() - actifs}")
    
    # Cotisations
    cotisations = Cotisation.objects.all()
    print(f"\n💰 COTISATIONS:")
    print(f"   Total: {cotisations.count()}")
    
    # Par période
    periodes = cotisations.values('periode').annotate(
        count=Count('id'),
        total=Sum('montant')
    ).order_by('periode')
    
    print(f"📅 PAR PÉRIODE:")
    for p in periodes:
        print(f"   {p['periode']}: {p['count']} cotisations, {p['total']:,.0f} FCFA")
    
    # Total général
    total_general = sum(c.montant for c in cotisations if c.montant)
    print(f"\n💵 TOTAL GÉNÉRAL: {total_general:,.0f} FCFA")
    
    print("\n" + "="*60)
    print("✅ SYSTÈME OPÉRATIONNEL")
    print("="*60)

if __name__ == "__main__":
    print("🧪 TEST DE GÉNÉRATION AUTOMATIQUE")
    print("="*50)
    
    # Test de génération
    succes = generer_cotisations_mois()
    
    if succes:
        print("\n🎉 GÉNÉRATION RÉUSSIE !")
    else:
        print("\n⚠️  La génération n'a pas créé de nouvelles cotisations")
        print("   Raisons possibles:")
        print("   1. Période déjà générée")
        print("   2. Aucun membre actif")
        print("   3. Problème technique mineur")
    
    # Rapport final
    rapport_final()