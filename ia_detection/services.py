import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os
from django.conf import settings
from membres.models import Membre
from agents.models import VerificationCotisation
from ia_detection.models import ModeleIA, AnalyseIA
from django.utils import timezone

class ServiceDetectionFraude:
    def __init__(self):
        self.modele = None
        self.scaler = StandardScaler()
        self.charger_modele_actif()
    
    def charger_modele_actif(self):
        """Charge le modèle IA actif depuis la base"""
        try:
            modele_actif = ModeleIA.objects.filter(
                type_modele='detection_fraude',
                est_actif=True
            ).first()
            
            if modele_actif and modele_actif.fichier_modele:
                self.modele = joblib.load(modele_actif.fichier_modele.path)
                print(f"✅ Modèle IA chargé: {modele_actif.nom}")
            else:
                self.initialiser_modele_par_defaut()
                
        except Exception as e:
            print(f"❌ Erreur chargement modèle IA: {e}")
            self.initialiser_modele_par_defaut()
    
    def initialiser_modele_par_defaut(self):
        """Initialise un modèle par défaut si aucun n'existe"""
        print("🔄 Initialisation modèle IA par défaut...")
        self.modele = IsolationForest(contamination=0.1, random_state=42)
    
    def preparer_donnees_verification(self, verification):
        """Prépare les données pour l'analyse IA"""
        # Récupérer l'historique du membre
        historique = VerificationCotisation.objects.filter(membre=verification.membre)
        
        if historique.exists():
            retard_moyen = historique.aggregate(avg=Avg('jours_retard'))['avg'] or 0
            dette_moyenne = historique.aggregate(avg=Avg('montant_dette'))['avg'] or 0
        else:
            retard_moyen = 0
            dette_moyenne = 0
        
        donnees = {
            'montant_dernier_paiement': float(verification.montant_dernier_paiement or 0),
            'jours_retard': verification.jours_retard or 0,
            'montant_dette': float(verification.montant_dette or 0),
            'retard_moyen_historique': retard_moyen,
            'dette_moyenne_historique': dette_moyenne,
            'nb_verifications': historique.count(),
        }
        return pd.DataFrame([donnees])
    
    def analyser_verification(self, verification):
        """Analyse une vérification avec l'IA"""
        try:
            # Préparer les données
            donnees = self.preparer_donnees_verification(verification)
            donnees_scaled = self.scaler.fit_transform(donnees)
            
            # Prédiction
            prediction = self.modele.predict(donnees_scaled)
            score_anomalie = self.modele.decision_function(donnees_scaled)[0]
            
            # Analyser les motifs
            motifs = self.analyser_motifs_suspicion(verification, score_anomalie)
            
            # Sauvegarder le résultat
            analyse = AnalyseIA.objects.create(
                membre=verification.membre,
                verification=verification,
                type_analyse='detection_fraude',
                score_confiance=abs(score_anomalie) * 100,
                resultat={
                    'est_anomalie': prediction[0] == -1,
                    'score_anomalie': float(score_anomalie),
                    'motifs_suspicion': motifs,
                    'donnees_analyse': donnees.to_dict('records')[0]
                }
            )
            
            # Mettre à jour la vérification
            verification.score_anomalie_ia = abs(score_anomalie) * 100
            verification.motifs_suspicion = motifs
            verification.priorite_ia = self.determiner_priorite(score_anomalie, motifs)
            verification.save()
            
            return analyse
            
        except Exception as e:
            print(f"❌ Erreur analyse IA: {e}")
            return None
    
    def analyser_motifs_suspicion(self, verification, score_anomalie):
        """Analyse les motifs spécifiques de suspicion"""
        motifs = []
        
        if verification.montant_dernier_paiement and verification.montant_dernier_paiement < 10:
            motifs.append("Paiement anormalement bas")
        
        if verification.jours_retard > 30:
            motifs.append("Retard de paiement sévère")
        
        if verification.montant_dette and verification.montant_dernier_paiement:
            if verification.montant_dette > verification.montant_dernier_paiement * 5:
                motifs.append("Dette disproportionnée")
        
        if abs(score_anomalie) > 0.5:
            motifs.append("Comportement anormal détecté par IA")
        
        return motifs
    
    def determiner_priorite(self, score_anomalie, motifs):
        """Détermine la priorité basée sur le score et les motifs"""
        if score_anomalie < -0.7 or len(motifs) >= 3:
            return 'critique'
        elif score_anomalie < -0.4 or len(motifs) >= 2:
            return 'haute'
        elif score_anomalie < -0.2:
            return 'normale'
        else:
            return 'basse'

def analyser_verification_ia(verification):
    """Fonction utilitaire pour analyser une vérification avec IA"""
    service = ServiceDetectionFraude()
    return service.analyser_verification(verification)

def analyser_fraude_membre(membre):
    """Analyse toutes les vérifications d'un membre pour fraude"""
    verifications = membre.verificationcotisation_set.all()
    analyses = []
    
    for verification in verifications:
        analyse = analyser_verification_ia(verification)
        if analyse:
            analyses.append(analyse)
    
    # Mettre à jour le statut fraude du membre
    fraude_suspectee = any(
        analyse.resultat.get('est_anomalie', False) 
        for analyse in analyses
    )
    membre.fraude_suspectee = fraude_suspectee
    membre.date_derniere_analyse_ia = timezone.now()
    membre.save()
    
    return analyses
