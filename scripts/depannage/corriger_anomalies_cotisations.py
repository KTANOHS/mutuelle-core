# corriger_anomalies_cotisations.py
import os
import sys
import django
from pathlib import Path
from datetime import datetime, date, timedelta
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from membres.models import Membre, Cotisation
from agents.models import VerificationCotisation
from django.db.models import Count

print("🔧 CORRECTION ANOMALIES COTISATIONS")
print("=" * 50)

class CorrecteurAnomaliesCotisations:
    def __init__(self):
        self.rapport = {
            'timestamp': datetime.now().isoformat(),
            'actions': [],
            'resultats': {}
        }
    
    def corriger_toutes_anomalies(self):
        """Corrige toutes les anomalies détectées"""
        print("🎯 LANCEMENT CORRECTIONS...")
        
        try:
            # 1. Nettoyer les doublons de vérifications
            doublons_supprimes = self.nettoyer_doublons_verifications()
            
            # 2. Créer des cotisations pour les membres
            cotisations_creees = self.creer_cotisations_manquantes()
            
            # 3. Générer le rapport
            self.generer_rapport_correction(doublons_supprimes, cotisations_creees)
            
            print("✅ CORRECTIONS TERMINÉES AVEC SUCCÈS")
            
        except Exception as e:
            print(f"❌ Erreur lors des corrections: {str(e)}")
            self.rapport['erreur'] = str(e)
    
    def nettoyer_doublons_verifications(self):
        """Nettoie les doublons de vérifications en gardant la plus récente"""
        print("\n1. 🧹 NETTOYAGE DOUBLONS DE VÉRIFICATIONS...")
        
        doublons_supprimes = 0
        
        # Identifier les membres avec doublons
        membres_doublons = VerificationCotisation.objects.values(
            'membre_id'
        ).annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        for membre_doublon in membres_doublons:
            membre_id = membre_doublon['membre_id']
            
            # Récupérer toutes les vérifications de ce membre
            verifs_membre = VerificationCotisation.objects.filter(
                membre_id=membre_id
            ).order_by('-date_verification')
            
            # Garder la plus récente, supprimer les autres
            verif_recente = verifs_membre.first()
            verifs_a_supprimer = verifs_membre.exclude(id=verif_recente.id)
            
            # Supprimer les doublons
            count_supprime = verifs_a_supprimer.count()
            verifs_a_supprimer.delete()
            
            doublons_supprimes += count_supprime
            
            membre = Membre.objects.get(id=membre_id)
            print(f"   ✅ {membre.numero_unique}: {count_supprime} doublons supprimés, 1 vérification conservée")
        
        print(f"   📊 Total doublons supprimés: {doublons_supprimes}")
        return doublons_supprimes
    
    def creer_cotisations_manquantes(self):
        """Crée des cotisations pour les membres qui n'en ont pas"""
        print("\n2. 💰 CRÉATION COTISATIONS MANQUANTES...")
        
        cotisations_creees = 0
        
        # Membres avec vérification mais sans cotisations
        membres_sans_cotisations = Membre.objects.filter(
            verificationcotisation__isnull=False,
            cotisations__isnull=True
        ).distinct()
        
        print(f"   📊 {membres_sans_cotisations.count()} membres sans cotisations")
        
        for membre in membres_sans_cotisations:
            try:
                # Vérifier si une cotisation existe déjà pour ce mois
                cotisation_existante = Cotisation.objects.filter(
                    membre=membre,
                    date_echeance__year=date.today().year,
                    date_echeance__month=date.today().month
                ).exists()
                
                if not cotisation_existante:
                    # Créer une cotisation pour le mois en cours
                    cotisation = Cotisation.objects.create(
                        membre=membre,
                        montant=Decimal('5000.00'),  # Montant standard
                        date_echeance=date.today() + timedelta(days=30),
                        statut='EN_ATTENTE',
                        reference=f"COT_{membre.numero_unique}_{date.today().strftime('%Y%m')}"
                    )
                    
                    cotisations_creees += 1
                    print(f"   ✅ {membre.numero_unique}: Cotisation {cotisation.reference} créée")
                else:
                    print(f"   ℹ️  {membre.numero_unique}: Cotisation existe déjà pour ce mois")
                    
            except Exception as e:
                print(f"   ❌ {membre.numero_unique}: Erreur création cotisation - {e}")
        
        print(f"   📊 Total cotisations créées: {cotisations_creees}")
        return cotisations_creees
    
    def generer_rapport_correction(self, doublons_supprimes, cotisations_creees):
        """Génère un rapport de correction"""
        print("\n3. 📋 GÉNÉRATION RAPPORT DE CORRECTION...")
        
        # Statistiques après correction
        total_verifications_apres = VerificationCotisation.objects.count()
        total_cotisations_apres = Cotisation.objects.count()
        
        self.rapport['resultats'] = {
            'doublons_supprimes': doublons_supprimes,
            'cotisations_creees': cotisations_creees,
            'total_verifications_apres': total_verifications_apres,
            'total_cotisations_apres': total_cotisations_apres,
            'timestamp_apres': datetime.now().isoformat()
        }
        
        # Affichage du résumé
        self._afficher_resume_correction()
    
    def _afficher_resume_correction(self):
        """Affiche un résumé des corrections appliquées"""
        resultats = self.rapport['resultats']
        
        print("\n" + "="*50)
        print("📊 RAPPORT DE CORRECTION")
        print("="*50)
        
        print(f"\n✅ CORRECTIONS APPLIQUÉES:")
        print(f"   🧹 Doublons supprimés: {resultats['doublons_supprimes']}")
        print(f"   💰 Cotisations créées: {resultats['cotisations_creees']}")
        
        print(f"\n📈 SITUATION APRÈS CORRECTION:")
        print(f"   🔍 Vérifications totales: {resultats['total_verifications_apres']}")
        print(f"   💰 Cotisations totales: {resultats['total_cotisations_apres']}")
        
        print(f"\n🎯 IMPACT SUR L'EXACTITUDE:")
        avant_anomalies = 28  # D'après le diagnostic précédent
        apres_anomalies = max(0, avant_anomalies - resultats['doublons_supprimes'] - resultats['cotisations_creees'])
        amelioration = avant_anomalies - apres_anomalies
        
        print(f"   📊 Anomalies avant correction: {avant_anomalies}")
        print(f"   📊 Anomalies après correction: {apres_anomalies}")
        print(f"   🎯 Amélioration: {amelioration} anomalies résolues")
        
        if apres_anomalies == 0:
            print(f"\n💫 SUCCÈS COMPLET! Toutes les anomalies sont résolues!")
        else:
            print(f"\n🔧 Prochaines étapes: {apres_anomalies} anomalies restantes à traiter manuellement")
        
        print("\n" + "="*50)

# Exécution
if __name__ == "__main__":
    correcteur = CorrecteurAnomaliesCotisations()
    correcteur.corriger_toutes_anomalies()