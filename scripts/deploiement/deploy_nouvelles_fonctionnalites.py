# deploy_nouvelles_fonctionnalites.py
import os
import sys
import django
import subprocess
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(str(Path(__file__).parent.parent))

django.setup()

from django.core.management import call_command
from django.conf import settings
from django.db import connection
import shutil

class DeployeurNouvellesFonctionnalites:
    def __init__(self):
        self.etapes = []
        self.erreurs = []
    
    def executer_etape(self, description, fonction):
        """Exécute une étape avec gestion d'erreur"""
        print(f"\n🎯 {description}...")
        try:
            resultat = fonction()
            self.etapes.append(f"✅ {description}")
            return resultat
        except Exception as e:
            self.etapes.append(f"❌ {description} - ERREUR: {str(e)}")
            self.erreurs.append(str(e))
            return None
    
    def creer_structure_dossiers(self):
        """Crée la structure de dossiers pour les nouvelles apps"""
        nouveaux_dossiers = [
            'ia_detection',
            'ia_detection/migrations',
            'scoring',
            'scoring/migrations', 
            'relances',
            'relances/migrations',
            'relances/templates/emails',
            'dashboard',
            'dashboard/migrations',
            'dashboard/templatetags',
            'dashboard/templates/dashboard',
            'scripts'
        ]
        
        for dossier in nouveaux_dossiers:
            os.makedirs(dossier, exist_ok=True)
            with open(os.path.join(dossier, '__init__.py'), 'w') as f:
                f.write('')
        
        print("✅ Structure de dossiers créée")
    
    def creer_fichiers_models(self):
        """Crée les fichiers models.py pour les nouvelles apps"""
        
        # Modèle IA Detection
        modele_ia_content = '''from django.db import models
from membres.models import Membre
from agents.models import VerificationCotisation
from django.utils import timezone

class ModeleIA(models.Model):
    nom = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    type_modele = models.CharField(
        max_length=50,
        choices=[
            ('detection_fraude', 'Détection de fraude'),
            ('scoring_risque', 'Scoring de risque'),
            ('prediction_retard', 'Prédiction de retard'),
        ]
    )
    fichier_modele = models.FileField(upload_to='modeles_ia/', null=True, blank=True)
    accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    date_entrainement = models.DateTimeField(default=timezone.now)
    est_actif = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Modèle IA"
        verbose_name_plural = "Modèles IA"
    
    def __str__(self):
        return f"{self.nom} v{self.version}"

class AnalyseIA(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    verification = models.ForeignKey(VerificationCotisation, on_delete=models.CASCADE, null=True, blank=True)
    type_analyse = models.CharField(max_length=50)
    score_confiance = models.DecimalField(max_digits=5, decimal_places=2)
    resultat = models.JSONField(default=dict)
    date_analyse = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Analyse IA"
        verbose_name_plural = "Analyses IA"
        ordering = ['-date_analyse']
    
    def __str__(self):
        return f"Analyse {self.type_analyse} - {self.membre}"
'''
        
        with open('ia_detection/models.py', 'w', encoding='utf-8') as f:
            f.write(modele_ia_content)
        
        # Modèle Scoring
        modele_scoring_content = '''from django.db import models
from membres.models import Membre
from django.utils import timezone

class HistoriqueScore(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    niveau_risque = models.CharField(max_length=20)
    details_calcul = models.JSONField(default=dict)
    date_calcul = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Historique Score"
        verbose_name_plural = "Historiques Scores"
        ordering = ['-date_calcul']
    
    def __str__(self):
        return f"Score {self.score} - {self.membre}"

class RegleScoring(models.Model):
    nom = models.CharField(max_length=100)
    critere = models.CharField(max_length=200)
    poids = models.DecimalField(max_digits=4, decimal_places=2)
    est_active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Règle Scoring"
        verbose_name_plural = "Règles Scoring"
        ordering = ['-poids']
    
    def __str__(self):
        return f"{self.nom} (poids: {self.poids})"
'''
        
        with open('scoring/models.py', 'w', encoding='utf-8') as f:
            f.write(modele_scoring_content)
        
        # Modèle Relances
        modele_relances_content = '''from django.db import models
from membres.models import Membre
from django.utils import timezone

class TemplateRelance(models.Model):
    nom = models.CharField(max_length=100)
    type_relance = models.CharField(
        max_length=50,
        choices=[
            ('premier_rappel', 'Premier rappel'),
            ('relance_urgente', 'Relance urgente'),
            ('suspension_imminente', 'Suspension imminente'),
        ]
    )
    sujet = models.CharField(max_length=200)
    template_html = models.TextField()
    template_texte = models.TextField()
    delai_jours = models.IntegerField(default=7)
    
    class Meta:
        verbose_name = "Template Relance"
        verbose_name_plural = "Templates Relance"
    
    def __str__(self):
        return f"{self.nom} ({self.type_relance})"

class RelanceProgrammee(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    template = models.ForeignKey(TemplateRelance, on_delete=models.CASCADE)
    date_programmation = models.DateTimeField(default=timezone.now)
    date_envoi = models.DateTimeField(null=True, blank=True)
    envoyee = models.BooleanField(default=False)
    statut = models.CharField(
        max_length=20,
        choices=[
            ('programmee', 'Programmée'),
            ('envoyee', 'Envoyée'),
            ('erreur', 'Erreur'),
            ('annulee', 'Annulée'),
        ],
        default='programmee'
    )
    
    class Meta:
        verbose_name = "Relance Programmee"
        verbose_name_plural = "Relances Programmees"
        ordering = ['-date_programmation']
    
    def __str__(self):
        return f"Relance {self.template.nom} - {self.membre}"
'''
        
        with open('relances/models.py', 'w', encoding='utf-8') as f:
            f.write(modele_relances_content)
        
        print("✅ Fichiers models.py créés")
    
    def creer_fichiers_services(self):
        """Crée les fichiers services pour la logique métier"""
        
        # Service IA
        service_ia_content = '''import pandas as pd
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
'''
        
        with open('ia_detection/services.py', 'w', encoding='utf-8') as f:
            f.write(service_ia_content)
        
        # Service Scoring
        service_scoring_content = '''from django.db.models import Avg, Count, Sum
from membres.models import Membre
from scoring.models import HistoriqueScore, RegleScoring
from django.utils import timezone
from datetime import timedelta

class CalculateurScoreMembre:
    def __init__(self):
        self.regles = self.charger_regles_actives()
    
    def charger_regles_actives(self):
        """Charge les règles de scoring actives"""
        return RegleScoring.objects.filter(est_active=True)
    
    def calculer_score_complet(self, membre):
        """Calcule le score complet d'un membre"""
        scores_criteres = {}
        
        for regle in self.regles:
            score_critere = self.calculer_critere(regle.critere, membre)
            scores_criteres[regle.critere] = {
                'score': score_critere,
                'poids': float(regle.poids),
                'nom_regle': regle.nom
            }
        
        # Calcul du score pondéré
        score_final = sum(
            data['score'] * data['poids'] 
            for data in scores_criteres.values()
        )
        
        # Normalisation entre 0-100
        score_final = max(0, min(100, score_final * 100))
        
        resultat = {
            'score_final': round(score_final, 2),
            'details_scores': scores_criteres,
            'niveau_risque': self.determiner_niveau_risque(score_final)
        }
        
        # Sauvegarder l'historique
        HistoriqueScore.objects.create(
            membre=membre,
            score=resultat['score_final'],
            niveau_risque=resultat['niveau_risque'],
            details_calcul=resultat['details_scores']
        )
        
        return resultat
    
    def calculer_critere(self, critere, membre):
        """Calcule le score pour un critère spécifique"""
        method_name = f"calculer_{critere}"
        if hasattr(self, method_name):
            return getattr(self, method_name)(membre)
        else:
            return 0.5  # Valeur par défaut
    
    def calculer_ponctualite_paiements(self, membre):
        """Calcule la ponctualité des paiements"""
        verifications = membre.verificationcotisation_set.all()
        if not verifications.exists():
            return 0.5
        
        paiements_ponctuels = verifications.filter(jours_retard=0).count()
        return paiements_ponctuels / verifications.count()
    
    def calculer_historique_retards(self, membre):
        """Calcule l'historique des retards"""
        retard_moyen = membre.verificationcotisation_set.aggregate(
            avg_retard=Avg('jours_retard')
        )['avg_retard'] or 0
        
        return max(0, 1 - (retard_moyen / 30))
    
    def calculer_niveau_dette(self, membre):
        """Calcule le score basé sur le niveau d'endettement"""
        dette_totale = membre.verificationcotisation_set.aggregate(
            total_dette=Sum('montant_dette')
        )['total_dette'] or 0
        
        return max(0, 1 - (dette_totale / 1000))
    
    def calculer_anciennete_membre(self, membre):
        """Calcule le score basé sur l'ancienneté"""
        # Si pas de date création, retourner score neutre
        if not hasattr(membre, 'date_creation'):
            return 0.7
        
        anciennete_jours = (timezone.now() - membre.date_creation).days
        if anciennete_jours > 365:  # Plus d'un an
            return 1.0
        elif anciennete_jours > 180:  # Plus de 6 mois
            return 0.8
        elif anciennete_jours > 90:   # Plus de 3 mois
            return 0.6
        else:
            return 0.4
    
    def calculer_frequence_verifications(self, membre):
        """Calcule le score basé sur la fréquence des vérifications"""
        verifications = membre.verificationcotisation_set.all()
        total = verifications.count()
        
        if total == 0:
            return 0.5
        
        # Plus il y a de vérifications, plus c'est positif (si pas d'anomalies)
        return min(1.0, total / 10)
    
    def determiner_niveau_risque(self, score):
        """Détermine le niveau de risque basé sur le score"""
        if score >= 80:
            return "🟢 FAIBLE RISQUE"
        elif score >= 60:
            return "🟡 RISQUE MODÉRÉ"
        elif score >= 40:
            return "🟠 RISQUE ÉLEVÉ"
        else:
            return "🔴 RISQUE TRÈS ÉLEVÉ"

def recalculer_scores_automatique():
    """Fonction pour recalculer tous les scores automatiquement"""
    membres = Membre.objects.all()
    calculateur = CalculateurScoreMembre()
    compteur = 0
    
    for membre in membres:
        calculateur.calculer_score_complet(membre)
        compteur += 1
    
    print(f"✅ Scores recalculés pour {compteur} membres")
    return compteur
'''
        
        with open('scoring/calculators.py', 'w', encoding='utf-8') as f:
            f.write(service_scoring_content)
        
        print("✅ Fichiers services créés")
    
    def modifier_modeles_existants(self):
        """Modifie les modèles existants pour ajouter les nouveaux champs"""
        
        # Lecture du modèle Membre existant
        try:
            with open('membres/models.py', 'r', encoding='utf-8') as f:
                contenu_membre = f.read()
            
            # Vérifier si les nouveaux champs existent déjà
            if 'score_risque' not in contenu_membre:
                # Trouver la classe Membre et ajouter les champs avant la dernière }
                lignes = contenu_membre.split('\\n')
                nouvelle_contenu = []
                dans_classe_membre = False
                champs_ajoutes = False
                
                for ligne in lignes:
                    nouvelle_contenu.append(ligne)
                    
                    if 'class Membre' in ligne:
                        dans_classe_membre = True
                    
                    if dans_classe_membre and ligne.strip() == '}' and not champs_ajoutes:
                        # Ajouter les nouveaux champs avant la fermeture de classe
                        nouveaux_champs = '''
    # NOUVEAUX CHAMPS POUR L'IA ET SCORING
    score_risque = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=50.00,
        verbose_name="Score de risque"
    )
    date_dernier_score = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Date du dernier calcul de score"
    )
    niveau_risque = models.CharField(
        max_length=20,
        choices=[
            ('faible', '🟢 Faible risque'),
            ('modere', '🟡 Risque modéré'), 
            ('eleve', '🟠 Risque élevé'),
            ('tres_eleve', '🔴 Risque très élevé'),
        ],
        default='faible'
    )
    fraude_suspectee = models.BooleanField(
        default=False,
        verbose_name="Fraude suspectée par IA"
    )
    date_derniere_analyse_ia = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Dernière analyse IA"
    )
    
    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"
    
    def __str__(self):
        return f"{self.nom}"
'''
                        nouvelle_contenu.append(nouveaux_champs)
                        champs_ajoutes = True
                
                with open('membres/models.py', 'w', encoding='utf-8') as f:
                    f.write('\\n'.join(nouvelle_contenu))
                
                print("✅ Champs ajoutés au modèle Membre")
            else:
                print("✅ Modèle Membre déjà à jour")
                
        except Exception as e:
            print(f"❌ Erreur modification modèle Membre: {e}")
        
        # Modification du modèle VerificationCotisation
        try:
            with open('agents/models.py', 'r', encoding='utf-8') as f:
                contenu_verif = f.read()
            
            if 'score_anomalie_ia' not in contenu_verif:
                lignes = contenu_verif.split('\\n')
                nouvelle_contenu = []
                dans_classe_verif = False
                champs_ajoutes = False
                
                for ligne in lignes:
                    nouvelle_contenu.append(ligne)
                    
                    if 'class VerificationCotisation' in ligne:
                        dans_classe_verif = True
                    
                    if dans_classe_verif and ligne.strip() == '}' and not champs_ajoutes:
                        # Ajouter les nouveaux champs
                        nouveaux_champs = '''
    # NOUVEAUX CHAMPS POUR L'IA
    score_anomalie_ia = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Score d'anomalie IA"
    )
    motifs_suspicion = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Motifs de suspicion IA"
    )
    priorite_ia = models.CharField(
        max_length=20,
        choices=[
            ('basse', 'Basse priorité'),
            ('normale', 'Priorité normale'), 
            ('haute', 'Haute priorité'),
            ('critique', 'Priorité critique'),
        ],
        default='normale'
    )
    
    class Meta:
        verbose_name = "Vérification Cotisation"
        verbose_name_plural = "Vérifications Cotisations"
    
    def __str__(self):
        return f"Vérification {self.membre} - {self.agent}"
'''
                        nouvelle_contenu.append(nouveaux_champs)
                        champs_ajoutes = True
                
                with open('agents/models.py', 'w', encoding='utf-8') as f:
                    f.write('\\n'.join(nouvelle_contenu))
                
                print("✅ Champs ajoutés au modèle VerificationCotisation")
            else:
                print("✅ Modèle VerificationCotisation déjà à jour")
                
        except Exception as e:
            print(f"❌ Erreur modification modèle VerificationCotisation: {e}")
    
    def creer_fichiers_admin(self):
        """Crée les fichiers admin.py pour les nouvelles apps"""
        
        # Admin IA
        admin_ia_content = '''from django.contrib import admin
from .models import ModeleIA, AnalyseIA

@admin.register(ModeleIA)
class ModeleIAAdmin(admin.ModelAdmin):
    list_display = ['nom', 'version', 'type_modele', 'est_actif', 'date_entrainement']
    list_filter = ['type_modele', 'est_actif']
    search_fields = ['nom', 'version']
    readonly_fields = ['date_entrainement']

@admin.register(AnalyseIA)
class AnalyseIAAdmin(admin.ModelAdmin):
    list_display = ['membre', 'type_analyse', 'score_confiance', 'date_analyse']
    list_filter = ['type_analyse', 'date_analyse']
    search_fields = ['membre__nom', 'membre__email']
    readonly_fields = ['date_analyse']
    date_hierarchy = 'date_analyse'
'''
        
        with open('ia_detection/admin.py', 'w', encoding='utf-8') as f:
            f.write(admin_ia_content)
        
        # Admin Scoring
        admin_scoring_content = '''from django.contrib import admin
from .models import HistoriqueScore, RegleScoring

@admin.register(HistoriqueScore)
class HistoriqueScoreAdmin(admin.ModelAdmin):
    list_display = ['membre', 'score', 'niveau_risque', 'date_calcul']
    list_filter = ['niveau_risque', 'date_calcul']
    search_fields = ['membre__nom']
    readonly_fields = ['date_calcul']
    date_hierarchy = 'date_calcul'

@admin.register(RegleScoring)
class RegleScoringAdmin(admin.ModelAdmin):
    list_display = ['nom', 'critere', 'poids', 'est_active']
    list_filter = ['est_active']
    search_fields = ['nom', 'critere']
    list_editable = ['poids', 'est_active']
'''
        
        with open('scoring/admin.py', 'w', encoding='utf-8') as f:
            f.write(admin_scoring_content)
        
        # Admin Relances
        admin_relances_content = '''from django.contrib import admin
from .models import TemplateRelance, RelanceProgrammee

@admin.register(TemplateRelance)
class TemplateRelanceAdmin(admin.ModelAdmin):
    list_display = ['nom', 'type_relance', 'delai_jours']
    list_filter = ['type_relance']
    search_fields = ['nom', 'sujet']

@admin.register(RelanceProgrammee)
class RelanceProgrammeeAdmin(admin.ModelAdmin):
    list_display = ['membre', 'template', 'date_programmation', 'statut', 'envoyee']
    list_filter = ['statut', 'envoyee', 'date_programmation']
    search_fields = ['membre__nom']
    readonly_fields = ['date_programmation']
    date_hierarchy = 'date_programmation'
'''
        
        with open('relances/admin.py', 'w', encoding='utf-8') as f:
            f.write(admin_relances_content)
        
        print("✅ Fichiers admin.py créés")
    
    def creer_signals(self):
        """Crée les fichiers signals.py pour les actions automatiques"""
        
        # Signals Scoring
        signals_scoring_content = '''from django.db.models.signals import post_save
from django.dispatch import receiver
from membres.models import Membre
from agents.models import VerificationCotisation
from scoring.calculators import CalculateurScoreMembre
from ia_detection.services import analyser_verification_ia

@receiver(post_save, sender=VerificationCotisation)
def recalculer_score_apres_verification(sender, instance, created, **kwargs):
    """Recalcule le score après chaque nouvelle vérification"""
    try:
        if created:
            calculateur = CalculateurScoreMembre()
            calculateur.calculer_score_complet(instance.membre)
            
            # Analyser aussi avec l'IA
            analyser_verification_ia(instance)
    except Exception as e:
        print(f"❌ Erreur recalcul score: {e}")

@receiver(post_save, sender=Membre)
def initialiser_score_nouveau_membre(sender, instance, created, **kwargs):
    """Initialise le score pour un nouveau membre"""
    if created:
        try:
            calculateur = CalculateurScoreMembre()
            calculateur.calculer_score_complet(instance)
        except Exception as e:
            print(f"❌ Erreur initialisation score: {e}")
'''
        
        with open('scoring/signals.py', 'w', encoding='utf-8') as f:
            f.write(signals_scoring_content)
        
        # Signals Relances
        signals_relances_content = '''from django.db.models.signals import post_save
from django.dispatch import receiver
from membres.models import Membre
from agents.models import VerificationCotisation
from relances.services import ServiceRelances

@receiver(post_save, sender=VerificationCotisation)
def verifier_relance_apres_verification(sender, instance, created, **kwargs):
    """Vérifie si une relance est nécessaire après mise à jour vérification"""
    if created or instance.jours_retard > 0:
        try:
            service = ServiceRelances()
            service.planifier_relances_automatiques()
        except Exception as e:
            print(f"❌ Erreur vérification relances: {e}")
'''
        
        with open('relances/signals.py', 'w', encoding='utf-8') as f:
            f.write(signals_relances_content)
        
        print("✅ Fichiers signals.py créés")
    
    def creer_script_initialisation(self):
        """Crée le script d'initialisation des données"""
        
        script_content = '''from django.core.management.base import BaseCommand
from ia_detection.models import ModeleIA
from relances.models import TemplateRelance
from scoring.models import RegleScoring
from django.utils import timezone

class Command(BaseCommand):
    help = 'Initialise les données pour les nouvelles fonctionnalités IA et scoring'
    
    def handle(self, *args, **options):
        self.stdout.write('🚀 Initialisation des données des nouvelles fonctionnalités...')
        
        # Créer les templates de relance par défaut
        self.creer_templates_relance()
        
        # Créer les règles de scoring par défaut
        self.creer_regles_scoring()
        
        # Créer un modèle IA par défaut
        self.creer_modele_ia_par_defaut()
        
        self.stdout.write(
            self.style.SUCCESS('✅ Initialisation terminée avec succès!')
        )
    
    def creer_templates_relance(self):
        templates_data = [
            {
                'nom': 'Premier rappel amiable',
                'type_relance': 'premier_rappel',
                'sujet': 'Rappel de paiement de votre cotisation',
                'template_html': '<h1>Rappel de paiement</h1><p>Bonjour {{ membre.nom }},</p><p>Nous vous rappelons que votre cotisation est due.</p><p>Montant: {{ verification.montant_dette }}€</p>',
                'template_texte': 'Rappel de paiement. Bonjour {{ membre.nom }}, votre cotisation est due.',
                'delai_jours': 7
            },
            {
                'nom': 'Relance urgente',
                'type_relance': 'relance_urgente', 
                'sujet': 'URGENT - Retard de paiement important',
                'template_html': '<h1>Relance urgente</h1><p>Bonjour {{ membre.nom }},</p><p>Votre retard de paiement nécessite une action immédiate.</p>',
                'template_texte': 'URGENT - Retard de paiement important. Action requise.',
                'delai_jours': 15
            },
            {
                'nom': 'Avertissement suspension',
                'type_relance': 'suspension_imminente',
                'sujet': 'AVERTISSEMENT - Suspension de service imminente',
                'template_html': '<h1>Avertissement suspension</h1><p>Bonjour {{ membre.nom }},</p><p>Votre service risque d\\'être suspendu pour non-paiement.</p>',
                'template_texte': 'AVERTISSEMENT - Suspension imminente pour non-paiement.',
                'delai_jours': 30
            },
        ]
        
        for data in templates_data:
            obj, created = TemplateRelance.objects.get_or_create(
                type_relance=data['type_relance'],
                defaults=data
            )
            if created:
                self.stdout.write(f"✅ Template créé: {data['nom']}")
    
    def creer_regles_scoring(self):
        regles_data = [
            {'nom': 'Ponctualité paiements', 'critere': 'ponctualite_paiements', 'poids': 0.35},
            {'nom': 'Historique retards', 'critere': 'historique_retards', 'poids': 0.25},
            {'nom': 'Niveau dette', 'critere': 'niveau_dette', 'poids': 0.20},
            {'nom': 'Ancienneté membre', 'critere': 'anciennete_membre', 'poids': 0.10},
            {'nom': 'Fréquence vérifications', 'critere': 'frequence_verifications', 'poids': 0.10},
        ]
        
        for data in regles_data:
            obj, created = RegleScoring.objects.get_or_create(
                critere=data['critere'],
                defaults=data
            )
            if created:
                self.stdout.write(f"✅ Règle créée: {data['nom']}")
    
    def creer_modele_ia_par_defaut(self):
        """Crée un modèle IA par défaut"""
        if not ModeleIA.objects.filter(type_modele='detection_fraude').exists():
            ModeleIA.objects.create(
                nom='Modèle Détection Fraude Par Défaut',
                version='1.0',
                type_modele='detection_fraude',
                est_actif=True,
                date_entrainement=timezone.now()
            )
            self.stdout.write("✅ Modèle IA par défaut créé")
'''
        
        with open('scripts/initialiser_donnees.py', 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print("✅ Script d'initialisation créé")
    
    def mettre_a_jour_settings(self):
        """Met à jour le settings.py pour inclure les nouvelles apps"""
        
        try:
            with open('votre_projet/settings.py', 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Vérifier si les apps sont déjà présentes
            apps_a_ajouter = ["'ia_detection',", "'scoring',", "'relances',", "'dashboard',"]
            
            for app in apps_a_ajouter:
                if app not in contenu:
                    # Trouver INSTALLED_APPS et ajouter les nouvelles apps
                    if 'INSTALLED_APPS' in contenu:
                        # Méthode simple: ajouter à la fin de la liste
                        contenu = contenu.replace(
                            "    'dashboard',",  # Si dashboard existe déjà
                            "    'dashboard',\\n    'ia_detection',\\n    'scoring',\\n    'relances',"
                        )
            
            with open('votre_projet/settings.py', 'w', encoding='utf-8') as f:
                f.write(contenu)
            
            print("✅ Settings.py mis à jour")
            
        except Exception as e:
            print(f"⚠️  Impossible de mettre à jour settings.py automatiquement: {e}")
            print("📋 Veuillez ajouter manuellement dans settings.py:")
            print("    'ia_detection',")
            print("    'scoring',") 
            print("    'relances',")
            print("    'dashboard',")
            print("à la liste INSTALLED_APPS")
    
    def executer_migrations(self):
        """Exécute les migrations Django"""
        try:
            print("\\n📦 Création des migrations...")
            
            # Créer les migrations pour les nouvelles apps
            call_command('makemigrations', 'ia_detection')
            call_command('makemigrations', 'scoring')
            call_command('makemigrations', 'relances')
            call_command('makemigrations', 'dashboard')
            
            # Migrations pour les modèles modifiés
            call_command('makemigrations', 'membres')
            call_command('makemigrations', 'agents')
            
            print("\\n🚀 Application des migrations...")
            call_command('migrate')
            
            print("✅ Migrations exécutées avec succès")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors des migrations: {e}")
            return False
    
    def initialiser_donnees(self):
        """Initialise les données par défaut"""
        try:
            print("\\n🎯 Initialisation des données...")
            call_command('initialiser_donnees')
            print("✅ Données initialisées avec succès")
            return True
        except Exception as e:
            print(f"❌ Erreur initialisation données: {e}")
            return False
    
    def tester_integration(self):
        """Teste l'intégration des nouvelles fonctionnalités"""
        try:
            print("\\n🧪 Test de l'intégration...")
            
            from membres.models import Membre
            from scoring.calculators import CalculateurScoreMembre
            
            # Tester sur un membre existant
            membre = Membre.objects.first()
            if membre:
                calculateur = CalculateurScoreMembre()
                resultat = calculateur.calculer_score_complet(membre)
                print(f"✅ Test scoring réussi: {membre.nom} - Score: {resultat['score_final']}")
            else:
                print("⚠️  Aucun membre trouvé pour le test")
            
            print("✅ Tests d'intégration réussis")
            return True
            
        except Exception as e:
            print(f"❌ Erreur test intégration: {e}")
            return False
    
    def generer_rapport(self):
        """Génère un rapport final de déploiement"""
        print("\\n" + "="*60)
        print("📊 RAPPORT DE DÉPLOIEMENT")
        print("="*60)
        
        for etape in self.etapes:
            print(etape)
        
        if self.erreurs:
            print(f"\\n❌ {len(self.erreurs)} erreur(s) rencontrée(s):")
            for erreur in self.erreurs:
                print(f"   - {erreur}")
        else:
            print("\\n🎉 DÉPLOIEMENT RÉUSSI SANS ERREUR!")
        
        print("\\n📋 PROCHAINES ÉTAPES MANUELLES:")
        print("1. Vérifier que les nouvelles apps sont dans INSTALLED_APPS")
        print("2. Configurer les signaux dans apps.py si nécessaire")
        print("3. Tester manuellement les fonctionnalités dans l'admin")
        print("4. Planifier les tâches automatiques (Celery si utilisé)")

def main():
    """Fonction principale de déploiement"""
    deployeur = DeployeurNouvellesFonctionnalites()
    
    print("🚀 DÉPLOIEMENT DES NOUVELLES FONCTIONNALITÉS")
    print("="*50)
    
    # Exécution des étapes
    deployeur.executer_etape(
        "Création de la structure de dossiers",
        deployeur.creer_structure_dossiers
    )
    
    deployeur.executer_etape(
        "Création des fichiers models.py",
        deployeur.creer_fichiers_models
    )
    
    deployeur.executer_etape(
        "Création des fichiers services",
        deployeur.creer_fichiers_services
    )
    
    deployeur.executer_etape(
        "Modification des modèles existants", 
        deployeur.modifier_modeles_existants
    )
    
    deployeur.executer_etape(
        "Création des fichiers admin.py",
        deployeur.creer_fichiers_admin
    )
    
    deployeur.executer_etape(
        "Création des signaux automatiques",
        deployeur.creer_signals
    )
    
    deployeur.executer_etape(
        "Création du script d'initialisation",
        deployeur.creer_script_initialisation
    )
    
    deployeur.executer_etape(
        "Mise à jour des settings",
        deployeur.mettre_a_jour_settings
    )
    
    # Étapes nécessitant Django opérationnel
    if not deployeur.erreurs:
        deployeur.executer_etape(
            "Exécution des migrations",
            deployeur.executer_migrations
        )
        
        deployeur.executer_etape(
            "Initialisation des données",
            deployeur.initialiser_donnees
        )
        
        deployeur.executer_etape(
            "Test d'intégration",
            deployeur.tester_integration
        )
    
    # Rapport final
    deployeur.generer_rapport()

if __name__ == "__main__":
    main()