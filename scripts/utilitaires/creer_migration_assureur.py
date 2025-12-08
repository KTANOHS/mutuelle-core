# creer_migration_assureur.py
import os
import django
from django.db import migrations, models
import django.db.models.deletion

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def creer_migration_assureur():
    """Crée et exécute la migration pour ajouter le champ assureur"""
    print("🔄 CRÉATION DE LA MIGRATION POUR LE CHAMP ASSUREUR")
    print("=" * 60)
    
    try:
        # Créer le fichier de migration
        migration_content = '''
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('agents', '0001_initial'),
        ('assureur', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='assureur',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='assureur.assureur',
                verbose_name='Assureur associé'
            ),
        ),
    ]
'''
        
        # Écrire le fichier de migration
        migration_path = 'agents/migrations/0002_agent_assureur.py'
        with open(migration_path, 'w') as f:
            f.write(migration_content)
        
        print(f"✅ Fichier de migration créé: {migration_path}")
        
    except Exception as e:
        print(f"❌ Erreur création migration: {e}")

def associer_agents_assureurs():
    """Associe les agents existants à des assureurs"""
    print("\n🔗 ASSOCIATION DES AGENTS AUX ASSUREURS")
    print("=" * 50)
    
    from agents.models import Agent
    from assureur.models import Assureur
    
    try:
        assureurs = Assureur.objects.all()
        agents = Agent.objects.all()
        
        print(f"Assureurs disponibles: {assureurs.count()}")
        print(f"Agents à associer: {agents.count()}")
        
        if assureurs.count() == 0:
            print("❌ Aucun assureur disponible pour l'association")
            return
        
        assureur_par_defaut = assureurs.first()
        print(f"✅ Assureur par défaut: {assureur_par_defaut}")
        
        agents_associes = 0
        for agent in agents:
            if not hasattr(agent, 'assureur') or agent.assureur is None:
                agent.assureur = assureur_par_defaut
                agent.save()
                agents_associes += 1
                print(f"   ✅ Agent {agent.nom_complet} associé à {assureur_par_defaut}")
        
        print(f"\n🎯 {agents_associes} agents associés à des assureurs")
        
    except Exception as e:
        print(f"❌ Erreur association agents: {e}")

def verifier_correction():
    """Vérifie que la correction a fonctionné"""
    print("\n🔍 VÉRIFICATION DE LA CORRECTION")
    print("=" * 50)
    
    from agents.models import Agent
    
    try:
        agents = Agent.objects.all()
        agents_avec_assureur = 0
        
        for agent in agents:
            if hasattr(agent, 'assureur') and agent.assureur:
                agents_avec_assureur += 1
                print(f"✅ {agent.nom_complet} -> {agent.assureur}")
            else:
                print(f"❌ {agent.nom_complet} -> PAS D'ASSUREUR")
        
        print(f"\n📊 RÉSULTAT: {agents_avec_assureur}/{agents.count()} agents avec assureur")
        
        if agents_avec_assureur == agents.count():
            print("🎯 CORRECTION RÉUSSIE!")
        else:
            print("⚠️  CORRECTION PARTIELLE")
            
    except Exception as e:
        print(f"❌ Erreur vérification: {e}")

if __name__ == "__main__":
    creer_migration_assureur()
    print("\n💡 EXÉCUTEZ MAINTENANT:")
    print("python manage.py makemigrations agents")
    print("python manage.py migrate")
    print("\n⏳ Après la migration, exécutez:")
    print("python associer_agents.py")