# analyse_cotisations_existant.py
import os
import sys
import django
from django.db import models
from django.apps import apps
from datetime import datetime, timedelta
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyser_modeles_existants():
    """Analyse les modèles existants dans la base de données"""
    print("=" * 80)
    print("🔍 ANALYSE DES MODÈLES EXISTANTS")
    print("=" * 80)
    
    modeles_pertinents = [
        'Membre', 'Cotisation', 'Paiement', 'Bon', 'Soin', 
        'Assureur', 'Agent', 'VerificationCotisation'
    ]
    
    for modele_name in modeles_pertinents:
        try:
            modele = apps.get_model('assureur', modele_name)
            print(f"\n📊 MODÈLE: {modele_name}")
            print(f"   📍 Application: {modele._meta.app_label}")
            print(f"   📋 Champs:")
            
            for champ in modele._meta.get_fields():
                if hasattr(champ, 'name'):
                    type_champ = champ.get_internal_type()
                    print(f"      • {champ.name} ({type_champ})")
                    
        except LookupError:
            print(f"\n❌ MODÈLE: {modele_name} - NON TROUVÉ")

def analyser_membres_existants():
    """Analyse les membres existants et leurs données"""
    print("\n" + "=" * 80)
    print("👥 ANALYSE DES MEMBRES EXISTANTS")
    print("=" * 80)
    
    try:
        Membre = apps.get_model('assureur', 'Membre')
        total_membres = Membre.objects.count()
        
        print(f"📈 Total membres: {total_membres}")
        
        if total_membres > 0:
            # Statuts des membres
            statuts = Membre.objects.values('statut').annotate(count=models.Count('id'))
            print(f"\n📊 Répartition par statut:")
            for statut in statuts:
                print(f"   • {statut['statut']}: {statut['count']} membres")
            
            # Types de contrat
            contrats = Membre.objects.values('type_contrat').annotate(count=models.Count('id'))
            print(f"\n📄 Répartition par type de contrat:")
            for contrat in contrats:
                print(f"   • {contrat['type_contrat']}: {contrat['count']} membres")
            
            # Taux de couverture
            couverture_stats = Membre.objects.aggregate(
                avg=models.Avg('taux_couverture'),
                min=models.Min('taux_couverture'),
                max=models.Max('taux_couverture')
            )
            print(f"\n🎯 Statistiques taux de couverture:")
            print(f"   • Moyenne: {couverture_stats['avg']:.2f}%")
            print(f"   • Min: {couverture_stats['min']}%")
            print(f"   • Max: {couverture_stats['max']}%")
            
            # Membres avec user associé
            membres_avec_user = Membre.objects.filter(user__isnull=False).count()
            print(f"\n👤 Membres avec compte utilisateur: {membres_avec_user}/{total_membres}")
            
    except Exception as e:
        print(f"❌ Erreur analyse membres: {e}")

def analyser_cotisations_existantes():
    """Analyse les données de cotisations existantes"""
    print("\n" + "=" * 80)
    print("💰 ANALYSE DES COTISATIONS EXISTANTES")
    print("=" * 80)
    
    try:
        Cotisation = apps.get_model('assureur', 'Cotisation')
        total_cotisations = Cotisation.objects.count()
        
        print(f"📈 Total cotisations: {total_cotisations}")
        
        if total_cotisations > 0:
            # Statuts des cotisations
            statuts = Cotisation.objects.values('statut').annotate(count=models.Count('id'))
            print(f"\n📊 Répartition par statut:")
            for statut in statuts:
                print(f"   • {statut['statut']}: {statut['count']} cotisations")
            
            # Montants
            montant_stats = Cotisation.objects.aggregate(
                total=models.Sum('montant'),
                avg=models.Avg('montant'),
                min=models.Min('montant'),
                max=models.Max('montant')
            )
            print(f"\n💵 Statistiques montants:")
            print(f"   • Total: {montant_stats['total'] or 0:.2f} FCFA")
            print(f"   • Moyenne: {montant_stats['avg'] or 0:.2f} FCFA")
            print(f"   • Min: {montant_stats['min'] or 0:.2f} FCFA")
            print(f"   • Max: {montant_stats['max'] or 0:.2f} FCFA")
            
            # Périodes
            periodes = Cotisation.objects.values('periode').annotate(
                count=models.Count('id'),
                total=models.Sum('montant')
            ).order_by('-periode')[:12]  # 12 derniers mois
            
            print(f"\n📅 Cotisations par période (12 derniers mois):")
            for periode in periodes:
                print(f"   • {periode['periode']}: {periode['count']} cotisations, {periode['total'] or 0:.2f} FCFA")
                
    except LookupError:
        print("ℹ️  Modèle Cotisation non trouvé - À créer")
    except Exception as e:
        print(f"❌ Erreur analyse cotisations: {e}")

def analyser_paiements_existants():
    """Analyse les paiements existants"""
    print("\n" + "=" * 80)
    print("💳 ANALYSE DES PAIEMENTS EXISTANTS")
    print("=" * 80)
    
    try:
        Paiement = apps.get_model('assureur', 'Paiement')
        total_paiements = Paiement.objects.count()
        
        print(f"📈 Total paiements: {total_paiements}")
        
        if total_paiements > 0:
            # Modes de paiement
            modes = Paiement.objects.values('mode_paiement').annotate(count=models.Count('id'))
            print(f"\n💳 Répartition par mode de paiement:")
            for mode in modes:
                print(f"   • {mode['mode_paiement']}: {mode['count']} paiements")
            
            # Statuts
            statuts = Paiement.objects.values('statut').annotate(count=models.Count('id'))
            print(f"\n📊 Répartition par statut:")
            for statut in statuts:
                print(f"   • {statut['statut']}: {statut['count']} paiements")
            
            # Montants
            montant_stats = Paiement.objects.aggregate(
                total=models.Sum('montant'),
                avg=models.Avg('montant'),
                min=models.Min('montant'),
                max=models.Max('montant')
            )
            print(f"\n💵 Statistiques montants:")
            print(f"   • Total: {montant_stats['total'] or 0:.2f} FCFA")
            print(f"   • Moyenne: {montant_stats['avg'] or 0:.2f} FCFA")
            print(f"   • Min: {montant_stats['min'] or 0:.2f} FCFA")
            print(f"   • Max: {montant_stats['max'] or 0:.2f} FCFA")
                
    except Exception as e:
        print(f"❌ Erreur analyse paiements: {e}")

def analyser_bons_soins_existants():
    """Analyse les bons et soins existants"""
    print("\n" + "=" * 80)
    print("🏥 ANALYSE DES BONS ET SOINS EXISTANTS")
    print("=" * 80)
    
    try:
        Bon = apps.get_model('assureur', 'Bon')
        Soin = apps.get_model('assureur', 'Soin')
        
        total_bons = Bon.objects.count()
        total_soins = Soin.objects.count()
        
        print(f"📈 Total bons: {total_bons}")
        print(f"📈 Total soins: {total_soins}")
        
        if total_bons > 0:
            # Statuts des bons
            statuts_bons = Bon.objects.values('statut').annotate(count=models.Count('id'))
            print(f"\n📊 Statuts des bons:")
            for statut in statuts_bons:
                print(f"   • {statut['statut']}: {statut['count']} bons")
            
            # Types de soins
            types_soins = Bon.objects.values('type_soin').annotate(count=models.Count('id'))
            print(f"\n🏥 Types de soins des bons:")
            for type_soin in types_soins:
                print(f"   • {type_soin['type_soin']}: {type_soin['count']} bons")
        
        if total_soins > 0:
            # Statuts des soins
            statuts_soins = Soin.objects.values('statut').annotate(count=models.Count('id'))
            print(f"\n📊 Statuts des soins:")
            for statut in statuts_soins:
                print(f"   • {statut['statut']}: {statut['count']} soins")
                
    except Exception as e:
        print(f"❌ Erreur analyse bons/soins: {e}")

def analyser_structure_financiere():
    """Analyse la structure financière existante"""
    print("\n" + "=" * 80)
    print("🏦 ANALYSE DE LA STRUCTURE FINANCIÈRE")
    print("=" * 80)
    
    try:
        # Calcul des indicateurs financiers
        Paiement = apps.get_model('assureur', 'Paiement')
        Cotisation = apps.get_model('assureur', 'Cotisation')
        Bon = apps.get_model('assureur', 'Bon')
        
        # Total des paiements (si modèle existe)
        total_paiements = 0
        try:
            total_paiements = Paiement.objects.filter(statut='valide').aggregate(
                total=models.Sum('montant')
            )['total'] or 0
        except:
            pass
        
        # Total des cotisations payées (si modèle existe)
        total_cotisations = 0
        try:
            total_cotisations = Cotisation.objects.filter(statut='payee').aggregate(
                total=models.Sum('montant')
            )['total'] or 0
        except:
            pass
        
        # Total des montants des bons (si modèle existe)
        total_bons = 0
        try:
            total_bons = Bon.objects.filter(statut='valide').aggregate(
                total=models.Sum('montant_total')
            )['total'] or 0
        except:
            pass
        
        print(f"💰 Chiffres financiers existants:")
        print(f"   • Total paiements: {total_paiements:.2f} FCFA")
        print(f"   • Total cotisations: {total_cotisations:.2f} FCFA")
        print(f"   • Total bons émis: {total_bons:.2f} FCFA")
        
        # Projection selon nouveau modèle
        Membre = apps.get_model('assureur', 'Membre')
        total_membres_actifs = Membre.objects.filter(statut='actif').count()
        
        print(f"\n📈 PROJECTION NOUVEAU MODÈLE:")
        print(f"   • Membres actifs: {total_membres_actifs}")
        print(f"   • Revenu mensuel projeté: {total_membres_actifs * 5000} FCFA")
        print(f"   • Répartition mensuelle projetée:")
        print(f"        - Cliniques: {total_membres_actifs * 2000} FCFA")
        print(f"        - Pharmacies: {total_membres_actifs * 2000} FCFA")
        print(f"        - Charges mutuelle: {total_membres_actifs * 1000} FCFA")
        
    except Exception as e:
        print(f"❌ Erreur analyse financière: {e}")

def verifier_compatibilite_nouveau_modele():
    """Vérifie la compatibilité avec le nouveau modèle"""
    print("\n" + "=" * 80)
    print("🔄 VÉRIFICATION COMPATIBILITÉ NOUVEAU MODÈLE")
    print("=" * 80)
    
    try:
        Membre = apps.get_model('assureur', 'Membre')
        
        # Vérifier les champs manquants pour le nouveau modèle
        champs_requis = [
            'est_femme_enceinte', 'date_debut_grossesse', 
            'date_accouchement_prevue', 'avance_payee', 'carte_adhesion_payee'
        ]
        
        champs_existants = [f.name for f in Membre._meta.get_fields()]
        champs_manquants = [champ for champ in champs_requis if champ not in champs_existants]
        
        if champs_manquants:
            print("❌ CHAMPS MANQUANTS dans modèle Membre:")
            for champ in champs_manquants:
                print(f"   • {champ}")
        else:
            print("✅ Tous les champs requis sont présents")
        
        # Vérifier la présence des modèles requis
        modeles_requis = ['Cotisation', 'VerificationCotisation']
        for modele_name in modeles_requis:
            try:
                apps.get_model('assureur', modele_name)
                print(f"✅ Modèle {modele_name} existe")
            except LookupError:
                print(f"❌ Modèle {modele_name} à créer")
        
    except Exception as e:
        print(f"❌ Erreur vérification compatibilité: {e}")

def generer_recommandations():
    """Génère des recommandations basées sur l'analyse"""
    print("\n" + "=" * 80)
    print("🎯 RECOMMANDATIONS POUR L'IMPLÉMENTATION")
    print("=" * 80)
    
    try:
        Membre = apps.get_model('assureur', 'Membre')
        total_membres = Membre.objects.count()
        
        print("📋 PLAN D'ACTION RECOMMANDÉ:")
        print("\n1. ✅ MODIFICATIONS IMMÉDIATES:")
        print("   • Ajouter les champs grossesse au modèle Membre")
        print("   • Ajouter les champs paiements initiaux (avance, carte)")
        print("   • Mettre à jour taux_couverture à 100% par défaut")
        
        print("\n2. 🆕 NOUVEAUX MODÈLES À CRÉER:")
        print("   • Modèle Cotisation avec répartition automatique")
        print("   • Modèle VerificationCotisation pour les agents")
        
        print("\n3. 🔄 MIGRATION DES DONNÉES:")
        print("   • Initialiser avance_payee et carte_adhesion_payee pour membres existants")
        print("   • Générer les cotisations rétroactives si nécessaire")
        print("   • Mettre à jour les taux de couverture existants")
        
        print("\n4. 🚀 DÉPLOIEMENT:")
        print("   • Commandes de gestion pour génération automatique")
        print("   • Formation des assureurs et agents")
        print("   • Communication aux membres")
        
        print(f"\n5. 📊 IMPACT SUR {total_membres} MEMBRES EXISTANTS:")
        print("   • Vérifier la cohérence des données existantes")
        print("   • Planifier la transition progressive")
        
    except Exception as e:
        print(f"❌ Erreur génération recommandations: {e}")

def analyser_risques_migration():
    """Analyse les risques potentiels de la migration"""
    print("\n" + "=" * 80)
    print("⚠️  ANALYSE DES RISQUES DE MIGRATION")
    print("=" * 80)
    
    try:
        Membre = apps.get_model('assureur', 'Membre')
        Bon = apps.get_model('assureur', 'Bon')
        
        # Membres avec bons en cours
        membres_avec_bons = Membre.objects.filter(bons_assureur__isnull=False).distinct().count()
        total_bons_actifs = Bon.objects.filter(statut='valide').count()
        
        print("🔍 RISQUES IDENTIFIÉS:")
        print(f"   • {membres_avec_bons} membres ont des bons existants")
        print(f"   • {total_bons_actifs} bons actifs à prendre en compte")
        print("   • Risque d'interruption de service pendant la migration")
        print("   • Compatibilité avec les applications existantes (membres, medecin, pharmacien)")
        
        print("\n🛡️  MITIGATION DES RISQUES:")
        print("   • Migration progressive par lots")
        print("   • Période de test avec un sous-ensemble de membres")
        print("   • Sauvegarde complète avant déploiement")
        print("   • Plan de rollback en cas de problème")
        
    except Exception as e:
        print(f"❌ Erreur analyse risques: {e}")

def main():
    """Fonction principale d'analyse"""
    print("🚀 DÉMARRAGE DE L'ANALYSE DE L'EXISTANT")
    print("Cette analyse va examiner votre base de données actuelle")
    print("pour préparer l'implémentation du nouveau système de cotisations.\n")
    
    # Exécution des analyses
    analyser_modeles_existants()
    analyser_membres_existants()
    analyser_cotisations_existantes()
    analyser_paiements_existants()
    analyser_bons_soins_existants()
    analyser_structure_financiere()
    verifier_compatibilite_nouveau_modele()
    analyser_risques_migration()
    generer_recommandations()
    
    print("\n" + "=" * 80)
    print("✅ ANALYSE TERMINÉE")
    print("=" * 80)
    print("\n📞 Prochaines étapes:")
    print("1. Examiner les résultats de l'analyse")
    print("2. Planifier la migration selon les recommandations")
    print("3. Sauvegarder la base de données")
    print("4. Procéder aux modifications étape par étape")

if __name__ == "__main__":
    main()