#!/usr/bin/env python
"""
SCRIPT DE RÉPARATION AUTOMATIQUE
Corrige les problèmes courants détectés dans le diagnostic
"""

import os
import sys
from pathlib import Path
import re

class AutoFix:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.fixes_applied = []
        self.errors = []
    
    def fix_import_require_post(self):
        """Corrige l'importation de require_POST"""
        views_path = self.project_path / 'communication' / 'views.py'
        
        if not views_path.exists():
            self.errors.append("Fichier communication/views.py introuvable")
            return False
        
        try:
            with open(views_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Recherche et corrige l'import
            if 'from django.views.decorators.csrf import csrf_exempt, require_POST' in content:
                new_content = content.replace(
                    'from django.views.decorators.csrf import csrf_exempt, require_POST',
                    'from django.views.decorators.csrf import csrf_exempt\nfrom django.views.decorators.http import require_POST'
                )
                
                with open(views_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                self.fixes_applied.append("✅ Import require_POST corrigé")
                return True
            else:
                self.fixes_applied.append("⚠ Import require_POST déjà corrigé")
                return True
                
        except Exception as e:
            self.errors.append(f"Erreur correction import: {str(e)}")
            return False
    
    def add_communication_home_view(self):
        """Ajoute la vue communication_home manquante"""
        views_path = self.project_path / 'communication' / 'views.py'
        
        if not views_path.exists():
            self.errors.append("Fichier communication/views.py introuvable")
            return False
        
        try:
            with open(views_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifie si la vue existe déjà
            if 'def communication_home' in content:
                self.fixes_applied.append("⚠ Vue communication_home existe déjà")
                return True
            
            # Ajoute la vue après les imports
            view_code = '''
def communication_home(request):
    """Page d'accueil de la communication"""
    if not request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('login')
    
    # Redirection selon le type d'utilisateur
    from core.utils import get_user_redirect_url
    try:
        redirect_url = get_user_redirect_url(request.user)
        return redirect(redirect_url)
    except Exception:
        # Fallback vers la messagerie
        return redirect('messagerie')
'''
            
            # Trouve le bon endroit pour insérer
            lines = content.split('\n')
            import_end = 0
            
            for i, line in enumerate(lines):
                if line.strip() and not line.strip().startswith(('import ', 'from ', '#')):
                    import_end = i
                    break
            
            if import_end > 0:
                lines.insert(import_end, '\n' + view_code.strip())
                new_content = '\n'.join(lines)
                
                with open(views_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                self.fixes_applied.append("✅ Vue communication_home ajoutée")
                return True
            else:
                self.errors.append("Impossible de trouver l'endroit pour insérer la vue")
                return False
                
        except Exception as e:
            self.errors.append(f"Erreur ajout vue: {str(e)}")
            return False
    
    def fix_csrf_in_login_template(self):
        """Ajoute le token CSRF dans le template de login"""
        template_path = self.project_path / 'templates' / 'registration' / 'login.html'
        
        # Crée le répertoire si nécessaire
        template_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not template_path.exists():
            # Crée un template de login basique avec CSRF
            template_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>Connexion - Mutuelle</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Connexion</h1>
    
    {% if form.errors %}
    <p style="color: red">Nom d'utilisateur ou mot de passe incorrect.</p>
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        <p>
            <label for="id_username">Nom d'utilisateur:</label>
            <input type="text" name="username" id="id_username" required>
        </p>
        <p>
            <label for="id_password">Mot de passe:</label>
            <input type="password" name="password" id="id_password" required>
        </p>
        <button type="submit">Se connecter</button>
    </form>
</body>
</html>
'''
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(template_content)
            
            self.fixes_applied.append("✅ Template login créé avec CSRF")
            return True
        else:
            # Vérifie et corrige le template existant
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if '{% csrf_token %}' not in content:
                # Essaie d'ajouter le token CSRF
                if '<form' in content and 'method="post"' in content:
                    # Ajoute après la balise form
                    new_content = content.replace('<form', '<form\n    {% csrf_token %}')
                    with open(template_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    self.fixes_applied.append("✅ Token CSRF ajouté au template login")
                else:
                    self.errors.append("Template login sans balise form method='post'")
                    return False
            else:
                self.fixes_applied.append("⚠ Token CSRF déjà présent dans login")
            
            return True
    
    def create_clear_sessions_script(self):
        """Crée un script pour nettoyer les sessions"""
        script_path = self.project_path / 'clear_sessions.py'
        
        script_content = '''#!/usr/bin/env python
"""
Script pour nettoyer les sessions expirées
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.sessions.models import Session
from django.utils import timezone

def clear_expired_sessions():
    """Supprime toutes les sessions expirées"""
    expired_count = Session.objects.filter(expire_date__lt=timezone.now()).count()
    Session.objects.filter(expire_date__lt=timezone.now()).delete()
    return expired_count

if __name__ == '__main__':
    cleared = clear_expired_sessions()
    print(f"Sessions expirées nettoyées: {cleared}")
    print("✅ Sessions nettoyées avec succès")
'''
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Rend le script exécutable (Unix)
        if os.name != 'nt':
            os.chmod(script_path, 0o755)
        
        self.fixes_applied.append("✅ Script clear_sessions.py créé")
        return True
    
    def create_test_api_script(self):
        """Crée un script de test pour l'API"""
        script_path = self.project_path / 'test_api.py'
        
        script_content = '''#!/usr/bin/env python
"""
Script de test pour l'API de messagerie
"""
import requests
import json
import sys

BASE_URL = 'http://127.0.0.1:8000'

def test_login(username, password):
    """Teste la connexion"""
    print(f"\\n🔐 Test de connexion pour {username}...")
    
    # Récupère d'abord le token CSRF
    session = requests.Session()
    response = session.get(f'{BASE_URL}/accounts/login/')
    
    # Extrait le token CSRF (simplifié)
    csrf_token = None
    if 'csrfmiddlewaretoken' in response.text:
        # Recherche simplifiée du token
        import re
        match = re.search(r"name='csrfmiddlewaretoken' value='([^']+)'", response.text)
        if match:
            csrf_token = match.group(1)
    
    if not csrf_token:
        print("⚠ Impossible de récupérer le token CSRF")
        return None
    
    # Tente la connexion
    login_data = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token
    }
    
    headers = {
        'Referer': f'{BASE_URL}/accounts/login/'
    }
    
    response = session.post(
        f'{BASE_URL}/accounts/login/',
        data=login_data,
        headers=headers,
        allow_redirects=False
    )
    
    if response.status_code == 302:
        print("✅ Connexion réussie")
        return session
    else:
        print(f"❌ Échec connexion: {response.status_code}")
        return None

def test_send_message(session, destinataire_id, message):
    """Teste l'envoi d'un message"""
    print(f"\\n📨 Test envoi message à {destinataire_id}...")
    
    # Test avec JSON
    json_data = {
        'destinataire': destinataire_id,
        'contenu': message
    }
    
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json'
    }
    
    try:
        response = session.post(
            f'{BASE_URL}/communication/envoyer-message-api/',
            json=json_data,
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
        if response.status_code == 200:
            print("✅ Message envoyé avec succès")
        else:
            print("❌ Échec envoi message")
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

def main():
    """Fonction principale"""
    print("🧪 Script de test API")
    print("=" * 40)
    
    # Demande les identifiants
    username = input("Nom d'utilisateur: ").strip()
    password = input("Mot de passe: ").strip()
    
    # Teste la connexion
    session = test_login(username, password)
    
    if session:
        # Teste l'envoi de message
        destinataire = input("\\nID du destinataire (appuyez sur Entrée pour sauter): ").strip()
        if destinataire and destinataire.isdigit():
            message = input("Message: ").strip()
            if message:
                test_send_message(session, int(destinataire), message)
            else:
                print("⚠ Message vide, test annulé")
        else:
            print("⚠ Test d'envoi annulé")
    
    print("\\n✅ Tests terminés")

if __name__ == '__main__':
    main()
'''
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        self.fixes_applied.append("✅ Script test_api.py créé")
        return True
    
    def run_all_fixes(self):
        """Exécute toutes les réparations"""
        print("🔧 LANCEMENT DES RÉPARATIONS AUTOMATIQUES")
        print("=" * 50)
        
        # Liste des réparations à appliquer
        fixes = [
            ("Correction import require_POST", self.fix_import_require_post),
            ("Ajout vue communication_home", self.add_communication_home_view),
            ("Vérification template login CSRF", self.fix_csrf_in_login_template),
            ("Création script nettoyage sessions", self.create_clear_sessions_script),
            ("Création script test API", self.create_test_api_script),
        ]
        
        for description, fix_function in fixes:
            print(f"\n🔨 {description}...")
            try:
                fix_function()
            except Exception as e:
                self.errors.append(f"Erreur lors de {description}: {str(e)}")
        
        # Affiche le rapport
        print("\n" + "=" * 50)
        print("RAPPORT DES RÉPARATIONS")
        print("=" * 50)
        
        if self.fixes_applied:
            print("\n✅ RÉPARATIONS APPLIQUÉES:")
            for fix in self.fixes_applied:
                print(f"  {fix}")
        
        if self.errors:
            print("\n❌ ERREURS RENCONTRÉES:")
            for error in self.errors:
                print(f"  {error}")
        
        # Recommandations finales
        print("\n📋 PROCHAINES ÉTAPES:")
        print("1. Exécutez: python clear_sessions.py")
        print("2. Redémarrez le serveur: python manage.py runserver")
        print("3. Testez avec: python test_api.py")
        print("4. Utilisez une session privée pour tester")
        
        return len(self.errors) == 0

def main():
    """Fonction principale"""
    # Détermine le chemin du projet
    script_dir = Path(__file__).parent
    project_path = script_dir
    
    # Vérifie que nous sommes dans le projet
    if not (project_path / 'manage.py').exists():
        project_path = Path(input("Chemin du projet Django: ")).expanduser().resolve()
    
    # Lance les réparations
    fixer = AutoFix(project_path)
    success = fixer.run_all_fixes()
    
    if success:
        print("\n✨ Toutes les réparations ont été appliquées avec succès!")
    else:
        print("\n⚠ Certaines réparations ont échoué, consultez les erreurs ci-dessus.")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()