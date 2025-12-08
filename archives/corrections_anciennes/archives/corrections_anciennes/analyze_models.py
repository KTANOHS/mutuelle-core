import os
import django
from django.apps import apps
from django.db import models

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyze_all_models():
    """
    Analyse tous les modèles Django du projet et génère un rapport détaillé
    """
    print("=" * 80)
    print("ANALYSE COMPLÈTE DES MODÈLES DJANGO")
    print("=" * 80)
    
    all_models = apps.get_models()
    
    rapport = {
        'total_modeles': 0,
        'modeles_avec_statut': 0,
        'modeles_sans_statut': [],
        'champs_par_modele': {},
        'erreurs_potentielles': []
    }
    
    for model in all_models:
        rapport['total_modeles'] += 1
        app_label = model._meta.app_label
        model_name = model._meta.model_name
        full_name = f"{app_label}.{model_name}"
        
        print(f"\n🔍 Analyse du modèle: {full_name}")
        print("-" * 50)
        
        # Récupérer tous les champs
        fields = model._meta.get_fields()
        field_names = [field.name for field in fields]
        
        # Stocker les informations des champs
        rapport['champs_par_modele'][full_name] = {
            'champs': field_names,
            'total_champs': len(field_names)
        }
        
        # Afficher tous les champs disponibles
        print("📋 Champs disponibles:")
        for field in fields:
            field_type = type(field).__name__
            if isinstance(field, models.ForeignKey):
                related_model = field.related_model
                related_name = f" -> {related_model._meta.app_label}.{related_model._meta.model_name}"
            else:
                related_name = ""
            print(f"   - {field.name} ({field_type}){related_name}")
        
        # Vérifier la présence du champ 'statut'
        has_statut = any(field.name == 'statut' for field in fields)
        
        if has_statut:
            rapport['modeles_avec_statut'] += 1
            print("✅ Champ 'statut' trouvé!")
            
            # Analyser le champ statut spécifiquement
            statut_field = next(field for field in fields if field.name == 'statut')
            if hasattr(statut_field, 'choices') and statut_field.choices:
                print(f"   📊 Choices disponibles: {statut_field.choices}")
        else:
            rapport['modeles_sans_statut'].append(full_name)
            print("❌ Champ 'statut' NON trouvé!")
            
            # Vérifier les champs similaires qui pourraient être utilisés comme statut
            champs_similaires = [f for f in field_names if any(keyword in f.lower() for keyword in 
                            ['status', 'state', 'etat', 'phase', 'stage', 'type'])]
            if champs_similaires:
                print(f"   💡 Champs similaires potentiels: {champs_similaires}")
    
    # Générer le rapport final
    print("\n" + "=" * 80)
    print("📊 RAPPORT FINAL")
    print("=" * 80)
    
    print(f"📈 Total des modèles analysés: {rapport['total_modeles']}")
    print(f"✅ Modèles avec champ 'statut': {rapport['modeles_avec_statut']}")
    print(f"❌ Modèles SANS champ 'statut': {len(rapport['modeles_sans_statut'])}")
    
    if rapport['modeles_sans_statut']:
        print("\n📋 Modèles sans champ 'statut':")
        for modele in rapport['modeles_sans_statut']:
            print(f"   - {modele}")
            
            # Suggestions basées sur le nom du modèle
            if 'pharmacien' in modele.lower() or 'validation' in modele.lower():
                print(f"     💡 SUGGESTION: Ce modèle pourrait avoir besoin d'un champ 'statut'")
    
    # Rechercher les modèles problématiques basés sur l'erreur originale
    print("\n🔎 RECHERCHE DES MODÈLES PROBLÉMATIQUES")
    print("-" * 50)
    
    # Les champs mentionnés dans l'erreur
    champs_erreur = ['bon_de_soin', 'bon_de_soin_id', 'date_creation', 'duree', 'id', 'instructions', 'medicament', 'posologie']
    
    for model in all_models:
        field_names = [field.name for field in model._meta.get_fields()]
        
        # Vérifier si ce modèle correspond aux champs de l'erreur
        correspondance = sum(1 for champ in champs_erreur if champ in field_names)
        
        if correspondance >= 5:  # Au moins 5 champs correspondent
            print(f"⚠️  Modèle suspecté: {model._meta.app_label}.{model._meta.model_name}")
            print(f"   Correspondance: {correspondance}/8 champs de l'erreur")
            print(f"   Champ 'statut' présent: {'statut' in field_names}")
            
            if 'statut' not in field_names:
                print("   🚨 ACTION REQUISE: Ajouter le champ 'statut' à ce modèle")
                
                # Générer le code pour ajouter le champ statut
                print("\n   💻 CODE POUR CORRIGER:")
                print(f"   class {model._meta.model_name}(models.Model):")
                print("       STATUT_CHOICES = [")
                print("           ('en_attente', 'En attente'),")
                print("           ('valide', 'Validé'),")
                print("           ('refuse', 'Refusé'),")
                print("           ('termine', 'Terminé'),")
                print("       ]")
                print("       statut = models.CharField(")
                print("           max_length=20,")
                print("           choices=STATUT_CHOICES,")
                print("           default='en_attente'")
                print("       )")
                print("       # ... autres champs existants ...")

def find_model_by_fields(target_fields):
    """
    Trouve les modèles qui contiennent des champs spécifiques
    """
    print(f"\n🔍 RECHERCHE DE MODÈLES AVEC LES CHAMPS: {target_fields}")
    
    for model in apps.get_models():
        field_names = [field.name for field in model._meta.get_fields()]
        
        if all(field in field_names for field in target_fields):
            print(f"✅ MODÈLE TROUVÉ: {model._meta.app_label}.{model._meta.model_name}")
            print(f"   Champs: {field_names}")
            return model
    
    print("❌ Aucun modèle trouvé avec tous ces champs")
    return None

def generate_migration_fix():
    """
    Génère le code pour créer une migration de correction
    """
    print("\n" + "=" * 80)
    print("🛠️  GÉNÉRATION DE LA MIGRATION DE CORRECTION")
    print("=" * 80)
    
    print("""
# Créer un fichier dans votre application concernée, par exemple:
# pharmacien/migrations/0002_add_statut_field.py

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('pharmacien', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='votremodele',  # Remplacez par le nom réel du modèle
            name='statut',
            field=models.CharField(
                choices=[
                    ('en_attente', 'En attente'),
                    ('valide', 'Validé'),
                    ('refuse', 'Refusé'),
                    ('termine', 'Terminé'),
                ],
                default='en_attente',
                max_length=20,
            ),
        ),
    ]
    """)

if __name__ == "__main__":
    # Analyse complète
    analyze_all_models()
    
    # Recherche spécifique du modèle problématique
    champs_problematiques = ['bon_de_soin', 'date_creation', 'medicament', 'posologie']
    model_trouve = find_model_by_fields(champs_problematiques)
    
    # Génération de la solution
    generate_migration_fix()
    
    print("\n🎯 PROCHAINES ÉTAPES:")
    print("1. Identifiez le modèle exact qui cause l'erreur")
    print("2. Ajoutez le champ 'statut' au modèle concerné")
    print("3. Créez et appliquez les migrations: python manage.py makemigrations && python manage.py migrate")
    print("4. Testez le tableau de bord pharmacien")