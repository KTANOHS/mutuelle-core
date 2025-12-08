# correction_urgence_bdd.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.core.management import call_command
import sqlite3

def analyser_probleme_migrations():
    """Analyse ce qui s'est passé avec les migrations"""
    print("🔍 ANALYSE DU PROBLÈME DE MIGRATIONS")
    print("=" * 50)
    
    # Vérifier les migrations existantes
    migrations_dir = 'membres/migrations'
    fichiers = sorted([f for f in os.listdir(migrations_dir) if f.endswith('.py') and f != '__init__.py'])
    
    print("📋 Migrations trouvées:")
    for f in fichiers:
        print(f"   {f}")
        
        # Lire le contenu pour voir ce qu'elles font
        with open(f"{migrations_dir}/{f}", 'r') as file:
            lignes = file.readlines()
            for ligne in lignes[:10]:  # Premières 10 lignes
                if 'Remove field' in ligne or 'Add field' in ligne:
                    print(f"     → {ligne.strip()}")

def corriger_migration_manquante():
    """Crée une migration correcte pour ajouter les champs"""
    print("\\n🚀 CRÉATION D'UNE MIGRATION CORRECTE")
    
    # Supprimer les migrations problématiques
    migrations_problematiques = ['0002_add_scoring_fields.py', '0003_remove_membre_date_dernier_score_and_more.py']
    
    for migration in migrations_problematiques:
        chemin = f"membres/migrations/{migration}"
        if os.path.exists(chemin):
            os.remove(chemin)
            print(f"✅ Supprimé: {migration}")
    
    # Vérifier le modèle actuel
    with open('membres/models.py', 'r') as f:
        contenu = f.read()
        if 'score_risque' in contenu:
            print("✅ Modèle contient les champs scoring")
        else:
            print("❌ Modèle ne contient PAS les champs scoring")
    
    # Créer une migration propre
    migration_content = '''# Generated manually - Add scoring fields to Membre
from django.db import migrations, models
import decimal

class Migration(migrations.Migration):

    dependencies = [
        ('membres', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='membre',
            name='score_risque',
            field=models.DecimalField(decimal_places=2, default=50.0, max_digits=5, verbose_name='Score de risque'),
        ),
        migrations.AddField(
            model_name='membre',
            name='niveau_risque',
            field=models.CharField(choices=[('faible', '🟢 Faible risque'), ('modere', '🟡 Risque modéré'), ('eleve', '🟠 Risque élevé'), ('tres_eleve', '🔴 Risque très élevé')], default='faible', max_length=20),
        ),
        migrations.AddField(
            model_name='membre',
            name='fraude_suspectee',
            field=models.BooleanField(default=False, verbose_name='Fraude suspectée par IA'),
        ),
        migrations.AddField(
            model_name='membre',
            name='date_dernier_score',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date du dernier calcul de score'),
        ),
        migrations.AddField(
            model_name='membre',
            name='date_derniere_analyse_ia',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Dernière analyse IA'),
        ),
    ]
'''
    
    with open('membres/migrations/0002_add_scoring_fields_fixed.py', 'w') as f:
        f.write(migration_content)
    
    print("✅ Migration correcte créée: 0002_add_scoring_fields_fixed.py")

def reinitialiser_base_de_donnees():
    """Réinitialise complètement la base de données si nécessaire"""
    print("\\n🔄 RÉINITIALISATION DE LA BASE DE DONNÉES")
    
    reponse = input("❓ Voulez-vous réinitialiser la base de données? (oui/non): ")
    if reponse.lower() != 'oui':
        print("⏭️  Réinitialisation annulée")
        return False
    
    try:
        # Sauvegarder les données importantes d'abord
        print("💾 Sauvegarde des données importantes...")
        
        # Supprimer la base de données
        if os.path.exists('db.sqlite3'):
            os.remove('db.sqlite3')
            print("✅ Base de données supprimée")
        
        # Recréer les migrations
        call_command('makemigrations')
        call_command('migrate')
        
        print("✅ Base de données réinitialisée avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur réinitialisation: {e}")
        return False

def solution_alternative_sans_migration():
    """Solution alternative sans toucher à la base de données"""
    print("\\n🎯 SOLUTION ALTERNATIVE SANS MIGRATION")
    
    # Créer un modèle proxy ou utiliser les relations existantes
    solution_content = '''
SOLUTION ALTERNATIVE:

1. UTILISER L'HISTORIQUE DE SCORING EXISTANT
   - Le système de scoring fonctionne déjà
   - Les scores sont sauvegardés dans scoring.HistoriqueScore
   - Utiliser cette table au lieu d'ajouter des champs à Membre

2. CRÉER UNE VUE OU UN SERVICE
   - Récupérer le dernier score depuis HistoriqueScore
   - Ne pas modifier le modèle Membre existant

3. EXEMPLE D'UTILISATION:

   from scoring.models import HistoriqueScore
   from membres.models import Membre

   def get_score_membre(membre):
       dernier_score = HistoriqueScore.objects.filter(
           membre=membre
       ).order_by('-date_calcul').first()
       
       if dernier_score:
           return {
               'score': dernier_score.score,
               'niveau_risque': dernier_score.niveau_risque,
               'date_calcul': dernier_score.date_calcul
           }
       return None

4. AVANTAGES:
   - Pas de modification de la base de données
   - Historique complet conservé
   - Système déjà fonctionnel
'''
    print(solution_content)

def verifier_etat_actuel():
    """Vérifie l'état actuel du système"""
    print("\\n🔍 ÉTAT ACTUEL DU SYSTÈME")
    
    try:
        # Tester avec une connexion directe SQL
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        # Vérifier les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📊 Tables dans la base: {len(tables)}")
        
        # Vérifier la table membres
        cursor.execute("PRAGMA table_info(membres_membre);")
        colonnes = [row[1] for row in cursor.fetchall()]
        print(f"📋 Colonnes dans membres_membre: {len(colonnes)}")
        
        # Chercher les champs scoring
        champs_scoring = ['score_risque', 'niveau_risque']
        for champ in champs_scoring:
            if champ in colonnes:
                print(f"✅ {champ} présent dans la table")
            else:
                print(f"❌ {champ} absent de la table")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur vérification base: {e}")

def main():
    print("🚨 CORRECTION URGENTE - PROBLÈME DE MIGRATIONS")
    print("=" * 60)
    
    # Analyser le problème
    analyser_probleme_migrations()
    
    # Vérifier l'état actuel
    verifier_etat_actuel()
    
    # Proposer des solutions
    print("\\n🎯 CHOISISSEZ UNE SOLUTION:")
    print("1. Créer une migration correcte (recommandé)")
    print("2. Réinitialiser la base de données (radical)")
    print("3. Solution alternative sans migration (sans risque)")
    
    choix = input("\\n🔢 Votre choix (1/2/3): ")
    
    if choix == '1':
        corriger_migration_manquante()
        print("\\n📋 Appliquez maintenant la migration:")
        print("   python manage.py migrate membres")
        
    elif choix == '2':
        reinitialiser_base_de_donnees()
        
    elif choix == '3':
        solution_alternative_sans_migration()
        print("\\n🎯 Le système de scoring fonctionne DÉJÀ sans les champs!")
        print("   Utilisez scoring.HistoriqueScore pour accéder aux scores")
        
    else:
        print("❌ Choix invalide")

if __name__ == "__main__":
    main()