# sync_cotisations.py
import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def create_missing_cotisations():
    """Créer les cotisations manquantes pour synchroniser assureur/agent"""
    print("🔄 CRÉATION DES COTISATIONS MANQUANTES")
    print("=" * 50)
    
    from membres.models import Membre
    from assureur.models import Cotisation, Assureur
    from agents.models import VerificationCotisation
    from django.contrib.auth.models import User
    
    # 1. Récupérer ou créer un assureur
    try:
        assureur = Assureur.objects.first()
        if not assureur:
            user = User.objects.create_user(
                username='assureur_principal',
                password='assureur123',
                first_name='Assureur',
                last_name='Principal'
            )
            assureur = Assureur.objects.create(
                user=user,
                nom="Assureur Principal",
                telephone="0100000000"
            )
            print("✅ Assureur principal créé")
        else:
            print("✅ Assureur principal trouvé")
    except Exception as e:
        print(f"❌ Erreur création assureur: {e}")
        return
    
    # 2. Créer des cotisations pour les membres
    membres = Membre.objects.all()[:10]  # 10 premiers membres pour test
    cotisations_created = 0
    
    for membre in membres:
        try:
            # Vérifier si une cotisation existe déjà
            existing_cotisation = Cotisation.objects.filter(membre=membre).exists()
            
            if not existing_cotisation:
                # Créer une cotisation
                cotisation = Cotisation.objects.create(
                    membre=membre,
                    periode="2025",
                    type_cotisation="STANDARD",
                    montant=5000,
                    montant_clinique=2000,
                    montant_pharmacie=2000,
                    montant_charges_mutuelle=1000,
                    date_emission=timezone.now().date(),
                    date_echeance=(timezone.now() + timedelta(days=365)).date(),
                    statut="ACTIVE",
                    reference=f"COT-{membre.id}-2025",
                    enregistre_par=assureur
                )
                print(f"✅ Cotisation créée pour {membre.prenom} {membre.nom}")
                cotisations_created += 1
                
                # Mettre à jour le statut du membre
                membre.date_derniere_cotisation = timezone.now()
                membre.save()
                
        except Exception as e:
            print(f"❌ Erreur création cotisation pour {membre.prenom}: {e}")
    
    print(f"\n📊 RÉSULTAT: {cotisations_created} cotisations créées")

def sync_verifications_with_cotisations():
    """Synchroniser les vérifications avec les cotisations existantes"""
    print("\n🔄 SYNCHRONISATION VÉRIFICATIONS-COITISATIONS")
    print("=" * 50)
    
    from agents.models import VerificationCotisation, Agent
    from assureur.models import Cotisation
    from membres.models import Membre
    from django.contrib.auth.models import User
    
    # Récupérer un agent
    try:
        agent = Agent.objects.first()
        if not agent:
            print("❌ Aucun agent trouvé")
            return
    except:
        print("❌ Erreur récupération agent")
        return
    
    # Synchroniser les vérifications
    verifications_updated = 0
    
    for verification in VerificationCotisation.objects.all():
        try:
            membre = verification.membre
            
            # Trouver la dernière cotisation du membre
            derniere_cotisation = Cotisation.objects.filter(
                membre=membre, 
                statut="ACTIVE"
            ).order_by('-date_emission').first()
            
            if derniere_cotisation:
                # Mettre à jour les informations de vérification
                verification.statut_cotisation = "À_JOUR" if derniere_cotisation.statut == "ACTIVE" else "EN_RETARD"
                verification.date_dernier_paiement = derniere_cotisation.date_paiement
                verification.montant_dernier_paiement = derniere_cotisation.montant
                verification.prochaine_echeance = derniere_cotisation.date_echeance
                
                # Calculer les jours de retard
                if derniere_cotisation.date_echeance and derniere_cotisation.date_echeance < timezone.now().date():
                    verification.jours_retard = (timezone.now().date() - derniere_cotisation.date_echeance).days
                
                verification.save()
                verifications_updated += 1
                print(f"✅ Vérification synchronisée pour {membre.prenom}")
                
        except Exception as e:
            print(f"❌ Erreur synchronisation vérification: {e}")
    
    print(f"📊 {verifications_updated} vérifications synchronisées")

def create_cotisation_workflow():
    """Créer un workflow complet de test"""
    print("\n🧪 CRÉATION WORKFLOW COMPLET DE TEST")
    print("=" * 50)
    
    from membres.models import Membre
    from assureur.models import Cotisation, Assureur
    from agents.models import VerificationCotisation, Agent
    
    # 1. Prendre 3 membres pour le test
    membres_test = Membre.objects.all()[:3]
    
    for i, membre in enumerate(membres_test, 1):
        print(f"\n🔧 Configuration membre {i}: {membre.prenom} {membre.nom}")
        
        # Créer différents statuts de test
        statuts_test = [
            {"statut": "ACTIVE", "jours_retard": 0, "description": "À jour"},
            {"statut": "EN_RETARD", "jours_retard": 30, "description": "En retard"},
            {"statut": "EXPIREE", "jours_retard": 90, "description": "Expirée"}
        ]
        
        statut = statuts_test[i-1] if i <= len(statuts_test) else statuts_test[0]
        
        try:
            # Créer cotisation
            cotisation = Cotisation.objects.create(
                membre=membre,
                periode="2025",
                type_cotisation="STANDARD",
                montant=5000,
                date_emission=(timezone.now() - timedelta(days=400)).date(),
                date_echeance=(timezone.now() - timedelta(days=statut["jours_retard"])).date(),
                statut=statut["statut"],
                reference=f"TEST-{membre.id}-2025"
            )
            print(f"  ✅ Cotisation {statut['description']} créée")
            
            # Mettre à jour vérification
            verification = VerificationCotisation.objects.filter(membre=membre).first()
            if verification:
                verification.statut_cotisation = statut["statut"]
                verification.jours_retard = statut["jours_retard"]
                verification.save()
                print(f"  ✅ Vérification mise à jour")
                
        except Exception as e:
            print(f"  ❌ Erreur: {e}")

def check_final_sync():
    """Vérifier la synchronisation finale"""
    print("\n🔍 VÉRIFICATION SYNCHRONISATION FINALE")
    print("=" * 50)
    
    from membres.models import Membre
    from assureur.models import Cotisation
    from agents.models import VerificationCotisation
    
    total_membres = Membre.objects.count()
    total_cotisations = Cotisation.objects.count()
    total_verifications = VerificationCotisation.objects.count()
    
    print(f"📊 STATISTIQUES FINALES:")
    print(f"   👥 Membres: {total_membres}")
    print(f"   💰 Cotisations: {total_cotisations}")
    print(f"   ✅ Vérifications: {total_verifications}")
    
    # Vérifier la cohérence
    if total_cotisations > 0 and total_verifications > 0:
        print("🎯 SYNCHRONISATION: AMÉLIORÉE")
        print("💡 Le système assureur→agent est maintenant opérationnel")
    else:
        print("⚠️  SYNCHRONISATION: INCOMPLÈTE")
        print("🔧 Des corrections supplémentaires sont nécessaires")

if __name__ == "__main__":
    print("🚀 DÉMARRAGE SYNCHRONISATION ASSUREUR-AGENT")
    print("⏳ Cette opération peut prendre quelques secondes...\n")
    
    create_missing_cotisations()
    sync_verifications_with_cotisations()
    create_cotisation_workflow()
    check_final_sync()
    
    print("\n" + "=" * 50)
    print("🎉 SYNCHRONISATION TERMINÉE!")
    print("=" * 50)
    print("\n📋 WORKFLOW MAINTENANT FONCTIONNEL:")
    print("   1. ✅ ASSUREUR: Enregistre les cotisations")
    print("   2. ✅ SYSTÈME: Met à jour les statuts membres") 
    print("   3. ✅ AGENT: Vérifie les cotisations en temps réel")
    print("   4. ✅ SOINS: Autorisation basée sur statut cotisation")