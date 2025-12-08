#!/usr/bin/env python
"""
Script de correction pour l'application Assureur - Version adaptée
Exécutez: python correction_assureur_final.py
"""

import os
import sys
import django
from pathlib import Path

# Chercher le répertoire du projet
def trouver_projet():
    """Trouve le répertoire du projet Django"""
    # Chercher manage.py dans les répertoires parents
    current = Path(__file__).resolve().parent
    for _ in range(5):  # Chercher jusqu'à 5 niveaux au-dessus
        if (current / 'manage.py').exists():
            return current
        current = current.parent
    # Si non trouvé, utiliser le répertoire courant
    return Path.cwd()

# Définir le chemin du projet
PROJECT_DIR = trouver_projet()
print(f"📁 Répertoire du projet détecté: {PROJECT_DIR}")

# Ajouter au chemin Python
sys.path.insert(0, str(PROJECT_DIR))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')

try:
    django.setup()
    print("✅ Django configuré avec succès")
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    # Essayer avec un autre nom de settings
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
        django.setup()
        print("✅ Django configuré avec le nom alternatif")
    except:
        print("❌ Impossible de configurer Django")
        sys.exit(1)

from django.contrib.auth.models import User

class CorrectionAssureur:
    """Classe pour corriger tous les problèmes d'assureur"""
    
    def __init__(self):
        self.project_dir = PROJECT_DIR
        self.corrections_appliquees = []
        self.erreurs = []
        
    def print_header(self, title):
        """Affiche un en-tête"""
        print(f"\n{'='*60}")
        print(f" {title}")
        print(f"{'='*60}")
    
    def trouver_app_assureur(self):
        """Trouve le chemin de l'application assureur"""
        # Chercher dans plusieurs emplacements possibles
        locations = [
            self.project_dir / 'assureur',
            self.project_dir / 'apps' / 'assureur',
            self.project_dir / 'assureur' / 'assureur',
        ]
        
        for location in locations:
            if location.exists() and (location / 'models.py').exists():
                print(f"✅ Application assureur trouvée: {location}")
                return location
        
        # Si non trouvé, chercher par import
        try:
            import assureur
            app_path = Path(assureur.__file__).parent
            print(f"✅ Application assureur trouvée via import: {app_path}")
            return app_path
        except ImportError:
            # Chercher dans INSTALLED_APPS
            from django.conf import settings
            for app in settings.INSTALLED_APPS:
                if 'assureur' in app:
                    try:
                        app_module = __import__(app)
                        app_path = Path(app_module.__file__).parent
                        print(f"✅ Application assureur trouvée dans INSTALLED_APPS: {app_path}")
                        return app_path
                    except:
                        continue
        
        print("❌ Application assureur non trouvée")
        return None
    
    def etape_1_verifier_relations(self):
        """Vérifie les relations entre User et Assureur"""
        self.print_header("ÉTAPE 1: Vérification des relations")
        
        try:
            users = User.objects.all()
            print(f"Total utilisateurs: {users.count()}")
            
            # Vérifier la relation
            users_avec_assureur = []
            for user in users:
                if hasattr(user, 'assureur_profile'):
                    users_avec_assureur.append(user)
            
            print(f"Utilisateurs avec assureur_profile: {len(users_avec_assureur)}")
            
            for user in users_avec_assureur[:5]:
                assureur = user.assureur_profile
                print(f"  - {user.username}: {assureur.numero_employe}")
            
            return True
        except Exception as e:
            print(f"❌ Erreur vérification relations: {e}")
            return False
    
    def etape_2_ajouter_proprietes_model(self):
        """Ajoute les propriétés nom et email au modèle Assureur"""
        self.print_header("ÉTAPE 2: Ajout des propriétés au modèle Assureur")
        
        app_dir = self.trouver_app_assureur()
        if not app_dir:
            return False
        
        model_path = app_dir / 'models.py'
        
        if not model_path.exists():
            print(f"❌ Fichier models.py non trouvé: {model_path}")
            return False
        
        # Lire le contenu actuel
        try:
            with open(model_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(model_path, 'r', encoding='latin-1') as f:
                content = f.read()
        
        # Vérifier si les propriétés existent déjà
        if '@property' in content and 'def nom' in content and 'self.user' in content:
            print("✅ Propriétés déjà présentes dans le modèle")
            return True
        
        # Chercher la classe Assureur
        if 'class Assureur' not in content:
            print("❌ Classe Assureur non trouvée dans models.py")
            return False
        
        # Trouver la fin de la classe Assureur
        lines = content.split('\n')
        class_start = -1
        
        for i, line in enumerate(lines):
            if line.strip().startswith('class Assureur'):
                class_start = i
                break
        
        if class_start == -1:
            print("❌ Classe Assureur non trouvée")
            return False
        
        # Trouver la prochaine classe
        class_end = len(lines)
        for i in range(class_start + 1, len(lines)):
            if lines[i].strip().startswith('class ') and not lines[i].strip().startswith('class Meta'):
                class_end = i
                break
        
        # Ajouter les propriétés
        proprietes = [
            '',
            '    # Propriétés pour accéder aux informations utilisateur',
            '    @property',
            '    def nom(self):',
            '        """Retourne le nom complet de l\'utilisateur"""',
            '        return self.user.get_full_name() or self.user.username',
            '',
            '    @property',
            '    def email(self):',
            '        """Retourne l\'email de l\'utilisateur"""',
            '        return self.user.email',
            '',
            '    @property',
            '    def prenom(self):',
            '        """Retourne le prénom de l\'utilisateur"""',
            '        return self.user.first_name',
            '',
            '    @property',
            '    def nom_famille(self):',
            '        """Retourne le nom de famille de l\'utilisateur"""',
            '        return self.user.last_name',
            '',
        ]
        
        # Insérer les propriétés
        lines = lines[:class_end] + proprietes + lines[class_end:]
        
        # Sauvegarder
        try:
            with open(model_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
        except:
            with open(model_path, 'w', encoding='latin-1') as f:
                f.write('\n'.join(lines))
        
        print("✅ Propriétés ajoutées au modèle Assureur")
        self.corrections_appliquees.append("Propriétés nom/email ajoutées au modèle")
        return True
    
    def etape_3_corriger_base_template(self):
        """Corrige le template base_assureur.html pour gérer les cas None"""
        self.print_header("ÉTAPE 3: Correction du template de base")
        
        # Chercher le template
        template_paths = [
            self.project_dir / 'templates' / 'assureur' / 'base_assureur.html',
            self.project_dir / 'assureur' / 'templates' / 'assureur' / 'base_assureur.html',
        ]
        
        template_path = None
        for path in template_paths:
            if path.exists():
                template_path = path
                break
        
        if not template_path:
            print("❌ Template base_assureur.html non trouvé")
            return False
        
        print(f"✅ Template trouvé: {template_path}")
        
        # Lire le contenu
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(template_path, 'r', encoding='latin-1') as f:
                content = f.read()
        
        # Compter les lignes pour debug
        lines = content.split('\n')
        print(f"Nombre de lignes: {len(lines)}")
        
        # Chercher les lignes problématiques
        for i, line in enumerate(lines):
            if 'assureur.user' in line:
                print(f"Ligne {i+1}: {line[:80]}...")
        
        # Remplacer les références problématiques
        nouvelles_lignes = []
        modifications = 0
        
        for line in lines:
            nouvelle_ligne = line
            
            # Remplacer assureur.user.first_name|first|upper
            if 'assureur.user.first_name|first|upper' in line and 'assureur.user.last_name|first|upper' in line:
                nouvelle_ligne = line.replace(
                    '{{ assureur.user.first_name|first|upper }}{{ assureur.user.last_name|first|upper }}',
                    '{% if assureur %}{{ assureur.user.first_name|first|upper }}{{ assureur.user.last_name|first|upper }}{% else %}{{ user.first_name|first|upper }}{{ user.last_name|first|upper }}{% endif %}'
                )
                modifications += 1
            
            # Remplacer assureur.user.get_full_name
            elif 'assureur.user.get_full_name|default:assureur.user.username' in line:
                nouvelle_ligne = line.replace(
                    '{{ assureur.user.get_full_name|default:assureur.user.username }}',
                    '{% if assureur %}{{ assureur.user.get_full_name|default:assureur.user.username }}{% else %}{{ user.get_full_name|default:user.username }}{% endif %}'
                )
                modifications += 1
            
            nouvelles_lignes.append(nouvelle_ligne)
        
        # Sauvegarder si modifications
        if modifications > 0:
            try:
                with open(template_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(nouvelles_lignes))
                print(f"✅ Template corrigé ({modifications} modifications)")
                self.corrections_appliquees.append("Template base corrigé")
            except Exception as e:
                print(f"❌ Erreur sauvegarde template: {e}")
                return False
        else:
            print("ℹ️  Aucune modification nécessaire")
        
        return True
    
    def etape_4_creer_fichiers_manquants(self):
        """Crée les fichiers manquants"""
        self.print_header("ÉTAPE 4: Création des fichiers manquants")
        
        app_dir = self.trouver_app_assureur()
        if not app_dir:
            return False
        
        # 1. Créer context_processors.py
        context_file = app_dir / 'context_processors.py'
        if not context_file.exists():
            context_code = '''"""
Context processors pour l'application assureur
"""

from django.contrib.auth.models import AnonymousUser


def assureur_context(request):
    """
    Ajoute l'assureur connecté au contexte de tous les templates
    """
    context = {}
    
    if hasattr(request, 'user') and not isinstance(request.user, AnonymousUser):
        # Vérifier si l'utilisateur a un profil assureur
        if hasattr(request.user, 'assureur_profile'):
            context['assureur'] = request.user.assureur_profile
        else:
            context['assureur'] = None
    else:
        context['assureur'] = None
    
    return context
'''
            try:
                with open(context_file, 'w', encoding='utf-8') as f:
                    f.write(context_code)
                print("✅ context_processors.py créé")
                self.corrections_appliquees.append("Context processor créé")
            except Exception as e:
                print(f"❌ Erreur création context_processors.py: {e}")
        else:
            print("✅ context_processors.py existe déjà")
        
        # 2. Créer un decorators.py simple
        decorators_file = app_dir / 'decorators.py'
        if not decorators_file.exists():
            decorators_code = '''"""
Décorateurs pour l'application assureur
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def assureur_required(view_func):
    """
    Décorateur qui vérifie que l'utilisateur a un profil assureur
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'assureur_profile'):
            messages.error(request, "Accès réservé aux assureurs.")
            return redirect('login')
        
        assureur = getattr(request.user, 'assureur_profile', None)
        if not assureur:
            messages.error(request, "Profil assureur non configuré.")
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper
'''
            try:
                with open(decorators_file, 'w', encoding='utf-8') as f:
                    f.write(decorators_code)
                print("✅ decorators.py créé")
            except Exception as e:
                print(f"❌ Erreur création decorators.py: {e}")
        else:
            print("✅ decorators.py existe déjà")
        
        return True
    
    def etape_5_verifier_settings(self):
        """Vérifie et met à jour les settings"""
        self.print_header("ÉTAPE 5: Vérification des settings")
        
        # Chercher settings.py
        settings_files = [
            self.project_dir / 'settings.py',
            self.project_dir / 'settings' / '__init__.py',
            self.project_dir / 'settings' / 'base.py',
            self.project_dir / 'projet' / 'settings.py',
        ]
        
        settings_path = None
        for path in settings_files:
            if path.exists():
                settings_path = path
                break
        
        if not settings_path:
            print("❌ settings.py non trouvé")
            return False
        
        print(f"✅ Settings trouvé: {settings_path}")
        
        # Lire le contenu
        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(settings_path, 'r', encoding='latin-1') as f:
                content = f.read()
        
        # Vérifier si le context processor est déjà présent
        if 'assureur.context_processors.assureur_context' in content:
            print("✅ Context processor déjà dans les settings")
            return True
        
        # Chercher la section TEMPLATES
        if 'TEMPLATES' not in content:
            print("❌ Section TEMPLATES non trouvée")
            return False
        
        # Ajouter le context processor
        lines = content.split('\n')
        modifications = 0
        
        for i, line in enumerate(lines):
            if "'django.contrib.messages.context_processors.messages'," in line:
                # Vérifier la ligne suivante
                if i + 1 < len(lines) and "'assureur.context_processors.assureur_context'," not in lines[i + 1]:
                    lines[i] = line + "\n                'assureur.context_processors.assureur_context',"
                    modifications += 1
                    break
        
        if modifications > 0:
            try:
                with open(settings_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
                print("✅ Context processor ajouté aux settings")
                self.corrections_appliquees.append("Settings mis à jour")
            except Exception as e:
                print(f"❌ Erreur mise à jour settings: {e}")
                return False
        else:
            print("ℹ️  Aucune modification nécessaire dans settings")
        
        return True
    
    def etape_6_tester_corrections(self):
        """Teste les corrections"""
        self.print_header("ÉTAPE 6: Test des corrections")
        
        try:
            from django.template.loader import render_to_string
            
            # Tester avec un utilisateur
            user = User.objects.filter(assureur_profile__isnull=False).first()
            
            if user:
                print(f"Utilisateur de test: {user.username}")
                assureur = user.assureur_profile
                
                # Tester les propriétés
                print(f"Assureur: {assureur}")
                print(f"Test propriétés:")
                
                # Ajouter propriétés dynamiquement si nécessaire
                if not hasattr(assureur.__class__, 'nom'):
                    print("⚠️  Ajout dynamique des propriétés...")
                    assureur.__class__.nom = property(lambda self: self.user.get_full_name() or self.user.username)
                    assureur.__class__.email = property(lambda self: self.user.email)
                
                print(f"  - nom: {assureur.nom}")
                print(f"  - email: {assureur.email}")
                
                # Tester le template
                context = {
                    'user': user,
                    'assureur': assureur,
                }
                
                try:
                    html = render_to_string('assureur/base_assureur.html', context)
                    print("✅ Template base_assureur.html rendu avec succès")
                except Exception as e:
                    print(f"❌ Erreur rendu template: {e}")
            else:
                print("⚠️  Aucun utilisateur avec assureur_profile trouvé")
            
            return True
        except Exception as e:
            print(f"❌ Erreur test: {e}")
            return False
    
    def executer_corrections(self):
        """Exécute toutes les corrections"""
        print("🚀 LANCEMENT DES CORRECTIONS ASSUREUR")
        print("="*60)
        
        try:
            # Étape 1: Vérifier les relations
            self.etape_1_verifier_relations()
            
            # Étape 2: Ajouter propriétés au modèle
            self.etape_2_ajouter_proprietes_model()
            
            # Étape 3: Corriger template
            self.etape_3_corriger_base_template()
            
            # Étape 4: Créer fichiers manquants
            self.etape_4_creer_fichiers_manquants()
            
            # Étape 5: Vérifier settings
            self.etape_5_verifier_settings()
            
            # Étape 6: Tester
            self.etape_6_tester_corrections()
            
            # Résumé
            self.print_resume()
            
        except Exception as e:
            print(f"\n❌ Erreur lors des corrections: {e}")
            import traceback
            traceback.print_exc()
    
    def print_resume(self):
        """Affiche le résumé"""
        self.print_header("RÉSUMÉ DES CORRECTIONS")
        
        if self.corrections_appliquees:
            print("✅ Corrections appliquées:")
            for correction in self.corrections_appliquees:
                print(f"  • {correction}")
        else:
            print("ℹ️  Aucune correction appliquée")
        
        if self.erreurs:
            print(f"\n❌ Erreurs: {len(self.erreurs)}")
            for erreur in self.erreurs:
                print(f"  • {erreur}")
        
        print("\n📋 ACTIONS MANUELLES REQUISES:")
        print("1. Vérifiez que votre vue dashboard passe 'assureur' dans le contexte:")
        print("   context = {")
        print("       'assureur': assureur,  # ← CETTE LIGNE EST CRUCIALE")
        print("       'stats': {...},")
        print("       ...")
        print("   }")
        print("\n2. Redémarrez le serveur Django: python manage.py runserver")
        print("\n3. Testez l'accès: /assureur/")
        print("\n🎉 Si l'erreur persiste, vérifiez que 'assureur' est bien passé dans le contexte.")

def main():
    correcteur = CorrectionAssureur()
    correcteur.executer_corrections()

if __name__ == "__main__":
    main()