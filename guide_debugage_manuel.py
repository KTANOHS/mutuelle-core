# guide_debugage_manuel.py
def guide_debugage_manuel():
    print("🛠️ GUIDE DE DÉBUGAGE MANUEL - CRÉATION MEMBRE")
    print("=" * 60)
    
    print("\n1. 🔍 VÉRIFIEZ LES LOGS EN TEMPS RÉEL:")
    print("   Terminal 1: python manage.py runserver")
    print("   Terminal 2: tail -f logs/django.log (si configuré)")
    print("   Ou surveillez la console du runserver")
    
    print("\n2. 🔐 TESTEZ LA CONNEXION:")
    print("   Allez sur: http://127.0.0.1:8000/admin/")
    print("   Essayez de vous connecter avec koffitanoh")
    print("   Si ça marche, le problème n'est pas l'authentification")
    
    print("\n3. 🧪 TESTEZ LE FORMULAIRE:")
    print("   a. Allez sur: http://127.0.0.1:8000/agents/creer-membre/")
    print("   b. Remplissez le formulaire")
    print("   c. Surveillez la console pour les erreurs")
    print("   d. Vérifiez les messages flash (alertes)")
    
    print("\n4. 🔧 SOLUTIONS COURANTES:")
    print("   Problème: Mauvais mot de passe")
    print("   Solution: Réinitialiser le mot de passe dans admin")
    print("   Commande: python manage.py changepassword koffitanoh")
    
    print("   Problème: Permissions manquantes")
    print("   Solution: Ajouter l'utilisateur au groupe 'Agents'")
    print("   Ou: python manage.py createsuperuser")
    
    print("   Problème: Erreur de validation")
    print("   Solution: Vérifier les champs obligatoires du modèle Membre")
    
    print("\n5. 📞 TEST ULTIME:")
    print("   Créez un superutilisateur:")
    print("   python manage.py createsuperuser")
    print("   Testez avec ce compte")
    
    print("=" * 60)

if __name__ == "__main__":
    guide_debugage_manuel()