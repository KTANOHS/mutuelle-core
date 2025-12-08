#!/usr/bin/env python
"""
GÉNÉRATEUR DE COTISATIONS - VERSION FINALE POUR VOTRE PROJET
Script prêt à être utilisé régulièrement
"""

import os
import sys
import django
from datetime import datetime, timedelta
import random
from django.db.models import Sum, Count

# Configuration Django
def setup_django():
    """Configuration de l'environnement Django"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.abspath(os.path.join(current_dir, '..'))
        sys.path.append(project_dir)
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        django.setup()
        return True
    except Exception as e:
        print(f"❌ Erreur de configuration Django: {e}")
        return False

def generer_cotisations_mensuelles(mois_a_generer=6, supprimer_anciennes=True):
    """
    Générer des cotisations mensuelles pour tous les membres actifs
    Args:
        mois_a_generer: Nombre de mois à générer (par défaut 6)
        supprimer_anciennes: Supprimer les anciennes cotisations (True par défaut)
    """
    
    if not setup_django():
        return False
    
    print("\n" + "="*60)
    print("🚀 GÉNÉRATION DE COTISATIONS MENSUELLES")
    print("="*60)
    
    # Import des modèles
    from membres.models import Membre
    from assureur.models import Cotisation
    from django.contrib.auth.models import User
    
    # Utilisateur pour l'enregistrement
    try:
        admin_user = User.objects.filter(is_superuser=True).first() or User.objects.first()
        print(f"👤 Enregistré par: {admin_user.username if admin_user else 'System'}")
    except:
        admin_user = None
    
    # Récupérer les membres actifs
    membres = Membre.objects.filter(statut='actif')
    total_membres = membres.count()
    
    print(f"👥 Membres actifs: {total_membres}")
    
    if total_membres == 0:
        print("❌ Aucun membre actif trouvé")
        return False
    
    # Nettoyage si demandé
    if supprimer_anciennes:
        print("\n🧹 Nettoyage des anciennes cotisations...")
        supprimees = Cotisation.objects.all().delete()
        print(f"✅ {supprimees[0]} cotisations supprimées")
    
    # Générer les périodes (mois précédents)
    aujourdhui = datetime.now()
    periodes = []
    
    for i in range(mois_a_generer):
        mois = aujourdhui.month - i
        annee = aujourdhui.year
        
        if mois <= 0:
            mois += 12
            annee -= 1
        
        periode = f"{annee}-{mois:02d}"
        periodes.append(periode)
    
    print(f"\n📅 Périodes à générer: {len(periodes)} mois")
    
    total_cree = 0
    
    # Génération pour chaque période
    for periode in periodes:
        print(f"\n🔄 Génération {periode}...")
        
        for membre in membres:
            try:
                # Vérifier si une cotisation existe déjà pour cette période
                if Cotisation.objects.filter(membre=membre, periode=periode).exists():
                    print(f"  ⚠️  {membre.nom} {membre.prenom}: Existe déjà, ignoré")
                    continue
                
                # Montant selon le type de cotisation
                types_cotisation = [
                    ('mensuelle', (3000, 8000)),      # Mensuelle: 3k-8k
                    ('trimestrielle', (10000, 15000)), # Trimestrielle: 10k-15k
                    ('annuelle', (20000, 30000)),     # Annuelle: 20k-30k
                    ('exceptionnelle', (5000, 12000)), # Exceptionnelle: 5k-12k
                ]
                
                type_cot, (montant_min, montant_max) = random.choice(types_cotisation)
                montant = random.randint(montant_min, montant_max)
                
                # Dates
                annee, mois = map(int, periode.split('-'))
                date_emission = datetime(annee, mois, 1).date()
                date_echeance = date_emission + timedelta(days=30)
                
                # Statut (80% payées, 20% en attente)
                statut = 'payee' if random.random() < 0.8 else 'en_attente'
                date_paiement = date_emission + timedelta(days=random.randint(1, 15)) if statut == 'payee' else None
                
                # Création
                cotisation = Cotisation.objects.create(
                    membre=membre,
                    periode=periode,
                    type_cotisation=type_cot,
                    montant=montant,
                    date_emission=date_emission,
                    date_echeance=date_echeance,
                    date_paiement=date_paiement,
                    statut=statut,
                    reference=f"COT-{periode}-{membre.id:03d}",
                    enregistre_par=admin_user,
                    notes=f"Cotisation {type_cot} {periode}"
                )
                
                print(f"  ✅ {membre.nom} {membre.prenom}: {montant:,} FCFA ({type_cot}, {statut})")
                total_cree += 1
                
            except Exception as e:
                print(f"  ❌ Erreur pour {membre.nom}: {str(e)[:50]}...")
    
    # Vérification finale
    print("\n" + "="*60)
    print("📊 VÉRIFICATION FINALE")
    print("="*60)
    
    total_base = Cotisation.objects.count()
    total_montant = Cotisation.objects.aggregate(total=Sum('montant'))['total'] or 0
    
    print(f"✅ Cotisations créées: {total_cree}")
    print(f"📈 Total en base: {total_base}")
    print(f"💰 Montant total: {total_montant:,.0f} FCFA")
    
    if total_base > 0:
        # Statistiques
        print(f"\n📊 STATISTIQUES:")
        
        # Par période
        stats_periode = Cotisation.objects.values('periode').annotate(
            count=Count('id'),
            total=Sum('montant')
        ).order_by('-periode')
        
        print(f"📅 Par période:")
        for stat in stats_periode:
            print(f"  • {stat['periode']}: {stat['count']} cotisations = {stat['total']:,.0f} FCFA")
        
        # Par statut
        stats_statut = Cotisation.objects.values('statut').annotate(
            count=Count('id'),
            total=Sum('montant')
        )
        
        print(f"\n📋 Par statut:")
        for stat in stats_statut:
            pourcentage = (stat['total'] / total_montant * 100) if total_montant > 0 else 0
            print(f"  • {stat['statut']}: {stat['count']} = {stat['total']:,.0f} FCFA ({pourcentage:.1f}%)")
    
    print("\n🎉 Génération terminée avec succès !")
    return True

def afficher_statistiques():
    """Afficher les statistiques actuelles des cotisations"""
    
    if not setup_django():
        return
    
    from assureur.models import Cotisation
    from membres.models import Membre
    
    print("\n" + "="*60)
    print("📈 STATISTIQUES DES COTISATIONS")
    print("="*60)
    
    total_cotisations = Cotisation.objects.count()
    total_membres = Membre.objects.filter(statut='actif').count()
    
    if total_cotisations == 0:
        print("❌ Aucune cotisation enregistrée")
        return
    
    # Montant total
    stats = Cotisation.objects.aggregate(
        total=Sum('montant'),
        moyenne=Sum('montant') / total_cotisations,
        max=Max('montant'),
        min=Min('montant')
    )
    
    print(f"\n📊 GÉNÉRAL:")
    print(f"  • Cotisations: {total_cotisations}")
    print(f"  • Membres actifs: {total_membres}")
    print(f"  • Montant total: {stats['total']:,.0f} FCFA")
    print(f"  • Montant moyen: {stats['moyenne']:,.0f} FCFA")
    print(f"  • Montant max: {stats['max']:,.0f} FCFA")
    print(f"  • Montant min: {stats['min']:,.0f} FCFA")
    
    # Dernière période
    derniere_periode = Cotisation.objects.order_by('-periode').first()
    if derniere_periode:
        print(f"  • Dernière période: {derniere_periode.periode}")
    
    # Top 5 membres par cotisations
    print(f"\n🏆 TOP 5 MEMBRES:")
    top_membres = Cotisation.objects.values(
        'membre__nom', 'membre__prenom'
    ).annotate(
        count=Count('id'),
        total=Sum('montant')
    ).order_by('-total')[:5]
    
    for i, membre in enumerate(top_membres, 1):
        nom = f"{membre['membre__prenom']} {membre['membre__nom']}"
        print(f"  {i}. {nom}: {membre['total']:,.0f} FCFA ({membre['count']} cotisations)")

def ajouter_cotisation_manuel():
    """Ajouter une cotisation manuellement pour un membre"""
    
    if not setup_django():
        return
    
    from membres.models import Membre
    from assureur.models import Cotisation
    from django.contrib.auth.models import User
    
    print("\n" + "="*60)
    print("👥 AJOUT MANUEL DE COTISATION")
    print("="*60)
    
    # Lister les membres
    membres = Membre.objects.all()
    print(f"\n📋 LISTE DES MEMBRES:")
    for i, membre in enumerate(membres, 1):
        print(f"  {i}. {membre.prenom} {membre.nom} ({membre.statut})")
    
    try:
        choix = int(input("\n🔢 Numéro du membre: ")) - 1
        if choix < 0 or choix >= len(membres):
            print("❌ Choix invalide")
            return
        
        membre = membres[choix]
        print(f"\n👤 Membre sélectionné: {membre.prenom} {membre.nom}")
        
        # Saisie des informations
        periode = input("📅 Période (AAAA-MM): ").strip()
        montant = float(input("💰 Montant (FCFA): "))
        type_cot = input("🏷️  Type (mensuelle/trimestrielle/annuelle/exceptionnelle): ").strip()
        statut = input("📋 Statut (payee/en_attente/due): ").strip()
        
        # Date d'émission (par défaut: 1er du mois)
        annee, mois = map(int, periode.split('-'))
        date_emission = datetime(annee, mois, 1).date()
        date_echeance = date_emission + timedelta(days=30)
        
        date_paiement = None
        if statut == 'payee':
            date_paiement = date_emission + timedelta(days=random.randint(1, 15))
        
        # Utilisateur admin
        admin_user = User.objects.filter(is_superuser=True).first()
        
        # Création
        cotisation = Cotisation.objects.create(
            membre=membre,
            periode=periode,
            type_cotisation=type_cot,
            montant=montant,
            date_emission=date_emission,
            date_echeance=date_echeance,
            date_paiement=date_paiement,
            statut=statut,
            reference=f"MAN-{periode}-{membre.id:03d}",
            enregistre_par=admin_user,
            notes="Cotisation ajoutée manuellement"
        )
        
        print(f"\n✅ Cotisation créée avec succès!")
        print(f"📋 ID: {cotisation.id}")
        print(f"💰 Montant: {cotisation.montant} FCFA")
        print(f"📅 Période: {cotisation.periode}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    # Menu principal
    print("\n" + "="*60)
    print("💰 GESTION DES COTISATIONS")
    print("="*60)
    print("1. Générer cotisations mensuelles (6 derniers mois)")
    print("2. Afficher les statistiques")
    print("3. Ajouter une cotisation manuellement")
    print("4. Tester la connexion Django")
    print("5. Quitter")
    
    try:
        choix = input("\n🎯 Votre choix (1-5): ").strip()
        
        if choix == "1":
            # Demander confirmation
            confirm = input("⚠️  Cela va supprimer les anciennes cotisations. Continuer? (o/N): ")
            if confirm.lower() in ['o', 'oui', 'y', 'yes']:
                generer_cotisations_mensuelles()
            else:
                print("❌ Annulé")
        
        elif choix == "2":
            afficher_statistiques()
        
        elif choix == "3":
            ajouter_cotisation_manuel()
        
        elif choix == "4":
            if setup_django():
                print("✅ Django configuré avec succès")
                from assureur.models import Cotisation
                count = Cotisation.objects.count()
                print(f"📊 Cotisations en base: {count}")
        
        elif choix == "5":
            print("👋 Au revoir!")
        
        else:
            print("❌ Choix invalide")
    
    except KeyboardInterrupt:
        print("\n\n👋 Interruption utilisateur")
    except Exception as e:
        print(f"❌ Erreur: {e}")