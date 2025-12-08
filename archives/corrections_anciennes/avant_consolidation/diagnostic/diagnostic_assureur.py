#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC COMPLET - APPLICATION ASSUREUR
Analyse la structure, les modèles, les vues et les templates assureur
"""

import os
import sys
import django
from pathlib import Path
import inspect

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

# Import des modules assureur - CORRECTION DES IMPORTS
try:
    from assureur.models import Assureur
    import assureur.views as assureur_views
    print("✅ Import des modèles assureur réussi")
except ImportError as e:
    print(f"❌ Erreur import assureur: {e}")
    # Continuer avec les imports disponibles
    assureur_views = None

def print_header(title):
    """Affiche un en-tête stylisé"""
    print("\n" + "="*80)
    print(f"🔍 {title}")
    print("="*80)

def analyse_structure_fichiers():
    """Analyse la structure des fichiers de l'application assureur"""
    print_header("STRUCTURE DES FICHIERS ASSUREUR")
    
    assureur_dir = BASE_DIR / "assureur"
    templates_dir = BASE_DIR / "templates" / "assureur"
    
    print("📁 Répertoire assureur/ :")
    if assureur_dir.exists():
        for file in sorted(assureur_dir.rglob("*")):
            if file.is_file():
                rel_path = file.relative_to(BASE_DIR)
                size = file.stat().st_size
                print(f"   📄 {rel_path} ({size} octets)")
    else:
        print("   ❌ Répertoire assureur/ non trouvé")
    
    print("\n📁 Templates assureur/ :")
    if templates_dir.exists():
        for file in sorted(templates_dir.rglob("*.html")):
            rel_path = file.relative_to(BASE_DIR)
            size = file.stat().st_size
            print(f"   🎨 {rel_path} ({size} octets)")
    else:
        print("   ❌ Répertoire templates/assureur/ non trouvé")

def analyse_modeles_assureur():
    """Analyse les modèles de l'application assureur"""
    print_header("ANALYSE DES MODÈLES ASSUREUR")
    
    try:
        # Analyse du modèle Assureur
        print("📊 MODÈLE ASSUREUR :")
        for field in Assureur._meta.get_fields():
            if hasattr(field, 'name'):
                field_info = f"   • {field.name}: {field.get_internal_type()}"
                if hasattr(field, 'max_length'):
                    field_info += f" (max_length={field.max_length})"
                if field.null:
                    field_info += " [NULL]"
                if hasattr(field, 'blank') and field.blank:
                    field_info += " [BLANK]"
                print(field_info)
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse des modèles: {e}")

def analyse_base_donnees_assureur():
    """Analyse la structure de la base de données pour l'assureur"""
    print_header("ANALYSE BASE DE DONNÉES ASSUREUR")
    
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Tables assureur
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name LIKE '%assureur%'
            """)
            tables_assureur = cursor.fetchall()
            print("🗃️ Tables liées aux assureurs :")
            for table in tables_assureur:
                print(f"   • {table[0]}")
            
            # Structure table assureur_assureur
            try:
                cursor.execute("PRAGMA table_info(assureur_assureur)")
                colonnes = cursor.fetchall()
                print("\n📋 Structure de assureur_assureur :")
                for col in colonnes:
                    print(f"   • {col[1]} ({col[2]}) - NULL: {col[3]} - PK: {col[5]}")
            except Exception as e:
                print(f"   ❌ Impossible d'analyser la table assureur_assureur: {e}")
                
            # Données statistiques
            try:
                cursor.execute("SELECT COUNT(*) FROM assureur_assureur")
                count = cursor.fetchone()[0]
                print(f"\n📊 Nombre total d'assureurs : {count}")
            except:
                print("   ❌ Impossible de compter les assureurs")
                
            # Membres liés aux assureurs
            try:
                cursor.execute("SELECT COUNT(*) FROM assureur_membre")
                count_membres = cursor.fetchone()[0]
                print(f"📊 Nombre de membres dans assureur_membre : {count_membres}")
            except:
                print("   ❌ Impossible de compter les membres assureur")
                
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")

def analyse_vues_assureur():
    """Analyse les vues de l'application assureur"""
    print_header("ANALYSE DES VUES ASSUREUR")
    
    if not assureur_views:
        print("❌ Module assureur.views non disponible")
        return
        
    try:
        print("👁️ VUES DISPONIBLES :")
        views = [name for name, obj in inspect.getmembers(assureur_views) 
                if inspect.isfunction(obj) and not name.startswith('_')]
        
        for view in sorted(views)[:15]:  # Limiter l'affichage
            func = getattr(assureur_views, view)
            docstring = func.__doc__ or 'Pas de docstring'
            print(f"\n   🎯 {view}:")
            print(f"      📝 {docstring[:100]}...")
            
    except Exception as e:
        print(f"❌ Erreur analyse vues: {e}")

def verification_urls_assureur():
    """Vérifie la configuration des URLs assureur"""
    print_header("VÉRIFICATION URLs ASSUREUR")
    
    try:
        print("🌐 URLs définies dans assureur/urls.py :")
        
        # Analyse directe du fichier urls.py
        urls_file = BASE_DIR / "assureur" / "urls.py"
        if urls_file.exists():
            with open(urls_file, 'r') as f:
                content = f.read()
                # Extraire les patterns d'URL
                import re
                url_patterns = re.findall(r"path\(['\"]([^'\"]+)['\"]", content)
                for url in sorted(url_patterns):
                    print(f"   • {url}")
        else:
            print("   ❌ Fichier assureur/urls.py non trouvé")
            
    except Exception as e:
        print(f"❌ Erreur URLs: {e}")

def test_imports_assureur():
    """Teste les imports critiques pour l'assureur"""
    print_header("TEST DES IMPORTS ASSUREUR")
    
    tests = [
        ("models.Assureur", "assureur.models", "Assureur"),
        ("views", "assureur", "views"),
    ]
    
    for test_name, module_name, attr_name in tests:
        try:
            if attr_name == "views":
                # Test spécial pour views
                import assureur.views
                print(f"✅ {test_name} - IMPORT RÉUSSI")
            else:
                module = __import__(module_name, fromlist=[''])
                if attr_name:
                    obj = getattr(module, attr_name)
                print(f"✅ {test_name} - IMPORT RÉUSSI")
        except Exception as e:
            print(f"❌ {test_name} - ÉCHEC: {e}")

def verification_permissions_assureur():
    """Vérifie le système de permissions pour les assureurs"""
    print_header("VÉRIFICATION PERMISSIONS ASSUREUR")
    
    try:
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        
        # Vérifier le groupe Assureurs
        try:
            groupe_assureurs = Group.objects.get(name='Assureurs')
            print("✅ Groupe 'Assureurs' trouvé")
            
            # Permissions du groupe
            permissions = groupe_assureurs.permissions.all()
            print(f"📋 {permissions.count()} permissions associées")
            
        except Group.DoesNotExist:
            print("❌ Groupe 'Assureurs' non trouvé")
        
        # Vérifier les content types
        content_types = ContentType.objects.filter(app_label='assureur')
        print(f"📊 ContentTypes assureur: {content_types.count()}")
        
    except Exception as e:
        print(f"❌ Erreur permissions: {e}")

def diagnostic_relations_membres():
    """Diagnostique les relations entre assureurs et membres"""
    print_header("DIAGNOSTIQUE RELATIONS ASSUREUR-MEMBRES")
    
    try:
        from membres.models import Membre as MembrePrincipal
        from django.db import connection
        
        # Compter les membres principaux
        total_membres = MembrePrincipal.objects.count()
        print(f"📊 Membres dans modèle principal: {total_membres}")
        
        # Vérifier la table assureur_membre
        with connection.cursor() as cursor:
            try:
                cursor.execute("PRAGMA table_info(assureur_membre)")
                colonnes = cursor.fetchall()
                print("\n📋 Structure de assureur_membre :")
                for col in colonnes:
                    print(f"   • {col[1]} ({col[2]})")
                    
                cursor.execute("SELECT COUNT(*) FROM assureur_membre")
                count = cursor.fetchone()[0]
                print(f"📊 Membres dans assureur_membre: {count}")
                
            except Exception as e:
                print(f"   ❌ Table assureur_membre: {e}")
        
        # Vérifier les relations via agent_createur
        membres_avec_agent = MembrePrincipal.objects.filter(agent_createur__isnull=False).count()
        print(f"📊 Membres avec agent_createur: {membres_avec_agent}")
        
        if membres_avec_agent > 0:
            premier_membre = MembrePrincipal.objects.filter(agent_createur__isnull=False).first()
            if premier_membre and hasattr(premier_membre.agent_createur, 'assureur'):
                print(f"✅ Relation agent→assureur fonctionnelle")
            else:
                print("❌ Problème relation agent→assureur")
                
    except Exception as e:
        print(f"❌ Erreur relations: {e}")

def resume_problemes_templates():
    """Résume les problèmes détectés dans l'analyse des templates"""
    print_header("RÉSUMÉ DES PROBLÈMES TEMPLATES ASSUREUR")
    
    print("📋 TEMPLATES AVEC 'numero_membre' (à corriger en 'numero_unique'):")
    templates_problematiques = [
        "liste_membres.html",
        "creer_cotisation.html", 
        "detail_cotisation.html",
        "liste_cotisations.html",
        "detail_soin.html",
        "export_bons_html.html",
        "liste_bons.html",
        "liste_paiements.html"
    ]
    
    for template in templates_problematiques:
        print(f"   • {template}")
    
    print(f"\n🔧 {len(templates_problematiques)} templates à corriger")

def suggestions_amelioration_assureur():
    """Donne des suggestions d'amélioration pour l'assureur"""
    print_header("SUGGESTIONS D'AMÉLIORATION ASSUREUR")
    
    suggestions = [
        "🔧 CORRIGER LES TEMPLATES: Remplacer 'numero_membre' par 'numero_unique'",
        "🔧 CORRIGER LES TEMPLATES: Remplacer 'date_adhesion' par 'date_inscription'", 
        "🔧 Vérifier la cohérence entre modèle Membre principal et assureur_membre",
        "🔧 Implémenter la pagination dans les vues de liste",
        "🔧 Ajouter des tests unitaires pour les vues assureur",
        "🔧 Optimiser les requêtes avec select_related/prefetch_related",
        "🔧 Mettre en place un système de caching pour les statistiques",
    ]
    
    for suggestion in suggestions:
        print(f"   {suggestion}")

def main():
    """Fonction principale"""
    print("🚀 DIAGNOSTIC COMPLET - APPLICATION ASSUREUR")
    print("📅 Généré le :", django.utils.timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(f"📁 Répertoire projet : {BASE_DIR}")
    
    try:
        analyse_structure_fichiers()
        analyse_modeles_assureur()
        analyse_base_donnees_assureur()
        analyse_vues_assureur()
        verification_urls_assureur()
        test_imports_assureur()
        verification_permissions_assureur()
        diagnostic_relations_membres()
        resume_problemes_templates()
        suggestions_amelioration_assureur()
        
        print_header("✅ DIAGNOSTIC ASSUREUR TERMINÉ")
        print("💡 Consultez les suggestions d'amélioration ci-dessus")
        
    except Exception as e:
        print(f"💥 ERREUR CRITIQUE DANS LE DIAGNOSTIC: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()