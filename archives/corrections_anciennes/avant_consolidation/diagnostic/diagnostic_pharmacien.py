#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC COMPLET - APPLICATION PHARMACIEN
Analyse la structure, les modèles, les vues et les templates pharmacien
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

# Import des modules pharmacien
try:
    from pharmacien.models import Pharmacien, Medicament
    import pharmacien.views as pharmacien_views
    print("✅ Import des modèles pharmacien réussi")
except ImportError as e:
    print(f"❌ Erreur import pharmacien: {e}")
    pharmacien_views = None

def print_header(title):
    """Affiche un en-tête stylisé"""
    print("\n" + "="*80)
    print(f"🔍 {title}")
    print("="*80)

def analyse_structure_fichiers():
    """Analyse la structure des fichiers de l'application pharmacien"""
    print_header("STRUCTURE DES FICHIERS PHARMACIEN")
    
    pharmacien_dir = BASE_DIR / "pharmacien"
    templates_dir = BASE_DIR / "templates" / "pharmacien"
    
    print("📁 Répertoire pharmacien/ :")
    if pharmacien_dir.exists():
        for file in sorted(pharmacien_dir.rglob("*")):
            if file.is_file():
                rel_path = file.relative_to(BASE_DIR)
                size = file.stat().st_size
                print(f"   📄 {rel_path} ({size} octets)")
    else:
        print("   ❌ Répertoire pharmacien/ non trouvé")
    
    print("\n📁 Templates pharmacien/ :")
    if templates_dir.exists():
        for file in sorted(templates_dir.rglob("*.html")):
            rel_path = file.relative_to(BASE_DIR)
            size = file.stat().st_size
            print(f"   🎨 {rel_path} ({size} octets)")
    else:
        print("   ❌ Répertoire templates/pharmacien/ non trouvé")

def analyse_modeles_pharmacien():
    """Analyse les modèles de l'application pharmacien"""
    print_header("ANALYSE DES MODÈLES PHARMACIEN")
    
    try:
        # Analyse du modèle Pharmacien
        print("📊 MODÈLE PHARMACIEN :")
        for field in Pharmacien._meta.get_fields():
            if hasattr(field, 'name'):
                field_info = f"   • {field.name}: {field.get_internal_type()}"
                if hasattr(field, 'max_length'):
                    field_info += f" (max_length={field.max_length})"
                if field.null:
                    field_info += " [NULL]"
                if hasattr(field, 'blank') and field.blank:
                    field_info += " [BLANK]"
                print(field_info)
        
        # Analyse du modèle Medicament
        print("\n📊 MODÈLE MEDICAMENT :")
        for field in Medicament._meta.get_fields():
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

def analyse_base_donnees_pharmacien():
    """Analyse la structure de la base de données pour le pharmacien"""
    print_header("ANALYSE BASE DE DONNÉES PHARMACIEN")
    
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Tables pharmacien
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name LIKE '%pharmacien%'
            """)
            tables_pharmacien = cursor.fetchall()
            print("🗃️ Tables liées aux pharmaciens :")
            for table in tables_pharmacien:
                print(f"   • {table[0]}")
            
            # Structure table pharmacien_pharmacien
            try:
                cursor.execute("PRAGMA table_info(pharmacien_pharmacien)")
                colonnes = cursor.fetchall()
                print("\n📋 Structure de pharmacien_pharmacien :")
                for col in colonnes:
                    print(f"   • {col[1]} ({col[2]}) - NULL: {col[3]} - PK: {col[5]}")
            except Exception as e:
                print(f"   ❌ Impossible d'analyser la table pharmacien_pharmacien: {e}")
            
            # Structure table pharmacien_medicament
            try:
                cursor.execute("PRAGMA table_info(pharmacien_medicament)")
                colonnes = cursor.fetchall()
                print("\n📋 Structure de pharmacien_medicament :")
                for col in colonnes:
                    print(f"   • {col[1]} ({col[2]}) - NULL: {col[3]} - PK: {col[5]}")
            except Exception as e:
                print(f"   ❌ Impossible d'analyser la table pharmacien_medicament: {e}")
                
            # Données statistiques
            try:
                cursor.execute("SELECT COUNT(*) FROM pharmacien_pharmacien")
                count = cursor.fetchone()[0]
                print(f"\n📊 Nombre total de pharmaciens : {count}")
            except:
                print("   ❌ Impossible de compter les pharmaciens")
                
            try:
                cursor.execute("SELECT COUNT(*) FROM pharmacien_medicament")
                count_medicaments = cursor.fetchone()[0]
                print(f"📊 Nombre de médicaments : {count_medicaments}")
            except:
                print("   ❌ Impossible de compter les médicaments")
                
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")

def analyse_vues_pharmacien():
    """Analyse les vues de l'application pharmacien"""
    print_header("ANALYSE DES VUES PHARMACIEN")
    
    if not pharmacien_views:
        print("❌ Module pharmacien.views non disponible")
        return
        
    try:
        print("👁️ VUES DISPONIBLES :")
        views = [name for name, obj in inspect.getmembers(pharmacien_views) 
                if inspect.isfunction(obj) and not name.startswith('_')]
        
        for view in sorted(views)[:15]:  # Limiter l'affichage
            func = getattr(pharmacien_views, view)
            docstring = func.__doc__ or 'Pas de docstring'
            print(f"\n   🎯 {view}:")
            print(f"      📝 {docstring[:100]}...")
            
    except Exception as e:
        print(f"❌ Erreur analyse vues: {e}")

def verification_urls_pharmacien():
    """Vérifie la configuration des URLs pharmacien"""
    print_header("VÉRIFICATION URLs PHARMACIEN")
    
    try:
        print("🌐 URLs définies dans pharmacien/urls.py :")
        
        # Analyse directe du fichier urls.py
        urls_file = BASE_DIR / "pharmacien" / "urls.py"
        if urls_file.exists():
            with open(urls_file, 'r') as f:
                content = f.read()
                # Extraire les patterns d'URL
                import re
                url_patterns = re.findall(r"path\(['\"]([^'\"]+)['\"]", content)
                for url in sorted(url_patterns):
                    print(f"   • {url}")
        else:
            print("   ❌ Fichier pharmacien/urls.py non trouvé")
            
    except Exception as e:
        print(f"❌ Erreur URLs: {e}")

def test_imports_pharmacien():
    """Teste les imports critiques pour le pharmacien"""
    print_header("TEST DES IMPORTS PHARMACIEN")
    
    tests = [
        ("models.Pharmacien", "pharmacien.models", "Pharmacien"),
        ("models.Medicament", "pharmacien.models", "Medicament"),
        ("views", "pharmacien", "views"),
    ]
    
    for test_name, module_name, attr_name in tests:
        try:
            if attr_name == "views":
                # Test spécial pour views
                import pharmacien.views
                print(f"✅ {test_name} - IMPORT RÉUSSI")
            else:
                module = __import__(module_name, fromlist=[''])
                if attr_name:
                    obj = getattr(module, attr_name)
                print(f"✅ {test_name} - IMPORT RÉUSSI")
        except Exception as e:
            print(f"❌ {test_name} - ÉCHEC: {e}")

def verification_permissions_pharmacien():
    """Vérifie le système de permissions pour les pharmaciens"""
    print_header("VÉRIFICATION PERMISSIONS PHARMACIEN")
    
    try:
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        
        # Vérifier le groupe Pharmaciens
        try:
            groupe_pharmaciens = Group.objects.get(name='Pharmaciens')
            print("✅ Groupe 'Pharmaciens' trouvé")
            
            # Permissions du groupe
            permissions = groupe_pharmaciens.permissions.all()
            print(f"📋 {permissions.count()} permissions associées")
            
        except Group.DoesNotExist:
            print("❌ Groupe 'Pharmaciens' non trouvé")
        
        # Vérifier les content types
        content_types = ContentType.objects.filter(app_label='pharmacien')
        print(f"📊 ContentTypes pharmacien: {content_types.count()}")
        
    except Exception as e:
        print(f"❌ Erreur permissions: {e}")

def analyse_templates_pharmacien():
    """Analyse les templates pharmacien pour détecter les problèmes"""
    print_header("ANALYSE DES TEMPLATES PHARMACIEN")
    
    templates_dir = BASE_DIR / "templates" / "pharmacien"
    
    if not templates_dir.exists():
        print("❌ Répertoire templates/pharmacien/ non trouvé")
        return
    
    templates_problematiques = []
    champs_problematiques = ['numero_membre', 'date_adhesion']
    
    for template_file in templates_dir.rglob("*.html"):
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            problemes = []
            for champ in champs_problematiques:
                if champ in content:
                    problemes.append(champ)
            
            if problemes:
                templates_problematiques.append((template_file.name, problemes))
                print(f"⚠️  {template_file.name}:")
                for pb in problemes:
                    print(f"   • {pb}")
                
        except Exception as e:
            print(f"❌ Erreur lecture {template_file.name}: {e}")
    
    if not templates_problematiques:
        print("✅ Aucun template problématique détecté")
    else:
        print(f"\n📋 {len(templates_problematiques)} templates avec problèmes")

def verification_relations_medecin():
    """Vérifie les relations avec les modèles medecin"""
    print_header("VÉRIFICATION RELATIONS MÉDECIN")
    
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Vérifier les tables liées aux ordonnances
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name LIKE '%ordonnance%'
            """)
            tables_ordonnances = cursor.fetchall()
            print("🗃️ Tables liées aux ordonnances :")
            for table in tables_ordonnances:
                print(f"   • {table[0]}")
                
            # Vérifier la structure d'une table ordonnance
            if tables_ordonnances:
                try:
                    cursor.execute("PRAGMA table_info(medecin_ordonnance)")
                    colonnes = cursor.fetchall()
                    print("\n📋 Structure de medecin_ordonnance :")
                    for col in colonnes[:10]:  # Limiter l'affichage
                        print(f"   • {col[1]} ({col[2]})")
                except:
                    print("   ❌ Impossible d'analyser medecin_ordonnance")
                    
    except Exception as e:
        print(f"❌ Erreur relations: {e}")

def verification_vues_critiques_pharmacien():
    """Vérifie les vues critiques pour le pharmacien"""
    print_header("VÉRIFICATION VUES CRITIQUES PHARMACIEN")
    
    if not pharmacien_views:
        print("❌ Module views non disponible")
        return
    
    vues_critiques = [
        'dashboard',
        'liste_ordonnances', 
        'valider_ordonnance',
        'refuser_ordonnance',
        'gestion_stock'
    ]
    
    for vue in vues_critiques:
        if hasattr(pharmacien_views, vue):
            func = getattr(pharmacien_views, vue)
            print(f"✅ {vue}: PRÉSENTE")
        else:
            print(f"❌ {vue}: MANQUANTE")

def suggestions_amelioration_pharmacien():
    """Donne des suggestions d'amélioration pour le pharmacien"""
    print_header("SUGGESTIONS D'AMÉLIORATION PHARMACIEN")
    
    suggestions = [
        "🔧 Vérifier l'intégration avec le module medecin pour les ordonnances",
        "🔧 Implémenter un système de validation des ordonnances",
        "🔧 Ajouter la gestion des stocks avec alertes de rupture",
        "🔧 Créer un système de recherche de médicaments",
        "🔧 Implémenter l'historique des validations",
        "🔧 Ajouter des exports pour les rapports de stock",
        "🔧 Créer un dashboard avec statistiques des validations",
        "🔧 Implémenter un système de notifications pour les ordonnances en attente",
    ]
    
    for suggestion in suggestions:
        print(f"   {suggestion}")

def main():
    """Fonction principale"""
    print("🚀 DIAGNOSTIC COMPLET - APPLICATION PHARMACIEN")
    print("📅 Généré le :", django.utils.timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(f"📁 Répertoire projet : {BASE_DIR}")
    
    try:
        analyse_structure_fichiers()
        analyse_modeles_pharmacien()
        analyse_base_donnees_pharmacien()
        analyse_vues_pharmacien()
        verification_urls_pharmacien()
        test_imports_pharmacien()
        verification_permissions_pharmacien()
        analyse_templates_pharmacien()
        verification_relations_medecin()
        verification_vues_critiques_pharmacien()
        suggestions_amelioration_pharmacien()
        
        print_header("✅ DIAGNOSTIC PHARMACIEN TERMINÉ")
        print("💡 Consultez les suggestions d'amélioration ci-dessus")
        
    except Exception as e:
        print(f"💥 ERREUR CRITIQUE DANS LE DIAGNOSTIC: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()