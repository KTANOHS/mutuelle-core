#!/usr/bin/env python
"""
Script de vérification du système Paiement pour l'assureur
Vérifie la cohérence entre Modèle, Formulaire et Vue
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps
from django.db import connection
from django.core.exceptions import FieldDoesNotExist
import inspect

print("🔍 VÉRIFICATION SYSTÈME PAIEMENT ASSUREUR")
print("=" * 60)

# ============================================================================
# 1. VÉRIFICATION DU MODÈLE
# ============================================================================
print("\n📦 1. VÉRIFICATION DU MODÈLE 'Paiement'")
print("-" * 40)

try:
    # Récupérer le modèle
    Paiement = apps.get_model('assureur', 'Paiement')
    print(f"✅ Modèle trouvé: {Paiement}")
    
    # Vérifier les champs
    print(f"\n📋 Champs du modèle:")
    for field in Paiement._meta.fields:
        print(f"  - {field.name}: {field.__class__.__name__}")
        if hasattr(field, 'choices') and field.choices:
            print(f"    Choix: {field.choices}")
    
    # Vérifier spécifiquement le champ mode_paiement
    try:
        mode_field = Paiement._meta.get_field('mode_paiement')
        print(f"\n🎯 Champ 'mode_paiement' spécifique:")
        print(f"  Type: {mode_field.__class__.__name__}")
        print(f"  Max length: {getattr(mode_field, 'max_length', 'N/A')}")
        
        if hasattr(mode_field, 'choices') and mode_field.choices:
            print(f"  Choix disponibles:")
            for value, label in mode_field.choices:
                print(f"    '{value}' -> '{label}'")
            
            # Vérifier la présence de 'espece'
            choix_values = [choice[0] for choice in mode_field.choices]
            if 'espece' in choix_values:
                print(f"  ✅ 'espece' est présent dans les choix")
            else:
                print(f"  ❌ 'espece' NON TROUVÉ dans les choix!")
                print(f"     Choix disponibles: {choix_values}")
        else:
            print(f"  ⚠️  Aucun choix défini pour mode_paiement")
            
    except FieldDoesNotExist:
        print(f"  ❌ Champ 'mode_paiement' non trouvé dans le modèle")
    
    # Vérifier les contraintes et relations
    print(f"\n🔗 Relations du modèle:")
    for field in Paiement._meta.related_objects:
        print(f"  - {field.name}: {field.related_model}")
        
except LookupError:
    print(f"❌ Modèle 'Paiement' non trouvé dans l'application 'assureur'")
    print(f"   Applications disponibles: {[app.label for app in apps.get_app_configs()]}")

# ============================================================================
# 2. VÉRIFICATION DU FORMULAIRE
# ============================================================================
print("\n📝 2. VÉRIFICATION DU FORMULAIRE 'PaiementForm'")
print("-" * 40)

try:
    # Essayer d'importer le formulaire
    from assureur.forms import PaiementForm
    
    print(f"✅ Formulaire trouvé: {PaiementForm}")
    
    # Vérifier la classe Meta
    if hasattr(PaiementForm, 'Meta'):
        meta = PaiementForm.Meta
        print(f"\n📄 Configuration Meta:")
        print(f"  Modèle: {getattr(meta, 'model', 'Non spécifié')}")
        print(f"  Champs: {getattr(meta, 'fields', 'Non spécifié')}")
        print(f"  Exclusions: {getattr(meta, 'exclude', 'Aucune')}")
    
    # Vérifier les champs du formulaire
    print(f"\n📋 Champs du formulaire:")
    for field_name, field in PaiementForm.base_fields.items():
        print(f"  - {field_name}: {field.__class__.__name__}")
        
        # Vérifier les choix pour mode_paiement
        if field_name == 'mode_paiement':
            if hasattr(field, 'choices'):
                print(f"    Choix dans le formulaire:")
                if callable(field.choices):
                    choices = field.choices()
                else:
                    choices = field.choices
                
                for value, label in choices:
                    print(f"      '{value}' -> '{label}'")
                
                # Vérifier 'espece'
                if callable(field.choices):
                    choix_list = [(v, l) for v, l in field.choices()]
                else:
                    choix_list = list(field.choices)
                    
                choix_values = [choice[0] for choice in choix_list if choice[0]]
                
                if 'espece' in choix_values:
                    print(f"    ✅ 'espece' présent dans le formulaire")
                else:
                    print(f"    ❌ 'espece' NON TROUVÉ dans le formulaire!")
    
    # Tester le formulaire avec des données
    print(f"\n🧪 Test de validation du formulaire:")
    test_data = {
        'mode_paiement': 'espece',
        # Ajouter d'autres champs requis ici
    }
    
    form = PaiementForm(data=test_data)
    print(f"  Formulaire valide: {form.is_valid()}")
    if not form.is_valid():
        print(f"  Erreurs: {form.errors}")
        
except ImportError as e:
    print(f"❌ Impossible d'importer PaiementForm: {e}")
    print(f"   Vérifiez le fichier forms.py dans l'application assureur")
except Exception as e:
    print(f"❌ Erreur lors de l'analyse du formulaire: {e}")

# ============================================================================
# 3. VÉRIFICATION DES VUES
# ============================================================================
print("\n🖥️  3. VÉRIFICATION DES VUES")
print("-" * 40)

try:
    from assureur import views
    
    print(f"✅ Module views trouvé: {views}")
    
    # Chercher les vues liées à Paiement
    paiement_views = []
    for name, obj in inspect.getmembers(views):
        if inspect.isclass(obj) or inspect.isfunction(obj):
            # Vérifier si c'est une vue (nom contenant 'paiement' ou 'Paiement')
            if 'paiement' in name.lower():
                paiement_views.append((name, obj))
    
    print(f"\n🔍 Vues liées aux paiements:")
    if paiement_views:
        for name, view in paiement_views:
            print(f"  - {name}: {view}")
            
            # Essayer d'inspecter les paramètres pour les vues basées sur les classes
            if inspect.isclass(view):
                # Vérifier si c'est une CreateView, UpdateView, etc.
                if hasattr(view, 'form_class'):
                    print(f"    Formulaire: {view.form_class}")
                if hasattr(view, 'model'):
                    print(f"    Modèle: {view.model}")
                if hasattr(view, 'fields'):
                    print(f"    Champs: {view.fields}")
    else:
        print(f"  ℹ️  Aucune vue spécifique 'paiement' trouvée")
        
except ImportError as e:
    print(f"❌ Impossible d'importer les views: {e}")

# ============================================================================
# 4. VÉRIFICATION DE LA BASE DE DONNÉES
# ============================================================================
print("\n🗄️  4. VÉRIFICATION DE LA BASE DE DONNÉES")
print("-" * 40)

try:
    with connection.cursor() as cursor:
        # Vérifier si la table existe
        table_name = Paiement._meta.db_table
        cursor.execute(f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        print(f"📊 Structure de la table '{table_name}':")
        for col in columns:
            print(f"  - {col[0]}: {col[1]} (Nullable: {col[2]})")
            
except Exception as e:
    print(f"❌ Erreur lors de la vérification de la base: {e}")

# ============================================================================
# 5. TEST COMPLET D'UN PAIEMENT
# ============================================================================
print("\n🧪 5. TEST COMPLET D'UN PAIEMENT")
print("-" * 40)

try:
    from django.contrib.auth.models import User
    from django.utils import timezone
    
    # Créer un utilisateur de test
    test_user, created = User.objects.get_or_create(
        username='test_user_paiement',
        defaults={'email': 'test@example.com', 'password': 'testpass123'}
    )
    
    # Créer un paiement de test
    print("Création d'un paiement de test...")
    
    paiement_data = {
        'mode_paiement': 'espece',
        'montant': 100.00,
        'date_paiement': timezone.now(),
        # Ajouter d'autres champs requis
    }
    
    # Essayer de créer l'instance
    try:
        paiement = Paiement(**paiement_data)
        paiement.save()
        print(f"✅ Paiement créé avec succès! ID: {paiement.id}")
        print(f"   Mode de paiement: {paiement.mode_paiement}")
        
        # Nettoyer
        paiement.delete()
        print(f"✅ Paiement de test supprimé")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        
except Exception as e:
    print(f"❌ Erreur lors du test: {e}")

# ============================================================================
# 6. RÉCAPITULATIF ET RECOMMANDATIONS
# ============================================================================
print("\n📋 6. RÉCAPITULATIF")
print("-" * 40)

print(""\
"Recommandations:
1. Vérifiez que 'espece' est dans les choix de mode_paiement dans models.py
2. Assurez-vous que le formulaire utilise les choix du modèle
3. Vérifiez les migrations: python manage.py makemigrations && python manage.py migrate
4. Testez avec: python manage.py shell < test_formulaire_paiement.py

Problèmes courants:
- Choix différents entre modèle et formulaire
- Migrations non appliquées
- Valeurs de test qui ne correspondent pas exactement aux choix
""")

print("=" * 60)
print("✅ Vérification terminée")