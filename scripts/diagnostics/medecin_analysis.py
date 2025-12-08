# medecin_analysis.py
import os
import django
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
from django.db.models import Count, Sum, Avg, Q, F, Value
from django.db.models.functions import TruncMonth, TruncWeek, Concat
from django.utils import timezone

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from medecin.models import Medecin, Consultation, Ordonnance, SpecialiteMedicale
from soins.models import BonDeSoin, TypeSoin
from membres.models import Membre
from django.contrib.auth.models import User

class MedecinAnalytics:
    """
    Classe complète d'analyse des données médecins
    """
    
    def __init__(self, medecin_id=None):
        self.medecin_id = medecin_id
        self.medecin = None
        self.data_loaded = False
        
        if medecin_id:
            self.load_medecin_data()
    
    def load_medecin_data(self):
        """Charger les données du médecin"""
        try:
            self.medecin = Medecin.objects.get(id=self.medecin_id)
            self.data_loaded = True
            print(f"✅ Données chargées pour le Dr {self.medecin.nom_complet}")
        except Medecin.DoesNotExist:
            print(f"❌ Médecin avec ID {self.medecin_id} non trouvé")
            return False
        return True
    
    def get_medecin_stats_overview(self, periode_jours=30):
        """
        Statistiques générales du médecin
        """
        if not self.data_loaded:
            return None
        
        date_debut = timezone.now() - timedelta(days=periode_jours)
        
        stats = {
            # Consultations
            'consultations_total': Consultation.objects.filter(
                medecin=self.medecin
            ).count(),
            
            'consultations_periode': Consultation.objects.filter(
                medecin=self.medecin,
                date_consultation__gte=date_debut
            ).count(),
            
            'consultations_planifiees': Consultation.objects.filter(
                medecin=self.medecin,
                statut='PLANIFIEE'
            ).count(),
            
            'consultations_terminees': Consultation.objects.filter(
                medecin=self.medecin,
                statut='TERMINEE'
            ).count(),
            
            # Bons de soin
            'bons_soin_total': BonDeSoin.objects.filter(
                medecin=self.medecin.user
            ).count(),
            
            'bons_soin_valides': BonDeSoin.objects.filter(
                medecin=self.medecin.user,
                statut='VALIDE'
            ).count(),
            
            'bons_soin_attente': BonDeSoin.objects.filter(
                medecin=self.medecin.user,
                statut='EN_ATTENTE'
            ).count(),
            
            # Ordonnances
            'ordonnances_total': Ordonnance.objects.filter(
                medecin=self.medecin.user
            ).count(),
            
            'ordonnances_urgentes': Ordonnance.objects.filter(
                medecin=self.medecin.user,
                est_urgent=True
            ).count(),
            
            # Revenus estimés
            'revenus_consultations': Consultation.objects.filter(
                medecin=self.medecin,
                statut='TERMINEE'
            ).count() * self.medecin.tarif_consultation,
            
            'revenus_bons_soin': BonDeSoin.objects.filter(
                medecin=self.medecin.user,
                statut='VALIDE'
            ).aggregate(total=Sum('montant'))['total'] or 0,
        }
        
        stats['revenus_totaux'] = stats['revenus_consultations'] + stats['revenus_bons_soin']
        
        return stats
    
    def get_consultations_timeseries(self, periode='mois', nb_periodes=12):
        """
        Série temporelle des consultations
        """
        if not self.data_loaded:
            return None
        
        if periode == 'mois':
            trunc_func = TruncMonth('date_consultation')
        elif periode == 'semaine':
            trunc_func = TruncWeek('date_consultation')
        else:
            trunc_func = TruncMonth('date_consultation')
        
        timeseries = (
            Consultation.objects
            .filter(medecin=self.medecin)
            .annotate(period=trunc_func)
            .values('period')
            .annotate(
                total=Count('id'),
                terminees=Count('id', filter=Q(statut='TERMINEE')),
                planifiees=Count('id', filter=Q(statut='PLANIFIEE'))
            )
            .order_by('period')
        )
        
        return list(timeseries)
    
    def get_specialite_stats(self):
        """
        Statistiques par spécialité (pour comparaison)
        """
        if not self.data_loaded:
            return None
        
        specialite_stats = (
            Medecin.objects
            .filter(specialite=self.medecin.specialite)
            .aggregate(
                nb_medecins=Count('id'),
                tarif_moyen=Avg('tarif_consultation'),
                experience_moyenne=Avg('annees_experience')
            )
        )
        
        return specialite_stats
    
    def get_patient_analytics(self, top_n=10):
        """
        Analyse des patients les plus fréquents
        """
        if not self.data_loaded:
            return None
        
        top_patients = (
            Consultation.objects
            .filter(medecin=self.medecin)
            .annotate(
                nom_complet=Concat('membre__nom', Value(' '), 'membre__prenom')
            )
            .values('membre_id', 'nom_complet')
            .annotate(
                nb_consultations=Count('id'),
                derniere_consultation=Max('date_consultation')
            )
            .order_by('-nb_consultations')[:top_n]
        )
        
        return list(top_patients)
    
    def get_ordonnances_analysis(self):
        """
        Analyse détaillée des ordonnances
        """
        if not self.data_loaded:
            return None
        
        analysis = {
            'par_type': list(
                Ordonnance.objects
                .filter(medecin=self.medecin.user)
                .values('type_ordonnance')
                .annotate(total=Count('id'))
                .order_by('-total')
            ),
            
            'par_urgence': list(
                Ordonnance.objects
                .filter(medecin=self.medecin.user)
                .values('est_urgent')
                .annotate(total=Count('id'))
            ),
            
            'renouvelables_stats': {
                'total_renouvelables': Ordonnance.objects.filter(
                    medecin=self.medecin.user, renouvelable=True
                ).count(),
                'moyenne_renouvellements': Ordonnance.objects.filter(
                    medecin=self.medecin.user, renouvelable=True
                ).aggregate(moyenne=Avg('nombre_renouvellements'))['moyenne'] or 0
            }
        }
        
        return analysis
    
    def get_bons_soin_analysis(self):
        """
        Analyse des bons de soin
        """
        if not self.data_loaded:
            return None
        
        analysis = {
            'par_statut': list(
                BonDeSoin.objects
                .filter(medecin=self.medecin.user)
                .values('statut')
                .annotate(
                    total=Count('id'),
                    montant_total=Sum('montant')
                )
                .order_by('statut')
            ),
            
            'par_type_soin': list(
                BonDeSoin.objects
                .filter(medecin=self.medecin.user)
                .values('type_soin__nom')
                .annotate(
                    total=Count('id'),
                    montant_moyen=Avg('montant')
                )
                .order_by('-total')[:10]
            ),
            
            'evolution_mensuelle': list(
                BonDeSoin.objects
                .filter(medecin=self.medecin.user)
                .annotate(mois=TruncMonth('date_soin'))
                .values('mois')
                .annotate(
                    total_bons=Count('id'),
                    montant_total=Sum('montant')
                )
                .order_by('mois')
            )
        }
        
        return analysis
    
    def get_disponibilite_analysis(self):
        """
        Analyse de la disponibilité et de l'occupation
        """
        if not self.data_loaded:
            return None
        
        # Calcul du taux d'occupation
        consultations_terminees = Consultation.objects.filter(
            medecin=self.medecin, statut='TERMINEE'
        ).count()
        
        # Estimation du temps de travail (à adapter selon vos données)
        heures_travail_semaine = 35  # À modifier selon la réalité
        semaines_activite = 48       # Estimation
        
        heures_totales = heures_travail_semaine * semaines_activite
        heures_consultees = consultations_terminees * 0.5  # Estimation 30min par consultation
        
        taux_occupation = (heures_consultees / heures_totales) * 100 if heures_totales > 0 else 0
        
        analysis = {
            'taux_occupation': round(taux_occupation, 2),
            'consultations_par_heure': round(consultations_terminees / heures_consultees, 2) if heures_consultees > 0 else 0,
            'disponibilite_actuelle': self.medecin.disponible,
            'est_actif': self.medecin.est_actif
        }
        
        return analysis
    
    def generate_performance_report(self):
        """
        Génère un rapport de performance complet
        """
        if not self.data_loaded:
            return None
        
        report = {
            'medecin_info': {
                'nom': self.medecin.nom_complet,
                'specialite': self.medecin.specialite.nom if self.medecin.specialite else 'Non spécifiée',
                'experience': self.medecin.annees_experience,
                'tarif_consultation': self.medecin.tarif_consultation,
                'etablissement': self.medecin.etablissement.nom if self.medecin.etablissement else 'Non spécifié'
            },
            'statistiques_generales': self.get_medecin_stats_overview(),
            'analyse_consultations': self.get_consultations_timeseries(),
            'analyse_patients': self.get_patient_analytics(),
            'analyse_ordonnances': self.get_ordonnances_analysis(),
            'analyse_bons_soin': self.get_bons_soin_analysis(),
            'analyse_disponibilite': self.get_disponibilite_analysis(),
            'comparaison_specialite': self.get_specialite_stats(),
            'date_generation': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return report

class MedecinComparison:
    """
    Classe pour comparer les médecins entre eux
    """
    
    def __init__(self, specialite_id=None):
        self.specialite_id = specialite_id
        self.medecins_data = []
    
    def load_comparison_data(self):
        """Charger les données de comparaison"""
        queryset = Medecin.objects.select_related('specialite', 'etablissement', 'user')
        
        if self.specialite_id:
            queryset = queryset.filter(specialite_id=self.specialite_id)
        
        self.medecins_data = list(queryset)
        return len(self.medecins_data)
    
    def get_specialite_comparison(self):
        """Comparaison des médecins par spécialité"""
        comparison_data = []
        
        for medecin in self.medecins_data:
            stats = MedecinAnalytics(medecin.id).get_medecin_stats_overview()
            
            if stats:
                comparison_data.append({
                    'medecin_id': medecin.id,
                    'nom_complet': medecin.nom_complet,
                    'specialite': medecin.specialite.nom if medecin.specialite else 'N/A',
                    'etablissement': medecin.etablissement.nom if medecin.etablissement else 'N/A',
                    'experience': medecin.annees_experience,
                    'tarif_consultation': medecin.tarif_consultation,
                    'consultations_total': stats['consultations_total'],
                    'bons_soin_valides': stats['bons_soin_valides'],
                    'ordonnances_total': stats['ordonnances_total'],
                    'revenus_totaux': stats['revenus_totaux'],
                    'taux_validation_bons': (
                        (stats['bons_soin_valides'] / stats['bons_soin_total'] * 100) 
                        if stats['bons_soin_total'] > 0 else 0
                    )
                })
        
        return comparison_data
    
    def generate_ranking_report(self, metric='consultations_total'):
        """
        Génère un classement des médecins
        """
        comparison_data = self.get_specialite_comparison()
        
        if not comparison_data:
            return None
        
        df = pd.DataFrame(comparison_data)
        df['rang'] = df[metric].rank(ascending=False, method='dense')
        df = df.sort_values('rang')
        
        return df.to_dict('records')

def export_to_excel(medecin_id, output_path='rapport_medecin.xlsx'):
    """
    Exporte les données d'un médecin vers Excel
    """
    analyzer = MedecinAnalytics(medecin_id)
    report = analyzer.generate_performance_report()
    
    if not report:
        print("❌ Impossible de générer le rapport")
        return False
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Feuille 1: Informations générales
        info_df = pd.DataFrame([report['medecin_info']])
        info_df.to_excel(writer, sheet_name='Informations', index=False)
        
        # Feuille 2: Statistiques
        stats_df = pd.DataFrame([report['statistiques_generales']])
        stats_df.to_excel(writer, sheet_name='Statistiques', index=False)
        
        # Feuille 3: Consultations
        consultations_df = pd.DataFrame(report['analyse_consultations'])
        consultations_df.to_excel(writer, sheet_name='Consultations', index=False)
        
        # Feuille 4: Patients
        patients_df = pd.DataFrame(report['analyse_patients'])
        patients_df.to_excel(writer, sheet_name='Patients', index=False)
        
        # Feuille 5: Ordonnances
        ordonnances_df = pd.DataFrame(report['analyse_ordonnances']['par_type'])
        ordonnances_df.to_excel(writer, sheet_name='Ordonnances', index=False)
    
    print(f"✅ Rapport exporté vers: {output_path}")
    return True

def create_visualizations(medecin_id, output_dir='visualizations'):
    """
    Crée des visualisations pour le médecin
    """
    analyzer = MedecinAnalytics(medecin_id)
    report = analyzer.generate_performance_report()
    
    if not report:
        return False
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Configuration des styles
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # 1. Graphique des consultations par mois
    consultations_data = report['analyse_consultations']
    if consultations_data:
        df_consult = pd.DataFrame(consultations_data)
        plt.figure(figsize=(12, 6))
        plt.plot(df_consult['period'], df_consult['total'], marker='o', linewidth=2)
        plt.title(f"Évolution des consultations - Dr {report['medecin_info']['nom']}")
        plt.xlabel('Mois')
        plt.ylabel('Nombre de consultations')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/consultations_evolution.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    # 2. Graphique camembert des statuts de bons de soin
    bons_data = report['analyse_bons_soin']['par_statut']
    if bons_data:
        df_bons = pd.DataFrame(bons_data)
        plt.figure(figsize=(8, 8))
        plt.pie(df_bons['total'], labels=df_bons['statut'], autopct='%1.1f%%', startangle=90)
        plt.title('Répartition des bons de soin par statut')
        plt.savefig(f'{output_dir}/bons_soin_statuts.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    # 3. Graphique des types d'ordonnances
    ordonnances_data = report['analyse_ordonnances']['par_type']
    if ordonnances_data:
        df_ordo = pd.DataFrame(ordonnances_data)
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df_ordo, x='type_ordonnance', y='total')
        plt.title('Répartition des ordonnances par type')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/ordonnances_types.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    print(f"✅ Visualisations créées dans: {output_dir}")
    return True

# ==============================================================================
# EXEMPLE D'UTILISATION
# ==============================================================================

def example_usage():
    """
    Exemple d'utilisation du script d'analyse
    """
    print("🚀 Démonstration du script d'analyse médicale")
    print("=" * 50)
    
    # 1. Analyse d'un médecin spécifique
    medecin_id = 1  # Remplacez par un ID réel
    
    analyzer = MedecinAnalytics(medecin_id)
    
    if analyzer.data_loaded:
        # A. Rapport complet
        report = analyzer.generate_performance_report()
        print("📊 RAPPORT DE PERFORMANCE")
        print(f"Médecin: {report['medecin_info']['nom']}")
        print(f"Spécialité: {report['medecin_info']['specialite']}")
        print(f"Consultations totales: {report['statistiques_generales']['consultations_total']}")
        print(f"Revenus totaux: {report['statistiques_generales']['revenus_totaux']:.2f} €")
        print(f"Taux d'occupation: {report['analyse_disponibilite']['taux_occupation']}%")
        
        # B. Export Excel
        export_to_excel(medecin_id, f'rapport_medecin_{medecin_id}.xlsx')
        
        # C. Visualisations
        create_visualizations(medecin_id, f'viz_medecin_{medecin_id}')
    
    # 2. Comparaison entre médecins
    print("\n🏆 COMPARAISON ENTRE MÉDECINS")
    comparator = MedecinComparison(specialite_id=1)  # ID de spécialité
    nb_medecins = comparator.load_comparison_data()
    print(f"Nombre de médecins chargés: {nb_medecins}")
    
    if nb_medecins > 0:
        ranking = comparator.generate_ranking_report('consultations_total')
        print("\nClassement par consultations:")
        for medecin in ranking[:5]:  # Top 5
            print(f"{int(medecin['rang'])}. {medecin['nom_complet']}: {medecin['consultations_total']} consultations")

def analyze_all_medecins():
    """
    Analyse tous les médecins du système
    """
    print("🔍 Analyse de tous les médecins...")
    
    all_medecins = Medecin.objects.all()
    results = []
    
    for medecin in all_medecins:
        analyzer = MedecinAnalytics(medecin.id)
        if analyzer.data_loaded:
            stats = analyzer.get_medecin_stats_overview()
            if stats:
                results.append({
                    'id': medecin.id,
                    'nom': medecin.nom_complet,
                    'specialite': medecin.specialite.nom if medecin.specialite else 'N/A',
                    'consultations': stats['consultations_total'],
                    'revenus': stats['revenus_totaux'],
                    'bons_valides': stats['bons_soin_valides']
                })
    
    # Tri par revenus
    results.sort(key=lambda x: x['revenus'], reverse=True)
    
    print(f"\n📈 TOP 10 MÉDECINS PAR REVENUS:")
    for i, medecin in enumerate(results[:10], 1):
        print(f"{i}. {medecin['nom']} - {medecin['revenus']:.2f} €")
    
    return results

if __name__ == "__main__":
    # Exécuter la démonstration
    example_usage()
    
    # Analyser tous les médecins
    analyze_all_medecins()