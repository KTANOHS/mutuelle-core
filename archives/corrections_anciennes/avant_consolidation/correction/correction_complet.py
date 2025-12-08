#!/usr/bin/env python
"""
Script de correction complet pour l'application Assureur
Exécutez: python correction_complete.py
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(str(BASE_DIR))

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

from django.contrib.auth.models import User
from assureur.models import Assureur

class CorrectionAssureur:
    """Classe pour corriger tous les problèmes d'assureur"""
    
    def __init__(self):
        self.base_dir = BASE_DIR
        self.corrections_appliquees = []
        self.erreurs = []
        
    def print_header(self, title):
        """Affiche un en-tête"""
        print(f"\n{'='*60}")
        print(f" {title}")
        print(f"{'='*60}")
    
    def etape_1_verifier_relations(self):
        """Vérifie les relations entre User et Assureur"""
        self.print_header("ÉTAPE 1: Vérification des relations")
        
        users = User.objects.all()
        print(f"Total utilisateurs: {users.count()}")
        
        users_avec_assureur = User.objects.filter(assureur_profile__isnull=False)
        print(f"Utilisateurs avec assureur_profile: {users_avec_assureur.count()}")
        
        for user in users_avec_assureur[:5]:
            assureur = user.assureur_profile
            print(f"  - {user.username}: {assureur.numero_employe}")
        
        return True
    
    def etape_2_ajouter_proprietes_model(self):
        """Ajoute les propriétés nom et email au modèle Assureur"""
        self.print_header("ÉTAPE 2: Ajout des propriétés au modèle Assureur")
        
        model_path = self.base_dir / 'assureur' / 'models.py'
        
        if not model_path.exists():
            print(f"❌ Fichier models.py non trouvé: {model_path}")
            return False
        
        # Lire le contenu actuel
        with open(model_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier si les propriétés existent déjà
        if '@property' in content and 'def nom' in content:
            print("✅ Propriétés déjà présentes dans le modèle")
            return True
        
        # Chercher la classe Assureur
        if 'class Assureur' not in content:
            print("❌ Classe Assureur non trouvée dans models.py")
            return False
        
        # Trouver la fin de la classe Assureur (avant la prochaine classe ou la fin du fichier)
        lines = content.split('\n')
        assureur_class_start = -1
        assureur_class_end = -1
        
        for i, line in enumerate(lines):
            if line.strip().startswith('class Assureur'):
                assureur_class_start = i
            elif assureur_class_start != -1 and line.strip().startswith('class ') and i > assureur_class_start:
                assureur_class_end = i
                break
        
        if assureur_class_end == -1:
            assureur_class_end = len(lines)
        
        # Ajouter les propriétés avant la fin de la classe
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
            '    def get_nom_complet(self):',
            '        """Retourne le nom complet formaté"""',
            '        nom_complet = self.user.get_full_name()',
            '        return nom_complet if nom_complet else self.user.username',
            ''
        ]
        
        # Insérer les propriétés
        lines = lines[:assureur_class_end] + proprietes + lines[assureur_class_end:]
        
        # Sauvegarder
        with open(model_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print("✅ Propriétés ajoutées au modèle Assureur")
        self.corrections_appliquees.append("Propriétés nom/email ajoutées au modèle")
        return True
    
    def etape_3_verifier_vue_dashboard(self):
        """Vérifie et corrige la vue dashboard"""
        self.print_header("ÉTAPE 3: Vérification de la vue Dashboard")
        
        views_path = self.base_dir / 'assureur' / 'views.py'
        
        if not views_path.exists():
            print(f"❌ Fichier views.py non trouvé: {views_path}")
            return False
        
        with open(views_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Rechercher la vue dashboard_assureur
        if 'def dashboard_assureur' not in content:
            print("❌ Fonction dashboard_assureur non trouvée")
            
            # Vérifier si c'est une classe-based view
            if 'DashboardAssureurView' in content or 'dashboard' in content.lower():
                print("⚠️  Vue dashboard détectée sous un autre nom")
                return True
            
            # Proposer de créer la vue
            return self.creer_vue_dashboard()
        
        # Vérifier si la vue passe 'assureur' dans le contexte
        if "'assureur'" not in content and '"assureur"' not in content:
            print("❌ La vue ne passe pas 'assureur' dans le contexte")
            
            # Corriger la vue
            return self.corriger_vue_dashboard(content, views_path)
        
        print("✅ Vue dashboard semble correcte")
        return True
    
    def creer_vue_dashboard(self):
        """Crée la vue dashboard si elle n'existe pas"""
        self.print_header("Création de la vue Dashboard")
        
        views_path = self.base_dir / 'assureur' / 'views.py'
        
        vue_code = '''
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

@login_required
def dashboard_assureur(request):
    """
    Vue pour le dashboard de l'assureur
    """
    # Récupérer l'assureur connecté via la relation assureur_profile
    assureur = getattr(request.user, 'assureur_profile', None)
    
    if not assureur:
        messages.error(request, "Vous n'avez pas de profil assureur associé.")
        return render(request, 'assureur/acces_interdit.html')
    
    # Calculer les statistiques de base
    stats = {
        'membres_actifs': 0,
        'nouveaux_membres_mois': 0,
        'cotisations_mois': 0,
        'cotisations_payees_mois': 0,
        'cotisations_retard': 0,
        'montant_cotisations_mois': 0,
        'bons_attente': 0,
        'bons_valides_mois': 0,
        'bons_traites_semaine': 0,
        'taux_satisfaction': 85,
        'soins_valides': 0,
        'taux_recouvrement': 0,
        'femmes_enceintes': 0,
        'paiements_mois': 0,
        'economies_realisees': 0,
        'total_bons': 0,
    }
    
    # Context pour le template
    context = {
        'assureur': assureur,  # IMPORTANT: passer l'assureur
        'stats': stats,
        'alertes_importantes': [],
        'recent_activities': [],
    }
    
    return render(request, 'assureur/dashboard.html', context)
'''
        
        # Ajouter à la fin du fichier views.py
        with open(views_path, 'a', encoding='utf-8') as f:
            f.write(vue_code)
        
        print("✅ Vue dashboard_assureur créée")
        self.corrections_appliquees.append("Vue dashboard créée")
        return True
    
    def corriger_vue_dashboard(self, content, views_path):
        """Corrige la vue dashboard existante"""
        self.print_header("Correction de la vue Dashboard")
        
        lines = content.split('\n')
        vue_start = -1
        
        # Trouver le début de la fonction dashboard_assureur
        for i, line in enumerate(lines):
            if 'def dashboard_assureur' in line:
                vue_start = i
                break
        
        if vue_start == -1:
            print("❌ Impossible de trouver la fonction dashboard_assureur")
            return False
        
        # Trouver la fin de la fonction (par indentation)
        vue_end = vue_start + 1
        while vue_end < len(lines) and (lines[vue_end].startswith(' ') or lines[vue_end].startswith('\t') or lines[vue_end].strip() == ''):
            vue_end += 1
        
        # Vérifier si 'assureur' est dans le contexte
        context_found = False
        context_line = -1
        
        for i in range(vue_start, vue_end):
            if ('context =' in lines[i] or 'context={' in lines[i] or 
                'render(' in lines[i] and 'context' in lines[i]):
                context_line = i
                if "'assureur'" in lines[i] or '"assureur"' in lines[i]:
                    context_found = True
                break
        
        if context_found:
            print("✅ 'assureur' déjà dans le contexte")
            return True
        
        # Si pas de ligne context trouvée, chercher le render
        if context_line == -1:
            for i in range(vue_start, vue_end):
                if 'return render(' in lines[i]:
                    # Essayer d'ajouter le contexte
                    line = lines[i]
                    if 'context' not in line:
                        # Extraire les paramètres du render
                        parts = line.split('render(')
                        if len(parts) > 1:
                            render_params = parts[1].rsplit(')', 1)[0]
                            param_parts = render_params.split(',')
                            
                            # Reconstruire avec contexte
                            new_params = []
                            for param in param_parts:
                                if 'request' in param:
                                    new_params.append(param)
                                elif 'template' in param or 'dashboard.html' in param:
                                    new_params.append(param)
                            
                            # Ajouter le contexte
                            new_line = f"return render({', '.join(new_params)}, {{'assureur': assureur}})"
                            lines[i] = new_line
                            print("✅ Contexte ajouté à la ligne render")
        
        # Sinon, ajouter 'assureur' au dictionnaire context
        elif context_line != -1:
            # Trouver le dictionnaire context
            i = context_line
            while i < vue_end and '{' not in lines[i]:
                i += 1
            
            if i < vue_end:
                # Trouver la ligne de fermeture du dictionnaire
                j = i
                open_braces = lines[i].count('{') - lines[i].count('}')
                while open_braces > 0 and j < vue_end:
                    j += 1
                    open_braces += lines[j].count('{') - lines[j].count('}')
                
                # Ajouter 'assureur' avant la fermeture
                lines[j] = f"        'assureur': assureur,  # Profil de l'assureur connecté\n{lines[j]}"
                print("✅ 'assureur' ajouté au contexte")
        
        # Sauvegarder les modifications
        with open(views_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        self.corrections_appliquees.append("Vue dashboard corrigée")
        return True
    
    def etape_4_creer_context_processor(self):
        """Crée un context processor pour ajouter assureur globalement"""
        self.print_header("ÉTAPE 4: Création du context processor")
        
        # Créer le dossier s'il n'existe pas
        context_dir = self.base_dir / 'assureur'
        context_file = context_dir / 'context_processors.py'
        
        if context_file.exists():
            print("✅ Context processor déjà existant")
            return True
        
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
        
        # Écrire le fichier
        with open(context_file, 'w', encoding='utf-8') as f:
            f.write(context_code)
        
        print("✅ Context processor créé")
        
        # Vérifier et mettre à jour les settings
        return self.ajouter_context_processor_settings()
    
    def ajouter_context_processor_settings(self):
        """Ajoute le context processor aux settings"""
        self.print_header("Ajout du context processor aux settings")
        
        settings_path = self.base_dir / 'votre_projet' / 'settings.py'
        
        if not settings_path.exists():
            # Essayer de trouver le settings
            for file in self.base_dir.glob('**/settings.py'):
                if 'venv' not in str(file):
                    settings_path = file
                    break
        
        if not settings_path.exists():
            print("❌ Fichier settings.py non trouvé")
            return False
        
        with open(settings_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Chercher la section TEMPLATES
        if 'TEMPLATES' not in content:
            print("❌ Section TEMPLATES non trouvée dans settings.py")
            return False
        
        # Ajouter le context processor
        target_string = "'django.contrib.messages.context_processors.messages',"
        new_string = f"    'django.contrib.messages.context_processors.messages',\n                'assureur.context_processors.assureur_context',"
        
        if 'assureur.context_processors.assureur_context' in content:
            print("✅ Context processor déjà dans les settings")
            return True
        
        content = content.replace(target_string, new_string)
        
        # Sauvegarder
        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Context processor ajouté aux settings")
        self.corrections_appliquees.append("Context processor ajouté")
        return True
    
    def etape_5_creer_mixin_assureur(self):
        """Crée un mixin pour les class-based views"""
        self.print_header("ÉTAPE 5: Création du mixin Assureur")
        
        mixin_dir = self.base_dir / 'assureur'
        mixin_file = mixin_dir / 'mixins.py'
        
        if mixin_file.exists():
            print("✅ Fichier mixins.py déjà existant")
            return True
        
        mixin_code = '''"""
Mixins pour l'application assureur
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect


class AssureurMixin(LoginRequiredMixin):
    """
    Mixin qui ajoute l'assureur au contexte et vérifie les permissions
    """
    
    def dispatch(self, request, *args, **kwargs):
        # Vérifier si l'utilisateur a un profil assureur
        if not hasattr(request.user, 'assureur_profile'):
            messages.error(request, "Accès réservé aux assureurs.")
            return redirect('login')
        
        if not request.user.assureur_profile:
            messages.error(request, "Profil assureur non configuré.")
            return redirect('login')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assureur'] = self.request.user.assureur_profile
        return context


class AssureurRequiredMixin:
    """
    Mixin simplifié pour vérifier qu'un utilisateur est assureur
    """
    
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'assureur_profile'):
            messages.error(request, "Accès réservé aux assureurs.")
            return redirect('login')
        
        assureur = getattr(request.user, 'assureur_profile', None)
        if not assureur:
            messages.error(request, "Profil assureur non configuré.")
            return redirect('login')
        
        return super().dispatch(request, *args, **kwargs)
'''
        
        # Écrire le fichier
        with open(mixin_file, 'w', encoding='utf-8') as f:
            f.write(mixin_code)
        
        print("✅ Mixin Assureur créé")
        self.corrections_appliquees.append("Mixin Assureur créé")
        return True
    
    def etape_6_creer_decorateur(self):
        """Crée un décorateur pour les function-based views"""
        self.print_header("ÉTAPE 6: Création du décorateur")
        
        decorator_dir = self.base_dir / 'assureur'
        decorator_file = decorator_dir / 'decorators.py'
        
        if decorator_file.exists():
            print("✅ Fichier decorators.py déjà existant")
            return True
        
        decorator_code = '''"""
Décorateurs pour l'application assureur
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def assureur_required(view_func):
    """
    Décorateur qui vérifie que l'utilisateur a un profil assureur
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        # Vérifier si l'utilisateur a un profil assureur
        if not hasattr(request.user, 'assureur_profile'):
            messages.error(request, "Accès réservé aux assureurs.")
            return redirect('login')
        
        assureur = getattr(request.user, 'assureur_profile', None)
        if not assureur:
            messages.error(request, "Profil assureur non configuré.")
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def assureur_context(view_func):
    """
    Décorateur qui ajoute l'assureur au contexte
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Ajouter l'assureur au contexte si la vue retourne un dictionnaire
        response = view_func(request, *args, **kwargs)
        
        if isinstance(response, dict) and 'assureur' not in response:
            assureur = getattr(request.user, 'assureur_profile', None)
            response['assureur'] = assureur
        
        return response
    return wrapper
'''
        
        # Écrire le fichier
        with open(decorator_file, 'w', encoding='utf-8') as f:
            f.write(decorator_code)
        
        print("✅ Décorateur créé")
        self.corrections_appliquees.append("Décorateur créé")
        return True
    
    def etape_7_corriger_base_template(self):
        """Corrige le template base_assureur.html pour gérer les cas None"""
        self.print_header("ÉTAPE 7: Correction du template de base")
        
        template_path = self.base_dir / 'templates' / 'assureur' / 'base_assureur.html'
        
        if not template_path.exists():
            print(f"❌ Template base_assureur.html non trouvé: {template_path}")
            return False
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier les lignes problématiques (247 et 249 selon le grep)
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            # Ligne avec les initiales
            if 'assureur.user.first_name|first|upper}}{{ assureur.user.last_name|first|upper' in line:
                # Remplacer par une version sécurisée
                new_line = line.replace(
                    '{{ assureur.user.first_name|first|upper }}{{ assureur.user.last_name|first|upper }}',
                    '{% if assureur %}{{ assureur.user.first_name|first|upper }}{{ assureur.user.last_name|first|upper }}{% else %}{{ user.first_name|first|upper }}{{ user.last_name|first|upper }}{% endif %}'
                )
                lines[i] = new_line
                print(f"✅ Ligne {i+1} corrigée (initiales)")
            
            # Ligne avec le nom complet
            elif 'assureur.user.get_full_name|default:assureur.user.username' in line:
                new_line = line.replace(
                    '{{ assureur.user.get_full_name|default:assureur.user.username }}',
                    '{% if assureur %}{{ assureur.user.get_full_name|default:assureur.user.username }}{% else %}{{ user.get_full_name|default:user.username }}{% endif %}'
                )
                lines[i] = new_line
                print(f"✅ Ligne {i+1} corrigée (nom complet)")
        
        # Sauvegarder
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print("✅ Template base_assureur.html corrigé")
        self.corrections_appliquees.append("Template base corrigé")
        return True
    
    def etape_8_test_corrections(self):
        """Teste les corrections appliquées"""
        self.print_header("ÉTAPE 8: Test des corrections")
        
        from django.template.loader import render_to_string
        from django.contrib.auth.models import User
        
        print("1. Test avec un utilisateur assureur:")
        user = User.objects.filter(assureur_profile__isnull=False).first()
        
        if user:
            print(f"   Utilisateur: {user.username}")
            print(f"   Assureur: {user.assureur_profile}")
            print(f"   Test propriétés:")
            print(f"   - nom: {user.assureur_profile.nom}")
            print(f"   - email: {user.assureur_profile.email}")
            
            # Test de rendu template
            context = {
                'user': user,
                'assureur': user.assureur_profile,
            }
            
            try:
                html = render_to_string('assureur/base_assureur.html', context)
                print("   ✅ Template rendu avec succès")
            except Exception as e:
                print(f"   ❌ Erreur template: {e}")
        else:
            print("   ⚠️  Aucun utilisateur avec assureur_profile trouvé")
        
        print("\n2. Test de la vue dashboard (simulé):")
        try:
            # Simuler la vue
            assureur = user.assureur_profile if user else None
            
            context = {
                'assureur': assureur,
                'stats': {'membres_actifs': 0},
            }
            
            html = render_to_string('assureur/dashboard.html', context)
            print("   ✅ Dashboard template rendu avec succès")
        except Exception as e:
            print(f"   ❌ Erreur dashboard: {e}")
        
        return True
    
    def executer_corrections(self):
        """Exécute toutes les corrections"""
        print("🚀 LANCEMENT DES CORRECTIONS ASSUREUR")
        print("="*60)
        
        try:
            # Étape 1: Vérifier les relations
            self.etape_1_verifier_relations()
            
            # Étape 2: Ajouter propriétés au modèle
            self.etape_2_ajouter_proprietes_model()
            
            # Étape 3: Vérifier/corriger la vue dashboard
            self.etape_3_verifier_vue_dashboard()
            
            # Étape 4: Créer context processor
            self.etape_4_creer_context_processor()
            
            # Étape 5: Créer mixin
            self.etape_5_creer_mixin_assureur()
            
            # Étape 6: Créer décorateur
            self.etape_6_creer_decorateur()
            
            # Étape 7: Corriger template de base
            self.etape_7_corriger_base_template()
            
            # Étape 8: Tester
            self.etape_8_test_corrections()
            
            # Résumé
            self.print_resume()
            
        except Exception as e:
            print(f"\n❌ Erreur lors des corrections: {e}")
            import traceback
            traceback.print_exc()
    
    def print_resume(self):
        """Affiche le résumé des corrections"""
        self.print_header("RÉSUMÉ DES CORRECTIONS")
        
        if self.corrections_appliquees:
            print("✅ Corrections appliquées avec succès:")
            for correction in self.corrections_appliquees:
                print(f"  • {correction}")
            
            print(f"\n🔧 {len(self.corrections_appliquees)} corrections appliquées")
        else:
            print("ℹ️  Aucune correction nécessaire")
        
        if self.erreurs:
            print(f"\n❌ Erreurs rencontrées: {len(self.erreurs)}")
            for erreur in self.erreurs:
                print(f"  • {erreur}")
        
        print("\n📋 PROCHAINES ÉTAPES:")
        print("1. Redémarrez le serveur Django")
        print("2. Testez l'accès au dashboard: /assureur/")
        print("3. Vérifiez que les propriétés nom/email fonctionnent")
        print("\n🎉 Si des erreurs persistent, vérifiez:")
        print("   - Que la vue passe bien 'assureur' dans le contexte")
        print("   - Que le context processor est activé dans settings.py")
        print("   - Que les templates utilisent {% if assureur %} pour les cas None")

def main():
    """Fonction principale"""
    correcteur = CorrectionAssureur()
    correcteur.executer_corrections()

if __name__ == "__main__":
    main()