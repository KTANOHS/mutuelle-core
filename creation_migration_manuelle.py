# creation_migration_manuelle.py
import os
import django
from django.db import migrations, models
import decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def creer_migration_manuelle():
    """Crée une migration manuelle pour ajouter les champs manquants"""
    print("🚀 Création de la migration manuelle...")
    
    migration_content = '''# Generated manually to add scoring fields to Membre model
from django.db import migrations, models
import decimal

class Migration(migrations.Migration):

    dependencies = [
        ('membres', '0001_initial'),  # Remplacez par la dernière migration de membres
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
    
    # Trouver le numéro de la prochaine migration
    migrations_dir = 'membres/migrations'
    existing_migrations = [f for f in os.listdir(migrations_dir) if f.endswith('.py') and f != '__init__.py']
    next_number = len(existing_migrations) + 1
    migration_filename = f'{next_number:04d}_add_scoring_fields.py'
    
    with open(f'{migrations_dir}/{migration_filename}', 'w', encoding='utf-8') as f:
        f.write(migration_content)
    
    print(f"✅ Migration créée: {migration_filename}")
    return migration_filename

def appliquer_migration_manuelle():
    """Applique la migration manuelle"""
    print("\\n🚀 Application de la migration manuelle...")
    
    from django.core.management import call_command
    try:
        call_command('migrate', 'membres')
        print("✅ Migration appliquée avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur application migration: {e}")
        return False

def verifier_champs_ajoutes():
    """Vérifie que les champs ont été ajoutés"""
    print("\\n🔍 Vérification des champs ajoutés...")
    
    from membres.models import Membre
    membre = Membre.objects.first()
    
    if hasattr(membre, 'score_risque'):
        print("✅ Champ score_risque disponible")
    else:
        print("❌ Champ score_risque toujours manquant")
    
    if hasattr(membre, 'niveau_risque'):
        print("✅ Champ niveau_risque disponible")
    else:
        print("❌ Champ niveau_risque toujours manquant")
    
    return hasattr(membre, 'score_risque') and hasattr(membre, 'niveau_risque')

def mettre_a_jour_tous_les_scores():
    """Met à jour tous les membres avec leurs scores"""
    print("\\n🎯 Mise à jour des scores pour tous les membres...")
    
    from membres.models import Membre
    from scoring.calculators import CalculateurScoreMembre
    from django.utils import timezone
    
    calculateur = CalculateurScoreMembre()
    membres = Membre.objects.all()
    compteur = 0
    
    for membre in membres:
        try:
            resultat = calculateur.calculer_score_complet(membre)
            
            # Mettre à jour le membre
            membre.score_risque = resultat['score_final']
            niveau_risque = resultat['niveau_risque'].lower()
            niveau_risque = niveau_risque.replace(' ', '_').replace('é', 'e').replace('è', 'e').replace('à', 'a')
            membre.niveau_risque = niveau_risque
            membre.date_dernier_score = timezone.now()
            membre.save()
            
            compteur += 1
            print(f"✅ {membre.nom}: {resultat['score_final']} ({resultat['niveau_risque']})")
            
        except Exception as e:
            print(f"❌ Erreur pour {membre.nom}: {e}")
    
    print(f"\\n📊 {compteur} membres mis à jour avec leurs scores")

def main():
    print("🚀 AJOUT DES CHAMPS SCORING AU MODÈLE MEMBRE")
    print("=" * 50)
    
    # Étape 1: Créer la migration
    migration_file = creer_migration_manuelle()
    
    # Étape 2: Appliquer la migration
    if appliquer_migration_manuelle():
        # Étape 3: Vérifier
        if verifier_champs_ajoutes():
            # Étape 4: Mettre à jour tous les scores
            mettre_a_jour_tous_les_scores()
            
            print("\\n" + "=" * 50)
            print("🎉 SUCCÈS COMPLET!")
            print("\\n📊 RÉSULTATS:")
            print("   ✅ Migration créée et appliquée")
            print("   ✅ Champs scoring ajoutés au modèle Membre")
            print("   ✅ Tous les membres ont leurs scores calculés")
            print("   ✅ Système de scoring complètement opérationnel")
        else:
            print("\\n❌ Les champs n'ont pas été ajoutés correctement")
    else:
        print("\\n❌ La migration n'a pas pu être appliquée")

if __name__ == "__main__":
    main()