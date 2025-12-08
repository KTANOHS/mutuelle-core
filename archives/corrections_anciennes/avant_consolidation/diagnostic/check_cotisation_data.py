# check_cotisation_data.py
import os
import sys
import django
import csv

sys.path.append('/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db import connection

def check_cotisation_data():
    """Vérifie les données dans les champs inutiles"""
    
    print("🔍 Vérification des données dans les champs problématiques")
    print("="*60)
    
    with connection.cursor() as cursor:
        # Récupérer les données des champs problématiques
        cursor.execute("""
            SELECT 
                id,
                reference,
                membre_id,
                periode,
                montant,
                montant_clinique,
                montant_pharmacie,
                montant_charges_mutuelle,
                statut
            FROM assureur_cotisation
            WHERE montant_clinique != 0 
               OR montant_pharmacie != 0 
               OR montant_charges_mutuelle != 0
            ORDER BY id
        """)
        
        rows = cursor.fetchall()
        
        if not rows:
            print("✅ Aucune donnée dans les champs problématiques")
            return
        
        print(f"\n📊 {len(rows)} enregistrements avec des données:")
        print("-" * 100)
        
        total_clinique = 0
        total_pharmacie = 0
        total_charges = 0
        
        for row in rows:
            print(f"ID: {row[0]:3} | Réf: {row[1]:20} | Membre: {row[2]:3} | Période: {row[3]} | "
                  f"Montant: {float(row[4]):8.2f} | Clinique: {float(row[5]):8.2f} | "
                  f"Pharmacie: {float(row[6]):8.2f} | Charges: {float(row[7]):8.2f} | "
                  f"Statut: {row[8]}")
            
            total_clinique += float(row[5])
            total_pharmacie += float(row[6])
            total_charges += float(row[7])
        
        print("-" * 100)
        print(f"TOTAUX: Clinique: {total_clinique:8.2f} | Pharmacie: {total_pharmacie:8.2f} | "
              f"Charges: {total_charges:8.2f} | Total général: {total_clinique + total_pharmacie + total_charges:8.2f}")
        
        # Vérifier si ces montants sont inclus dans le montant total
        print("\n🔍 Vérification de la cohérence avec le montant total:")
        cursor.execute("""
            SELECT 
                COUNT(*) as total_records,
                SUM(CASE WHEN montant = montant_clinique + montant_pharmacie + montant_charges_mutuelle THEN 1 ELSE 0 END) as matches_total,
                SUM(CASE WHEN montant != montant_clinique + montant_pharmacie + montant_charges_mutuelle THEN 1 ELSE 0 END) as not_matching
            FROM assureur_cotisation
            WHERE montant_clinique != 0 OR montant_pharmacie != 0 OR montant_charges_mutuelle != 0
        """)
        
        stats = cursor.fetchone()
        print(f"   Enregistrements avec données: {stats[0]}")
        print(f"   Où montant = somme des 3 champs: {stats[1]}")
        print(f"   Où montant ≠ somme des 3 champs: {stats[2]}")
        
        # Sauvegarder les données dans un CSV
        save_to_csv(rows)
        
        return rows

def save_to_csv(rows):
    """Sauvegarde les données dans un fichier CSV"""
    
    filename = 'cotisations_champs_problematiques.csv'
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # En-têtes
        writer.writerow([
            'ID', 'Référence', 'Membre_ID', 'Période', 'Montant_Total',
            'Montant_Clinique', 'Montant_Pharmacie', 'Montant_Charges_Mutuelle',
            'Statut', 'Somme_3_Champs', 'Différence'
        ])
        
        # Données
        for row in rows:
            somme = float(row[5]) + float(row[6]) + float(row[7])
            diff = float(row[4]) - somme
            
            writer.writerow([
                row[0], row[1], row[2], row[3], float(row[4]),
                float(row[5]), float(row[6]), float(row[7]), row[8],
                somme, diff
            ])
    
    print(f"\n💾 Données sauvegardées dans: {filename}")

def propose_solution(rows):
    """Propose une solution basée sur les données"""
    
    print("\n" + "="*60)
    print("🎯 Analyse et recommandations")
    print("="*60)
    
    if not rows:
        print("✅ Aucune donnée problématique. Vous pouvez supprimer les champs.")
        return
    
    print("\n🔍 Options disponibles:")
    print("\n1. **Option A: Sauvegarder et supprimer**")
    print("   - Les données sont sauvegardées dans un CSV")
    print("   - Supprimer les champs (données perdues)")
    print("   ✓ Recommandé si ces données ne sont pas utilisées")
    
    print("\n2. **Option B: Transférer les données**")
    print("   - Ajouter un champ 'notes' ou 'details' pour conserver l'info")
    print("   - Exemple: 'Clinique: X, Pharmacie: Y, Charges: Z'")
    print("   ✓ Recommandé si vous voulez conserver l'historique")
    
    print("\n3. **Option C: Ajouter les champs au modèle**")
    print("   - Garder les champs mais les rendre optionnels")
    print("   - Mettre à jour le modèle avec default=0.00")
    print("   ⚠️  Non recommandé (vous avez dit que ces champs ne devraient pas être là)")
    
    print("\n4. **Option D: Fusionner avec le montant total**")
    print("   - Vérifier si montant_total = somme des 3 champs")
    print("   - Si oui, les données sont redondantes et peuvent être supprimées")
    print("   - Si non, ajuster le montant_total")
    
    print("\n" + "="*60)
    print("💡 Ma recommandation:")
    print("   Si ces données ne sont pas utilisées dans l'application,")
    print("   optez pour l'Option A (sauvegarder en CSV et supprimer).")
    print("   Vous avez déjà le CSV comme backup.")

def implement_option_a():
    """Implémente l'option A: sauvegarder et supprimer"""
    
    print("\n" + "="*60)
    print("🛠️  Implémentation de l'Option A")
    print("="*60)
    
    # 1. Supprimer le trigger problématique si existe
    print("\n1. Suppression du trigger problématique...")
    with connection.cursor() as cursor:
        cursor.execute("DROP TRIGGER IF EXISTS auto_share_ordonnance")
        print("   ✅ Trigger supprimé")
    
    # 2. Appliquer la migration
    print("\n2. Application de la migration...")
    try:
        import subprocess
        result = subprocess.run(
            ['python', 'manage.py', 'migrate', 'assureur'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("   ✅ Migration appliquée avec succès")
            print(result.stdout)
        else:
            print("   ❌ Erreur lors de la migration:")
            print(result.stderr)
            
            # Essayer avec --fake si nécessaire
            print("\n   ⚠️  Tentative avec --fake...")
            result = subprocess.run(
                ['python', 'manage.py', 'migrate', 'assureur', '--fake'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("   ✅ Migration --fake appliquée")
            else:
                print("   ❌ Échec même avec --fake")
                print(result.stderr)
    
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # 3. Vérifier que les champs ont été supprimés
    print("\n3. Vérification de la suppression...")
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA table_info(assureur_cotisation)")
        columns = [col[1] for col in cursor.fetchall()]
        
        problem_fields = ['montant_clinique', 'montant_pharmacie', 'montant_charges_mutuelle']
        
        for field in problem_fields:
            if field in columns:
                print(f"   ❌ {field} existe encore")
            else:
                print(f"   ✅ {field} a été supprimé")

def implement_option_b():
    """Implémente l'option B: transférer dans les notes"""
    
    print("\n" + "="*60)
    print("🛠️  Implémentation de l'Option B")
    print("="*60)
    
    print("\n1. Transfert des données dans le champ 'notes'...")
    
    with connection.cursor() as cursor:
        # Compter les enregistrements à mettre à jour
        cursor.execute("""
            SELECT COUNT(*) FROM assureur_cotisation
            WHERE montant_clinique != 0 
               OR montant_pharmacie != 0 
               OR montant_charges_mutuelle != 0
        """)
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("   ✅ Aucune donnée à transférer")
        else:
            # Mettre à jour les notes
            cursor.execute("""
                UPDATE assureur_cotisation
                SET notes = 
                    CASE 
                        WHEN notes IS NULL OR notes = '' THEN
                            'Détails: Clinique=' || montant_clinique || 
                            ', Pharmacie=' || montant_pharmacie || 
                            ', Charges=' || montant_charges_mutuelle
                        ELSE
                            notes || ' | Détails: Clinique=' || montant_clinique || 
                            ', Pharmacie=' || montant_pharmacie || 
                            ', Charges=' || montant_charges_mutuelle
                    END
                WHERE montant_clinique != 0 
                   OR montant_pharmacie != 0 
                   OR montant_charges_mutuelle != 0
            """)
            
            print(f"   ✅ {count} enregistrement(s) mis à jour")
            print("   ℹ️  Les détails ont été ajoutés au champ 'notes'")
    
    # 2. Maintenant supprimer les champs
    implement_option_a()

if __name__ == "__main__":
    print("🔍 ANALYSE DES DONNÉES COTISATION")
    print("="*60)
    
    # Vérifier les données
    rows = check_cotisation_data()
    
    if rows:
        # Proposer des solutions
        propose_solution(rows)
        
        print("\n" + "="*60)
        choice = input("Choisissez une option (A/B/C/D ou Q pour quitter): ").upper()
        
        if choice == 'A':
            confirm = input("Êtes-vous sûr? Les données seront supprimées de la BD (oui/non): ")
            if confirm.lower() == 'oui':
                implement_option_a()
        elif choice == 'B':
            implement_option_b()
        elif choice == 'C':
            print("\n⚠️  Non implémenté - Ajoutez manuellement les champs au modèle")
        elif choice == 'D':
            print("\n⚠️  Non implémenté - Analysez d'abord si les données sont redondantes")
        else:
            print("❌ Aucune action effectuée")
    else:
        print("\n✅ Pas de données problématiques. Application de la suppression...")
        implement_option_a()
    
    print("\n" + "="*60)
    print("📋 Résumé:")
    print("   - Données vérifiées et sauvegardées dans CSV")
    print("   - Choisissez une option pour continuer")
    print("   - Redémarrez le serveur après les modifications")
    print("="*60)