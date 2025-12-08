# dashboard_verifications_cotisations.py
import os
import django
from django.utils import timezone
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from agents.models import Agent, VerificationCotisation
from django.db.models import Count, Avg, Sum, Q

class DashboardVerifications:
    def __init__(self):
        self.date_reference = timezone.now()
    
    def generer_tableau_bord_complet(self):
        print("=" * 80)
        print("📊 TABLEAU DE BORD COMPLET - VÉRIFICATIONS COTISATIONS")
        print("=" * 80)
        
        self.afficher_metriques_globales()
        print("\n" + "─" * 80)
        self.afficher_performance_agents()
        print("\n" + "─" * 80)
        self.afficher_alertes_anomalies()
        print("\n" + "─" * 80)
        self.afficher_statistiques_avancees()
    
    def afficher_metriques_globales(self):
        print("🎯 MÉTRIQUES GLOBALES")
        print("─" * 40)
        
        total_membres = Membre.objects.count()
        total_verifications = VerificationCotisation.objects.count()
        verifications_completes = VerificationCotisation.objects.filter(
            date_verification__isnull=False
        ).count()
        
        # Statuts des cotisations
        statuts = VerificationCotisation.objects.values('statut_cotisation').annotate(
            total=Count('id')
        )
        
        print(f"👥 Membres totaux: {total_membres}")
        print(f"✅ Vérifications créées: {total_verifications}")
        print(f"📋 Vérifications complétées: {verifications_completes}")
        print(f"⏳ Taux complétion: {(verifications_completes/total_verifications*100) if total_verifications > 0 else 0:.1f}%")
        
        print("\n📈 RÉPARTITION DES STATUTS:")
        for statut in statuts:
            pourcentage = (statut['total'] / total_verifications * 100) if total_verifications > 0 else 0
            print(f"  - {statut['statut_cotisation']}: {statut['total']} ({pourcentage:.1f}%)")
    
    def afficher_performance_agents(self):
        print("👨‍💼 PERFORMANCE DES AGENTS")
        print("─" * 40)
        
        # Métriques par agent
        agents_performance = Agent.objects.filter(est_actif=True).annotate(
            total_verifications=Count('verificationcotisation'),
            verifications_completes=Count('verificationcotisation', 
                                        filter=Q(verificationcotisation__date_verification__isnull=False)),
            moyenne_jours_retard=Avg('verificationcotisation__jours_retard'),
            total_dette=Sum('verificationcotisation__montant_dette')
        )
        
        print(f"{'Agent':<12} {'Vérif. Total':<14} {'Complétées':<12} {'Taux %':<8} {'Retard Moy':<12} {'Dette Total':<12}")
        print("─" * 80)
        
        for agent in agents_performance:
            taux_completion = (agent.verifications_completes / agent.total_verifications * 100) if agent.total_verifications > 0 else 0
            
            print(f"{agent.matricule:<12} {agent.total_verifications:<14} "
                  f"{agent.verifications_completes:<12} {taux_completion:<7.1f}% "
                  f"{agent.moyenne_jours_retard or 0:<11.1f} "
                  f"{agent.total_dette or 0:<11.2f} €")
    
    def afficher_alertes_anomalies(self):
        print("🚨 ALERTES ET ANOMALIES")
        print("─" * 40)
        
        # Alertes par catégorie
        alertes = {
            "🔴 CRITIQUE": [],
            "🟡 ATTENTION": [],
            "🔵 INFORMATION": []
        }
        
        # Vérifications en retard sévère
        retards_severes = VerificationCotisation.objects.filter(
            jours_retard__gt=30
        ).count()
        if retards_severes > 0:
            alertes["🔴 CRITIQUE"].append(f"{retards_severes} membres avec +30 jours de retard")
        
        # Dettes importantes
        dettes_importantes = VerificationCotisation.objects.filter(
            montant_dette__gt=500
        ).count()
        if dettes_importantes > 0:
            alertes["🔴 CRITIQUE"].append(f"{dettes_importantes} membres avec dette > 500€")
        
        # Vérifications anciennes non traitées
        seuil_inactivite = self.date_reference - timedelta(days=7)
        verifications_inactives = VerificationCotisation.objects.filter(
            date_verification__isnull=True,
            date_dernier_paiement__lt=seuil_inactivite.date()
        ).count()
        if verifications_inactives > 0:
            alertes["🟡 ATTENTION"].append(f"{verifications_inactives} vérifications non traitées depuis +7 jours")
        
        # Échéances proches
        echeance_proche = self.date_reference.date() + timedelta(days=7)
        echeances_imminentes = VerificationCotisation.objects.filter(
            prochaine_echeance__lte=echeance_proche,
            prochaine_echeance__gte=self.date_reference.date()
        ).count()
        if echeances_imminentes > 0:
            alertes["🔵 INFORMATION"].append(f"{echeances_imminentes} échéances dans les 7 prochains jours")
        
        # Agents sous-performants
        agents_sous_performants = Agent.objects.filter(
            est_actif=True
        ).annotate(
            verifications_completes=Count('verificationcotisation', 
                                       filter=Q(verificationcotisation__date_verification__isnull=False))
        ).filter(verifications_completes=0)
        
        if agents_sous_performants.exists():
            alertes["🟡 ATTENTION"].append(f"{agents_sous_performants.count()} agents n'ont complété aucune vérification")
        
        # Affichage des alertes
        for niveau, messages in alertes.items():
            if messages:
                print(f"\n{niveau}:")
                for message in messages:
                    print(f"  • {message}")
        
        if not any(alertes.values()):
            print("✅ Aucune alerte critique détectée")
    
    def afficher_statistiques_avancees(self):
        print("📈 STATISTIQUES AVANCÉES")
        print("─" * 40)
        
        # Tendances des retards
        retards_moyens = VerificationCotisation.objects.aggregate(
            avg_retard=Avg('jours_retard'),
            max_retard=Avg('jours_retard')
        )
        
        # Distribution des dettes
        distribution_dettes = {
            "0-50€": VerificationCotisation.objects.filter(montant_dette__lte=50).count(),
            "51-200€": VerificationCotisation.objects.filter(montant_dette__gt=50, montant_dette__lte=200).count(),
            "201-500€": VerificationCotisation.objects.filter(montant_dette__gt=200, montant_dette__lte=500).count(),
            "500+€": VerificationCotisation.objects.filter(montant_dette__gt=500).count()
        }
        
        print(f"📊 Retard moyen: {retards_moyens['avg_retard'] or 0:.1f} jours")
        print(f"📊 Retard maximum: {retards_moyens['max_retard'] or 0:.1f} jours")
        
        print("\n💰 DISTRIBUTION DES DETTES:")
        for range_dette, count in distribution_dettes.items():
            pourcentage = (count / VerificationCotisation.objects.count() * 100) if VerificationCotisation.objects.count() > 0 else 0
            print(f"  - {range_dette}: {count} membres ({pourcentage:.1f}%)")
        
        # Taux de résolution par agent
        print("\n🎯 TAUX DE RÉSOLUTION PAR AGENT:")
        agents = Agent.objects.filter(est_actif=True)
        for agent in agents:
            verifications_agent = VerificationCotisation.objects.filter(agent=agent)
            total = verifications_agent.count()
            resolues = verifications_agent.filter(statut_cotisation='a_jour').count()
            taux_resolution = (resolues / total * 100) if total > 0 else 0
            
            print(f"  - {agent.matricule}: {taux_resolution:.1f}% de résolution")

def generer_rapport_quotidien():
    """Génère un rapport quotidien automatisé"""
    dashboard = DashboardVerifications()
    
    print(f"\n📅 RAPPORT QUOTIDIEN - {timezone.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 80)
    
    dashboard.generer_tableau_bord_complet()
    
    # Sauvegarde du rapport
    nom_fichier = f"rapport_verifications_{timezone.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(nom_fichier, 'w', encoding='utf-8') as f:
        import sys
        original_stdout = sys.stdout
        sys.stdout = f
        dashboard.generer_tableau_bord_complet()
        sys.stdout = original_stdout
    
    print(f"\n💾 Rapport sauvegardé: {nom_fichier}")

if __name__ == "__main__":
    generer_rapport_quotidien()