from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from assureur.models import ConfigurationAssureur, BonDeSoin
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Initialise les données de base pour l\'application assureur'
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.MIGRATE_HEADING("🚀 Initialisation de l'application assureur...")
        )
        
        # 1. Création du groupe Assureurs
        self.creer_groupe_assureurs()
        
        # 2. Configuration par défaut
        self.creer_configurations_defaut()
        
        # 3. Vérification des permissions
        self.verifier_permissions()
        
        self.stdout.write(
            self.style.SUCCESS("✅ Initialisation de l'assureur terminée avec succès!")
        )

    def creer_groupe_assureurs(self):
        """Crée le groupe Assureurs avec les permissions appropriées"""
        groupe, created = Group.objects.get_or_create(name='Assureurs')
        
        if created:
            self.stdout.write(
                self.style.SUCCESS("✅ Groupe 'Assureurs' créé")
            )
        else:
            self.stdout.write(
                self.style.WARNING("ℹ️  Groupe 'Assureurs' existe déjà")
            )
        
        # Ajouter les permissions au groupe
        content_type = ContentType.objects.get_for_model(BonDeSoin)
        permissions = Permission.objects.filter(content_type=content_type)
        
        groupe.permissions.set(permissions)
        self.stdout.write(
            self.style.SUCCESS(f"✅ {permissions.count()} permissions ajoutées au groupe Assureurs")
        )

    def creer_configurations_defaut(self):
        """Crée les configurations par défaut"""
        configurations = [
            {
                'cle': 'TAUX_REMBOURSEMENT_DEFAULT',
                'valeur': '80',
                'type_valeur': 'NUMERIQUE',
                'description': 'Taux de remboursement par défaut pour les nouveaux bons (%)',
                'categorie': 'Financier'
            },
            {
                'cle': 'DELAI_EXPIRATION_JOURS',
                'valeur': '30',
                'type_valeur': 'NUMERIQUE',
                'description': 'Délai d\'expiration par défaut des bons (en jours)',
                'categorie': 'Gestion Bons'
            },
            {
                'cle': 'NOTIFICATION_EXPIRATION',
                'valeur': 'true',
                'type_valeur': 'BOOLEEN',
                'description': 'Activer les notifications d\'expiration des bons',
                'categorie': 'Notifications'
            },
            {
                'cle': 'LIMITE_BONS_PAR_JOUR',
                'valeur': '50',
                'type_valeur': 'NUMERIQUE',
                'description': 'Nombre maximum de bons qu\'un assureur peut créer par jour',
                'categorie': 'Limites'
            }
        ]
        
        for config in configurations:
            obj, created = ConfigurationAssureur.objects.get_or_create(
                cle=config['cle'],
                defaults={
                    'valeur': config['valeur'],
                    'type_valeur': config['type_valeur'],
                    'description': config['description'],
                    'categorie': config['categorie']
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Configuration '{config['cle']}' créée")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"ℹ️  Configuration '{config['cle']}' existe déjà")
                )

    def verifier_permissions(self):
        """Vérifie que toutes les permissions nécessaires existent"""
        content_types = [
            ContentType.objects.get_for_model(BonDeSoin),
            ContentType.objects.get_for_model(ConfigurationAssureur),
        ]
        
        permissions_count = Permission.objects.filter(
            content_type__in=content_types
        ).count()
        
        self.stdout.write(
            self.style.SUCCESS(f"✅ {permissions_count} permissions vérifiées")
        )