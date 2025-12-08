# diagnostic_affichage_recherche_cotisations.py
import os
import sys
import django
from pathlib import Path
from datetime import datetime, date

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from membres.models import Membre, Cotisation
from agents.models import VerificationCotisation
from django.db.models import Q

print("🔍 DIAGNOSTIC AFFICHAGE RECHERCHE COTISATIONS")
print("=" * 60)

class DiagnosticAffichageRecherche:
    def __init__(self):
        self.rapport = {
            'timestamp': datetime.now().isoformat(),
            'problemes_affichage': [],
            'suggestions_amelioration': [],
            'exemples_corriges': []
        }
    
    def analyser_affichage_actuel(self):
        """Analyse l'affichage actuel des résultats de recherche"""
        print("🎯 ANALYSE DE L'AFFICHAGE ACTUEL...")
        
        # Simuler une recherche avec différents critères
        criteres_test = [
            {'telephone': '0710569896'},
            {'numero_unique': 'USER0014'},
            {'nom': 'Test'},
            {'statut': 'en_retard'}
        ]
        
        for critere in criteres_test:
            self.tester_recherche(critere)
    
    def tester_recherche(self, critere):
        """Teste une recherche avec un critère spécifique"""
        print(f"\n📋 TEST RECHERCHE: {critere}")
        
        queryset = Membre.objects.all()
        
        if 'telephone' in critere:
            queryset = queryset.filter(telephone__icontains=critere['telephone'])
            print(f"   🔍 Recherche par téléphone: {critere['telephone']}")
        
        elif 'numero_unique' in critere:
            queryset = queryset.filter(numero_unique__icontains=critere['numero_unique'])
            print(f"   🔍 Recherche par numéro: {critere['numero_unique']}")
        
        elif 'nom' in critere:
            queryset = queryset.filter(
                Q(nom__icontains=critere['nom']) | 
                Q(prenom__icontains=critere['nom'])
            )
            print(f"   🔍 Recherche par nom: {critere['nom']}")
        
        elif 'statut' in critere:
            # Recherche par statut de vérification
            queryset = queryset.filter(
                verificationcotisation__statut_cotisation=critere['statut']
            ).distinct()
            print(f"   🔍 Recherche par statut: {critere['statut']}")
        
        resultats = queryset[:5]  # Limiter aux 5 premiers pour l'analyse
        
        print(f"   📊 {resultats.count()} résultat(s) trouvé(s)")
        
        for membre in resultats:
            self.analyser_affichage_membre(membre)
    
    def analyser_affichage_membre(self, membre):
        """Analyse l'affichage détaillé d'un membre"""
        print(f"\n   👤 MEMBRE: {membre.nom_complet} ({membre.numero_unique})")
        
        # Récupérer la vérification la plus récente
        verification = VerificationCotisation.objects.filter(
            membre=membre
        ).order_by('-date_verification').first()
        
        # Récupérer les cotisations
        cotisations = Cotisation.objects.filter(membre=membre).order_by('-date_echeance')
        
        # Analyser les problèmes d'affichage
        problemes = self.detecter_problemes_affichage(membre, verification, cotisations)
        
        # Afficher l'état actuel
        self.afficher_etat_actuel(membre, verification, cotisations)
        
        # Afficher les problèmes détectés
        if problemes:
            for probleme in problemes:
                print(f"   🚨 PROBLÈME: {probleme}")
        
        # Proposer un affichage amélioré
        self.proposer_affichage_ameliore(membre, verification, cotisations)
    
    def detecter_problemes_affichage(self, membre, verification, cotisations):
        """Détecte les problèmes potentiels dans l'affichage"""
        problemes = []
        
        # 1. Vérification des incohérences Numéro: N/A
        if not membre.numero_unique or membre.numero_unique == 'N/A':
            problemes.append("Numéro membre affiché comme 'N/A'")
        
        # 2. Vérification du statut contradictoire
        if verification:
            if verification.statut_cotisation == 'en_retard' and verification.montant_dette == 0:
                problemes.append("Statut 'En retard' mais montant dû à 0 FCFA")
            
            if verification.statut_cotisation == 'a_jour' and verification.montant_dette > 0:
                problemes.append("Statut 'À jour' mais montant dû positif")
        
        # 3. Vérification des dates incohérentes
        if verification and verification.date_dernier_paiement:
            if verification.date_dernier_paiement > date.today():
                problemes.append("Date dernier paiement dans le futur")
            
            if verification.prochaine_echeance and verification.prochaine_echeance < date.today():
                problemes.append("Échéance dépassée mais statut potentiellement incorrect")
        
        # 4. Vérification des cotisations manquantes
        if not cotisations.exists() and verification:
            problemes.append("Vérification existe mais aucune cotisation enregistrée")
        
        return problemes
    
    def afficher_etat_actuel(self, membre, verification, cotisations):
        """Affiche l'état actuel (simulation de l'affichage problème)"""
        print(f"   📱 AFFICHAGE ACTUEL:")
        print(f"      Numéro: {membre.numero_unique or 'N/A'}")
        print(f"      Téléphone: {membre.telephone or 'Non renseigné'}")
        
        if verification:
            statut_display = "En retard" if verification.statut_cotisation == 'en_retard' else "À jour"
            print(f"      Statut: {statut_display}")
            
            # Incohérence détectée dans votre exemple
            print(f"      ✅ Le membre est à jour dans ses cotisations")
            print(f"      Dernier paiement: {verification.date_dernier_paiement.strftime('%d/%m/%Y') if verification.date_dernier_paiement else 'N/A'}")
            print(f"      Prochaine échéance: {verification.prochaine_echeance.strftime('%d/%m/%Y') if verification.prochaine_echeance else 'N/A'}")
            print(f"      Montant dû: {verification.montant_dette} FCFA")
            print(f"      Vérification ID: {verification.id} | {verification.date_verification.strftime('%d/%m/%Y %H:%M:%S')}")
        else:
            print(f"      ❌ Aucune vérification trouvée")
    
    def proposer_affichage_ameliore(self, membre, verification, cotisations):
        """Propose un affichage amélioré et cohérent"""
        print(f"   💡 AFFICHAGE AMÉLIORÉ SUGGÉRÉ:")
        print(f"      ┌────────────────────────────────────────┐")
        print(f"      │           FICHE COTISATION            │")
        print(f"      ├────────────────────────────────────────┤")
        
        # Informations membre
        print(f"      │ 👤 {membre.nom_complet}")
        print(f"      │ #️⃣  {membre.numero_unique}")
        print(f"      │ 📞 {membre.telephone or 'Non renseigné'}")
        print(f"      │ 🏷️  Catégorie: {membre.get_categorie_display()}")
        
        if verification:
            print(f"      ├────────────────────────────────────────┤")
            print(f"      │           ÉTAT DES COTISATIONS         │")
            
            # Déterminer le statut réel
            statut_reel, icone = self.determiner_statut_reel(verification)
            print(f"      │ {icone} {statut_reel}")
            
            # Détails financiers
            print(f"      ├────────────────────────────────────────┤")
            print(f"      │ 💰 Dernier paiement: {verification.date_dernier_paiement.strftime('%d/%m/%Y') if verification.date_dernier_paiement else 'Aucun'}")
            print(f"      │ 📅 Prochaine échéance: {verification.prochaine_echeance.strftime('%d/%m/%Y') if verification.prochaine_echeance else 'Non définie'}")
            
            if verification.montant_dette > 0:
                print(f"      │ 💸 Montant dû: {verification.montant_dette} FCFA")
                print(f"      │ ⏰ Jours de retard: {verification.jours_retard}")
            else:
                print(f"      │ ✅ Montant dû: 0 FCFA")
            
            # Cotisations enregistrées
            if cotisations.exists():
                cotisation_active = cotisations.first()
                print(f"      │ 📋 Cotisation active: {cotisation_active.reference}")
                print(f"      │ 💵 Montant: {cotisation_active.montant} FCFA")
            
            print(f"      │ 🔍 Vérification: #{verification.id}")
            print(f"      │ 🕐 Dernière mise à jour: {verification.date_verification.strftime('%d/%m/%Y %H:%M')}")
        
        else:
            print(f"      ├────────────────────────────────────────┤")
            print(f"      │ ⚠️  AUCUNE VÉRIFICATION DISPONIBLE     │")
            print(f"      │ Contactez un agent pour initialiser    │")
            print(f"      │ le suivi des cotisations               │")
        
        print(f"      └────────────────────────────────────────┘")
    
    def determiner_statut_reel(self, verification):
        """Détermine le statut réel basé sur tous les critères"""
        aujourdhui = date.today()
        
        # Critère 1: Montant dû
        if verification.montant_dette > 0:
            return "En retard de paiement", "🔴"
        
        # Critère 2: Échéance dépassée
        if verification.prochaine_echeance and verification.prochaine_echeance < aujourdhui:
            jours_retard = (aujourdhui - verification.prochaine_echeance).days
            return f"Échéance dépassée (+{jours_retard}j)", "🟡"
        
        # Critère 3: Proche échéance (7 jours)
        if verification.prochaine_echeance:
            jours_restants = (verification.prochaine_echeance - aujourdhui).days
            if 0 <= jours_restants <= 7:
                return f"Échéance proche ({jours_restants}j)", "🟠"
        
        # Tous les critères sont bons
        return "À jour des cotisations", "✅"
    
    def generer_recommandations(self):
        """Génère des recommandations pour améliorer l'affichage"""
        print("\n💡 RECOMMANDATIONS POUR L'AFFICHAGE:")
        
        recommandations = [
            {
                'probleme': "Incohérence statut/montant",
                'solution': "Unifier la logique de statut: vérifier montant dû + date échéance",
                'priorite': "HAUTE"
            },
            {
                'probleme': "Affichage 'N/A' pour numéro",
                'solution': "Forcer la génération de numéro unique à la création",
                'priorite': "HAUTE"
            },
            {
                'probleme': "Messages contradictoires",
                'solution': "Afficher un seul message de statut cohérent",
                'priorite': "MOYENNE"
            },
            {
                'probleme': "Manque d'information sur les cotisations",
                'solution': "Afficher les détails des cotisations actives",
                'priorite': "MOYENNE"
            },
            {
                'probleme': "Formatage incohérent",
                'solution': "Utiliser un template uniforme pour tous les résultats",
                'priorite': "BASSE"
            }
        ]
        
        for reco in recommandations:
            icone = "🔴" if reco['priorite'] == "HAUTE" else "🟡" if reco['priorite'] == "MOYENNE" else "🟢"
            print(f"   {icone} [{reco['priorite']}] {reco['probleme']}")
            print(f"      💡 {reco['solution']}")
    
    def executer_diagnostic_complet(self):
        """Exécute le diagnostic complet"""
        print("🎯 LANCEMENT DIAGNOSTIC AFFICHAGE...")
        
        try:
            self.analyser_affichage_actuel()
            self.generer_recommandations()
            
            print("\n✅ DIAGNOSTIC TERMINÉ")
            print("📋 Des scripts de correction seront proposés pour résoudre les problèmes identifiés")
            
        except Exception as e:
            print(f"❌ Erreur lors du diagnostic: {str(e)}")

# Exécution
if __name__ == "__main__":
    diagnostic = DiagnosticAffichageRecherche()
    diagnostic.executer_diagnostic_complet()