from django.core.management.base import BaseCommand
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
                'template_html': '<h1>Avertissement suspension</h1><p>Bonjour {{ membre.nom }},</p><p>Votre service risque d\'être suspendu pour non-paiement.</p>',
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
