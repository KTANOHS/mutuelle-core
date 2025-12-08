#!/usr/bin/env python
"""
Script de correction complète et profonde des problèmes agents
"""

import os
import sys
from pathlib import Path
import django
import subprocess

# Configuration Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"⚠️ Erreur Django setup: {e}")

class DeepAgentsFixer:
    def __init__(self):
        self.fixes_applied = []
    
    def run_command(self, command):
        """Exécute une commande shell"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
        except Exception as e:
            return False, str(e)
    
    def check_django_environment(self):
        """Vérifie l'environnement Django"""
        print("🔍 DIAGNOSTIC DE L'ENVIRONNEMENT DJANGO")
        print("=" * 50)
        
        try:
            from django.conf import settings
            print(f"✅ Django configuré")
            print(f"   - DEBUG: {settings.DEBUG}")
            print(f"   - Applications installées: {len(settings.INSTALLED_APPS)}")
            
            # Vérifier si l'app agents est installée
            if 'agents' in [app.split('.')[-1] for app in settings.INSTALLED_APPS]:
                print("✅ Application 'agents' dans INSTALLED_APPS")
            else:
                print("❌ Application 'agents' manquante dans INSTALLED_APPS")
                return False
                
            return True
        except Exception as e:
            print(f"❌ Erreur configuration Django: {e}")
            return False
    
    def check_agent_model(self):
        """Vérifie et corrige le modèle Agent"""
        print("\n🔍 INSPECTION DU MODÈLE AGENT")
        print("=" * 50)
        
        try:
            from agents.models import Agent
            print("✅ Modèle Agent importé avec succès")
            
            # Lister tous les champs
            fields = Agent._meta.get_fields()
            field_names = [f.name for f in fields]
            print(f"   Champs disponibles: {', '.join(field_names)}")
            
            return True, field_names
        except Exception as e:
            print(f"❌ Erreur import modèle Agent: {e}")
            return False, []
    
    def create_agent_model_if_missing(self):
        """Crée le modèle Agent s'il est manquant"""
        models_path = Path('agents/models.py')
        
        if not models_path.exists():
            print("❌ Fichier agents/models.py n'existe pas")
            return False
        
        # Vérifier si le modèle Agent existe dans le fichier
        content = models_path.read_text()
        if 'class Agent' not in content:
            print("❌ Classe Agent non trouvée dans models.py")
            
            # Ajouter le modèle Agent
            agent_model = '''
class Agent(models.Model):
    """Modèle Agent"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agent'
    )
    telephone = models.CharField(max_length=20, blank=True, null=True)
    limite_bons_quotidienne = models.IntegerField(default=10)
    est_actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Agent"
        verbose_name_plural = "Agents"

    def __str__(self):
        return f"Agent: {self.user.get_full_name() or self.user.username}"

    def get_nom_complet(self):
        return self.user.get_full_name() or self.user.username

    @property
    def actif(self):
        return self.est_actif
'''
            # Ajouter à la fin du fichier
            with open(models_path, 'a') as f:
                f.write(agent_model)
            
            print("✅ Modèle Agent ajouté à agents/models.py")
            self.fixes_applied.append("Modèle Agent créé")
            return True
        else:
            print("✅ Modèle Agent existe dans models.py")
            return True
    
    def run_migrations(self):
        """Exécute les migrations"""
        print("\n🔄 EXÉCUTION DES MIGRATIONS")
        print("=" * 50)
        
        commands = [
            'python manage.py makemigrations agents',
            'python manage.py migrate agents'
        ]
        
        for cmd in commands:
            success, output = self.run_command(cmd)
            if success:
                print(f"✅ {cmd}")
                if output.strip():
                    print(f"   Output: {output.strip()}")
            else:
                print(f"❌ {cmd}")
                print(f"   Erreur: {output}")
                return False
        
        self.fixes_applied.append("Migrations exécutées")
        return True
    
    def create_test_agent_user(self):
        """Crée l'utilisateur et le profil agent de test"""
        print("\n👤 CRÉATION DE L'UTILISATEUR AGENT DE TEST")
        print("=" * 50)
        
        try:
            from django.contrib.auth.models import User
            
            # Créer ou récupérer l'utilisateur
            user, created = User.objects.get_or_create(
                username='test_agent',
                defaults={
                    'email': 'test_agent@example.com',
                    'first_name': 'Test',
                    'last_name': 'Agent'
                }
            )
            
            if created:
                user.set_password('testpass123')
                user.save()
                print("✅ Utilisateur test_agent créé")
            else:
                # Réinitialiser le mot de passe au cas où
                user.set_password('testpass123')
                user.save()
                print("✅ Utilisateur test_agent existe (mot de passe réinitialisé)")
            
            # Créer le profil agent
            from agents.models import Agent
            agent, agent_created = Agent.objects.get_or_create(
                user=user,
                defaults={
                    'telephone': '+2250102030405',
                    'limite_bons_quotidienne': 10,
                    'est_actif': True
                }
            )
            
            if agent_created:
                print("✅ Profil Agent créé")
            else:
                print("✅ Profil Agent existe déjà")
            
            self.fixes_applied.append("Utilisateur et profil agent de test créés")
            return True
            
        except Exception as e:
            print(f"❌ Erreur création utilisateur agent: {e}")
            return False
    
    def fix_creer_bon_soin_template(self):
        """Corrige définitivement le template creer_bon_soin.html"""
        print("\n🔧 CORRECTION DU TEMPLATE creer_bon_soin.html")
        print("=" * 50)
        
        template_path = Path('agents/templates/agents/creer_bon_soin.html')
        
        if not template_path.exists():
            print("❌ Template creer_bon_soin.html n'existe pas")
            return False
        
        # Lire le contenu actuel
        content = template_path.read_text()
        
        # Supprimer complètement les références au filtre multiply
        # Remplacer par une solution simple sans filtres personnalisés
        simple_template = '''{% extends "agents/base.html" %}
{% load static %}

{% block title %}Créer un bon de soin - Agent{% endblock %}
{% block page_title %}Créer un bon de soin{% endblock %}

{% block content %}
<div class="row">
    <div class="col-lg-8">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">
                    <i class="fas fa-file-medical me-2"></i>Nouveau bon de soin
                </h5>
            </div>
            <div class="card-body">
                <form method="post" id="bonSoinForm">
                    {% csrf_token %}
                    
                    <!-- Alertes -->
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle me-2"></i>
                        Bons créés aujourd'hui: <strong>{{ bons_du_jour }}</strong> / {{ limite_quotidienne }}
                    </div>

                    {% if form.errors %}
                    <div class="alert alert-danger">
                        <strong>Veuillez corriger les erreurs suivantes :</strong>
                        {{ form.errors }}
                    </div>
                    {% endif %}

                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Membre</label>
                            {{ form.membre }}
                            {% if form.membre.errors %}
                            <div class="text-danger">{{ form.membre.errors }}</div>
                            {% endif %}
                        </div>

                        <div class="col-md-6 mb-3">
                            <label class="form-label">Montant maximum</label>
                            <div class="input-group">
                                {{ form.montant_max }}
                                <span class="input-group-text">FCFA</span>
                            </div>
                            {% if form.montant_max.errors %}
                            <div class="text-danger">{{ form.montant_max.errors }}</div>
                            {% endif %}
                        </div>
                    </div>

                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Type de soin</label>
                            {{ form.type_soin }}
                            {% if form.type_soin.errors %}
                            <div class="text-danger">{{ form.type_soin.errors }}</div>
                            {% endif %}
                        </div>

                        <div class="col-md-6 mb-3">
                            <label class="form-label">Médecin destinataire</label>
                            {{ form.medecin_destinataire }}
                            {% if form.medecin_destinataire.errors %}
                            <div class="text-danger">{{ form.medecin_destinataire.errors }}</div>
                            {% endif %}
                        </div>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Motif de consultation</label>
                        {{ form.motif_consultation }}
                        {% if form.motif_consultation.errors %}
                        <div class="text-danger">{{ form.motif_consultation.errors }}</div>
                        {% endif %}
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Niveau d'urgence</label>
                        {{ form.urgence }}
                        {% if form.urgence.errors %}
                        <div class="text-danger">{{ form.urgence.errors }}</div>
                        {% endif %}
                    </div>

                    <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                        <button type="reset" class="btn btn-outline-secondary me-md-2">
                            <i class="fas fa-undo me-1"></i>Réinitialiser
                        </button>
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save me-1"></i>Créer le bon de soin
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- Informations contextuelles -->
    <div class="col-lg-4">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">
                    <i class="fas fa-info-circle me-2"></i>Informations
                </h5>
            </div>
            <div class="card-body">
                <h6>Règles de création :</h6>
                <ul class="list-unstyled">
                    <li><i class="fas fa-check text-success me-2"></i>Vérification automatique de la cotisation</li>
                    <li><i class="fas fa-check text-success me-2"></i>Limite quotidienne: {{ limite_quotidienne }} bons</li>
                    <li><i class="fas fa-check text-success me-2"></i>Validité: 24 heures</li>
                    <li><i class="fas fa-check text-success me-2"></i>Notification automatique au médecin</li>
                </ul>

                <hr>

                <h6>Statistiques du jour :</h6>
                <div class="progress mb-2">
                    <div class="progress-bar" role="progressbar" 
                         style="width: {{ progress_width }}%">
                        {{ bons_du_jour }}/{{ limite_quotidienne }}
                    </div>
                </div>
                <small class="text-muted">
                    {% with limite_restante=limite_restante %}
                    {{ limite_restante }} bons restants aujourd'hui
                    {% endwith %}
                </small>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
// Recherche de membres en temps réel
document.addEventListener('DOMContentLoaded', function() {
    const membreField = document.getElementById('id_membre');
    if (membreField) {
        membreField.className = 'form-select';
    }
});
</script>
{% endblock %}'''
        
        # Écrire le nouveau template simplifié
        template_path.write_text(simple_template)
        print("✅ Template creer_bon_soin.html complètement réécrit")
        self.fixes_applied.append("Template creer_bon_soin.html corrigé")
        return True
    
    def fix_views_for_simple_template(self):
        """Corrige les vues pour le template simplifié"""
        print("\n🔧 CORRECTION DES VUES")
        print("=" * 50)
        
        views_path = Path('agents/views.py')
        
        if not views_path.exists():
            print("❌ Fichier agents/views.py n'existe pas")
            return False
        
        content = views_path.read_text()
        
        # Corriger la vue CreerBonSoinView pour ajouter les variables manquantes
        if 'class CreerBonSoinView' in content:
            # Trouver la méthode get_context_data
            if 'def get_context_data' in content:
                # Remplacer la méthode existante ou en ajouter une
                old_context_method = '''    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Créer un bon de soin"
        context['limite_quotidienne'] = self.request.user.agent.limite_bons_quotidienne
        
        # Statistiques du jour
        aujourd_hui = timezone.now().date()
        context['bons_du_jour'] = BonSoin.objects.filter(
            agent=self.request.user.agent,
            date_creation__date=aujourd_hui
        ).count()
        
        return context'''
                
                new_context_method = '''    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Créer un bon de soin"
        
        if hasattr(self.request.user, 'agent'):
            context['limite_quotidienne'] = self.request.user.agent.limite_bons_quotidienne
            
            # Statistiques du jour
            from django.utils import timezone
            aujourd_hui = timezone.now().date()
            context['bons_du_jour'] = BonSoin.objects.filter(
                agent=self.request.user.agent,
                date_creation__date=aujourd_hui
            ).count()
            
            # Calculer la largeur de progression
            if context['limite_quotidienne'] > 0:
                context['progress_width'] = min(100, int((context['bons_du_jour'] / context['limite_quotidienne']) * 100))
            else:
                context['progress_width'] = 0
                
            # Calculer la limite restante
            context['limite_restante'] = max(0, context['limite_quotidienne'] - context['bons_du_jour'])
        else:
            context['limite_quotidienne'] = 10
            context['bons_du_jour'] = 0
            context['progress_width'] = 0
            context['limite_restante'] = 10
        
        return context'''
                
                if old_context_method in content:
                    content = content.replace(old_context_method, new_context_method)
                else:
                    # Insérer après la classe
                    class_pos = content.find('class CreerBonSoinView')
                    if class_pos != -1:
                        # Trouver la fin de la classe
                        brace_count = 0
                        pos = class_pos
                        while pos < len(content):
                            if content[pos] == '{':
                                brace_count += 1
                            elif content[pos] == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    break
                            pos += 1
                        
                        # Insérer la méthode après la classe
                        content = content[:pos] + '\n\n' + new_context_method + '\n' + content[pos:]
                
                views_path.write_text(content)
                print("✅ Vue CreerBonSoinView corrigée")
                self.fixes_applied.append("Vue CreerBonSoinView mise à jour")
        
        return True
    
    def test_final_setup(self):
        """Test final de la configuration"""
        print("\n🧪 TEST FINAL DE LA CONFIGURATION")
        print("=" * 50)
        
        try:
            from django.contrib.auth import authenticate
            from django.test import Client
            
            # Test d'authentification
            user = authenticate(username='test_agent', password='testpass123')
            if user:
                print("✅ Authentification réussie")
            else:
                print("❌ Échec authentification")
                return False
            
            # Test de connexion client
            client = Client()
            login_success = client.login(username='test_agent', password='testpass123')
            if login_success:
                print("✅ Connexion client réussie")
            else:
                print("❌ Échec connexion client")
                return False
            
            # Test des templates
            from django.template.loader import get_template
            templates_to_test = [
                'agents/base.html',
                'agents/creer_bon_soin.html',
                'agents/dashboard.html'
            ]
            
            for template in templates_to_test:
                try:
                    get_template(template)
                    print(f"✅ Template {template} accessible")
                except Exception as e:
                    print(f"❌ Template {template} erreur: {e}")
                    return False
            
            # Test des URLs basique
            response = client.get('/agents/dashboard/')
            if response.status_code in [200, 302]:
                print("✅ URL dashboard accessible")
            else:
                print(f"❌ URL dashboard: {response.status_code}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur test final: {e}")
            return False
    
    def apply_all_fixes(self):
        """Applique toutes les corrections"""
        print("🚀 CORRECTION COMPLÈTE DE L'ESPACE AGENT")
        print("=" * 60)
        
        # 1. Vérifier l'environnement Django
        if not self.check_django_environment():
            return False
        
        # 2. Vérifier/créer le modèle Agent
        model_exists, fields = self.check_agent_model()
        if not model_exists:
            if not self.create_agent_model_if_missing():
                return False
        
        # 3. Exécuter les migrations
        if not self.run_migrations():
            return False
        
        # 4. Créer l'utilisateur de test
        if not self.create_test_agent_user():
            return False
        
        # 5. Corriger le template problématique
        if not self.fix_creer_bon_soin_template():
            return False
        
        # 6. Corriger les vues
        if not self.fix_views_for_simple_template():
            return False
        
        # 7. Test final
        if not self.test_final_setup():
            print("❌ Le test final a échoué")
            return False
        
        print("\n" + "=" * 60)
        print("🎉 CORRECTIONS APPLIQUÉES AVEC SUCCÈS!")
        print("=" * 60)
        
        for fix in self.fixes_applied:
            print(f"✅ {fix}")
        
        print(f"\n📋 Total des correctifs: {len(self.fixes_applied)}")
        
        print("\n🚀 INSTRUCTIONS FINALES:")
        print("1. Redémarrez le serveur: python manage.py runserver")
        print("2. Accédez à: http://127.0.0.1:8000/agents/dashboard/")
        print("3. Connectez-vous avec: test_agent / testpass123")
        print("4. Testez la création de bon: http://127.0.0.1:8000/agents/bons/creer/")
        
        return True

def main():
    fixer = DeepAgentsFixer()
    success = fixer.apply_all_fixes()
    
    if not success:
        print("\n❌ La correction automatique a échoué.")
        print("📝 Des interventions manuelles sont nécessaires.")
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()