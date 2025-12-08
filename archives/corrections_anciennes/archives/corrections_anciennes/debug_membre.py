from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from membres.models import Membre

class Command(BaseCommand):
    help = 'Debug de la création de membre'

    def handle(self, *args, **options):
        self.stdout.write("🔍 DEBUG CRÉATION MEMBRE")
        self.stdout.write("========================================")
        
        # Création d'un utilisateur de test
        test_user, created = User.objects.get_or_create(
            username='debug_test',
            defaults={
                'first_name': 'Debug',
                'last_name': 'Test',
                'email': 'debug@test.com'
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"✅ Utilisateur créé: {test_user.username}")
            )
            self.stdout.write(f"   First name: '{test_user.first_name}'")
            self.stdout.write(f"   Last name: '{test_user.last_name}'")
            self.stdout.write(f"   Full name: {test_user.get_full_name()}")
        else:
            self.stdout.write(f"✅ Utilisateur existant: {test_user.username}")
        
        # Tentative de création du membre avec les champs obligatoires
        self.stdout.write("\n🔄 Tentative de création Membre...")
        try:
            membre = Membre.objects.create(
                user=test_user,
                nom=test_user.last_name,      # Champ obligatoire
                prenom=test_user.first_name   # Champ obligatoire
            )
            self.stdout.write(
                self.style.SUCCESS(f"✅ Membre créé avec succès: {membre.numero_unique}")
            )
            self.stdout.write(f"   Nom: {membre.nom}")
            self.stdout.write(f"   Prénom: {membre.prenom}")
            self.stdout.write(f"   Statut: {membre.get_statut_display()}")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Erreur création Membre: {e}")
            )
            self.stdout.write(f"   Type d'erreur: {type(e).__name__}")
            self.stdout.write("\n📋 Stack trace complète:")
            import traceback
            self.stdout.write(traceback.format_exc())
        
        self.stdout.write("\n========================================")
        self.stdout.write("🔍 DEBUG TERMINÉ")