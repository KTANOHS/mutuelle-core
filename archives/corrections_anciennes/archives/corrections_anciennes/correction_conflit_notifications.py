# correction_conflit_notifications.py
import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def corriger_conflit_notifications():
    """Corrige le conflit de modèles Notification"""
    print("🔧 CORRECTION DU CONFLIT DE MODÈLES NOTIFICATION")
    print("=" * 60)
    
    # Option 1: Corriger notifications/models.py
    try:
        with open('notifications/models.py', 'r') as f:
            contenu = f.read()
        
        # Remplacer related_name
        contenu_corrige = contenu.replace(
            "related_name='notifications'", 
            "related_name='user_notifications'"
        )
        contenu_corrige = contenu_corrige.replace(
            "related_name='preferences_notifications'", 
            "related_name='user_preferences_notifications'"
        )
        
        with open('notifications/models.py', 'w') as f:
            f.write(contenu_corrige)
        
        print("✅ notifications/models.py corrigé")
        
    except Exception as e:
        print(f"❌ Erreur correction notifications/models.py: {e}")
        return False
    
    # Option 2: Vérifier communication/models.py
    try:
        if os.path.exists('communication/models.py'):
            with open('communication/models.py', 'r') as f:
                comm_contenu = f.read()
            
            if 'class Notification' in comm_contenu:
                print("⚠️  Modèle Notification trouvé dans communication/models.py")
                print("   ℹ️  Considérer fusionner ou supprimer un des deux modèles")
        else:
            print("✅ Aucun modèle Notification dans communication/")
            
    except Exception as e:
        print(f"⚠️  Erreur vérification communication: {e}")
    
    return True

def creer_migrations_notifications():
    """Crée les migrations pour notifications"""
    print("\n🔄 CRÉATION DES MIGRATIONS NOTIFICATIONS")
    print("=" * 50)
    
    try:
        import subprocess
        
        # Supprimer les anciennes migrations si existent
        migrations_dir = 'notifications/migrations'
        if os.path.exists(migrations_dir):
            for file in os.listdir(migrations_dir):
                if file.endswith('.py') and file != '__init__.py':
                    os.remove(os.path.join(migrations_dir, file))
                    print(f"🗑️  Migration supprimée: {file}")
        
        # Créer nouvelles migrations
        result = subprocess.run(
            ['python', 'manage.py', 'makemigrations', 'notifications'], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Migrations notifications créées")
            return True
        else:
            print("❌ Erreur création migrations notifications:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur migrations notifications: {e}")
        return False

def appliquer_migrations():
    """Applique toutes les migrations"""
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
            print("✅ Migrations appliquées avec succès")
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
        from notifications.models import Notification
        from django.contrib.auth.models import User
        
        print("✅ Modèle Notification importé sans erreur")
        
        # Vérifier que le related_name est correct
        user_field = Notification._meta.get_field('user')
        if user_field.related_name == 'user_notifications':
            print("✅ related_name corrigé: 'user_notifications'")
        else:
            print(f"❌ related_name incorrect: {user_field.related_name}")
            return False
        
        # Vérifier system check
        import subprocess
        result = subprocess.run(
            ['python', 'manage.py', 'check'], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print("✅ System check OK - Plus de conflits!")
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
    print("🔧 CORRECTION DU CONFLIT NOTIFICATIONS")
    print("=" * 60)
    
    # Étape 1: Correction du modèle
    if not corriger_conflit_notifications():
        return
    
    # Étape 2: Migrations
    if not creer_migrations_notifications():
        return
    
    # Étape 3: Application
    if not appliquer_migrations():
        return
    
    # Étape 4: Vérification
    if verifier_correction():
        print("\n🎉 CONFLIT RÉSOLU AVEC SUCCÈS!")
        print("📱 L'API mobile est maintenant opérationnelle")
    else:
        print("\n⚠️  Correction partielle - Vérification échouée")

if __name__ == "__main__":
    main()