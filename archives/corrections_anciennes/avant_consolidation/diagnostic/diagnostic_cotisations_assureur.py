# diagnostic_cotisations_assureur.py
import os
import django
import sys
from datetime import datetime, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostic_cotisations_assureur():
    """Script complet de diagnostic du modèle Cotisation dans assureur"""
    
    print("🔍 DIAGNOSTIC COMPLET DU MODÈLE COTISATION - ASSUREUR")
    print("=" * 60)
    
    try:
        from assureur.models import Cotisation, Membre, Assureur
        from django.contrib.auth.models import User
        from django.db import models
        from django.utils import timezone
        print("✅ Modèles importés avec succès")
    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        return
    
    # 1. DIAGNOSTIC STRUCTURE MODÈLE
    print("\n📊 STRUCTURE DU MODÈLE COTISATION")
    print("-" * 40)
    
    try:
        # Vérifier les champs du modèle Cotisation
        cotisation_fields = [f.name for f in Cotisation._meta.get_fields()]
        print(f"✅ Modèle Cotisation - {len(cotisation_fields)} champs:")
        
        champs_importants = [
            'membre', 'periode', 'type_cotisation', 'montant', 'statut',
            'date_emission', 'date_echeance', 'date_paiement', 'reference'
        ]
        
        for champ in champs_importants:
            try:
                field_obj = Cotisation._meta.get_field(champ)
                print(f"   ✅ {champ}: {field_obj.get_internal_type()}")
            except:
                print(f"   ❌ {champ}: CHAMP MANQUANT")
        
    except Exception as e:
        print(f"❌ Erreur analyse structure: {e}")
    
    # 2. VÉRIFICATION DONNÉES EXISTANTES
    print("\n📈 DONNÉES EXISTANTES")
    print("-" * 40)
    
    try:
        # Compter les enregistrements
        nb_cotisations = Cotisation.objects.count()
        nb_membres = Membre.objects.count()
        nb_assureurs = Assureur.objects.count()
        
        print(f"📦 Cotisations: {nb_cotisations}")
        print(f"👥 Membres: {nb_membres}")
        print(f"🏢 Assureurs: {nb_assureurs}")
        
        # Afficher quelques membres pour test
        if nb_membres > 0:
            print(f"\n📝 Membres disponibles:")
            for membre in Membre.objects.all()[:5]:
                print(f"   • {membre.nom} {membre.prenom} - {membre.numero_membre}")
                print(f"     Femme enceinte: {membre.est_femme_enceinte}")
                print(f"     Taux couverture: {membre.taux_couverture}%")
        
    except Exception as e:
        print(f"❌ Erreur comptage données: {e}")
    
    # 3. ANALYSE STATUTS COTISATIONS
    print("\n🎯 ANALYSE DES STATUTS COTISATIONS")
    print("-" * 40)
    
    try:
        if nb_cotisations > 0:
            statuts = Cotisation.objects.values('statut').annotate(count=models.Count('id'))
            print("📊 Répartition par statut:")
            for statut in statuts:
                print(f"   • {statut['statut']}: {statut['count']}")
            
            # Types de cotisation
            types = Cotisation.objects.values('type_cotisation').annotate(
                count=models.Count('id'),
                total_montant=models.Sum('montant')
            )
            print(f"\n💰 Types de cotisation:")
            for type_cot in types:
                print(f"   • {type_cot['type_cotisation']}: {type_cot['count']} - {type_cot['total_montant']} FCFA")
                
        else:
            print("ℹ️  Aucune cotisation en base de données")
            
    except Exception as e:
        print(f"❌ Erreur analyse statuts: {e}")
    
    # 4. TEST CRÉATION COTISATIONS
    print("\n🧪 TEST CRÉATION COTISATIONS")
    print("-" * 40)
    
    try:
        # Vérifier si on peut créer des cotisations
        membre_test = Membre.objects.first()
        assureur_test = Assureur.objects.first()
        
        if membre_test and assureur_test:
            print(f"🔬 Test avec membre: {membre_test}")
            print(f"🔬 Test avec assureur: {assureur_test}")
            
            # Test création cotisation normale
            cotisation_normale = Cotisation(
                membre=membre_test,
                periode="2024-01",
                type_cotisation="normale",
                montant=Decimal('5000.00'),
                date_echeance=timezone.now().date() + timedelta(days=30),
                enregistre_par=assureur_test.user
            )
            
            # Vérification automatique des valeurs
            print(f"💰 Montant avant save: {cotisation_normale.montant}")
            print(f"🎯 Type avant save: {cotisation_normale.type_cotisation}")
            
            cotisation_normale.save()
            print(f"✅ Cotisation test créée: {cotisation_normale.reference}")
            print(f"💰 Montant après save: {cotisation_normale.montant}")
            print(f"🎯 Type après save: {cotisation_normale.type_cotisation}")
            print(f"📊 Répartition: {cotisation_normale.get_repartition()}")
            
            # Test avec femme enceinte
            if not membre_test.est_femme_enceinte:
                membre_test.est_femme_enceinte = True
                membre_test.save()
                print(f"🔁 Membre marqué comme femme enceinte")
            
            cotisation_enceinte = Cotisation(
                membre=membre_test,
                periode="2024-02", 
                date_echeance=timezone.now().date() + timedelta(days=30),
                enregistre_par=assureur_test.user
            )
            cotisation_enceinte.save()
            print(f"✅ Cotisation femme enceinte créée: {cotisation_enceinte.reference}")
            print(f"💰 Montant: {cotisation_enceinte.montant}")
            print(f"🎯 Type: {cotisation_enceinte.type_cotisation}")
            
        else:
            print("❌ Impossible de tester: membre ou assureur manquant")
            
    except Exception as e:
        print(f"❌ Erreur test création: {e}")
    
    # 5. VÉRIFICATION MÉTHODES MEMBRE
    print("\n👤 VÉRIFICATION MÉTHODES MEMBRE")
    print("-" * 40)
    
    try:
        if Membre.objects.exists():
            membre = Membre.objects.first()
            print(f"🔍 Test sur membre: {membre}")
            
            # Test méthodes de calcul
            print(f"💰 Cotisation mensuelle: {membre.montant_cotisation_mensuelle()} FCFA")
            print(f"✅ À jour cotisations: {membre.est_a_jour_cotisations()}")
            print(f"📅 Prochaine échéance: {membre.prochaine_echeance()}")
            print(f"💳 Montant dette: {membre.montant_dette()} FCFA")
            print(f"🎂 Âge: {membre.age()} ans")
            print(f"🔰 Actif: {membre.est_actif()}")
            
    except Exception as e:
        print(f"❌ Erreur méthodes membre: {e}")
    
    # 6. TEST FONCTIONNALITÉS AVANCÉES
    print("\n⚡ TEST FONCTIONNALITÉS AVANCÉES")
    print("-" * 40)
    
    try:
        if Cotisation.objects.exists():
            cotisation = Cotisation.objects.first()
            print(f"🔬 Test sur: {cotisation}")
            
            # Test méthodes de cotisation
            print(f"⏰ Jours retard: {cotisation.jours_retard()}")
            print(f"⚠️  En retard: {cotisation.est_en_retard()}")
            print(f"📊 Répartition: {cotisation.get_repartition()}")
            
            # Test paiement
            if cotisation.statut in ['due', 'en_retard']:
                ancien_statut = cotisation.statut
                cotisation.marquer_comme_payee(timezone.now().date(), cotisation.enregistre_par)
                print(f"✅ Paiement simulé: {ancien_statut} → {cotisation.statut}")
            
    except Exception as e:
        print(f"❌ Erreur fonctionnalités avancées: {e}")
    
    # 7. VÉRIFICATION CONTRAINTES
    print("\n🔍 VÉRIFICATION CONTRAINTES")
    print("-" * 40)
    
    try:
        # Vérifier les contraintes d'intégrité
        from django.db import transaction
        
        with transaction.atomic():
            # Test unicité période-membre
            if Cotisation.objects.exists():
                cotisation_existante = Cotisation.objects.first()
                try:
                    doublon = Cotisation(
                        membre=cotisation_existante.membre,
                        periode=cotisation_existante.periode,
                        montant=Decimal('5000.00'),
                        date_echeance=timezone.now().date() + timedelta(days=30)
                    )
                    doublon.save()
                    print("❌ ERREUR: Doublon période-membre autorisé")
                except:
                    print("✅ Contrainte unicité période-membre: OK")
        
        # Vérifier les références uniques
        references_uniques = Cotisation.objects.values('reference').annotate(
            count=models.Count('id')
        ).filter(count__gt=1)
        print(f"✅ Références uniques: {references_uniques.count()} doublons")
        
    except Exception as e:
        print(f"❌ Erreur vérification contraintes: {e}")
    
    # 8. RAPPORT FINAL
    print("\n📋 RAPPORT FINAL")
    print("-" * 40)
    
    try:
        # Résumé des problèmes
        problemes = []
        recommendations = []
        
        # Vérifications critiques
        if not Membre.objects.exists():
            problemes.append("Aucun membre en base")
            recommendations.append("Créer des membres de test")
        
        if not Assureur.objects.exists():
            problemes.append("Aucun assureur en base") 
            recommendations.append("Créer des profils assureur")
        
        cotisations_test = Cotisation.objects.filter(periode__contains="2024")
        if not cotisations_test.exists():
            problemes.append("Aucune cotisation de test créée")
            recommendations.append("Vérifier la création automatique")
        
        # Afficher le résumé
        if problemes:
            print("🚨 PROBLÈMES IDENTIFIÉS:")
            for probleme in problemes:
                print(f"   • {probleme}")
        else:
            print("✅ Aucun problème critique identifié")
        
        if recommendations:
            print("\n💡 RECOMMANDATIONS:")
            for reco in recommendations:
                print(f"   • {reco}")
        
        # Statistiques finales
        print(f"\n📊 STATISTIQUES FINALES:")
        print(f"   • Cotisations totales: {Cotisation.objects.count()}")
        print(f"   • Membres: {Membre.objects.count()}")
        print(f"   • Assureurs: {Assureur.objects.count()}")
        
        # Répartition finale
        if Cotisation.objects.exists():
            stats_finales = Cotisation.objects.aggregate(
                total_montant=models.Sum('montant'),
                moyenne_montant=models.Avg('montant'),
                total_payees=models.Count('id', filter=models.Q(statut='payee'))
            )
            print(f"   • Montant total: {stats_finales['total_montant']} FCFA")
            print(f"   • Montant moyen: {stats_finales['moyenne_montant']:.2f} FCFA")
            print(f"   • Cotisations payées: {stats_finales['total_payees']}")
        
    except Exception as e:
        print(f"❌ Erreur rapport final: {e}")
    
    print("\n" + "=" * 60)
    print("✅ DIAGNOSTIC COTISATIONS ASSUREUR TERMINÉ")

if __name__ == "__main__":
    diagnostic_cotisations_assureur()