#!/usr/bin/env python3
"""
Script de récupération des données pour restaurer le système
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
from django.utils import timezone

def create_test_data():
    """Crée des données de test pour restaurer le système"""
    print("🔧 CRÉATION DE DONNÉES DE TEST POUR RÉCUPÉRATION")
    print("=" * 60)
    
    User = get_user_model()
    
    try:
        # 1. Récupérer les modèles
        Membre = apps.get_model('membres', 'Membre')
        Medecin = apps.get_model('medecin', 'Medecin')
        Soin = apps.get_model('soins', 'Soin')
        Ordonnance = apps.get_model('soins', 'Ordonnance')  # ou 'medecin', 'Ordonnance'
        Paiement = apps.get_model('paiements', 'Paiement')
        
        print("✅ Modèles chargés")
        
        # 2. Vérifier les données existantes
        membres_count = Membre.objects.count()
        medecins_count = Medecin.objects.count()
        
        print(f"📊 Données existantes - Membres: {membres_count}, Médecins: {medecins_count}")
        
        if membres_count == 0 or medecins_count == 0:
            print("❌ Données insuffisantes pour créer des données de test")
            return False
        
        # 3. Créer des soins de test
        print("\n🏥 CRÉATION DE SOINS DE TEST:")
        membre = Membre.objects.first()
        medecin = Medecin.objects.first()
        
        soin_data = [
            {'type_soin': 'Consultation générale', 'montant': 5000},
            {'type_soin': 'Radio pulmonaire', 'montant': 15000},
            {'type_soin': 'Analyse sanguine', 'montant': 8000},
        ]
        
        soins_created = 0
        for data in soin_data:
            soin, created = Soin.objects.get_or_create(
                membre=membre,
                medecin=medecin,
                type_soin=data['type_soin'],
                defaults={
                    'montant': data['montant'],
                    'date_soin': timezone.now().date(),
                    'statut': 'TERMINE'
                }
            )
            if created:
                soins_created += 1
                print(f"   ✅ Soin créé: {data['type_soin']}")
        
        print(f"🎯 Soins créés: {soins_created}")
        
        # 4. Créer des ordonnances de test
        print("\n💊 CRÉATION D'ORDONNANCES DE TEST:")
        try:
            ordonnance, created = Ordonnance.objects.get_or_create(
                medecin=medecin,
                membre=membre,
                defaults={
                    'date_prescription': timezone.now().date(),
                    'notes': 'Ordonnance de test pour récupération système'
                }
            )
            if created:
                print("   ✅ Ordonnance de test créée")
        except Exception as e:
            print(f"   ⚠️  Impossible de créer ordonnance: {e}")
        
        # 5. Créer des paiements de test
        print("\n💰 CRÉATION DE PAIEMENTS DE TEST:")
        paiements_created = 0
        for soin in Soin.objects.all()[:2]:  # Payer les 2 premiers soins
            paiement, created = Paiement.objects.get_or_create(
                membre=membre,
                montant=soin.montant,
                defaults={
                    'date_paiement': timezone.now().date(),
                    'methode_paiement': 'ESPECES',
                    'statut': 'PAYE'
                }
            )
            if created:
                paiements_created += 1
                print(f"   ✅ Paiement créé: {soin.montant} FCFA")
        
        print(f"🎯 Paiements créés: {paiements_created}")
        
        # 6. Résumé final
        print(f"\n📈 RÉSUMÉ DE LA RÉCUPÉRATION:")
        print(f"   👥 Membres: {Membre.objects.count()}")
        print(f"   🩺 Médecins: {Medecin.objects.count()}")
        print(f"   🏥 Soins: {Soin.objects.count()}")
        print(f"   💊 Ordonnances: {Ordonnance.objects.count()}")
        print(f"   💰 Paiements: {Paiement.objects.count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données de test: {e}")
        return False

def verify_system_integrity():
    """Vérifie l'intégrité du système après récupération"""
    print("\n🔍 VÉRIFICATION DE L'INTÉGRITÉ DU SYSTÈME")
    print("-" * 50)
    
    models_to_check = [
        ('membres', 'Membre'),
        ('medecin', 'Medecin'), 
        ('soins', 'Soin'),
        ('soins', 'Ordonnance'),
        ('paiements', 'Paiement')
    ]
    
    all_ok = True
    for app, model_name in models_to_check:
        try:
            model = apps.get_model(app, model_name)
            count = model.objects.count()
            status = "✅" if count > 0 else "❌"
            print(f"   {status} {app}.{model_name}: {count}")
            
            if count == 0 and model_name in ['Soin', 'Paiement', 'Ordonnance']:
                all_ok = False
                
        except LookupError:
            print(f"   ❌ {app}.{model_name}: Modèle non trouvé")
            all_ok = False
    
    return all_ok

def main():
    print("🩺 SCRIPT DE RÉCUPÉRATION DU SYSTÈME MÉDICAL")
    print("=" * 60)
    
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