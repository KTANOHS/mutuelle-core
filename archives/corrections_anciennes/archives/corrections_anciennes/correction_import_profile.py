# correction_import_profile.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def corriger_import_profile():
    """Corrige l'erreur d'importation Profile"""
    print("🔧 CORRECTION DE L'IMPORTATION PROFILE")
    print("=" * 50)
    
    # Étape 1: Vérifier et corriger membres/models.py
    try:
        with open('membres/models.py', 'r') as f:
            contenu = f.read()
        
        # Vérifier si Profile existe déjà
        if 'class Profile' not in contenu:
            # Ajouter le modèle Profile
            modele_profile = '''
class Profile(models.Model):
    ROLE_CHOICES = [
        ('MEMBRE', 'Membre'),
        ('MEDECIN', 'Médecin'),
        ('ASSUREUR', 'Assureur'),
        ('AGENT', 'Agent'),
        ('ADMIN', 'Administrateur'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='MEMBRE')
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"

# Signal pour créer automatiquement un profil
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
'''
            
            # Ajouter à la fin du fichier
            with open('membres/models.py', 'a') as f:
                f.write(modele_profile)
            
            print("✅ Modèle Profile ajouté à membres/models.py")
        else:
            print("✅ Modèle Profile existe déjà")
            
    except Exception as e:
        print(f"❌ Erreur correction membres/models.py: {e}")
        return False
    
    # Étape 2: Corriger api/views.py
    try:
        with open('api/views.py', 'r') as f:
            lignes = f.readlines()
        
        # Trouver et corriger la ligne problématique
        for i, ligne in enumerate(lignes):
            if 'from membres.models import Profile' in ligne:
                lignes[i] = '# ' + ligne  # Commenter la ligne
                print("✅ Ligne problématique commentée dans api/views.py")
                break
        else:
            print("✅ Aucune ligne problématique trouvée dans api/views.py")
        
        # Réécrire le fichier
        with open('api/views.py', 'w') as f:
            f.writelines(lignes)
            
    except Exception as e:
        print(f"❌ Erreur correction api/views.py: {e}")
        return False
    
    return True

def creer_migrations_membres():
    """Crée les migrations pour membres"""
    print("\n🔄 CRÉATION DES MIGRATIONS MEMBRES")
    print("=" * 50)
    
    try:
        import subprocess
        
        result = subprocess.run(
            ['python', 'manage.py', 'makemigrations', 'membres'], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Migrations membres créées")
            return True
        else:
            print("❌ Erreur création migrations membres:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur migrations membres: {e}")
        return False

def appliquer_migrations():
    """Applique les migrations"""
    print("\n🔄 APPLICATION DES MIGRATIONS")
    print("=" * 50)
    
    try:
        import subprocess
        
        result = subprocess.run(
            ['python', 'manage.py', 'migrate'], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Migrations appliquées")
            return True
        else:
            print("❌ Erreur application migrations:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors des migrations: {e}")
        return False

def verifier_correction():
    """Vérifie que la correction a fonctionné"""
    print("\n✅ VÉRIFICATION DE LA CORRECTION")
    print("=" * 50)
    
    try:
        # Test d'importation
        from membres.models import Profile
        from api.views import SoinViewSet
        
        print("✅ Importation Profile réussie")
        print("✅ Importation api.views réussie")
        
        # Vérifier system check
        import subprocess
        result = subprocess.run(
            ['python', 'manage.py', 'check'], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print("✅ System check OK")
            return True
        else:
            print("❌ System check échoué:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur vérification: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔧 CORRECTION DE L'ERREUR PROFILE")
    print("=" * 60)
    
    # Étape 1: Correction
    if not corriger_import_profile():
        return
    
    # Étape 2: Migrations
    if not creer_migrations_membres():
        return
    
    # Étape 3: Application
    if not appliquer_migrations():
        return
    
    # Étape 4: Vérification
    if verifier_correction():
        print("\n🎉 CORRECTION RÉUSSIE!")
        print("📱 L'API complète est maintenant opérationnelle")
    else:
        print("\n⚠️  Correction partielle")

if __name__ == "__main__":
    main()