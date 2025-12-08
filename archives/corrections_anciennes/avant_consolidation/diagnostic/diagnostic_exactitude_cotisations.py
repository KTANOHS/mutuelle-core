# diagnostic_exactitude_cotisations.py - VERSION CORRIGÉE
import os
import sys
import django
from pathlib import Path
from datetime import datetime, date, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from membres.models import Membre, Cotisation
from agents.models import VerificationCotisation
from django.db.models import Q, Count, Sum, Avg  # AJOUT: Import Avg manquant
from decimal import Decimal

print("🔍 DIAGNOSTIC EXACTITUDE VÉRIFICATIONS COTISATIONS")
print("=" * 60)

class DiagnosticExactitudeCotisations:
    def __init__(self):
        self.rapport = {
            'timestamp': datetime.now().isoformat(),
            'analyses': [],
            'anomalies': [],
            'recommandations': [],
            'statistiques': {}
        }
    
    def executer_diagnostic_complet(self):
        """Exécute le diagnostic complet d'exactitude"""
        print("🎯 LANCEMENT DIAGNOSTIC D'EXACTITUDE...")
        
        try:
            self.verifier_coherence_dates()
            self.verifier_montants_corrects()
            self.verifier_statuts_logiques()
            self.verifier_membres_sans_cotisations()
            self.verifier_doublons_verifications()
            self.generer_rapport_detaille()
            
            print("✅ DIAGNOSTIC D'EXACTITUDE TERMINÉ")
            
        except Exception as e:
            print(f"❌ Erreur lors du diagnostic: {str(e)}")
            self.rapport['erreur'] = str(e)
    
    def verifier_coherence_dates(self):
        """Vérifie la cohérence des dates dans les vérifications"""
        print("\n1. 📅 VÉRIFICATION COHÉRENCE DES DATES...")
        
        anomalies = []
        
        # Vérifications avec date dernier paiement dans le futur
        verifs_paiement_futur = VerificationCotisation.objects.filter(
            date_dernier_paiement__gt=date.today()
        )
        
        for verif in verifs_paiement_futur:
            anomalie = {
                'type': 'DATE_PAIEMENT_FUTUR',
                'verification_id': verif.id,
                'membre': f"{verif.membre.nom_complet} ({verif.membre.numero_unique})",
                'date_dernier_paiement': verif.date_dernier_paiement,
                'description': f"Date de dernier paiement dans le futur: {verif.date_dernier_paiement}"
            }
            anomalies.append(anomalie)
            print(f"   🔴 {verif.membre.numero_unique}: Date paiement futur {verif.date_dernier_paiement}")
        
        # Vérifications avec prochaine échéance dans le passé
        verifs_echeance_passee = VerificationCotisation.objects.filter(
            prochaine_echeance__lt=date.today()
        )
        
        for verif in verifs_echeance_passee:
            anomalie = {
                'type': 'ECHEANCE_DEPASSEE',
                'verification_id': verif.id,
                'membre': f"{verif.membre.nom_complet} ({verif.membre.numero_unique})",
                'prochaine_echeance': verif.prochaine_echeance,
                'jours_retard': (date.today() - verif.prochaine_echeance).days,
                'description': f"Échéance dépassée depuis {(date.today() - verif.prochaine_echeance).days} jours"
            }
            anomalies.append(anomalie)
            print(f"   🟡 {verif.membre.numero_unique}: Échéance dépassée depuis {(date.today() - verif.prochaine_echeance).days} jours")
        
        # Vérifications avec incohérence dates paiement/échéance
        verifs_incoherentes = VerificationCotisation.objects.filter(
            date_dernier_paiement__gt=date.today() - timedelta(days=30),
            prochaine_echeance__lt=date.today() + timedelta(days=15)
        )
        
        for verif in verifs_incoherentes:
            if verif.date_dernier_paiement and verif.prochaine_echeance:
                jours_entre = (verif.prochaine_echeance - verif.date_dernier_paiement).days
                if jours_entre < 25 or jours_entre > 35:  # Période normale: 30 jours
                    anomalie = {
                        'type': 'PERIODE_INCOHERENTE',
                        'verification_id': verif.id,
                        'membre': f"{verif.membre.nom_complet} ({verif.membre.numero_unique})",
                        'date_dernier_paiement': verif.date_dernier_paiement,
                        'prochaine_echeance': verif.prochaine_echeance,
                        'jours_entre': jours_entre,
                        'description': f"Période incohérente entre paiement et échéance: {jours_entre} jours"
                    }
                    anomalies.append(anomalie)
                    print(f"   🟠 {verif.membre.numero_unique}: Période incohérente {jours_entre} jours")
        
        self.rapport['analyses'].append({
            'categorie': 'coherence_dates',
            'anomalies': anomalies,
            'total_anomalies': len(anomalies)
        })
        
        print(f"   📊 {len(anomalies)} anomalies de dates détectées")
    
    def verifier_montants_corrects(self):
        """Vérifie l'exactitude des montants"""
        print("\n2. 💰 VÉRIFICATION EXACTITUDE DES MONTANTS...")
        
        anomalies = []
        
        # Vérifications avec montant dette négatif
        verifs_dette_negative = VerificationCotisation.objects.filter(
            montant_dette__lt=0
        )
        
        for verif in verifs_dette_negative:
            anomalie = {
                'type': 'DETTE_NEGATIVE',
                'verification_id': verif.id,
                'membre': f"{verif.membre.nom_complet} ({verif.membre.numero_unique})",
                'montant_dette': float(verif.montant_dette),
                'description': f"Montant dette négatif: {verif.montant_dette} FCFA"
            }
            anomalies.append(anomalie)
            print(f"   🔴 {verif.membre.numero_unique}: Dette négative {verif.montant_dette} FCFA")
        
        # Vérifications avec montant dernier paiement négatif
        verifs_paiement_negatif = VerificationCotisation.objects.filter(
            montant_dernier_paiement__lt=0
        )
        
        for verif in verifs_paiement_negatif:
            anomalie = {
                'type': 'PAIEMENT_NEGATIF',
                'verification_id': verif.id,
                'membre': f"{verif.membre.nom_complet} ({verif.membre.numero_unique})",
                'montant_dernier_paiement': float(verif.montant_dernier_paiement),
                'description': f"Montant dernier paiement négatif: {verif.montant_dernier_paiement} FCFA"
            }
            anomalies.append(anomalie)
            print(f"   🔴 {verif.membre.numero_unique}: Paiement négatif {verif.montant_dernier_paiement} FCFA")
        
        # Vérifications avec dette mais statut "à jour"
        verifs_incoherentes = VerificationCotisation.objects.filter(
            montant_dette__gt=0,
            statut_cotisation='a_jour'
        )
        
        for verif in verifs_incoherentes:
            anomalie = {
                'type': 'STATUT_MONTANT_INCOHERENT',
                'verification_id': verif.id,
                'membre': f"{verif.membre.nom_complet} ({verif.membre.numero_unique})",
                'statut': verif.statut_cotisation,
                'montant_dette': float(verif.montant_dette),
                'description': f"Statut 'à jour' mais dette de {verif.montant_dette} FCFA"
            }
            anomalies.append(anomalie)
            print(f"   🟡 {verif.membre.numero_unique}: Statut 'à jour' mais dette {verif.montant_dette} FCFA")
        
        self.rapport['analyses'].append({
            'categorie': 'exactitude_montants',
            'anomalies': anomalies,
            'total_anomalies': len(anomalies)
        })
        
        print(f"   📊 {len(anomalies)} anomalies de montants détectées")
    
    def verifier_statuts_logiques(self):
        """Vérifie la logique des statuts de cotisation"""
        print("\n3. 🏷️ VÉRIFICATION LOGIQUE DES STATUTS...")
        
        anomalies = []
        
        # Vérifications avec statut "à jour" mais échéance dépassée
        verifs_statut_incoherent = VerificationCotisation.objects.filter(
            statut_cotisation='a_jour',
            prochaine_echeance__lt=date.today()
        )
        
        for verif in verifs_statut_incoherent:
            jours_retard = (date.today() - verif.prochaine_echeance).days
            anomalie = {
                'type': 'STATUT_ECHEANCE_INCOHERENT',
                'verification_id': verif.id,
                'membre': f"{verif.membre.nom_complet} ({verif.membre.numero_unique})",
                'statut': verif.statut_cotisation,
                'prochaine_echeance': verif.prochaine_echeance,
                'jours_retard_reel': jours_retard,
                'jours_retard_indique': verif.jours_retard,
                'description': f"Statut 'à jour' mais échéance dépassée depuis {jours_retard} jours"
            }
            anomalies.append(anomalie)
            print(f"   🔴 {verif.membre.numero_unique}: Statut 'à jour' mais échéance dépassée (+{jours_retard}j)")
        
        # Vérifications avec jours retard incohérents
        verifs_retard_incoherent = VerificationCotisation.objects.filter(
            prochaine_echeance__isnull=False
        )
        
        for verif in verifs_retard_incoherent:
            if verif.prochaine_echeance < date.today():
                retard_reel = (date.today() - verif.prochaine_echeance).days
                if verif.jours_retard != retard_reel:
                    anomalie = {
                        'type': 'JOURS_RETARD_INCOHERENTS',
                        'verification_id': verif.id,
                        'membre': f"{verif.membre.nom_complet} ({verif.membre.numero_unique})",
                        'jours_retard_indique': verif.jours_retard,
                        'jours_retard_reel': retard_reel,
                        'prochaine_echeance': verif.prochaine_echeance,
                        'description': f"Jours retard incohérents: indiqué {verif.jours_retard}, réel {retard_reel}"
                    }
                    anomalies.append(anomalie)
                    print(f"   🟡 {verif.membre.numero_unique}: Jours retard incohérents ({verif.jours_retard} vs {retard_reel})")
        
        self.rapport['analyses'].append({
            'categorie': 'logique_statuts',
            'anomalies': anomalies,
            'total_anomalies': len(anomalies)
        })
        
        print(f"   📊 {len(anomalies)} anomalies de statuts détectées")
    
    def verifier_membres_sans_cotisations(self):
        """Vérifie les membres sans cotisations enregistrées"""
        print("\n4. 👥 VÉRIFICATION MEMBRES SANS COTISATIONS...")
        
        anomalies = []
        
        # Membres avec vérification mais sans cotisations enregistrées
        membres_avec_verif = Membre.objects.filter(
            verificationcotisation__isnull=False
        ).distinct()
        
        for membre in membres_avec_verif:
            cotisations_count = Cotisation.objects.filter(membre=membre).count()
            if cotisations_count == 0:
                verif = VerificationCotisation.objects.filter(membre=membre).first()
                anomalie = {
                    'type': 'MEMBRE_SANS_COTISATION',
                    'membre_id': membre.id,
                    'membre': f"{membre.nom_complet} ({membre.numero_unique})",
                    'verification_id': verif.id if verif else None,
                    'statut_verification': verif.statut_cotisation if verif else 'N/A',
                    'description': f"Membre avec vérification mais sans cotisations enregistrées"
                }
                anomalies.append(anomalie)
                print(f"   🟠 {membre.numero_unique}: Vérification mais 0 cotisation enregistrée")
        
        self.rapport['analyses'].append({
            'categorie': 'membres_sans_cotisations',
            'anomalies': anomalies,
            'total_anomalies': len(anomalies)
        })
        
        print(f"   📊 {len(anomalies)} membres sans cotisations détectés")
    
    def verifier_doublons_verifications(self):
        """Vérifie les doublons de vérifications"""
        print("\n5. 🔍 VÉRIFICATION DOUBLONS DE VÉRIFICATIONS...")
        
        anomalies = []
        
        # Recherche des doublons (même membre, statut similaire, dates proches)
        doublons = VerificationCotisation.objects.values(
            'membre_id', 'statut_cotisation'
        ).annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        for doublon in doublons:
            verifs = VerificationCotisation.objects.filter(
                membre_id=doublon['membre_id'],
                statut_cotisation=doublon['statut_cotisation']
            ).order_by('-date_verification')
            
            membre = verifs.first().membre
            anomalie = {
                'type': 'VERIFICATIONS_DOUBLONS',
                'membre': f"{membre.nom_complet} ({membre.numero_unique})",
                'statut': doublon['statut_cotisation'],
                'nombre_verifications': doublon['count'],
                'verifications_ids': [v.id for v in verifs],
                'description': f"{doublon['count']} vérifications avec le même statut"
            }
            anomalies.append(anomalie)
            print(f"   🟡 {membre.numero_unique}: {doublon['count']} vérifications statut '{doublon['statut_cotisation']}'")
        
        self.rapport['analyses'].append({
            'categorie': 'doublons_verifications',
            'anomalies': anomalies,
            'total_anomalies': len(anomalies)
        })
        
        print(f"   📊 {len(anomalies)} cas de doublons détectés")
    
    def generer_rapport_detaille(self):
        """Génère un rapport détaillé avec statistiques"""
        print("\n6. 📋 GÉNÉRATION RAPPORT DÉTAILLÉ...")
        
        # Statistiques globales
        total_verifications = VerificationCotisation.objects.count()
        total_membres = Membre.objects.count()
        total_cotisations = Cotisation.objects.count()
        
        # Répartition par statut
        stats_par_statut = VerificationCotisation.objects.values(
            'statut_cotisation'
        ).annotate(
            count=Count('id'),
            avg_dette=Avg('montant_dette'),
            avg_jours_retard=Avg('jours_retard')
        )
        
        # Vérifications correctes (sans anomalies détectées)
        total_anomalies = sum(analyse['total_anomalies'] for analyse in self.rapport['analyses'])
        verifications_correctes = total_verifications - total_anomalies
        
        self.rapport['statistiques'] = {
            'total_verifications': total_verifications,
            'total_membres': total_membres,
            'total_cotisations': total_cotisations,
            'total_anomalies': total_anomalies,
            'verifications_correctes': verifications_correctes,
            'taux_exactitude': round((verifications_correctes / total_verifications * 100), 2) if total_verifications > 0 else 0,
            'repartition_statuts': list(stats_par_statut)
        }
        
        # Affichage du résumé
        self._afficher_resume()
    
    def _afficher_resume(self):
        """Affiche un résumé du diagnostic"""
        stats = self.rapport['statistiques']
        
        print("\n" + "="*60)
        print("📊 RAPPORT D'EXACTITUDE DES VÉRIFICATIONS")
        print("="*60)
        
        print(f"\n📈 STATISTIQUES GLOBALES:")
        print(f"   👥 Membres dans le système: {stats['total_membres']}")
        print(f"   🔍 Vérifications de cotisation: {stats['total_verifications']}")
        print(f"   💰 Cotisations enregistrées: {stats['total_cotisations']}")
        print(f"   ✅ Vérifications correctes: {stats['verifications_correctes']}")
        print(f"   🚨 Anomalies détectées: {stats['total_anomalies']}")
        print(f"   🎯 Taux d'exactitude: {stats['taux_exactitude']}%")
        
        print(f"\n🏷️ RÉPARTITION PAR STATUT:")
        for statut in stats['repartition_statuts']:
            dette_moyenne = statut['avg_dette'] or 0
            retard_moyen = statut['avg_jours_retard'] or 0
            print(f"   • {statut['statut_cotisation']}: {statut['count']} vérifications (dette moyenne: {dette_moyenne:.2f} FCFA, retard moyen: {retard_moyen:.1f} jours)")
        
        print(f"\n🚨 SYNTHÈSE DES ANOMALIES:")
        for analyse in self.rapport['analyses']:
            if analyse['total_anomalies'] > 0:
                print(f"   • {analyse['categorie']}: {analyse['total_anomalies']} anomalies")
        
        print(f"\n💡 RECOMMANDATIONS:")
        if stats['total_anomalies'] == 0:
            print("   ✅ Toutes les vérifications sont exactes !")
        else:
            if any(analyse['categorie'] == 'coherence_dates' and analyse['total_anomalies'] > 0 for analyse in self.rapport['analyses']):
                print("   🔧 Corriger les incohérences de dates")
            if any(analyse['categorie'] == 'exactitude_montants' and analyse['total_anomalies'] > 0 for analyse in self.rapport['analyses']):
                print("   🔧 Vérifier et corriger les montants")
            if any(analyse['categorie'] == 'logique_statuts' and analyse['total_anomalies'] > 0 for analyse in self.rapport['analyses']):
                print("   🔧 Ajuster les statuts incohérents")
            if any(analyse['categorie'] == 'membres_sans_cotisations' and analyse['total_anomalies'] > 0 for analyse in self.rapport['analyses']):
                print("   🔧 Enregistrer les cotisations manquantes")
            if any(analyse['categorie'] == 'doublons_verifications' and analyse['total_anomalies'] > 0 for analyse in self.rapport['analyses']):
                print("   🔧 Nettoyer les doublons de vérifications")
        
        print("\n" + "="*60)

# Exécution
if __name__ == "__main__":
    diagnostic = DiagnosticExactitudeCotisations()
    diagnostic.executer_diagnostic_complet()