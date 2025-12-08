#!/usr/bin/env python3
"""
ANALYSE COMPLÈTE DU MODÈLE MEMBRE EXISTANT
"""

import os
import django
from pathlib import Path
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

BASE_DIR = Path(__file__).parent

def analyze_member_model():
    """Analyse complète du modèle Membre existant"""
    
    print("🔍 ANALYSE DU MODÈLE MEMBRE EXISTANT")
    print("=" * 50)
    
    # 1. Analyser le fichier models.py
    analyze_model_file()
    
    # 2. Analyser la structure de la base de données
    analyze_database_structure()
    
    # 3. Vérifier les relations existantes
    analyze_relationships()
    
    # 4. Analyser les migrations existantes
    analyze_existing_migrations()
    
    print("\n✅ ANALYSE TERMINÉE!")

def analyze_model_file():
    """Analyse le fichier models.py de l'app membres"""
    
    print("\n📄 ANALYSE DU FICHIER MODELS.PY...")
    
    model_file = BASE_DIR / 'membres' / 'models.py'
    
    if not model_file.exists():
        print("❌ Fichier models.py non trouvé dans l'app membres")
        return
    
    with open(model_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"   📏 Taille du fichier: {len(content)} caractères")
    print(f"   📊 Nombre de lignes: {content.count(chr(10)) + 1}")
    
    # Rechercher la classe Membre
    if 'class Membre' in content:
        print("   ✅ Classe Membre trouvée")
        
        # Extraire le contenu de la classe Membre
        class_start = content.find('class Membre')
        class_end = find_class_end(content, class_start)
        
        if class_start != -1 and class_end != -1:
            class_content = content[class_start:class_end]
            
            # Compter les champs
            fields = extract_fields_from_class(class_content)
            print(f"   🗄️  Nombre de champs détectés: {len(fields)}")
            
            # Afficher les champs
            print("\n   📋 CHAMPS EXISTANTS:")
            for field_name, field_type in fields.items():
                print(f"      🏷️  {field_name}: {field_type}")
            
            # Analyser les types de champs
            analyze_field_types(fields)
            
        else:
            print("   ❌ Impossible d'extraire le contenu de la classe Membre")
    else:
        print("   ❌ Classe Membre non trouvée")

def find_class_end(content, start_pos):
    """Trouve la fin d'une classe"""
    # Chercher la prochaine classe ou la fin du fichier
    next_class = content.find('class ', start_pos + 1)
    if next_class != -1:
        return next_class
    
    # Chercher la fin du fichier
    return len(content)

def extract_fields_from_class(class_content):
    """Extrait les champs d'une classe Model"""
    fields = {}
    
    # Pattern pour les champs de modèle
    field_patterns = [
        r'(\w+)\s*=\s*models\.(\w+)Field',
        r'(\w+)\s*=\s*models\.ForeignKey',
        r'(\w+)\s*=\s*models\.OneToOneField',
        r'(\w+)\s*=\s*models\.ManyToManyField'
    ]
    
    for pattern in field_patterns:
        matches = re.findall(pattern, class_content)
        for match in matches:
            if len(match) == 2:
                fields[match[0]] = match[1]
            else:
                fields[match[0]] = 'Relation'
    
    return fields

def analyze_field_types(fields):
    """Analyse les types de champs existants"""
    
    print("\n   📊 ANALYSE DES TYPES DE CHAMPS:")
    
    field_types = {}
    for field_name, field_type in fields.items():
        if field_type not in field_types:
            field_types[field_type] = []
        field_types[field_type].append(field_name)
    
    for field_type, field_names in field_types.items():
        print(f"      🔧 {field_type}: {len(field_names)} champ(s)")
        for name in field_names:
            print(f"         • {name}")

def analyze_database_structure():
    """Analyse la structure actuelle de la base de données"""
    
    print("\n🗄️ ANALYSE DE LA STRUCTURE BASE DE DONNÉES...")
    
    try:
        from membres.models import Membre
        from django.db import connection
        
        # Obtenir les informations de la table
        table_name = Membre._meta.db_table
        print(f"   📋 Table: {table_name}")
        
        # Obtenir les champs via la métadonnée Django
        fields = Membre._meta.fields
        print(f"   🏷️  Champs dans la base: {len(fields)}")
        
        print("\n   📋 STRUCTURE ACTUELLE:")
        for field in fields:
            field_info = {
                'name': field.name,
                'type': field.get_internal_type(),
                'null': field.null,
                'blank': field.blank,
                'max_length': getattr(field, 'max_length', None)
            }
            
            # Afficher les informations du champ
            null_info = "NULL" if field_info['null'] else "NOT NULL"
            blank_info = "BLANK" if field_info['blank'] else "REQUIRED"
            max_len = f"max_length={field_info['max_length']}" if field_info['max_length'] else ""
            
            print(f"      🗃️  {field_info['name']} ({field_info['type']}) {null_info} {blank_info} {max_len}")
        
        # Vérifier si des champs ImageField existent déjà
        image_fields = [f for f in fields if f.get_internal_type() == 'ImageField']
        if image_fields:
            print(f"\n   📸 CHAMPS IMAGE EXISTANTS: {len(image_fields)}")
            for field in image_fields:
                print(f"      🖼️  {field.name}")
        else:
            print("\n   ❌ AUCUN champ ImageField existant")
            
    except Exception as e:
        print(f"   ❌ Erreur analyse base de données: {e}")

def analyze_relationships():
    """Analyse les relations existantes du modèle Membre"""
    
    print("\n🔗 ANALYSE DES RELATIONS EXISTANTES...")
    
    try:
        from membres.models import Membre
        
        # Obtenir les relations
        relations = []
        
        # ForeignKey
        for field in Membre._meta.get_fields():
            if field.is_relation:
                relation_info = {
                    'name': field.name,
                    'type': field.__class__.__name__,
                    'related_model': field.related_model.__name__ if field.related_model else 'Unknown',
                    'on_delete': getattr(field, 'on_delete', None)
                }
                relations.append(relation_info)
        
        if relations:
            print(f"   🔗 Relations détectées: {len(relations)}")
            for rel in relations:
                on_delete = f"on_delete={rel['on_delete'].__name__}" if rel['on_delete'] else ""
                print(f"      🤝 {rel['name']} → {rel['related_model']} ({rel['type']}) {on_delete}")
        else:
            print("   🔗 Aucune relation détectée")
            
        # Vérifier spécifiquement la relation avec Agent
        agent_relation = any(rel['related_model'] == 'Agent' for rel in relations)
        if agent_relation:
            print("   ✅ Relation avec Agent existante")
        else:
            print("   ❌ Relation avec Agent manquante")
            
    except Exception as e:
        print(f"   ❌ Erreur analyse relations: {e}")

def analyze_existing_migrations():
    """Analyse les migrations existantes"""
    
    print("\n🔄 ANALYSE DES MIGRATIONS EXISTANTES...")
    
    migrations_dir = BASE_DIR / 'membres' / 'migrations'
    
    if not migrations_dir.exists():
        print("   ❌ Dossier migrations non trouvé")
        return
    
    migration_files = list(migrations_dir.glob('*.py'))
    migration_files = [f for f in migration_files if f.name != '__init__.py']
    
    print(f"   📁 Fichiers de migration: {len(migration_files)}")
    
    # Analyser le dernier fichier de migration
    if migration_files:
        latest_migration = max(migration_files, key=lambda x: x.name)
        print(f"   📅 Dernière migration: {latest_migration.name}")
        
        with open(latest_migration, 'r', encoding='utf-8') as f:
            migration_content = f.read()
        
        # Vérifier les opérations
        if 'migrations.CreateModel' in migration_content:
            print("   🆕 Dernière migration: Création de modèle")
        elif 'migrations.AddField' in migration_content:
            print("   ➕ Dernière migration: Ajout de champs")
        elif 'migrations.AlterField' in migration_content:
            print("   ✏️  Dernière migration: Modification de champs")
        else:
            print("   🔄 Dernière migration: Autre opération")
    
    # Vérifier si des migrations sont en attente
    try:
        from django.core.management import call_command
        from io import StringIO
        import sys
        
        # Capturer la sortie
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        call_command('makemigrations', 'membres', '--dry-run')
        
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        if 'No changes detected' in output:
            print("   ✅ Aucune migration en attente")
        else:
            print("   ⚠️  Migrations en attente détectées")
            
    except Exception as e:
        print(f"   ❌ Erreur vérification migrations: {e}")

def check_member_admin_config():
    """Vérifie la configuration admin existante"""
    
    print("\n⚙️ ANALYSE DE LA CONFIGURATION ADMIN...")
    
    admin_file = BASE_DIR / 'membres' / 'admin.py'
    
    if not admin_file.exists():
        print("   ❌ Fichier admin.py non trouvé")
        return
    
    with open(admin_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'class MembreAdmin' in content:
        print("   ✅ Configuration MembreAdmin trouvée")
        
        # Extraire list_display si présent
        list_display_match = re.search(r"list_display\s*=\s*\[([^\]]+)\]", content)
        if list_display_match:
            fields = list_display_match.group(1)
            print(f"   📋 list_display: [{fields}]")
        else:
            print("   ❌ list_display non configuré")
            
        # Vérifier list_filter
        list_filter_match = re.search(r"list_filter\s*=\s*\[([^\]]+)\]", content)
        if list_filter_match:
            filters = list_filter_match.group(1)
            print(f"   🔍 list_filter: [{filters}]")
            
        # Vérifier search_fields
        search_fields_match = re.search(r"search_fields\s*=\s*\[([^\]]+)\]", content)
        if search_fields_match:
            search_fields = search_fields_match.group(1)
            print(f"   🔎 search_fields: [{search_fields}]")
            
    else:
        print("   ❌ Configuration MembreAdmin non trouvée")

def create_analysis_report():
    """Crée un rapport d'analyse complet"""
    
    report = """
🔍 RAPPORT D'ANALYSE - MODÈLE MEMBRE EXISTANT

📊 ÉTAT ACTUEL DU MODÈLE:

Cette analyse révèle la structure exacte du modèle Membre avant toute modification.
Cela nous permet de:

1. Comprendre l'architecture existante
2. Identifier les éventuels conflits
3. Planifier les modifications de manière sécurisée
4. Préserver les fonctionnalités existantes

🎯 RECOMMANDATIONS POUR LES MODIFICATIONS:

1. AJOUT DES CHAMPS PHOTOS:
   • Vérifier l'espace disque disponible pour le stockage
   • Planifier la migration des données existantes
   • Configurer les permissions de fichiers

2. RELATION AVEC AGENT:
   • Déterminer le comportement on_delete approprié
   • Gérer les membres existants sans agent_createur
   • Mettre à jour les vues et templates

3. MIGRATIONS:
   • Créer une migration séparée pour chaque type de modification
   • Tester la migration sur une copie de la base de données
   • Prévoir un rollback en cas de problème

⚠️  CONSIDÉRATIONS IMPORTANTES:

• Sauvegarder la base de données avant toute modification
• Tester les migrations en environnement de développement
• Vérifier l'impact sur les performances
• Mettre à jour la documentation

🚀 PROCHAINES ÉTAPES:

1. Examiner le rapport d'analyse ci-dessus
2. Planifier les modifications nécessaires
3. Exécuter les scripts de modification étape par étape
4. Tester rigoureusement chaque changement

📝 NOTE:
Cette analyse fournit une base solide pour effectuer les modifications en toute sécurité.
"""
    
    report_file = BASE_DIR / 'RAPPORT_ANALYSE_MODELE_MEMBRE.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📄 Rapport d'analyse sauvegardé: {report_file}")

if __name__ == "__main__":
    analyze_member_model()
    check_member_admin_config()
    create_analysis_report()