#!/usr/bin/env python3
"""
Script de récupération des données CORRIGÉ pour restaurer le système
"""

import os
import django
import sys
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps
from django.contrib.auth import get_user_model

def create_test_data():
    """Crée des données de test pour restaurer le système - VERSION CORRIGÉE"""
    print("🔧 CRÉATION DE DONNÉES DE TEST POUR RÉCUPÉRATION")
    print("=" * 60)
    
    User = get_user_model()
    
    try:
        # 1. Récupérer les modèles
        Membre = apps.get_model('membres', 'Membre')
        Medecin = apps.get_model('medecin', 'Medecin')
        Soin = apps.get_model('soins', 'Soin')
        
        # Essayer différents noms pour Ordonnance
        try:
            Ordonnance = apps.get_model('soins', 'Ordonnance')
        except LookupError:
            try:
                Ordonnance = apps.get_model('medecin', 'Ordonnance')
            except LookupError:
                Ordonnance = None
                print("⚠️  Modèle Ordonnance non trouvé")
        
        try:
            Paiement = apps.get_model('paiements', 'Paiement')
        except LookupError:
            Paiement = None
            print("⚠️  Modèle Paiement non trouvé")
        
        print("✅ Modèles chargés")
        
        # 2. Vérifier les données existantes
        membres_count = Membre.objects.count()
        medecins_count = Medecin.objects.count()
        
        print(f"📊 Données existantes - Membres: {membres_count}, Médecins: {medecins_count}")
        
        if membres_count == 0 or medecins_count == 0:
            print("❌ Données insuffisantes pour créer des données de test")
            return False
        
        # 3. Récupérer les objets avec leurs relations CORRECTES
        membre = Membre.objects.first()
        medecin = Medecin.objects.first()
        
        # CORRECTION: Utiliser l'user du médecin, pas le médecin directement
        user_medecin = medecin.user
        
        print(f"👤 Membre sélectionné: {membre.nom} {membre.prenom}")
        print(f"🩺 Médecin sélectionné: {medecin.user.get_full_name()}")
        
        # 4. Créer des soins de test - CORRIGÉ
        print("\n🏥 CRÉATION DE SOINS DE TEST:")
        soin_data = [
            {'type_soin': 'Consultation générale', 'montant': 5000, 'description': 'Consultation de routine'},
            {'type_soin': 'Radio pulmonaire', 'montant': 15000, 'description': 'Examen radiologique'},
            {'type_soin': 'Analyse sanguine', 'montant': 8000, 'description': 'Bilan sanguin complet'},
        ]
        
        soins_created = 0
        for data in soin_data:
            try:
                # CORRECTION: Vérifier la structure exacte du modèle Soin
                soin_kwargs = {
                    'membre': membre,
                    'type_soin': data['type_soin'],
                    'montant': data['montant'],
                    'date_soin': datetime.now().date(),
                    'statut': 'TERMINE'
                }
                
                # Ajouter medecin ou user_medecin selon la structure
                if hasattr(Soin, 'medecin'):
                    soin_kwargs['medecin'] = medecin
                elif hasattr(Soin, 'user_medecin'):
                    soin_kwargs['user_medecin'] = user_medecin
                elif hasattr(Soin, 'medecin_user'):
                    soin_kwargs['medecin_user'] = user_medecin
                
                soin, created = Soin.objects.get_or_create(
                    membre=membre,
                    type_soin=data['type_soin'],
                    defaults=soin_kwargs
                )
                if created:
                    soins_created += 1
                    print(f"   ✅ Soin créé: {data['type_soin']} - {data['montant']} FCFA")
                else:
                    print(f"   ℹ️  Soin existe déjà: {data['type_soin']}")
                    
            except Exception as e:
                print(f"   ❌ Erreur création soin {data['type_soin']}: {e}")
        
        print(f"🎯 Soins créés: {soins_created}")
        
        # 5. Créer des ordonnances de test - CORRIGÉ
        if Ordonnance:
            print("\n💊 CRÉATION D'ORDONNANCES DE TEST:")
            try:
                ordonnance_kwargs = {
                    'date_prescription': datetime.now().date(),
                    'notes': 'Ordonnance de test pour récupération système'
                }
                
                # Adapter selon la structure du modèle
                if hasattr(Ordonnance, 'medecin'):
                    ordonnance_kwargs['medecin'] = medecin
                if hasattr(Ordonnance, 'membre'):
                    ordonnance_kwargs['membre'] = membre
                if hasattr(Ordonnance, 'patient'):
                    ordonnance_kwargs['patient'] = membre
                
                ordonnance, created = Ordonnance.objects.get_or_create(
                    medecin=medecin,
                    membre=membre,
                    date_prescription=datetime.now().date(),
                    defaults=ordonnance_kwargs
                )
                if created:
                    print("   ✅ Ordonnance de test créée")
                else:
                    print("   ℹ️  Ordonnance existe déjà")
            except Exception as e:
                print(f"   ⚠️  Impossible de créer ordonnance: {e}")
        
        # 6. Créer des paiements de test - CORRIGÉ
        if Paiement and Soin.objects.exists():
            print("\n💰 CRÉATION DE PAIEMENTS DE TEST:")
            paiements_created = 0
            
            for soin in Soin.objects.all()[:2]:  # Payer les 2 premiers soins
                try:
                    paiement_kwargs = {
                        'membre': membre,
                        'montant': soin.montant,
                        'date_paiement': datetime.now().date(),
                        'statut': 'PAYE'
                    }
                    
                    # Adapter selon la structure
                    if hasattr(Paiement, 'methode_paiement'):
                        paiement_kwargs['methode_paiement'] = 'ESPECES'
                    if hasattr(Paiement, 'soin'):
                        paiement_kwargs['soin'] = soin
                    
                    paiement, created = Paiement.objects.get_or_create(
                        membre=membre,
                        montant=soin.montant,
                        date_paiement=datetime.now().date(),
                        defaults=paiement_kwargs
                    )
                    if created:
                        paiements_created += 1
                        print(f"   ✅ Paiement créé: {soin.montant} FCFA pour {soin.type_soin}")
                    else:
                        print(f"   ℹ️  Paiement existe déjà pour {soin.type_soin}")
                        
                except Exception as e:
                    print(f"   ❌ Erreur création paiement: {e}")
            
            print(f"🎯 Paiements créés: {paiements_created}")
        
        # 7. Résumé final
        print(f"\n📈 RÉSUMÉ DE LA RÉCUPÉRATION:")
        print(f"   👥 Membres: {Membre.objects.count()}")
        print(f"   🩺 Médecins: {Medecin.objects.count()}")
        print(f"   🏥 Soins: {Soin.objects.count()}")
        if Ordonnance:
            print(f"   💊 Ordonnances: {Ordonnance.objects.count()}")
        if Paiement:
            print(f"   💰 Paiements: {Paiement.objects.count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données de test: {e}")
        import traceback
        traceback.print_exc()
        return False

def analyze_model_structure():
    """Analyse la structure des modèles pour comprendre les relations"""
    print("\n🔍 ANALYSE DE LA STRUCTURE DES MODÈLES")
    print("-" * 50)
    
    models_to_analyze = [
        ('membres', 'Membre'),
        ('medecin', 'Medecin'),
        ('soins', 'Soin'),
        ('paiements', 'Paiement')
    ]
    
    for app, model_name in models_to_analyze:
        try:
            model = apps.get_model(app, model_name)
            print(f"\n📋 {app}.{model_name}:")
            
            # Afficher les champs
            fields = model._meta.get_fields()
            for field in fields:
                field_info = f"   - {field.name} ({field.get_internal_type()})"
                
                if hasattr(field, 'related_model') and field.related_model:
                    field_info += f" → {field.related_model._meta.model_name}"
                
                print(field_info)
                
        except LookupError:
            print(f"❌ {app}.{model_name}: Modèle non trouvé")

def verify_system_integrity():
    """Vérifie l'intégrité du système après récupération"""
    print("\n🔍 VÉRIFICATION DE L'INTÉGRITÉ DU SYSTÈME")
    print("-" * 50)
    
    models_to_check = [
        ('membres', 'Membre'),
        ('medecin', 'Medecin'), 
        ('soins', 'Soin'),
        ('paiements', 'Paiement')
    ]
    
    # Essayer différents noms pour Ordonnance
    ordonnance_models = [
        ('soins', 'Ordonnance'),
        ('medecin', 'Ordonnance'),
        ('ordonnances', 'Ordonnance')
    ]
    
    all_ok = True
    for app, model_name in models_to_check:
        try:
            model = apps.get_model(app, model_name)
            count = model.objects.count()
            status = "✅" if count > 0 else "❌"
            print(f"   {status} {app}.{model_name}: {count}")
            
            if count == 0 and model_name in ['Soin', 'Paiement']:
                all_ok = False
                
        except LookupError:
            print(f"   ❌ {app}.{model_name}: Modèle non trouvé")
            all_ok = False
    
    # Vérifier les ordonnances
    ordonnance_found = False
    for app, model_name in ordonnance_models:
        try:
            model = apps.get_model(app, model_name)
            count = model.objects.count()
            status = "✅" if count > 0 else "⚠️ "
            print(f"   {status} {app}.{model_name}: {count}")
            ordonnance_found = True
            break
        except LookupError:
            continue
    
    if not ordonnance_found:
        print("   ⚠️  Aucun modèle Ordonnance trouvé")
    
    return all_ok

def main():
    print("🩺 SCRIPT DE RÉCUPÉRATION DU SYSTÈME MÉDICAL (CORRIGÉ)")
    print("=" * 60)
    
    # 0. Analyser d'abord la structure
    analyze_model_structure()
    
    # 1. Créer les données de test
    success = create_test_data()
    
    # 2. Vérifier l'intégrité
    integrity_ok = verify_system_integrity()
    
    # 3. Résultat final
    print(f"\n🎯 RÉSULTAT DE LA RÉCUPÉRATION:")
    if success and integrity_ok:
        print("✅ RÉCUPÉRATION RÉUSSIE!")
        print("   Le système a été restauré avec des données de test")
        print("   Vous pouvez maintenant tester les fonctionnalités")
    else:
        print("❌ RÉCUPÉRATION PARTIELLE")
        print("   Certaines données n'ont pas pu être créées")
        print("   Vérifiez la configuration des modèles")
    
    print("\n🔧 PROCHAINES ÉTAPES:")
    print("1. Testez le dashboard médecin: http://127.0.0.1:8000/medecin/")
    print("2. Testez le dashboard membre: http://127.0.0.1:8000/membres/dashboard/")
    print("3. Vérifiez la création de soins et paiements")

if __name__ == "__main__":
    main()