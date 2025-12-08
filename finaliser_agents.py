# finaliser_agents.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from agents.models import Agent
from django.core.management import call_command

def finaliser_systeme_agents():
    print("🚀 FINALISATION DU SYSTÈME AGENTS 🚀")
    print("="*60)
    
    try:
        # 1. Vérifier/créer le groupe AGENT
        print("\n1. 📋 Configuration des groupes...")
        groupe_agent, created = Group.objects.get_or_create(name='AGENT')
        if created:
            print("   ✅ Groupe AGENT créé")
        else:
            print("   ✅ Groupe AGENT existe déjà")
        
        # 2. Vérifier l'utilisateur ORNELLA
        print("\n2. 👤 Configuration de l'utilisateur ORNELLA...")
        try:
            user = User.objects.get(username='ORNELLA')
            print(f"   ✅ Utilisateur ORNELLA trouvé (ID: {user.id})")
            
            # Ajouter au groupe AGENT si nécessaire
            if not user.groups.filter(name='AGENT').exists():
                user.groups.add(groupe_agent)
                print("   ✅ ORNELLA ajoutée au groupe AGENT")
            
            # Définir un mot de passe si vide
            if not user.password or user.password == '':
                user.set_password('Ornella@2024')
                user.save()
                print("   ✅ Mot de passe défini pour ORNELLA")
            
        except User.DoesNotExist:
            print("   ❌ Utilisateur ORNELLA non trouvé")
            return
        
        # 3. Vérifier/créer l'agent ORNELLA
        print("\n3. 🏢 Configuration de l'agent ORNELLA...")
        try:
            agent = Agent.objects.get(user=user)
            print(f"   ✅ Agent existant trouvé (ID: {agent.pk})")
            
            # Vérifier les champs
            if not agent.matricule:
                agent.matricule = 'AG001'
                print("   ✅ Matricule ajouté")
            
            if not agent.poste:
                agent.poste = 'Agent commercial'
                print("   ✅ Poste ajouté")
            
            if not hasattr(agent, 'est_actif'):
                agent.est_actif = True
                print("   ✅ Statut actif défini")
            
            agent.save()
            
        except Agent.DoesNotExist:
            print("   ⚠️ Agent non trouvé, création...")
            agent = Agent.objects.create(
                user=user,
                matricule='AG001',
                poste='Agent commercial',
                est_actif=True,
                limite_bons_quotidienne=10,
                telephone='',
                email_professionnel=''
            )
            print(f"   ✅ Agent créé (ID: {agent.pk})")
        
        # 4. Vérifier les URLs
        print("\n4. 🔗 Vérification des URLs...")
        try:
            from django.urls import reverse, NoReverseMatch
            
            urls_a_verifier = [
                ('agents:dashboard', 'Tableau de bord'),
                ('agents:liste_membres', 'Liste membres'),
                ('agents:creer_membre', 'Créer membre'),
                ('agents:creer_bon_soin', 'Créer bon'),
                ('agents:verification_cotisations', 'Vérifications'),
                ('agents:liste_messages', 'Messages'),
                ('agents:envoyer_message', 'Envoyer message'),
                ('agents:liste_notifications', 'Notifications'),
            ]
            
            for url_name, description in urls_a_verifier:
                try:
                    url = reverse(url_name)
                    print(f"   ✅ {description}: {url}")
                except NoReverseMatch:
                    print(f"   ⚠️ {description}: URL non configurée")
                    
        except Exception as e:
            print(f"   ❌ Erreur vérification URLs: {e}")
        
        # 5. Vérifier les templates
        print("\n5. 🎨 Vérification des templates...")
        templates = [
            'agents/templates/agents/base_agent.html',
            'agents/templates/agents/dashboard.html',
        ]
        
        for template in templates:
            if os.path.exists(template):
                print(f"   ✅ {template}: Existe")
            else:
                print(f"   ❌ {template}: Manquant")
        
        # 6. Créer un superutilisateur de secours
        print("\n6. 🔑 Création superutilisateur de secours...")
        try:
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@mutuelle.core',
                    password='Admin@2024'
                )
                print("   ✅ Superutilisateur 'admin' créé")
            else:
                print("   ✅ Superutilisateur 'admin' existe déjà")
        except Exception as e:
            print(f"   ⚠️ Erreur création admin: {e}")
        
        # 7. Vider les sessions
        print("\n7. 🧹 Nettoyage des sessions...")
        try:
            call_command('clearsessions')
            print("   ✅ Sessions nettoyées")
        except Exception as e:
            print(f"   ⚠️ Erreur nettoyage sessions: {e}")
        
        print("\n" + "="*60)
        print("🎉 FINALISATION TERMINÉE AVEC SUCCÈS !")
        print("\n📋 INFORMATIONS DE CONNEXION :")
        print(f"   👤 Utilisateur: ORNELLA")
        print(f"   🔑 Mot de passe: [Celui que vous avez défini]")
        print(f"   🆔 Agent ID: {agent.pk}")
        print(f"   📋 Matricule: {agent.matricule}")
        print("\n🌐 URLS IMPORTANTES :")
        print(f"   📊 Dashboard: http://127.0.0.1:8000/agents/tableau-de-bord/")
        print(f"   👥 Membres: http://127.0.0.1:8000/agents/membres/")
        print(f"   📝 Créer bon: http://127.0.0.1:8000/agents/bons/creer/")
        
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    finaliser_systeme_agents()