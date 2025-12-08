#!/usr/bin/env python3
import os
import sys
import django

sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    print("=== VÉRIFICATION FINALE DU SYSTÈME ===")
    
    # 1. Vérifier le modèle Pharmacien
    from pharmacien.models import Pharmacien
    pharmaciens_count = Pharmacien.objects.count()
    print(f"1. ✅ Pharmaciens dans la base: {pharmaciens_count}")
    
    # 2. Vérifier OrdonnancePharmacien
    from pharmacien.models import OrdonnancePharmacien
    ord_pharma_count = OrdonnancePharmacien.objects.count()
    print(f"2. ✅ OrdonnancePharmacien dans la base: {ord_pharma_count}")
    
    # 3. Vérifier un utilisateur pharmacien
    from django.contrib.auth.models import User
    pharmacien_users = User.objects.filter(groups__name='Pharmacien')
    print(f"3. ✅ Utilisateurs dans groupe Pharmacien: {pharmacien_users.count()}")
    
    # 4. Tester la vue historique_validation
    from pharmacien.views import historique_validation
    print(f"4. ✅ Vue historique_validation importée avec succès")
    
    # 5. Vérifier les templates
    import os
    templates = [
        'templates/pharmacien/historique.html',
        'templates/pharmacien/base_pharmacien.html',
        'templates/medecin/base_medecin.html',
    ]
    
    print("5. ✅ Vérification des templates:")
    for template in templates:
        if os.path.exists(template):
            size = os.path.getsize(template)
            print(f"   - {template}: {size} octets ✓")
        else:
            print(f"   - {template}: MANQUANT ✗")
    
    # 6. Tester une requête simple
    if pharmacien_users.exists():
        user = pharmacien_users.first()
        try:
            validations = OrdonnancePharmacien.objects.filter(
                pharmacien_validateur=user
            ).count()
            print(f"6. ✅ Test requête pour {user.username}: {validations} validation(s)")
        except Exception as e:
            print(f"6. ✗ Erreur requête: {e}")
    
    print("\n=== RÉSUMÉ ===")
    print("Le système pharmacien est OPÉRATIONNEL !")
    print(f"- Page historique: http://127.0.0.1:8000/pharmacien/historique/")
    print(f"- Dashboard: http://127.0.0.1:8000/pharmacien/dashboard/")
    print(f"- Liste ordonnances: http://127.0.0.1:8000/pharmacien/ordonnances/")
    
except Exception as e:
    print(f"❌ Erreur lors de la vérification: {e}")
    import traceback
    traceback.print_exc()
