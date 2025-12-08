"""
TEST PAIEMENT - Version corrigée pour exécution via manage.py shell
Exécutez : python manage.py shell < test_paiement_manage.py
"""

from django.contrib.auth.models import User, Group
from django.utils import timezone
from decimal import Decimal

print("🔧 TEST PAIEMENT - Démarrage")
print("=" * 50)

# 1. Créer ou récupérer un utilisateur assureur
try:
    user, created = User.objects.get_or_create(
        username='test_assureur',
        defaults={
            'email': 'test@assureur.com',
            'first_name': 'Test',
            'last_name': 'Assureur',
            'is_active': True
        }
    )
    
    if created:
        user.set_password('test123')
        user.save()
        print(f"✅ Utilisateur créé: {user.username}")
    else:
        print(f"✅ Utilisateur existant: {user.username}")
    
    # 2. Ajouter au groupe ASSUREUR
    groupe, _ = Group.objects.get_or_create(name='assureur')
    user.groups.add(groupe)
    print(f"✅ Ajouté au groupe 'assureur'")
    
    # 3. Vérifier le modèle Assureur
    from assureur.models import Assureur
    print(f"✅ Modèle Assureur importé")
    
    # Afficher les champs du modèle Assureur
    print("📋 Champs du modèle Assureur:")
    for field in Assureur._meta.get_fields():
        print(f"  - {field.name} ({field.get_internal_type()})")
    
    # 4. Créer un profil Assureur si possible
    try:
        # Essayer de créer un profil Assureur avec les champs disponibles
        # Note: Le modèle peut ne pas avoir 'email' et 'nom' comme champs directs
        assureur, created = Assureur.objects.get_or_create(
            user=user
            # Ajouter d'autres champs par défaut si nécessaires
        )
        print(f"✅ Profil Assureur: {assureur}")
    except Exception as e:
        print(f"⚠️  Note: {e}")
        print("   Le profil assureur peut être créé différemment")
    
    # 5. Créer un membre de test
    from agents.models import Membre
    membre, created = Membre.objects.get_or_create(
        numero_unique='TESTPAY001',
        defaults={
            'nom': 'TestPaiement',
            'prenom': 'User',
            'statut': 'actif',
            'email': 'test.paiement@example.com'
        }
    )
    print(f"✅ Membre: {membre.nom} {membre.prenom}")
    
    # 6. Créer un soin de test
    from assureur.models import Soin
    soin, created = Soin.objects.get_or_create(
        membre=membre,
        code='TEST-SOIN-001',
        defaults={
            'type_soin': 'consultation',
            'montant_facture': Decimal('5000.00'),
            'montant_rembourse': Decimal('4000.00'),
            'statut': 'valide',
            'date_soin': timezone.now().date()
        }
    )
    print(f"✅ Soin: {soin.code} - {soin.montant_facture} FCFA")
    
    # 7. Créer un paiement de test
    from assureur.models import Paiement
    
    # Vérifier les champs du modèle Paiement
    print("\n📋 Champs du modèle Paiement:")
    for field in Paiement._meta.get_fields():
        print(f"  - {field.name} ({field.get_internal_type()})")
    
    # Créer le paiement
    paiement = Paiement.objects.create(
        membre=membre,
        montant=Decimal('5000.00'),
        mode_paiement='espece',
        date_paiement=timezone.now().date(),
        statut='valide',
        reference=f'PAY-TEST-{timezone.now().strftime("%Y%m%d%H%M%S")}',
        notes='Paiement de test créé via script',
        created_by=user
    )
    
    print(f"\n✅ PAIEMENT CRÉÉ AVEC SUCCÈS!")
    print(f"   Référence: {paiement.reference}")
    print(f"   Montant: {paiement.montant} FCFA")
    print(f"   Membre: {paiement.membre.nom} {paiement.membre.prenom}")
    print(f"   Statut: {paiement.statut}")
    print(f"   Date: {paiement.date_paiement}")
    
    # 8. Vérifier dans la base de données
    total_paiements = Paiement.objects.count()
    print(f"\n📊 Total paiements en base: {total_paiements}")
    
    # Afficher les derniers paiements
    derniers = Paiement.objects.select_related('membre').order_by('-date_paiement')[:5]
    print(f"📋 Derniers paiements ({len(derniers)}):")
    for p in derniers:
        print(f"  - {p.reference}: {p.montant} FCFA pour {p.membre.nom} ({p.date_paiement})")
    
    print("\n🎉 TEST TERMINÉ AVEC SUCCÈS!")
    
except Exception as e:
    print(f"\n❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()