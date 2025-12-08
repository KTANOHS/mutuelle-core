# inspect_assureur_safe.py
import os
import django
from django.apps import apps

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Django configuré avec succès")
except Exception as e:
    print(f"⚠️  Attention: {e}")

def inspect_assureur_safe():
    """Inspection SAFE des modèles - sans charger les formulaires"""
    
    print("=" * 80)
    print("🔍 INSPECTION SAFE DES MODÈLES ASSUREUR")
    print("=" * 80)
    
    # Applications cibles
    target_apps = ['membres', 'soins', 'paiements']
    
    for app_name in target_apps:
        try:
            print(f"\n📦 APPLICATION: {app_name.upper()}")
            print("-" * 50)
            
            app_config = apps.get_app_config(app_name)
            models = app_config.get_models()
            
            for model in models:
                print(f"\n🏷️  MODÈLE: {model.__name__}")
                print(f"📊 Table: {model._meta.db_table}")
                
                # Champs réguliers (non-relations)
                print("📍 CHAMPS:")
                for field in model._meta.fields:
                    if not field.is_relation:
                        field_info = f"   • {field.name} ({field.get_internal_type()})"
                        if hasattr(field, 'max_length') and field.max_length:
                            field_info += f" [max_length={field.max_length}]"
                        if field.null:
                            field_info += " [null=True]"
                        if field.blank:
                            field_info += " [blank=True]"
                        print(field_info)
                
                # Relations
                relations = [f for f in model._meta.get_fields() if f.is_relation]
                if relations:
                    print("🔗 RELATIONS:")
                    for rel in relations:
                        if rel.related_model:
                            rel_type = "ForeignKey"
                            if rel.many_to_many:
                                rel_type = "ManyToMany"
                            elif rel.one_to_one:
                                rel_type = "OneToOne"
                            print(f"   • {rel.name} ({rel_type} -> {rel.related_model.__name__})")
                        
        except Exception as e:
            print(f"❌ Erreur avec {app_name}: {e}")

def get_soin_model_details():
    """Détails spécifiques du modèle Soin"""
    print("\n" + "=" * 80)
    print("🔬 DÉTAILS DU MODÈLE SOIN")
    print("=" * 80)
    
    try:
        Soin = apps.get_model('soins', 'Soin')
        
        print("📋 TOUS LES CHAMPS EXISTANTS:")
        for field in Soin._meta.get_fields():
            field_info = f"   • {field.name} ({type(field).__name__})"
            
            # Ajouter des détails selon le type de champ
            if hasattr(field, 'max_length') and field.max_length:
                field_info += f" [max_length={field.max_length}]"
            if field.null:
                field_info += " [null=True]"
            if field.blank:
                field_info += " [blank=True]"
            if hasattr(field, 'choices') and field.choices:
                field_info += f" [choices: {len(field.choices)} options]"
            
            print(field_info)
            
    except Exception as e:
        print(f"❌ Impossible de charger le modèle Soin: {e}")

def generate_correct_soinform_code():
    """Génère le code CORRECT pour SoinForm basé sur le modèle réel"""
    
    print("\n" + "=" * 80)
    print("💡 CODE CORRECT POUR SoinForm")
    print("=" * 80)
    
    try:
        Soin = apps.get_model('soins', 'Soin')
        
        # Champs disponibles dans le modèle Soin (exclure les champs techniques)
        exclude_fields = ['id', 'created_at', 'updated_at', 'created_by']
        available_fields = []
        
        for field in Soin._meta.fields:
            if field.name not in exclude_fields and not field.primary_key:
                available_fields.append(field.name)
        
        print("```python")
        print("# Dans assureur/forms.py - REMPLACEZ le SoinForm existant par ceci:")
        print("class SoinForm(forms.ModelForm):")
        print("    \"\"\"Formulaire pour le modèle Soin - VERSION CORRECTE\"\"\"")
        print("    ")
        print("    class Meta:")
        print("        model = Soin")
        print(f"        fields = {available_fields}")
        print("        widgets = {")
        
        # Widgets recommandés basés sur le type de champ
        for field in Soin._meta.fields:
            if field.name in available_fields:
                internal_type = field.get_internal_type()
                
                if field.name in ['date_soin', 'date_realisation', 'date_validation']:
                    print(f"            '{field.name}': forms.DateInput(attrs={{'type': 'date'}}),")
                elif internal_type == 'TextField' or (internal_type == 'CharField' and field.max_length and field.max_length > 100):
                    print(f"            '{field.name}': forms.Textarea(attrs={{'rows': 3}}),")
                elif internal_type in ['DecimalField', 'FloatField']:
                    print(f"            '{field.name}': forms.NumberInput(attrs={{'step': '0.01'}}),")
                elif internal_type == 'IntegerField':
                    print(f"            '{field.name}': forms.NumberInput(attrs={{'step': '1'}}),")
        
        print("        }")
        print("        labels = {")
        
        # Labels français
        french_labels = {
            'patient': 'Patient',
            'type_soin': 'Type de soin',
            'date_soin': 'Date du soin',
            'date_realisation': 'Date de réalisation',
            'medecin': 'Médecin',
            'diagnostic': 'Diagnostic',
            'observations': 'Observations',
            'duree_sejour': 'Durée de séjour (jours)',
            'cout_estime': 'Coût estimé (FCFA)',
            'cout_reel': 'Coût réel (FCFA)',
            'taux_prise_charge': 'Taux de prise en charge (%)',
            'statut': 'Statut',
            'valide_par': 'Validé par',
            'date_validation': 'Date de validation',
            'motif_refus': 'Motif de refus',
        }
        
        for field_name in available_fields:
            if field_name in french_labels:
                print(f"            '{field_name}': '{french_labels[field_name]}',")
        
        print("        }")
        print("```")
        
    except Exception as e:
        print(f"❌ Impossible de générer le code: {e}")

def check_problematic_fields():
    """Identifie les champs problématiques dans les formulaires"""
    
    print("\n" + "=" * 80)
    print("🚨 CHAMPS PROBLÉMATIQUES DANS SoinForm")
    print("=" * 80)
    
    try:
        Soin = apps.get_model('soins', 'Soin')
        
        # Champs qui existent réellement dans le modèle
        real_fields = [f.name for f in Soin._meta.get_fields()]
        
        # Champs qui causent des erreurs dans l'ancien formulaire
        problematic_fields = ['description', 'notes', 'documents']
        
        print("Champs qui EXISTENT dans le modèle Soin:")
        for field in real_fields[:15]:  # Afficher les premiers 15
            print(f"   ✅ {field}")
        
        print(f"\nChamps qui CAUSENT des erreurs (à supprimer):")
        for field in problematic_fields:
            if field not in real_fields:
                print(f"   ❌ {field} - N'EXISTE PAS dans le modèle")
            else:
                print(f"   ⚠️  {field} - Existe mais peut-être mal utilisé")
                
        print(f"\n💡 Solution: Utilisez 'observations' au lieu de 'description' et 'notes'")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("🛡️  Lancement de l'inspection SAFE...")
    
    # 1. Inspection safe des modèles
    inspect_assureur_safe()
    
    # 2. Détails du modèle Soin
    get_soin_model_details()
    
    # 3. Identification des problèmes
    check_problematic_fields()
    
    # 4. Code correct
    generate_correct_soinform_code()
    
    print("\n" + "=" * 80)
    print("✅ INSPECTION SAFE TERMINÉE")
    print("=" * 80)
    print("\n💡 Conseil immédiat:")
    print("1. Ouvrez assureur/forms.py")
    print("2. REMPLACEZ le SoinForm existant par le code généré ci-dessus")
    print("3. Supprimez les références aux champs: 'description', 'notes', 'documents'")