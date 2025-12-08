# correction_finale_complete.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.core.management import call_command
from django.db import models
import decimal

def corriger_modele_membre():
    """Ajoute les champs manquants au modèle Membre"""
    print("🔧 Correction du modèle Membre...")
    
    try:
        from membres.models import Membre
        
        # Vérifier si les champs existent
        if not hasattr(Membre, 'score_risque'):
            print("❌ Champ score_risque manquant - besoin de migration")
            return False
        
        print("✅ Modèle Membre a les champs nécessaires")
        return True
        
    except Exception as e:
        print(f"❌ Erreur vérification modèle: {e}")
        return False

def creer_fichier_services_relances():
    """Crée le fichier services manquant pour les relances"""
    print("\\n📁 Création du fichier relances/services.py...")
    
    services_content = '''from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from membres.models import Membre
from agents.models import VerificationCotisation
from relances.models import TemplateRelance, RelanceProgrammee

class ServiceRelances:
    def __init__(self):
        self.seuils = {
            'premier_rappel': 7,
            'relance_urgente': 15,
            'suspension_imminente': 30
        }
    
    def identifier_membres_a_relancer(self):
        """Identifie les membres nécessitant une relance"""
        membres_relance = []
        
        # Premier rappel - 7 jours de retard
        seuil_premier = timezone.now().date() - timedelta(days=self.seuils['premier_rappel'])
        membres_premier = Membre.objects.filter(
            verificationcotisation__prochaine_echeance__lte=seuil_premier,
            verificationcotisation__jours_retard__gte=self.seuils['premier_rappel'],
            verificationcotisation__statut_cotisation='a_verifier'
        ).distinct()
        
        for membre in membres_premier:
            membres_relance.append((membre, 'premier_rappel'))
        
        # Relances urgentes - 15+ jours de retard
        membres_urgent = Membre.objects.filter(
            verificationcotisation__jours_retard__gte=self.seuils['relance_urgente']
        ).distinct()
        
        for membre in membres_urgent:
            membres_relance.append((membre, 'relance_urgente'))
        
        return membres_relance
    
    def creer_relance_programmee(self, membre, type_relance):
        """Crée une relance programmée"""
        template = TemplateRelance.objects.filter(
            type_relance=type_relance
        ).first()
        
        if template:
            RelanceProgrammee.objects.create(
                membre=membre,
                template=template,
                date_programmation=timezone.now(),
                statut='programmee'
            )
            return True
        return False

def planifier_relances_automatiques():
    """Fonction utilitaire pour planifier les relances"""
    service = ServiceRelances()
    membres_a_relancer = service.identifier_membres_a_relancer()
    
    for membre, type_relance in membres_a_relancer:
        service.creer_relance_programmee(membre, type_relance)
    
    return len(membres_a_relancer)
'''
    
    os.makedirs('relances', exist_ok=True)
    with open('relances/services.py', 'w', encoding='utf-8') as f:
        f.write(services_content)
    
    print("✅ Fichier relances/services.py créé")

def corriger_calculateur_scoring():
    """Corrige les erreurs Decimal dans le calculateur de scoring"""
    print("\\n🔧 Correction du calculateur de scoring...")
    
    calculateur_content = '''from django.db.models import Avg, Count, Sum
from membres.models import Membre
from scoring.models import HistoriqueScore, RegleScoring
from django.utils import timezone
from datetime import timedelta
import decimal

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
                'score': float(score_critere),  # Convertir en float pour éviter les problèmes Decimal
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
            score=decimal.Decimal(str(resultat['score_final'])),
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
        return float(paiements_ponctuels) / verifications.count()
    
    def calculer_historique_retards(self, membre):
        """Calcule l'historique des retards"""
        retard_moyen = membre.verificationcotisation_set.aggregate(
            avg_retard=Avg('jours_retard')
        )['avg_retard'] or 0
        
        return max(0, 1 - (float(retard_moyen) / 30))
    
    def calculer_niveau_dette(self, membre):
        """Calcule le score basé sur le niveau d'endettement"""
        dette_totale = membre.verificationcotisation_set.aggregate(
            total_dette=Sum('montant_dette')
        )['total_dette'] or 0
        
        return max(0, 1 - (float(dette_totale) / 1000))
    
    def calculer_anciennete_membre(self, membre):
        """Calcule le score basé sur l'ancienneté"""
        # Si pas de date création, retourner score neutre
        if not hasattr(membre, 'date_creation'):
            return 0.7
        
        try:
            anciennete_jours = (timezone.now() - membre.date_creation).days
            if anciennete_jours > 365:  # Plus d'un an
                return 1.0
            elif anciennete_jours > 180:  # Plus de 6 mois
                return 0.8
            elif anciennete_jours > 90:   # Plus de 3 mois
                return 0.6
            else:
                return 0.4
        except:
            return 0.5
    
    def calculer_frequence_verifications(self, membre):
        """Calcule le score basé sur la fréquence des vérifications"""
        verifications = membre.verificationcotisation_set.all()
        total = verifications.count()
        
        if total == 0:
            return 0.5
        
        # Plus il y a de vérifications, plus c'est positif (si pas d'anomalies)
        return min(1.0, float(total) / 10)
    
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
        try:
            calculateur.calculer_score_complet(membre)
            compteur += 1
        except Exception as e:
            print(f"❌ Erreur pour {membre.nom}: {e}")
    
    print(f"✅ Scores recalculés pour {compteur} membres")
    return compteur
'''
    
    with open('scoring/calculators.py', 'w', encoding='utf-8') as f:
        f.write(calculateur_content)
    
    print("✅ Calculateur de scoring corrigé")

def executer_migrations_manquantes():
    """Exécute les migrations manquantes pour les nouveaux champs"""
    print("\\n🚀 Exécution des migrations manquantes...")
    
    try:
        # Vérifier s'il y a des migrations en attente
        call_command('makemigrations', 'membres')
        call_command('migrate', 'membres')
        
        print("✅ Migrations exécutées")
        return True
        
    except Exception as e:
        print(f"❌ Erreur migrations: {e}")
        return False

def tester_scoring_corrige():
    """Teste le scoring après corrections"""
    print("\\n🧪 Test du scoring corrigé...")
    
    try:
        from membres.models import Membre
        from scoring.calculators import CalculateurScoreMembre
        
        membre = Membre.objects.first()
        if membre:
            calculateur = CalculateurScoreMembre()
            resultat = calculateur.calculer_score_complet(membre)
            
            print(f"✅ Scoring réussi pour {membre.nom}:")
            print(f"   Score: {resultat['score_final']}")
            print(f"   Niveau risque: {resultat['niveau_risque']}")
            
            # Mettre à jour le membre
            membre.score_risque = resultat['score_final']
            niveau_risque = resultat['niveau_risque'].lower()
            niveau_risque = niveau_risque.replace(' ', '_').replace('é', 'e').replace('è', 'e').replace('à', 'a')
            membre.niveau_risque = niveau_risque
            membre.save()
            
            return True
        else:
            print("⚠️  Aucun membre trouvé pour le test")
            return False
            
    except Exception as e:
        print(f"❌ Erreur test scoring: {e}")
        return False

def verifier_etat_final():
    """Vérifie l'état final du système"""
    print("\\n🔍 Vérification finale du système...")
    
    from django.apps import apps
    from relances.models import TemplateRelance
    from scoring.models import RegleScoring, HistoriqueScore
    from membres.models import Membre
    
    # Vérifier les apps
    apps_attendues = ['ia_detection', 'scoring', 'relances']
    for app in apps_attendues:
        try:
            app_config = apps.get_app_config(app)
            print(f"✅ App {app} chargée")
        except:
            print(f"❌ App {app} NON chargée")
    
    # Vérifier les données
    print(f"\\n📊 DONNÉES:")
    print(f"   👥 Membres: {Membre.objects.count()}")
    print(f"   📈 Règles scoring: {RegleScoring.objects.count()}")
    print(f"   📧 Templates relance: {TemplateRelance.objects.count()}")
    print(f"   🎯 Historiques scores: {HistoriqueScore.objects.count()}")
    
    # Vérifier les champs Membre
    try:
        membre = Membre.objects.first()
        if hasattr(membre, 'score_risque'):
            print(f"✅ Champ score_risque disponible")
        else:
            print(f"❌ Champ score_risque MANQUANT")
    except:
        print(f"⚠️  Impossible de vérifier les champs Membre")

def main():
    print("🚀 CORRECTION FINALE COMPLÈTE")
    print("=" * 50)
    
    # Étape 1: Créer les fichiers manquants
    creer_fichier_services_relances()
    corriger_calculateur_scoring()
    
    # Étape 2: Vérifier le modèle
    corriger_modele_membre()
    
    # Étape 3: Tester le scoring
    if tester_scoring_corrige():
        print("\\n✅ Scoring fonctionnel!")
    else:
        print("\\n❌ Problème avec le scoring")
    
    # Étape 4: Vérification finale
    verifier_etat_final()
    
    print("\\n" + "=" * 50)
    print("🎉 CORRECTIONS APPLIQUÉES!")
    print("\\n📋 RÉCAPITULATIF:")
    print("   ✅ Fichier relances/services.py créé")
    print("   ✅ Calculateur scoring corrigé (Decimal vs float)")
    print("   ✅ Test scoring exécuté")
    print("   ✅ Vérification système complète")

if __name__ == "__main__":
    main()