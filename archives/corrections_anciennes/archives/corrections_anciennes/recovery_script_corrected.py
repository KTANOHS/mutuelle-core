#!/usr/bin/env python3
"""
Diagnostic spécifique des relations entre modèles
"""

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps

def diagnose_relations():
    """Diagnostique les relations entre les modèles"""
    print("🔗 DIAGNOSTIC DES RELATIONS ENTRE MODÈLES")
    print("=" * 60)
    
    # Analyser le modèle Soin
    try:
        Soin = apps.get_model('soins', 'Soin')
        print(f"\n🏥 STRUCTURE DU MODÈLE SOIN:")
        for field in Soin._meta.get_fields():
            field_type = field.get_internal_type()
            field_info = f"   {field.name} ({field_type})"
            
            if hasattr(field, 'related_model') and field.related_model:
                field_info += f" → {field.related_model._meta.model_label}"
            
            print(field_info)
            
    except LookupError:
        print("❌ Modèle Soin non trouvé")
    
    # Analyser le modèle Medecin
    try:
        Medecin = apps.get_model('medecin', 'Medecin')
        print(f"\n🩺 STRUCTURE DU MODÈLE MEDECIN:")
        for field in Medecin._meta.get_fields():
            if field.name == 'user':
                print(f"   {field.name} → {field.related_model._meta.model_label}")
                break
    except LookupError:
        print("❌ Modèle Medecin non trouvé")
    
    # Tester la création manuelle
    print(f"\n🧪 TEST MANUEL DE CRÉATION:")
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        Membre = apps.get_model('membres', 'Membre')
        Medecin = apps.get_model('medecin', 'Medecin')
        Soin = apps.get_model('soins', 'Soin')
        
        membre = Membre.objects.first()
        medecin = Medecin.objects.first()
        
        print(f"   Membre: {membre}")
        print(f"   Medecin: {medecin}")
        print(f"   User du médecin: {medecin.user}")
        
        # Tester différentes signatures
        soin_params = [
            {'membre': membre, 'medecin': medecin},
            {'membre': membre, 'user_medecin': medecin.user},
            {'patient': membre, 'medecin': medecin},
        ]
        
        for params in soin_params:
            print(f"   Testing: {params}")
        
    except Exception as e:
        print(f"   ❌ Erreur test: {e}")

if __name__ == "__main__":
    diagnose_relations()