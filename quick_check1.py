#!/usr/bin/env python
"""
Diagnostic rapide du problème de paiement
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps

print("🔍 DIAGNOSTIC RAPIDE PAIEMENT")
print("=" * 50)

try:
    # 1. Modèle
    Paiement = apps.get_model('assureur', 'Paiement')
    mode_field = Paiement._meta.get_field('mode_paiement')
    
    print("📦 MODÈLE:")
    if hasattr(mode_field, 'choices') and mode_field.choices:
        print(f"  Choix dans le modèle:")
        for value, label in mode_field.choices:
            print(f"    - '{value}' : '{label}'")
        
        # Vérifier 'espece'
        choix_values = [choice[0] for choice in mode_field.choices]
        if 'espece' in choix_values:
            print(f"  ✅ 'espece' présent dans le modèle")
        else:
            print(f"  ❌ PROBLÈME: 'espece' absent du modèle")
            print(f"     Valeurs acceptées: {choix_values}")
    
    # 2. Formulaire
    print("\n📝 FORMULAIRE:")
    try:
        from assureur.forms import PaiementForm
        
        form_field = PaiementForm.base_fields.get('mode_paiement')
        if form_field and hasattr(form_field, 'choices'):
            if callable(form_field.choices):
                form_choices = form_field.choices()
            else:
                form_choices = form_field.choices
            
            print(f"  Choix dans le formulaire:")
            form_values = []
            for value, label in form_choices:
                if value:  # Ignorer les valeurs vides
                    print(f"    - '{value}' : '{label}'")
                    form_values.append(value)
            
            if 'espece' in form_values:
                print(f"  ✅ 'espece' présent dans le formulaire")
            else:
                print(f"  ❌ PROBLÈME: 'espece' absent du formulaire")
                print(f"     Valeurs dans le formulaire: {form_values}")
    except ImportError:
        print("  ⚠️  Formulaire PaiementForm non trouvé")
    
    # 3. Test de validation
    print("\n🧪 TEST DE VALIDATION:")
    test_data = {'mode_paiement': 'espece'}
    
    # Ajouter d'autres champs requis si nécessaire
    for field in Paiement._meta.fields:
        if field.name != 'mode_paiement' and not field.null and not field.blank:
            if field.__class__.__name__ == 'CharField':
                test_data[field.name] = 'test'
            elif field.__class__.__name__ == 'DecimalField':
                test_data[field.name] = 100.00
            elif field.__class__.__name__ == 'DateField':
                from django.utils import timezone
                test_data[field.name] = timezone.now().date()
    
    form = PaiementForm(data=test_data)
    print(f"  Formulaire valide: {form.is_valid()}")
    if not form.is_valid():
        print(f"  Erreurs: {form.errors}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")

print("\n" + "=" * 50)