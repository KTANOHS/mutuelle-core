#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC COMPLET - APPLICATION MEMBRES
Analyse la structure, les modèles, les vues et les templates
"""

import os
import sys
import django
from pathlib import Path
import inspect

# Configuration Django - CORRECTION DU CHEMIN
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

# CORRECTION : Import correct de l'application membres
from membres.models import Membre
import membres.views as membres_views
from membres.forms import InscriptionMembreForm

def print_header(title):
    """Affiche un en-tête stylisé"""
    print("\n" + "="*80)
    print(f"🔍 {title}")
    print("="*80)

def analyse_structure_fichiers():
    """Analyse la structure des fichiers de l'application"""
    print_header("STRUCTURE DES FICHIERS")
    
    membres_dir = BASE_DIR / "membres"
    templates_dir = BASE_DIR / "templates" / "membres"
    
    print("📁 Répertoire membres/ :")
    if membres_dir.exists():
        for file in sorted(membres_dir.rglob("*")):
            if file.is_file():
                rel_path = file.relative_to(BASE_DIR)
                size = file.stat().st_size
                print(f"   📄 {rel_path} ({size} octets)")
    else:
        print("   ❌ Répertoire membres/ non trouvé")
    
    print("\n📁 Templates membres/ :")
    if templates_dir.exists():
        for file in sorted(templates_dir.rglob("*.html")):
            rel_path = file.relative_to(BASE_DIR)
            size = file.stat().st_size
            print(f"   🎨 {rel_path} ({size} octets)")
    else:
        print("   ❌ Répertoire templates/membres/ non trouvé")

def analyse_modele_membre():
    """Analyse détaillée du modèle Membre"""
    print_header("ANALYSE DU MODÈLE MEMBRE")
    
    try:
        # Analyse des champs
        print("📊 CHAMPS DU MODÈLE MEMBRE :")
        for field in Membre._meta.get_fields():
            field_info = f"   • {field.name}: {field.get_internal_type()}"
            if hasattr(field, 'max_length'):
                field_info += f" (max_length={field.max_length})"
            if field.null:
                field_info += " [NULL]"
            if field.blank:
                field_info += " [BLANK]"
            if hasattr(field, 'default') and field.default != django.db.models.NOT_PROVIDED:
                field_info += f" [default={field.default}]"
            print(field_info)
        
        # Vérification des indexes
        print("\n🔍 INDEXES :")
        for index in Membre._meta.indexes:
            print(f"   • {index.name}: {index.fields}")
        
        # Vérification des propriétés
        print("\n⚡ PROPRIÉTÉS ET MÉTHODES :")
        members = [name for name, obj in inspect.getmembers(Membre) 
                  if not name.startswith('_') and not inspect.ismethod(obj)]
        for prop in sorted(members)[:15]:  # Limiter l'affichage
            print(f"   • {prop}")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse du modèle: {e}")
        import traceback
        traceback.print_exc()

def analyse_base_donnees():
    """Analyse la structure de la base de données"""
    print_header("ANALYSE BASE DE DONNÉES")
    
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Tables membres
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name LIKE '%membre%'
            """)
            tables_membres = cursor.fetchall()
            print("🗃️ Tables liées aux membres :")
            for table in tables_membres:
                print(f"   • {table[0]}")
            
            # Structure table membres_membre
            try:
                cursor.execute("PRAGMA table_info(membres_membre)")
                colonnes = cursor.fetchall()
                print("\n📋 Structure de membres_membre :")
                for col in colonnes:
                    print(f"   • {col[1]} ({col[2]}) - NULL: {col[3]} - PK: {col[5]}")
            except Exception as e:
                print(f"   ❌ Impossible d'analyser la table membres_membre: {e}")
                
            # Données statistiques
            try:
                cursor.execute("SELECT COUNT(*) FROM membres_membre")
                count = cursor.fetchone()[0]
                print(f"\n📊 Nombre total de membres : {count}")
            except:
                print("   ❌ Impossible de compter les membres")
                
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")

def analyse_vues():
    """Analyse les vues de l'application membres"""
    print_header("ANALYSE DES VUES")
    
    try:
        print("👁️ VUES DISPONIBLES :")
        views = [name for name, obj in inspect.getmembers(membres_views) 
                if inspect.isfunction(obj) and not name.startswith('_')]
        
        for view in sorted(views)[:10]:  # Limiter l'affichage
            func = getattr(membres_views, view)
            docstring = func.__doc__ or 'Pas de docstring'
            print(f"\n   🎯 {view}:")
            print(f"      📝 {docstring[:100]}...")
            
    except Exception as e:
        print(f"❌ Erreur analyse vues: {e}")

def verification_urls():
    """Vérifie la configuration des URLs"""
    print_header("VÉRIFICATION URLs")
    
    try:
        from django.urls import get_resolver
        from membres import urls as membres_urls
        
        print("🌐 URLs définies dans membres/urls.py :")
        
        # Analyse directe du fichier urls.py
        urls_file = BASE_DIR / "membres" / "urls.py"
        if urls_file.exists():
            with open(urls_file, 'r') as f:
                content = f.read()
                # Extraire les patterns d'URL
                import re
                url_patterns = re.findall(r"path\(['\"]([^'\"]+)['\"]", content)
                for url in sorted(url_patterns):
                    print(f"   • {url}")
        else:
            print("   ❌ Fichier membres/urls.py non trouvé")
            
    except Exception as e:
        print(f"❌ Erreur URLs: {e}")

def test_imports():
    """Teste les imports critiques"""
    print_header("TEST DES IMPORTS")
    
    tests = [
        ("models.Membre", "membres.models", "Membre"),
        ("views.dashboard", "membres.views", "dashboard"),
        ("forms.InscriptionMembreForm", "membres.forms", "InscriptionMembreForm"),
    ]
    
    for test_name, module_name, attr_name in tests:
        try:
            module = __import__(module_name, fromlist=[''])
            if attr_name:
                obj = getattr(module, attr_name)
            print(f"✅ {test_name} - IMPORT RÉUSSI")
        except Exception as e:
            print(f"❌ {test_name} - ÉCHEC: {e}")

def verification_champs_critiques():
    """Vérifie les champs critiques pour les templates"""
    print_header("VÉRIFICATION CHAMPS CRITIQUES")
    
    try:
        champs_critiques = {
            'numero_unique': 'Numéro unique du membre',
            'date_inscription': 'Date d\'inscription', 
            'statut': 'Statut du membre',
            'nom': 'Nom du membre',
            'prenom': 'Prénom du membre',
            'email': 'Email du membre',
            'telephone': 'Téléphone du membre',
        }
        
        print("🔍 CHAMPS CRITIQUES POUR TEMPLATES :")
        for champ, description in champs_critiques.items():
            try:
                field = Membre._meta.get_field(champ)
                print(f"✅ {champ}: {description} - PRÉSENT ({field.get_internal_type()})")
            except:
                print(f"❌ {champ}: {description} - MANQUANT")
                
        # Vérification propriétés
        print("\n🔍 PROPRIÉTÉS CRITIQUES :")
        proprietes_critiques = ['nom_complet', 'age', 'date_adhesion']
        for prop in proprietes_critiques:
            if hasattr(Membre, prop):
                print(f"✅ {prop} - PRÉSENT")
            else:
                print(f"❌ {prop} - MANQUANT")
                
    except Exception as e:
        print(f"❌ Erreur vérification champs: {e}")

def diagnostic_erreurs_communes():
    """Diagnostique les erreurs courantes"""
    print_header("DIAGNOSTIC ERREURS COURANTES")
    
    problemes = []
    
    # 1. Vérification conflit date_inscription
    try:
        champ_date = Membre._meta.get_field('date_inscription')
        print("✅ Champ date_inscription: OK")
    except Exception as e:
        problemes.append(f"Problème champ date_inscription: {e}")
    
    # 2. Vérification indexes
    try:
        indexes = Membre._meta.indexes
        print(f"✅ Indexes: {len(indexes)} index trouvés")
        for idx in indexes:
            print(f"   • {idx.name}: {idx.fields}")
    except Exception as e:
        problemes.append(f"Problème indexes: {e}")
    
    # 3. Vérification de la propriété date_adhesion
    if hasattr(Membre, 'date_adhesion'):
        print("✅ Propriété date_adhesion: PRÉSENTE")
    else:
        problemes.append("Propriété date_adhesion: MANQUANTE")
    
    if problemes:
        print("\n🚨 PROBLÈMES IDENTIFIÉS :")
        for pb in problemes:
            print(f"   • {pb}")
    else:
        print("✅ Aucun problème critique identifié")

def suggestions_amelioration():
    """Donne des suggestions d'amélioration"""
    print_header("SUGGESTIONS D'AMÉLIORATION")
    
    suggestions = [
        "🔧 Vérifier que tous les templates utilisent 'numero_unique' au lieu de 'numero_membre'",
        "🔧 S'assurer que les vues utilisent 'date_inscription' et non 'date_adhesion'", 
        "🔧 Ajouter la propriété 'date_adhesion' comme alias de 'date_inscription'",
        "🔧 Implémenter la pagination dans toutes les vues de liste",
        "🔧 Ajouter des docstrings à toutes les vues et modèles",
        "🔧 Créer des tests unitaires pour les modèles et vues",
    ]
    
    for suggestion in suggestions:
        print(f"   {suggestion}")

def main():
    """Fonction principale"""
    print("🚀 DIAGNOSTIC COMPLET - APPLICATION MEMBRES")
    print("📅 Généré le :", django.utils.timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(f"📁 Répertoire projet : {BASE_DIR}")
    
    try:
        analyse_structure_fichiers()
        analyse_modele_membre()
        analyse_base_donnees()
        analyse_vues()
        verification_urls()
        test_imports()
        verification_champs_critiques()
        diagnostic_erreurs_communes()
        suggestions_amelioration()
        
        print_header("✅ DIAGNOSTIC TERMINÉ")
        print("💡 Consultez les suggestions d'amélioration ci-dessus")
        
    except Exception as e:
        print(f"💥 ERREUR CRITIQUE DANS LE DIAGNOSTIC: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()