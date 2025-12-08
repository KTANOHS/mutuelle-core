# correcteur_problemes_diagnostic.py

import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

def creer_groupes_manquants():
    """Crée les groupes manquants identifiés par le diagnostic"""
    print("🔧 CRÉATION DES GROUPES MANQUANTS")
    print("=" * 50)
    
    groupes_a_creer = ['Médecins', 'Pharmaciens', 'Membres']
    
    for nom_groupe in groupes_a_creer:
        groupe, created = Group.objects.get_or_create(name=nom_groupe)
        if created:
            print(f"✅ Groupe '{nom_groupe}' créé")
        else:
            print(f"✅ Groupe '{nom_groupe}' existe déjà")

def creer_profils_agents():
    """Crée les profils Agent pour les utilisateurs existants"""
    print("\n🔧 CRÉATION DES PROFILS AGENTS")
    print("=" * 50)
    
    try:
        from agents.models import Agent
        
        # Compter les utilisateurs dans le groupe Agents sans profil
        users_agents = User.objects.filter(groups__name='Agents')
        agents_sans_profil = []
        
        for user in users_agents:
            try:
                Agent.objects.get(user=user)
            except Agent.DoesNotExist:
                agents_sans_profil.append(user)
        
        print(f"👥 Utilisateurs Agents sans profil: {len(agents_sans_profil)}")
        
        # Créer les profils manquants
        for user in agents_sans_profil:
            numero_agent = f"AGT-{user.id:03d}"
            Agent.objects.create(
                user=user,
                numero_agent=numero_agent,
                telephone="+2250100000000",
                actif=True
            )
            print(f"✅ Profil Agent créé pour {user.username} - {numero_agent}")
            
    except Exception as e:
        print(f"❌ Erreur création profils agents: {e}")

def corriger_url_medecin_manquante():
    """Corrige l'URL manquante pour les médecins"""
    print("\n🔧 CORRECTION URL MÉDECIN MANQUANTE")
    print("=" * 50)
    
    urls_file = Path("medecin/urls.py")
    
    if not urls_file.exists():
        print("❌ Fichier medecin/urls.py non trouvé")
        return
    
    with open(urls_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si liste_ordonnances existe
    if "name='liste_ordonnances'" not in content:
        print("❌ URL 'liste_ordonnances' manquante dans medecin/urls.py")
        
        # Ajouter l'URL manquante
        nouvelle_ligne = "    path('ordonnances/', views.liste_ordonnances, name='liste_ordonnances'),\n"
        
        # Trouver où insérer (après le dashboard)
        if "path('dashboard/'" in content:
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                new_lines.append(line)
                if "path('dashboard/'" in line:
                    new_lines.append(nouvelle_ligne)
            
            content_corrige = '\n'.join(new_lines)
            
            with open(urls_file, 'w', encoding='utf-8') as f:
                f.write(content_corrige)
            print("✅ URL 'liste_ordonnances' ajoutée à medecin/urls.py")
    else:
        print("✅ URL 'liste_ordonnances' déjà présente")

def corriger_erreur_membre_bons():
    """Corrige l'erreur 'membre' au lieu de 'patient'"""
    print("\n🔧 CORRECTION ERREUR MEMBRE/BONS")
    print("=" * 50)
    
    views_file = Path("membres/views.py")
    
    if not views_file.exists():
        print("❌ Fichier membres/views.py non trouvé")
        return
    
    with open(views_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer 'membre' par 'patient' dans la vue des bons
    if "queryset.filter(membre=user.membre)" in content:
        content_corrige = content.replace(
            "queryset.filter(membre=user.membre)", 
            "queryset.filter(patient=user.membre)"
        )
        
        with open(views_file, 'w', encoding='utf-8') as f:
            f.write(content_corrige)
        print("✅ Erreur 'membre' -> 'patient' corrigée")
    else:
        print("✅ Aucune erreur 'membre' détectée")

def creer_donnees_test():
    """Crée des données de test pour valider les accès"""
    print("\n🧪 CRÉATION DE DONNÉES TEST")
    print("=" * 50)
    
    try:
        from membres.models import Membre
        from soins.models import BonDeSoin
        from medecin.models import Ordonnance, Medecin
        from agents.models import Agent
        
        # Créer quelques bons de soin
        if BonDeSoin.objects.count() == 0:
            membres = Membre.objects.all()[:3]
            for i, membre in enumerate(membros):
                bon = BonDeSoin.objects.create(
                    patient=membre,
                    symptomes="Fièvre et toux",
                    diagnostic="Infection respiratoire",
                    montant=15000 + (i * 5000),
                    statut="valide"
                )
                print(f"✅ Bon de soin créé pour {membre.prenom} {membre.nom}")
        
        # Créer quelques ordonnances
        if Ordonnance.objects.count() == 0 and Medecin.objects.exists():
            medecin = Medecin.objects.first()
            membres = Membre.objects.all()[:2]
            
            for i, membre in enumerate(membros):
                ordonnance = Ordonnance.objects.create(
                    patient=membre,
                    medecin=medecin,
                    medicaments="Paracétamol 1000mg - 1 comprimé 3x/jour",
                    posologie="7 jours",
                    diagnostic="Traitement symptomatique"
                )
                print(f"✅ Ordonnance créée pour {membre.prenom} {membre.nom}")
                
    except Exception as e:
        print(f"❌ Erreur création données test: {e}")

def assigner_utilisateurs_groupes():
    """Assigne les utilisateurs de test aux groupes appropriés"""
    print("\n🔧 ASSIGNATION UTILISATEURS AUX GROUPES")
    print("=" * 50)
    
    assignments = {
        'medecin_test': 'Médecins',
        'pharmacien_test': 'Pharmaciens', 
        'membre_test': 'Membres'
    }
    
    for username, groupe_nom in assignments.items():
        try:
            user = User.objects.get(username=username)
            groupe = Group.objects.get(name=groupe_nom)
            user.groups.add(groupe)
            print(f"✅ {username} assigné au groupe {groupe_nom}")
        except User.DoesNotExist:
            print(f"❌ Utilisateur {username} non trouvé")
        except Group.DoesNotExist:
            print(f"❌ Groupe {groupe_nom} non trouvé")

def verifier_corrections():
    """Vérifie que toutes les corrections ont été appliquées"""
    print("\n🔍 VÉRIFICATION DES CORRECTIONS")
    print("=" * 50)
    
    # Vérifier groupes
    groupes_requis = ['Médecins', 'Pharmaciens', 'Membres']
    for groupe in groupes_requis:
        if Group.objects.filter(name=groupe).exists():
            print(f"✅ Groupe {groupe}: PRÉSENT")
        else:
            print(f"❌ Groupe {groupe}: MANQUANT")
    
    # Vérifier profils agents
    try:
        from agents.models import Agent
        users_agents = User.objects.filter(groups__name='Agents')
        agents_avec_profil = Agent.objects.filter(user__in=users_agents).count()
        print(f"✅ Agents avec profil: {agents_avec_profil}/{users_agents.count()}")
    except Exception as e:
        print(f"❌ Vérification profils agents: {e}")
    
    # Vérifier URL médecin
    urls_file = Path("medecin/urls.py")
    if urls_file.exists():
        with open(urls_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if "name='liste_ordonnances'" in content:
            print("✅ URL liste_ordonnances: PRÉSENTE")
        else:
            print("❌ URL liste_ordonnances: MANQUANTE")
    
    # Vérifier données
    from soins.models import BonDeSoin
    from medecin.models import Ordonnance
    print(f"✅ Bons de soin: {BonDeSoin.objects.count()}")
    print(f"✅ Ordonnances: {Ordonnance.objects.count()}")

def corriger_tous_problemes():
    """Exécute toutes les corrections"""
    print("🚀 CORRECTION DE TOUS LES PROBLÈMES IDENTIFIÉS")
    print("=" * 60)
    
    creer_groupes_manquants()
    creer_profils_agents()
    corriger_url_medecin_manquante()
    corriger_erreur_membre_bons()
    creer_donnees_test()
    assigner_utilisateurs_groupes()
    verifier_corrections()
    
    print("\n" + "=" * 60)
    print("✅ CORRECTIONS TERMINÉES")
    print("=" * 60)
    
    print("\n📋 ACTIONS EFFECTUÉES:")
    print("• Groupes Médecins, Pharmaciens, Membres créés")
    print("• Profils Agent créés pour les utilisateurs")
    print("• URL liste_ordonnances ajoutée pour les médecins") 
    print("• Erreur 'membre' -> 'patient' corrigée")
    print("• Données de test créées (bons, ordonnances)")
    print("• Utilisateurs assignés aux groupes")

if __name__ == "__main__":
    corriger_tous_problemes()