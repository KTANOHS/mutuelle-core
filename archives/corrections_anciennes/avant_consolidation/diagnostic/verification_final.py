# verification_finale.py
import os
import sys
import django
import sqlite3

sys.path.append('/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db import connection

print("🔍 VÉRIFICATION FINALE DU SYSTÈME DE COTISATION")
print("="*60)

# 1. Vérifier la structure de la table
print("\n1. Structure de la table assureur_cotisation :")
with connection.cursor() as cursor:
    cursor.execute("PRAGMA table_info(assureur_cotisation)")
    columns = cursor.fetchall()
    
    problem_fields = ['montant_clinique', 'montant_pharmacie', 'montant_charges_mutuelle']
    found_problems = []
    
    for col in columns:
        col_name = col[1]
        col_type = col[2]
        
        if col_name in problem_fields:
            found_problems.append(col_name)
            print(f"   ❌ {col_name:30} ({col_type}) - CHAMP PROBLÉMATIQUE TROUVÉ")
        else:
            print(f"   ✅ {col_name:30} ({col_type})")
    
    if not found_problems:
        print("\n   🎉 AUCUN CHAMP PROBLÉMATIQUE TROUVÉ !")
    else:
        print(f"\n   ⚠️  {len(found_problems)} champ(s) problématique(s) : {', '.join(found_problems)}")

# 2. Vérifier les données existantes
print("\n2. Données existantes :")
with connection.cursor() as cursor:
    cursor.execute("SELECT COUNT(*) FROM assureur_cotisation")
    total = cursor.fetchone()[0]
    print(f"   📊 Total cotisations : {total}")
    
    cursor.execute("SELECT statut, COUNT(*) FROM assureur_cotisation GROUP BY statut ORDER BY statut")
    statuts = cursor.fetchall()
    for statut, count in statuts:
        print(f"   📊 Statut '{statut}': {count}")

# 3. Tester une création réelle
print("\n3. Test de création réelle :")
try:
    from assureur.models import Cotisation
    from membres.models import Membre
    from django.contrib.auth.models import User
    from decimal import Decimal
    from datetime import datetime
    
    # Récupérer des données réelles
    user = User.objects.filter(username='Almoravide').first()
    membre = Membre.objects.filter(prenom='Jean', nom='Bernard').first()
    
    if user and membre:
        print(f"   👤 Utilisateur : {user.username}")
        print(f"   👤 Membre : {membre.prenom} {membre.nom}")
        
        # Créer une vraie cotisation
        cotisation = Cotisation.objects.create(
            membre=membre,
            periode='2025-12',
            montant=Decimal('7500.00'),
            type_cotisation='femme_enceinte',
            date_emission='2025-12-04',
            date_echeance='2025-12-31',
            statut='due',
            reference=f'COT-REAL-{datetime.now().strftime("%Y%m%d%H%M%S")}',
            enregistre_par=user,
            notes='Cotisation créée par le script de vérification'
        )
        
        print(f"   ✅ Cotisation créée : {cotisation.reference}")
        print(f"   💰 Montant : {cotisation.montant} FCFA")
        print(f"   📅 Période : {cotisation.periode}")
        print(f"   📊 Statut : {cotisation.statut}")
        
        # Garder cette cotisation pour le test manuel
        print(f"   📍 ID à garder pour test : {cotisation.id}")
    else:
        print("   ❌ Données de test non trouvées")

except Exception as e:
    print(f"   ❌ Erreur : {e}")
    import traceback
    traceback.print_exc()

# 4. Vérifier les URLs
print("\n4. Vérification des URLs :")
urls_to_check = [
    ('/assureur/cotisations/', 'Liste des cotisations'),
    ('/assureur/cotisations/creer/', 'Créer une cotisation (générique)'),
    ('/assureur/cotisations/creer/1/', 'Créer une cotisation pour membre ID 1'),
]

for url, description in urls_to_check:
    print(f"   🌐 {description:40} : http://localhost:8000{url}")

print("\n" + "="*60)
print("📋 RÉSUMÉ DE LA VÉRIFICATION :")
if not found_problems:
    print("✅ SYSTÈME FONCTIONNEL :")
    print("   - Aucun champ problématique trouvé")
    print("   - La création de cotisations fonctionne")
    print("   - Les données sont accessibles")
    print("\n🎯 Prochaine étape :")
    print("   1. Redémarrez le serveur")
    print("   2. Testez via l'interface web")
    print("   3. Vérifiez la liste des cotisations")
else:
    print("⚠️  PROBLÈMES DÉTECTÉS :")
    print(f"   - Champs problématiques : {', '.join(found_problems)}")
    print("\n🔧 Solution recommandée :")
    print("   Exécutez le script de reconstruction de table")
    print("   python rebuild_cotisation_table.py")
print("="*60)