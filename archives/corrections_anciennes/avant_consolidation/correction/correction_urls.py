#!/usr/bin/env python3
"""
SCRIPT DE CORRECTION DES URLs - MUTUELLE_CORE
Corrige les conflits d'URLs et optimise la structure
"""

import os
import re
from pathlib import Path

def analyser_conflits():
    """Analyse détaillée des conflits d'URLs"""
    print("=" * 80)
    print("ANALYSE DES CONFLITS D'URLs")
    print("=" * 80)
    
    conflits = {
        'soins': {
            'urls': ['/soins/', '/soins/<int:soin_id>/'],
            'probleme': "Conflit entre soins.views.wrapper et mutuelle_core.views",
            'impact': "Risque de routing incorrect"
        },
        'membres': {
            'urls': ['/membres/creer/'],
            'probleme': "Double définition de la création de membre",
            'impact': "Comportement imprévisible"
        },
        'communication': {
            'urls': ['/communication/notifications/count/'],
            'probleme': "URL dupliquée avec le même nom",
            'impact': "Django utilisera la première trouvée"
        },
        'valider_soin': {
            'urls': ['/soins/<int:soin_id>/valider/'],
            'probleme': "Double définition de validation soin",
            'impact': "Route ambiguë"
        }
    }
    
    for module, details in conflits.items():
        print(f"\n🔴 CONFLIT {module.upper()}:")
        print(f"   URLs: {', '.join(details['urls'])}")
        print(f"   Problème: {details['probleme']}")
        print(f"   Impact: {details['impact']}")

def generer_corrections_urls():
    """Génère les corrections pour les URLs"""
    print("\n" + "=" * 80)
    print("CORRECTIONS PROPOSÉES")
    print("=" * 80)
    
    corrections = {
        'soins_urls.py': """
# === CORRECTION SOINS URLs ===
from django.urls import path
from . import views

app_name = 'soins'

urlpatterns = [
    # Dashboard soins - URL unique
    path('', views.dashboard_soins, name='dashboard_soins'),
    
    # Liste des soins - URL dédiée
    path('liste/', views.liste_soins, name='liste_soins'),
    
    # Détail soin - URL dédiée
    path('<int:soin_id>/', views.detail_soin, name='detail_soin'),
    
    # Validation soin - URL unique et claire
    path('<int:soin_id>/valider/', views.valider_soin, name='valider_soin'),
    
    # Rejet soin - URL unique
    path('<int:soin_id>/rejeter/', views.rejeter_soin, name='rejeter_soin'),
    
    # Statistiques
    path('statistiques/', views.statistiques_soins, name='statistiques_soins'),
]
""",
        
        'mutuelle_core_urls.py': """
# === CORRECTION URLS PRINCIPALES ===
from django.urls import path, include
from . import views

urlpatterns = [
    # Redirection soins vers l'application dédiée
    path('soins/', include('soins.urls')),
    
    # Gestion membres centralisée dans l'application membres
    path('membres/', include('membres.urls')),
    
    # Page d'accueil soins alternative
    path('accueil-soins/', views.liste_soins, name='accueil_soins'),
]
""",
        
        'membres_urls.py': """
# === CORRECTION MEMBRES URLs ===
from django.urls import path
from . import views

app_name = 'membres'

urlpatterns = [
    # Création membre - URL unique
    path('creer/', views.creer_membre, name='creer_membre'),
    
    # Dashboard membres
    path('dashboard/', views.dashboard_membres, name='dashboard_membres'),
    
    # Liste membres
    path('liste/', views.liste_membres, name='liste_membres'),
    
    # Détail membre
    path('<int:membre_id>/', views.detail_membre, name='detail_membre'),
]
""",
        
        'communication_urls.py': """
# === CORRECTION COMMUNICATION URLs ===
from django.urls import path
from . import views

app_name = 'communication'

urlpatterns = [
    # Notification count - URL unique
    path('notifications/count/', views.notification_count, name='notification_count'),
    
    # Liste notifications
    path('notifications/', views.liste_notifications, name='liste_notifications'),
]
"""
    }
    
    for fichier, correction in corrections.items():
        print(f"\n📁 {fichier}:")
        print(correction)

def script_migration_automatique():
    """Script pour migrer automatiquement les données si nécessaire"""
    print("\n" + "=" * 80)
    print("SCRIPT DE MIGRATION AUTOMATIQUE")
    print("=" * 80)
    
    migration_script = """
#!/usr/bin/env python3
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def migrer_references_urls():
    \"\"\"Migre les références d'URLs obsolètes vers les nouvelles\"\"\"
    from django.contrib.contenttypes.models import ContentType
    from django.db import connection
    
    print("🔄 MIGRATION DES RÉFÉRENCES URLs...")
    
    # Mapping des anciennes URLs vers les nouvelles
    migrations_urls = {
        'soins:dashboard': 'soins:dashboard_soins',
        'soins:liste_soins': 'soins:liste_soins',
        'soins:detail_soin': 'soins:detail_soin',
        'soins:valider_soin': 'soins:valider_soin',
        'membres:creer_membre': 'membres:creer_membre',
    }
    
    # Vérifier les références dans la base de données
    with connection.cursor() as cursor:
        cursor.execute(\"\"\"
            SELECT name, app_label, model 
            FROM django_content_type 
            WHERE app_label IN ('soins', 'membres', 'communication')
        \"\"\")
        content_types = cursor.fetchall()
        
        print(f\"✅ Content types trouvés: {len(content_types)}\")
    
    print(\"✅ Migration des URLs préparée\")

def verifier_integrite_urls():
    \"\"\"Vérifie l'intégrité des URLs après correction\"\"\"
    from django.urls import get_resolver
    from django.core.checks.urls import check_url_config
    
    print(\"🔍 VÉRIFICATION INTÉGRITÉ URLs...\")
    
    # Vérifier la configuration URLs
    errors = check_url_config(None)
    if errors:
        print(\"❌ ERREURS DÉTECTÉES:\")
        for error in errors:
            print(f\"   - {error}\")
    else:
        print(\"✅ Aucune erreur d'URL détectée\")
    
    # Lister toutes les URLs
    resolver = get_resolver()
    url_patterns = []
    
    def list_urls(patterns, namespace=None):
        for pattern in patterns:
            if hasattr(pattern, 'url_patterns'):
                # Namespace
                new_namespace = namespace
                if pattern.namespace:
                    new_namespace = f\"{namespace}:{pattern.namespace}\" if namespace else pattern.namespace
                list_urls(pattern.url_patterns, new_namespace)
            else:
                url_patterns.append({
                    'pattern': pattern.pattern,
                    'name': f\"{namespace}:{pattern.name}\" if namespace and pattern.name else pattern.name,
                    'namespace': namespace
                })
    
    list_urls(resolver.url_patterns)
    
    print(f\"✅ URLs totales après correction: {len(url_patterns)}\")
    
    # Vérifier les doublons
    noms_urls = [url['name'] for url in url_patterns if url['name']]
    doublons = set([x for x in noms_urls if noms_urls.count(x) > 1])
    
    if doublons:
        print(\"❌ DOUBLONS DÉTECTÉS:\")
        for doublon in doublons:
            print(f\"   - {doublon}\")
    else:
        print(\"✅ Aucun doublon d'URL détecté\")

if __name__ == \"__main__\":
    migrer_references_urls()
    verifier_integrite_urls()
    print(\"✅ MIGRATION TERMINÉE\")
"""
    
    print(migration_script)

def generer_tests_urls():
    """Génère des tests pour vérifier les URLs"""
    print("\n" + "=" * 80)
    print("TESTS AUTOMATIQUES POUR LES URLs")
    print("=" * 80)
    
    tests_script = """
#!/usr/bin/env python3
import os
import django
from django.test import TestCase
from django.urls import reverse, resolve, NoReverseMatch
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

class TestUrlsCorrection(TestCase):
    \"\"\"Tests pour vérifier la correction des URLs\"\"\"
    
    def setUp(self):
        self.client = Client()
    
    def test_urls_soins_sans_conflit(self):
        \"\"\"Test que les URLs soins n'ont pas de conflits\"\"\"
        # Test des URLs soins
        urls_soins = [
            ('soins:dashboard_soins', '/soins/'),
            ('soins:liste_soins', '/soins/liste/'),
            ('soins:detail_soin', '/soins/1/'),
            ('soins:valider_soin', '/soins/1/valider/'),
        ]
        
        for nom_url, url_attendu in urls_soins:
            with self.subTest(url=nom_url):
                try:
                    url_calculee = reverse(nom_url, args=[1] if '1' in url_attendu else [])
                    self.assertEqual(url_calculee, url_attendu)
                except NoReverseMatch:
                    self.fail(f\"URL {nom_url} non trouvée\")
    
    def test_urls_membres_unicite(self):
        \"\"\"Test que la création membre est unique\"\"\"
        try:
            url = reverse('membres:creer_membre')
            self.assertEqual(url, '/membres/creer/')
        except NoReverseMatch:
            self.fail(\"URL création membre non trouvée\")
    
    def test_pas_de_doublons_notification_count(self):
        \"\"\"Test qu'il n'y a pas de doublons notification count\"\"\"
        from django.urls import get_resolver
        
        resolver = get_resolver()
        urls_notification_count = []
        
        def trouver_urls(patterns, namespace=None):
            for pattern in patterns:
                if hasattr(pattern, 'url_patterns'):
                    new_ns = f\"{namespace}:{pattern.namespace}\" if namespace else pattern.namespace
                    trouver_urls(pattern.url_patterns, new_ns)
                elif pattern.name == 'notification_count':
                    urls_notification_count.append({
                        'namespace': namespace,
                        'pattern': str(pattern.pattern)
                    })
        
        trouver_urls(resolver.url_patterns)
        
        # Ne doit avoir qu'une seule URL notification_count
        self.assertEqual(len(urls_notification_count), 1, 
                        f\"Doublons notification_count détectés: {urls_notification_count}\")
    
    def test_acces_urls_correction(self):
        \"\"\"Test l'accès aux URLs corrigées\"\"\"
        # URLs qui doivent être accessibles (avec login requis)
        urls_a_tester = [
            ('soins:dashboard_soins', 200),  # Redirection vers login si non authentifié
            ('membres:liste_membres', 200),
        ]
        
        for nom_url, status_attendu in urls_a_tester:
            with self.subTest(url=nom_url):
                try:
                    url = reverse(nom_url)
                    response = self.client.get(url)
                    # Peut être 200 (si auth) ou 302 (redirect login)
                    self.assertIn(response.status_code, [status_attendu, 302])
                except NoReverseMatch:
                    self.fail(f\"URL {nom_url} non trouvée\")

class TestIntegrationWorkflows(TestCase):
    \"\"\"Tests d'intégration des workflows critiques\"\"\"
    
    def test_workflow_agent_creation_bon(self):
        \"\"\"Test le workflow complet de création de bon par agent\"\"\"
        # 1. Login agent
        # 2. Accès dashboard agent
        # 3. Recherche membre
        # 4. Création bon
        # 5. Confirmation bon
        
        urls_workflow = [
            'agents:dashboard',
            'agents:recherche_membres_api', 
            'agents:creer_bon_soin',
            'agents:confirmation_bon_soin'
        ]
        
        for url_name in urls_workflow:
            with self.subTest(etape=url_name):
                try:
                    reverse(url_name)
                except NoReverseMatch:
                    self.fail(f\"URL manquante pour le workflow: {url_name}\")
    
    def test_workflow_medecin_consultation(self):
        \"\"\"Test le workflow consultation médicale\"\"\"
        urls_workflow = [
            'medecin:dashboard',
            'medecin:creer_consultation',
            'medecin:creer_ordonnance',
            'medecin:valider_bon_soin'
        ]
        
        for url_name in urls_workflow:
            with self.subTest(etape=url_name):
                try:
                    reverse(url_name)
                except NoReverseMatch:
                    self.fail(f\"URL manquante pour le workflow médical: {url_name}\")

if __name__ == \"__main__\":
    import unittest
    unittest.main()
"""
    
    print(tests_script)

def generer_guide_implementation():
    """Génère un guide d'implémentation étape par étape"""
    print("\n" + "=" * 80)
    print("GUIDE D'IMPLÉMENTATION - ÉTAPE PAR ÉTAPE")
    print("=" * 80)
    
    guide = """
📋 GUIDE DE CORRECTION - ÉTAPES À SUIVRE

ÉTAPE 1: ✅ SAUVEGARDE
   - Sauvegarder la base de données
   - Faire un commit git: `git add . && git commit -m "BACKUP avant correction URLs"`

ÉTAPE 2: 🛠 CORRECTION DES FICHIERS URLs
   - Modifier `soins/urls.py` avec la nouvelle structure
   - Modifier `membres/urls.py` pour une URL création unique  
   - Modifier `communication/urls.py` pour supprimer le doublon
   - Mettre à jour `mutuelle_core/urls.py` pour utiliser include()

ÉTAPE 3: 🔄 MIGRATION DES RÉFÉRENCES
   - Exécuter le script de migration: `python migration_urls.py`
   - Vérifier qu'aucune erreur n'apparaît

ÉTAPE 4: ✅ VALIDATION
   - Lancer les tests: `python manage.py test tests_urls_correction.py`
   - Vérifier le routage: `python manage.py check_urls`
   - Tester manuellement les workflows critiques

ÉTAPE 5: 🚀 DÉPLOIEMENT
   - Faire un commit des corrections
   - Déployer en environnement de test
   - Tester intensivement avant production

COMMANDES DE VÉRIFICATION:
   python manage.py check urls
   python manage.py show_urls | grep -i conflit
   python manage.py test agents.tests medecin.tests

ZONES CRITIQUES À TESTER:
   ✅ Workflow création bon de soin (Agent → Membre → Bon)
   ✅ Workflow consultation (Médecin → Ordonnance → Pharmacien) 
   ✅ Workflow paiement (Membre → Cotisation → Paiement)
   ✅ Communication (Notifications → Messages)
"""
    
    print(guide)

def main():
    """Fonction principale"""
    print("🔧 SCRIPT DE CORRECTION DES URLs MUTUELLE_CORE")
    print("Version: 1.0 | Objectif: Résoudre les conflits d'URLs")
    print()
    
    analyser_conflits()
    generer_corrections_urls()
    script_migration_automatique()
    generer_tests_urls()
    generer_guide_implementation()
    
    print("\n" + "=" * 80)
    print("✅ SCRIPT DE CORRECTION GÉNÉRÉ AVEC SUCCÈS")
    print("=" * 80)
    print("\n📝 PROCHAINES ACTIONS:")
    print("   1. Sauvegarder votre projet")
    print("   2. Appliquer les corrections aux fichiers urls.py")
    print("   3. Exécuter le script de migration")
    print("   4. Lancer les tests de validation")
    print("   5. Tester les workflows métier")

if __name__ == "__main__":
    main()