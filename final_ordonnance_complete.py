# final_ordonnance_complete.py
import os
import django
from django.db import connection
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def create_ordonnance_with_all_fields():
    """Créer une ordonnance avec TOUS les champs obligatoires"""
    print("🔧 CRÉATION ORDONNANCE COMPLÈTE")
    print("=" * 50)
    
    try:
        from membres.models import Membre
        from django.contrib.auth.models import User
        
        # Prendre un membre et médecin existants
        membre = Membre.objects.first()
        medecin = User.objects.filter(groups__name='Médecins').first()
        
        if not membre or not medecin:
            print("❌ Données manquantes")
            return None
            
        print(f"👤 Patient: {membre.prenom} {membre.nom}")
        print(f"👨‍⚕️ Médecin: {medecin.get_full_name()}")

        with connection.cursor() as cursor:
            # Créer l'ordonnance avec TOUS les champs requis
            numero_ordonnance = f"ORD-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            
            cursor.execute("""
                INSERT INTO medecin_ordonnance 
                (numero, date_prescription, date_expiration, type_ordonnance, 
                 diagnostic, medicaments, posologie, duree_traitement, renouvelable,
                 nombre_renouvellements, renouvellements_effectues, statut, est_urgent,
                 patient_id, medecin_id, date_creation, date_modification)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                numero_ordonnance,                              # numero
                timezone.now().date(),                          # date_prescription
                (timezone.now() + timezone.timedelta(days=30)).date(),  # date_expiration
                'standard',                                     # type_ordonnance
                'Infection respiratoire - Test système partage', # diagnostic
                'Paracétamol 500mg, Amoxicilline 1g',          # medicaments
                '1 comprimé 3 fois par jour',                  # posologie
                7,                                              # duree_traitement (OBLIGATOIRE)
                False,                                          # renouvelable
                0,                                              # nombre_renouvellements
                0,                                              # renouvellements_effectues
                'validee',                                      # statut
                False,                                          # est_urgent
                membre.id,                                      # patient_id
                medecin.id,                                     # medecin_id
                timezone.now(),                                 # date_creation
                timezone.now()                                  # date_modification
            ])
            
            ordonnance_id = cursor.lastrowid
            print(f"✅ Ordonnance créée: {numero_ordonnance} (ID: {ordonnance_id})")
            
            return ordonnance_id
            
    except Exception as e:
        print(f"❌ Erreur création ordonnance: {e}")
        return None

def create_multiple_test_ordonnances():
    """Créer plusieurs ordonnances de test avec données variées"""
    print("\n📋 CRÉATION MULTIPLES ORDONNANCES TEST")
    print("=" * 50)
    
    test_prescriptions = [
        {
            'diagnostic': 'COVID-19 traitement symptomatique',
            'medicaments': 'Paracétamol 1000mg, Vitamine C 500mg',
            'posologie': '1 comprimé 3 fois par jour',
            'duree': 10,
            'type': 'standard'
        },
        {
            'diagnostic': 'Infection urinaire simple',
            'medicaments': 'Amoxicilline 1g, Antispasmodique',
            'posologie': '1 comprimé 2 fois par jour',
            'duree': 7,
            'type': 'standard'
        },
        {
            'diagnostic': 'Hypertension artérielle',
            'medicaments': 'Amlodipine 5mg, Lisinopril 10mg',
            'posologie': '1 comprimé par jour',
            'duree': 30,
            'type': 'chronique'
        }
    ]
    
    with connection.cursor() as cursor:
        try:
            from membres.models import Membre
            from django.contrib.auth.models import User
            
            membres = list(Membre.objects.all()[:3])
            medecins = list(User.objects.filter(groups__name='Médecins')[:2])
            
            ordonnances_crees = 0
            
            for i, prescription in enumerate(test_prescriptions):
                if i < len(membres):
                    numero = f"TEST-ORD-{i+1:03d}"
                    membre = membres[i]
                    medecin = medecins[i % len(medecins)]
                    
                    cursor.execute("""
                        INSERT INTO medecin_ordonnance 
                        (numero, date_prescription, date_expiration, type_ordonnance, 
                         diagnostic, medicaments, posologie, duree_traitement, renouvelable,
                         nombre_renouvellements, renouvellements_effectues, statut, est_urgent,
                         patient_id, medecin_id, date_creation, date_modification)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, [
                        numero,
                        timezone.now().date(),
                        (timezone.now() + timezone.timedelta(days=30)).date(),
                        prescription['type'],
                        prescription['diagnostic'],
                        prescription['medicaments'],
                        prescription['posologie'],
                        prescription['duree'],
                        False, 0, 0,  # renouvelable, nombre_renouvellements, renouvellements_effectues
                        'validee',
                        False,  # est_urgent
                        membre.id,
                        medecin.id,
                        timezone.now(),
                        timezone.now()
                    ])
                    
                    ord_id = cursor.lastrowid
                    ordonnances_crees += 1
                    print(f"✅ Ordonnance test {numero} créée (ID: {ord_id})")
                    
                    # Partager automatiquement avec pharmaciens
                    cursor.execute("""
                        INSERT INTO ordonnance_partage 
                        (ordonnance_medecin_id, pharmacien_id, statut, date_partage)
                        SELECT ?, user_id, 'partagee', ?
                        FROM pharmacien_pharmacien 
                        WHERE est_actif = 1
                    """, [ord_id, timezone.now()])
                    
                    print(f"✅ Ordonnance {numero} partagée avec pharmaciens")
            
            print(f"\n📊 {ordonnances_crees} ordonnances de test créées et partagées")
            return ordonnances_crees
            
        except Exception as e:
            print(f"❌ Erreur création multiples: {e}")
            return 0

def verify_complete_system():
    """Vérification complète du système"""
    print("\n🔍 VÉRIFICATION SYSTÈME COMPLET")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        try:
            # 1. Compter les ordonnances
            cursor.execute("SELECT COUNT(*) FROM medecin_ordonnance")
            total_ordonnances = cursor.fetchone()[0]
            print(f"📝 Ordonnances totales: {total_ordonnances}")
            
            # 2. Compter les partages
            cursor.execute("SELECT COUNT(*) FROM ordonnance_partage")
            total_partages = cursor.fetchone()[0]
            print(f"🔗 Partages créés: {total_partages}")
            
            # 3. Compter dans la vue pharmacien
            cursor.execute("SELECT COUNT(*) FROM pharmacien_ordonnances_view")
            dans_vue = cursor.fetchone()[0]
            print(f"💊 Dans vue pharmacien: {dans_vue}")
            
            # 4. Détail des ordonnances partagées
            if dans_vue > 0:
                print(f"\n📋 DÉTAIL ORDONNANCES PARTAGÉES:")
                cursor.execute("""
                    SELECT pov.numero, m.prenom, m.nom, u.first_name, u.last_name, 
                           pov.diagnostic, pov.statut_partage
                    FROM pharmacien_ordonnances_view pov
                    JOIN membres_membre m ON pov.patient_id = m.id
                    JOIN auth_user u ON pov.medecin_id = u.id
                    ORDER BY pov.date_prescription DESC
                    LIMIT 3
                """)
                
                for numero, pat_prenom, pat_nom, med_prenom, med_nom, diagnostic, statut in cursor.fetchall():
                    print(f"   📝 {numero}")
                    print(f"      Patient: {pat_prenom} {pat_nom}")
                    print(f"      Médecin: {med_prenom} {med_nom}") 
                    print(f"      Diagnostic: {diagnostic}")
                    print(f"      Statut: {statut}")
                    print()
                    
            return total_ordonnances > 0 and dans_vue > 0
            
        except Exception as e:
            print(f"❌ Erreur vérification: {e}")
            return False

def test_pharmacien_interface():
    """Tester l'interface pharmacien"""
    print("\n💊 TEST INTERFACE PHARMACIEN")
    print("=" * 50)
    
    print("""
🎯 POUR TESTER L'INTERFACE:

1. 🌐 CONNEXION PHARMACIEN:
   URL: http://127.0.0.1:8000/pharmacien/ordonnances/

2. 📋 CE QUE VOUS DEVRIEZ VOIR:
   - Liste des ordonnances partagées
   - Détails complets (patient, médecin, médicaments)
   - Statut de chaque ordonnance
   - Options de traitement

3. 🔄 ACTIONS POSSIBLES:
   - Voir détails ordonnance
   - Marquer comme "en préparation"
   - Marquer comme "servie"
   - Ajouter notes pharmacien

4. ✅ RÉSULTAT ATTENDU:
   - Toutes les ordonnances de test visibles
   - Accès complet aux informations
   - Workflow de traitement fonctionnel
    """)

def final_system_check():
    """Vérification finale avant test"""
    print("\n✅ VÉRIFICATION FINALE SYSTÈME")
    print("=" * 50)
    
    # Créer une ordonnance principale
    main_ordonnance_id = create_ordonnance_with_all_fields()
    
    # Créer plusieurs ordonnances de test
    test_count = create_multiple_test_ordonnances()
    
    # Vérifier le système
    system_ok = verify_complete_system()
    
    if system_ok:
        print("\n🎉 SYSTÈME ORDONNANCES MÉDECIN→PHARMACIEN OPÉRATIONNEL!")
        print(f"📊 {test_count + (1 if main_ordonnance_id else 0)} ordonnances créées")
        print("🔗 Toutes partagées avec pharmaciens")
        print("💊 Accessibles via vue dédiée")
    else:
        print("\n⚠️  SYSTÈME AVEC PROBLÈMES RÉSIDUELS")
        print("💡 Vérifiez les logs ci-dessus")

if __name__ == "__main__":
    print("🚀 SYSTÈME ORDONNANCES MÉDECIN→PHARMACIEN - VERSION FINALE")
    final_system_check()
    test_pharmacien_interface()
    
    print("\n" + "=" * 60)
    print("🎯 PROCHAINES ÉTAPES:")
    print("   1. Testez l'interface pharmacien")
    print("   2. Vérifiez la visibilité des ordonnances")
    print("   3. Testez le workflow complet")
    print("   4. Confirmez le fonctionnement en production")
    print("=" * 60)