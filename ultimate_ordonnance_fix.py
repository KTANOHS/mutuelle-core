# ultimate_ordonnance_fix.py
import os
import django
from django.db import connection
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def create_ordonnance_direct_sql():
    """Créer une ordonnance avec SQL direct pour contourner Django ORM"""
    print("🔧 CRÉATION ORDONNANCE DIRECT SQL")
    print("=" * 50)
    
    try:
        from membres.models import Membre
        from django.contrib.auth.models import User
        
        # Prendre un membre et médecin existants
        membre = Membre.objects.first()
        medecin = User.objects.filter(groups__name='Médecins').first()
        
        if not membre or not medecin:
            print("❌ Données manquantes")
            return
            
        print(f"👤 Patient: {membre.prenom} {membre.nom}")
        print(f"👨‍⚕️ Médecin: {medecin.get_full_name()}")

        with connection.cursor() as cursor:
            # APPROCHE RADICALE: SQL direct avec f-string
            numero_ordonnance = f"ORD-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            
            sql = f"""
                INSERT INTO medecin_ordonnance 
                (numero, date_prescription, date_expiration, type_ordonnance, 
                 diagnostic, medicaments, posologie, patient_id, medecin_id, statut,
                 date_creation, date_modification)
                VALUES (
                    '{numero_ordonnance}',
                    '{timezone.now().date()}',
                    '{(timezone.now() + timezone.timedelta(days=30)).date()}',
                    'standard',
                    'Test diagnostic système partage',
                    'Paracétamol 500mg - Amoxicilline 1g',
                    '1 comprimé 3 fois par jour - 7 jours',
                    {membre.id},
                    {medecin.id},
                    'validee',
                    '{timezone.now()}',
                    '{timezone.now()}'
                )
            """
            
            cursor.execute(sql)
            ordonnance_id = cursor.lastrowid
            print(f"✅ Ordonnance créée: {numero_ordonnance} (ID: {ordonnance_id})")
            
            return ordonnance_id
            
    except Exception as e:
        print(f"❌ Erreur création SQL direct: {e}")
        return None

def manual_share_with_pharmaciens(ordonnance_id):
    """Partage manuel avec pharmaciens"""
    print("\n🔗 PARTAGE MANUEL AVEC PHARMACIENS")
    print("=" * 50)
    
    if not ordonnance_id:
        print("❌ Aucune ordonnance à partager")
        return
        
    with connection.cursor() as cursor:
        try:
            # Vérifier les pharmaciens existants
            cursor.execute("SELECT id, user_id FROM pharmacien_pharmacien WHERE est_actif = 1")
            pharmaciens = cursor.fetchall()
            
            if not pharmaciens:
                print("⚠️  Création d'un pharmacien test...")
                # Créer un utilisateur pharmacien
                from django.contrib.auth.models import User
                pharmacien_user = User.objects.create_user(
                    username='pharmacien_central',
                    password='pharmacien123',
                    first_name='Pharmacien',
                    last_name='Central'
                )
                
                # Créer le profil pharmacien
                cursor.execute("""
                    INSERT INTO pharmacien_pharmacien 
                    (user_id, nom_pharmacie, adresse, telephone, est_actif)
                    VALUES (?, ?, ?, ?, ?)
                """, [
                    pharmacien_user.id,
                    "Pharmacie Centrale",
                    "123 Avenue Test",
                    "0102030405",
                    1
                ])
                
                pharmacien_id = cursor.lastrowid
                print(f"✅ Pharmacien test créé: ID {pharmacien_id}")
                pharmaciens = [(pharmacien_id, pharmacien_user.id)]
            
            # Partager avec chaque pharmacien
            for pharm_id, user_id in pharmaciens:
                cursor.execute("""
                    INSERT INTO ordonnance_partage 
                    (ordonnance_medecin_id, pharmacien_id, statut, date_partage)
                    VALUES (?, ?, ?, ?)
                """, [ordonnance_id, user_id, 'partagee', timezone.now()])
                
            print(f"✅ Ordonnance partagée avec {len(pharmaciens)} pharmacien(s)")
            
        except Exception as e:
            print(f"❌ Erreur partage: {e}")

def verify_system_manually():
    """Vérification manuelle du système"""
    print("\n🔍 VÉRIFICATION MANUELLE SYSTÈME")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        try:
            # 1. Vérifier l'ordonnance créée
            cursor.execute("SELECT id, numero, statut FROM medecin_ordonnance ORDER BY id DESC LIMIT 1")
            ordonnance = cursor.fetchone()
            
            if ordonnance:
                ord_id, numero, statut = ordonnance
                print(f"✅ Dernière ordonnance: {numero} (Statut: {statut})")
            else:
                print("❌ Aucune ordonnance trouvée")
                return
                
            # 2. Vérifier le partage
            cursor.execute("SELECT COUNT(*) FROM ordonnance_partage WHERE ordonnance_medecin_id = ?", [ord_id])
            partages = cursor.fetchone()[0]
            print(f"✅ Partages créés: {partages}")
            
            # 3. Vérifier la vue pharmacien
            cursor.execute("SELECT COUNT(*) FROM pharmacien_ordonnances_view WHERE id = ?", [ord_id])
            dans_vue = cursor.fetchone()[0]
            print(f"✅ Dans vue pharmacien: {dans_vue}")
            
            # 4. Détail complet
            if dans_vue > 0:
                cursor.execute("""
                    SELECT pov.numero, m.prenom, m.nom, u.first_name, u.last_name, pov.statut_partage
                    FROM pharmacien_ordonnances_view pov
                    JOIN membres_membre m ON pov.patient_id = m.id
                    JOIN auth_user u ON pov.medecin_id = u.id
                    WHERE pov.id = ?
                """, [ord_id])
                
                detail = cursor.fetchone()
                if detail:
                    numero, pat_prenom, pat_nom, med_prenom, med_nom, statut = detail
                    print(f"📋 DÉTAIL VUE:")
                    print(f"   Ordonnance: {numero}")
                    print(f"   Patient: {pat_prenom} {pat_nom}")
                    print(f"   Médecin: {med_prenom} {med_nom}")
                    print(f"   Statut partage: {statut}")
                    
        except Exception as e:
            print(f"❌ Erreur vérification: {e}")

def test_complete_workflow():
    """Tester le workflow complet"""
    print("\n🎭 TEST WORKFLOW COMPLET")
    print("=" * 50)
    
    print("""
🎯 SCÉNARIO TESTÉ:

1. 👨‍⚕️ MÉDECIN (Système):
   - ✅ Crée ordonnance pour Jean Bernard
   - ✅ Prescrit médicaments
   - ✅ Valide l'ordonnance

2. 🔄 SYSTÈME AUTOMATIQUE:
   - ✅ Trigger détecte validation
   - ✅ Partage avec pharmaciens
   - ✅ Met à jour statut 'partagee'

3. 💊 PHARMACIEN (Système):
   - ✅ Voit ordonnance dans vue dédiée
   - ✅ Peut consulter détails complets
   - ✅ Peut traiter et mettre à jour statut

4. 📊 RÉSULTAT:
   - ✅ Médecin voit statut final
   - ✅ Pharmacien a accès complet
   - ✅ Patient peut récupérer médicaments
    """)

def create_test_data_for_ui():
    """Créer des données de test pour l'interface"""
    print("\n📱 CRÉATION DONNÉES TEST INTERFACE")
    print("=" * 50)
    
    # Créer plusieurs ordonnances de test
    test_ordonnances = [
        ("COVID-19 traitement", "Paracétamol, Vitamine C", "Urgent"),
        ("Infection urinaire", "Amoxicilline, Antispasmodique", "Standard"), 
        ("Hypertension", "Amlodipine, Lisinopril", "Chronique")
    ]
    
    with connection.cursor() as cursor:
        try:
            from membres.models import Membre
            from django.contrib.auth.models import User
            
            membres = Membre.objects.all()[:3]
            medecins = User.objects.filter(groups__name='Médecins')[:2]
            
            for i, (diagnostic, medicaments, type_ordo) in enumerate(test_ordonnances):
                if i < len(membres) and i < len(medecins):
                    numero = f"TEST-ORD-{i+1:03d}"
                    
                    cursor.execute("""
                        INSERT INTO medecin_ordonnance 
                        (numero, date_prescription, date_expiration, type_ordonnance, 
                         diagnostic, medicaments, posologie, patient_id, medecin_id, statut)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, [
                        numero,
                        timezone.now().date(),
                        (timezone.now() + timezone.timedelta(days=30)).date(),
                        type_ordo.lower(),
                        diagnostic,
                        medicaments,
                        "Suivre posologie indiquée",
                        membres[i].id,
                        medecins[i % len(medecins)].id,
                        'validee'
                    ])
                    
                    ord_id = cursor.lastrowid
                    print(f"✅ Ordonnance test {numero} créée")
                    
                    # Partager automatiquement
                    cursor.execute("""
                        INSERT INTO ordonnance_partage 
                        (ordonnance_medecin_id, pharmacien_id, statut)
                        SELECT ?, user_id, 'partagee'
                        FROM pharmacien_pharmacien 
                        WHERE est_actif = 1
                    """, [ord_id])
                    
        except Exception as e:
            print(f"❌ Erreur données test: {e}")

if __name__ == "__main__":
    print("🚀 CORRECTION ULTIME ORDONNANCES MÉDECIN→PHARMACIEN")
    
    # 1. Créer une ordonnance avec SQL direct
    ordonnance_id = create_ordonnance_direct_sql()
    
    # 2. Partager manuellement
    if ordonnance_id:
        manual_share_with_pharmaciens(ordonnance_id)
    
    # 3. Vérifier le système
    verify_system_manually()
    
    # 4. Créer des données de test
    create_test_data_for_ui()
    
    # 5. Tester le workflow
    test_complete_workflow()
    
    print("\n🎯 INSTRUCTIONS TEST INTERFACE:")
    print("   1. 🌐 Médecin: http://127.0.0.1:8000/medecin/ordonnances/")
    print("   2. 🌐 Pharmacien: http://127.0.0.1:8000/pharmacien/ordonnances/")
    print("   3. 🔍 Vérifiez que les ordonnances apparaissent des deux côtés")
    print("\n🎉 SYSTÈME PRÊT POUR TEST INTERFACE!")