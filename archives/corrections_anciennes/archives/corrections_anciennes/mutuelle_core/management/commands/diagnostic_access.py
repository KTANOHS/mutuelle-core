# management/commands/diagnostic_access.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.urls import get_resolver, reverse, NoReverseMatch
from django.db import connection

class Command(BaseCommand):
    help = 'Diagnostic complet des problèmes d\'accès non autorisé'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            help='Analyser un utilisateur spécifique'
        )
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Tenter de corriger les problèmes automatiquement'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            "🔍 LANCEMENT DU DIAGNOSTIC D'ACCÈS NON AUTORISÉ"
        ))
        
        if options['user']:
            self.analyser_utilisateur_specifique(options['user'])
        else:
            self.diagnostic_complet(options['fix'])

    def diagnostic_complet(self, fix=False):
        """Diagnostic complet"""
        self.analyser_utilisateurs_groupes(fix)
        self.analyser_urls_permissions()
        self.analyser_decorateurs()
        self.analyser_base_donnees()
        self.afficher_recommandations()

    def analyser_utilisateur_specifique(self, username):
        """Analyse un utilisateur spécifique"""
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f"\n👤 ANALYSE DE L'UTILISATEUR: {username}")
            
            groupes = list(user.groups.all().values_list('name', flat=True))
            self.stdout.write(f"   Groupes: {groupes}")
            
            # Vérifier les profils
            profils = []
            for model_name in ['assureur', 'medecin', 'pharmacien', 'membre']:
                if hasattr(user, model_name):
                    profils.append(model_name.capitalize())
            
            self.stdout.write(f"   Profils: {profils}")
            
            # Tester les permissions
            from mutuelle_core.utils import is_assureur, is_medecin, is_pharmacien, is_membre
            
            self.stdout.write(f"   is_assureur: {is_assureur(user)}")
            self.stdout.write(f"   is_medecin: {is_medecin(user)}")
            self.stdout.write(f"   is_pharmacien: {is_pharmacien(user)}")
            self.stdout.write(f"   is_membre: {is_membre(user)}")
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"❌ Utilisateur {username} non trouvé"))

    def analyser_utilisateurs_groupes(self, fix=False):
        """Analyse des utilisateurs et groupes"""
        self.stdout.write("\n📊 1. ANALYSE DES UTILISATEURS ET GROUPES")
        
        users = User.objects.all()
        problemes = []
        
        for user in users:
            groupes = list(user.groups.all().values_list('name', flat=True))
            
            # Vérifier les incohérences
            for groupe in ['Assureur', 'Medecin', 'Pharmacien', 'Membre']:
                if groupe in groupes and not hasattr(user, groupe.lower()):
                    problemes.append(f"{user.username}: Groupe {groupe} sans profil")
                    
                    if fix:
                        # Tentative de correction automatique
                        try:
                            self.creer_profil_manquant(user, groupe)
                            self.stdout.write(self.style.SUCCESS(
                                f"   ✅ Profil {groupe} créé pour {user.username}"
                            ))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(
                                f"   ❌ Erreur création profil: {e}"
                            ))
        
        if problemes:
            self.stdout.write(self.style.WARNING("⚠️  Problèmes détectés:"))
            for probleme in problemes:
                self.stdout.write(f"   - {probleme}")
        else:
            self.stdout.write(self.style.SUCCESS("   ✅ Aucun problème détecté"))

    def creer_profil_manquant(self, user, groupe):
        """Tente de créer un profil manquant"""
        model_name = groupe.lower()
        
        if model_name == 'assureur':
            from assureur.models import Assureur
            Assureur.objects.create(user=user, nom=user.username)
        elif model_name == 'medecin':
            from medecin.models import Medecin
            Medecin.objects.create(user=user, nom=user.get_full_name() or user.username)
        elif model_name == 'pharmacien':
            from pharmacien.models import Pharmacien
            Pharmacien.objects.create(user=user, nom=user.get_full_name() or user.username)
        elif model_name == 'membre':
            from membres.models import Membre
            Membre.objects.create(user=user, nom=user.get_full_name() or user.username)

    def analyser_urls_permissions(self):
        """Analyse des URLs et permissions"""
        self.stdout.write("\n🔗 2. ANALYSE DES URLs ET PERMISSIONS")
        
        resolver = get_resolver()
        urls_dashboard = []
        
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'name') and pattern.name:
                if 'dashboard' in pattern.name:
                    urls_dashboard.append(pattern.name)
        
        self.stdout.write(f"   URLs dashboard trouvées: {len(urls_dashboard)}")
        for url_name in urls_dashboard:
            self.stdout.write(f"   - {url_name}")

    def analyser_decorateurs(self):
        """Analyse des décorateurs"""
        self.stdout.write("\n🛡️  3. ANALYSE DES DÉCORATEURS")
        
        try:
            from mutuelle_core import decorators
            self.stdout.write("   ✅ Module decorators importé")
            
            # Vérifier l'existence des décorateurs
            decorateurs_requis = ['assureur_required', 'medecin_required', 
                                'pharmacien_required', 'membre_required']
            
            for decorateur in decorateurs_requis:
                if hasattr(decorators, decorateur):
                    self.stdout.write(f"   ✅ {decorateur} trouvé")
                else:
                    self.stdout.write(self.style.ERROR(f"   ❌ {decorateur} manquant"))
                    
        except ImportError as e:
            self.stdout.write(self.style.ERROR(f"   ❌ Erreur import: {e}"))

    def analyser_base_donnees(self):
        """Analyse de la base de données"""
        self.stdout.write("\n🗄️  4. ANALYSE DE LA BASE DE DONNÉES")
        
        tables = connection.introspection.table_names()
        tables_requises = ['auth_user', 'auth_group', 'auth_user_groups']
        
        for table in tables_requises:
            if table in tables:
                self.stdout.write(f"   ✅ {table}")
            else:
                self.stdout.write(self.style.ERROR(f"   ❌ {table} manquante"))

    def afficher_recommandations(self):
        """Affiche les recommandations"""
        self.stdout.write("\n🎯 5. RECOMMANDATIONS")
        self.stdout.write("   ✅ Vérifiez les groupes de chaque utilisateur")
        self.stdout.write("   ✅ Assurez-vous que les profils sont créés")
        self.stdout.write("   ✅ Testez les fonctions de permission")
        self.stdout.write("   ✅ Vérifiez les décorateurs dans les vues")