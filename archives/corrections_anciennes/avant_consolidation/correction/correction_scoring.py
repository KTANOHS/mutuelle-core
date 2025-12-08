# correction_scoring.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from scoring.models import RegleScoring, HistoriqueScore
from agents.models import VerificationCotisation
from django.db.models import Avg, Count, Sum
from django.utils import timezone
from datetime import timedelta

def corriger_regles_scoring():
    """Corrige et vérifie les règles de scoring"""
    print("🔧 Correction des règles de scoring...")
    
    # Supprimer les règles existantes et recréer
    RegleScoring.objects.all().delete()
    
    regles_data = [
        {'nom': 'Ponctualité paiements', 'critere': 'ponctualite_paiements', 'poids': 0.35},
        {'nom': 'Historique retards', 'critere': 'historique_retards', 'poids': 0.25},
        {'nom': 'Niveau dette', 'critere': 'niveau_dette', 'poids': 0.20},
        {'nom': 'Ancienneté membre', 'critere': 'anciennete_membre', 'poids': 0.10},
        {'nom': 'Fréquence vérifications', 'critere': 'frequence_verifications', 'poids': 0.10},
    ]
    
    for data in regles_data:
        RegleScoring.objects.create(**data)
        print(f"✅ Règle créée: {data['nom']}")

def calculer_scores_tous_membres():
    """Recalcule les scores pour tous les membres"""
    print("\\n🎯 Calcul des scores pour tous les membres...")
    
    from scoring.calculators import CalculateurScoreMembre
    calculateur = CalculateurScoreMembre()
    
    membres = Membre.objects.all()
    compteur = 0
    
    for membre in membres:
        try:
            resultat = calculateur.calculer_score_complet(membre)
            
            # Mettre à jour le membre
            membre.score_risque = resultat['score_final']
            niveau_risque = resultat['niveau_risque'].lower()
            niveau_risque = niveau_risque.replace(' ', '_').replace('é', 'e').replace('è', 'e').replace('à', 'a')
            membre.niveau_risque = niveau_risque
            membre.save()
            
            compteur += 1
            print(f"✅ {membre.nom}: {resultat['score_final']} ({resultat['niveau_risque']})")
            
        except Exception as e:
            print(f"❌ Erreur pour {membre.nom}: {e}")
    
    print(f"\\n📊 {compteur} membres mis à jour")

def verifier_donnees_scoring():
    """Vérifie les données nécessaires au scoring"""
    print("\\n🔍 Vérification des données...")
    
    # Vérifier les vérifications existantes
    total_verifications = VerificationCotisation.objects.count()
    print(f"📋 Vérifications totales: {total_verifications}")
    
    # Vérifier les données par membre
    for membre in Membre.objects.all()[:5]:  # Premiers 5 membres
        verifs = VerificationCotisation.objects.filter(membre=membre)
        print(f"👤 {membre.nom}: {verifs.count()} vérifications")
        
        if verifs.exists():
            stats = verifs.aggregate(
                avg_retard=Avg('jours_retard'),
                total_dette=Sum('montant_dette'),
                ponctuels=Count('id', filter=models.Q(jours_retard=0))
            )
            print(f"   📊 Retard moyen: {stats['avg_retard']}")
            print(f"   💰 Dette totale: {stats['total_dette']}")
            print(f"   ✅ Paiements ponctuels: {stats['ponctuels']}")

def initialiser_templates_relance():
    """Initialise les templates de relance"""
    print("\\n📧 Initialisation des templates de relance...")
    
    from relances.models import TemplateRelance
    
    # Supprimer les templates existants
    TemplateRelance.objects.all().delete()
    
    templates_data = [
        {
            'nom': 'Premier rappel amiable',
            'type_relance': 'premier_rappel',
            'sujet': 'Rappel de paiement de votre cotisation',
            'template_html': '<h1>Rappel de paiement</h1><p>Bonjour {{ membre.nom }},</p><p>Nous vous rappelons que votre cotisation est due.</p><p>Montant dû: {{ verification.montant_dette }}€</p>',
            'template_texte': 'Rappel de paiement. Bonjour {{ membre.nom }}, votre cotisation est due. Montant: {{ verification.montant_dette }}€',
            'delai_jours': 7
        },
        {
            'nom': 'Relance urgente', 
            'type_relance': 'relance_urgente',
            'sujet': 'URGENT - Retard de paiement important',
            'template_html': '<h1>Relance urgente</h1><p>Bonjour {{ membre.nom }},</p><p>Votre retard de paiement nécessite une action immédiate.</p><p>Jours de retard: {{ verification.jours_retard }}</p>',
            'template_texte': 'URGENT - Retard de paiement important. Jours de retard: {{ verification.jours_retard }}. Action requise.',
            'delai_jours': 15
        },
    ]
    
    for data in templates_data:
        TemplateRelance.objects.create(**data)
        print(f"✅ Template créé: {data['nom']}")

if __name__ == "__main__":
    from django.db import models
    
    print("🚀 CORRECTION DU SYSTÈME DE SCORING")
    print("=" * 50)
    
    # Exécuter les corrections
    corriger_regles_scoring()
    initialiser_templates_relance()
    verifier_donnees_scoring()
    calculer_scores_tous_membres()
    
    print("\\n" + "=" * 50)
    print("🎉 CORRECTION TERMINÉE AVEC SUCCÈS!")