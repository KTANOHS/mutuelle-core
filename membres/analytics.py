# membres/analytics.py
import json
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.db.models import Count, Avg, Q, F, ExpressionWrapper, DurationField
from django.db import models
from django.contrib.auth.models import User
from .models import Membre, UserLoginSession
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from django.http import JsonResponse

class AnalyseConnexions:
    """
    Classe pour analyser les connexions et le comportement des membres
    """
    
    def __init__(self):
        self.today = timezone.now().date()
    
    def get_periode_analyse(self, jours=30):
        """Définit la période d'analyse"""
        return self.today - timedelta(days=jours)
    
    def statistiques_connexions_globales(self, jours=30):
        """Statistiques globales des connexions"""
        date_limite = self.get_periode_analyse(jours)
        
        try:
            # Connexions totales
            connexions_total = UserLoginSession.objects.filter(
                login_time__gte=date_limite
            ).count()
            
            # Utilisateurs uniques connectés
            utilisateurs_uniques = UserLoginSession.objects.filter(
                login_time__gte=date_limite
            ).values('user').distinct().count()
            
            # Durée moyenne des sessions
            duree_moyenne = UserLoginSession.objects.filter(
                login_time__gte=date_limite,
                logout_time__isnull=False
            ).annotate(
                duree_session=ExpressionWrapper(
                    F('logout_time') - F('login_time'),
                    output_field=DurationField()
                )
            ).aggregate(
                moyenne_duree=Avg('duree_session')
            )['moyenne_duree']
            
            # Conversion en minutes
            duree_moyenne_minutes = duree_moyenne.total_seconds() / 60 if duree_moyenne else 0
            
            # Taux de rétention (utilisateurs revenants)
            utilisateurs_actifs = Membre.objects.filter(
                user__last_login__gte=date_limite
            ).count()
            
            total_membres = Membre.objects.count()
            taux_retention = (utilisateurs_actifs / total_membres * 100) if total_membres > 0 else 0
            
            return {
                'connexions_total': connexions_total,
                'utilisateurs_uniques': utilisateurs_uniques,
                'duree_moyenne_minutes': round(duree_moyenne_minutes, 2),
                'taux_retention': round(taux_retention, 2),
                'utilisateurs_actifs': utilisateurs_actifs,
                'total_membres': total_membres,
                'periode_jours': jours
            }
            
        except Exception as e:
            return {'erreur': f"Erreur lors de l'analyse: {str(e)}"}
    
    def evolution_connexions_quotidiennes(self, jours=30):
        """Évolution des connexions par jour"""
        date_limite = self.get_periode_analyse(jours)
        
        connexions_par_jour = UserLoginSession.objects.filter(
            login_time__gte=date_limite
        ).extra({
            'date': "DATE(login_time)"
        }).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        return list(connexions_par_jour)
    
    def heures_pointe_connexions(self, jours=30):
        """Analyse des heures de pointe de connexion"""
        date_limite = self.get_periode_analyse(jours)
        
        connexions_par_heure = UserLoginSession.objects.filter(
            login_time__gte=date_limite
        ).extra({
            'heure': "HOUR(login_time)"
        }).values('heure').annotate(
            count=Count('id')
        ).order_by('heure')
        
        return list(connexions_par_heure)
    
    def top_membres_actifs(self, limit=10, jours=30):
        """Top des membres les plus actifs"""
        date_limite = self.get_periode_analyse(jours)
        
        membres_actifs = UserLoginSession.objects.filter(
            login_time__gte=date_limite
        ).values(
            'user__id', 
            'user__membre__nom',
            'user__membre__prenom',
            'user__membre__numero_unique'
        ).annotate(
            nb_connexions=Count('id'),
            derniere_connexion=models.Max('login_time')
        ).order_by('-nb_connexions')[:limit]
        
        return list(membres_actifs)
    
    def analyse_par_categorie(self, jours=30):
        """Analyse des connexions par catégorie de membre"""
        date_limite = self.get_periode_analyse(jours)
        
        connexions_par_categorie = UserLoginSession.objects.filter(
            login_time__gte=date_limite,
            user__membre__isnull=False
        ).values(
            'user__membre__categorie'
        ).annotate(
            nb_connexions=Count('id'),
            membres_uniques=Count('user', distinct=True)
        ).order_by('-nb_connexions')
        
        return list(connexions_par_categorie)
    
    def sessions_longues_courtes(self, jours=30):
        """Identification des sessions longues et courtes"""
        date_limite = self.get_periode_analyse(jours)
        
        sessions = UserLoginSession.objects.filter(
            login_time__gte=date_limite,
            logout_time__isnull=False
        ).annotate(
            duree_session=ExpressionWrapper(
                F('logout_time') - F('login_time'),
                output_field=DurationField()
            )
        )
        
        # Sessions longues (plus de 30 minutes)
        sessions_longues = sessions.filter(
            duree_session__gt=timedelta(minutes=30)
        ).count()
        
        # Sessions courtes (moins de 5 minutes)
        sessions_courtes = sessions.filter(
            duree_session__lt=timedelta(minutes=5)
        ).count()
        
        # Sessions moyennes
        sessions_moyennes = sessions.filter(
            duree_session__gte=timedelta(minutes=5),
            duree_session__lte=timedelta(minutes=30)
        ).count()
        
        return {
            'sessions_longues': sessions_longues,
            'sessions_courtes': sessions_courtes,
            'sessions_moyennes': sessions_moyennes,
            'total_sessions': sessions.count()
        }
    
    def alertes_inactivite(self, jours_inactivite=30):
        """Détection des membres inactifs"""
        date_limite_inactivite = self.today - timedelta(days=jours_inactivite)
        
        membres_inactifs = Membre.objects.filter(
            Q(user__last_login__lt=date_limite_inactivite) | 
            Q(user__last_login__isnull=True)
        ).select_related('user').values(
            'id', 'nom', 'prenom', 'numero_unique', 'email',
            'user__last_login', 'statut'
        ).order_by('user__last_login')
        
        return list(membres_inactifs)
    
    def frequence_connexion_moyenne(self, jours=30):
        """Fréquence moyenne de connexion par membre"""
        date_limite = self.get_periode_analyse(jours)
        
        stats_frequence = UserLoginSession.objects.filter(
            login_time__gte=date_limite
        ).values('user').annotate(
            nb_connexions=Count('id')
        ).aggregate(
            moyenne=Avg('nb_connexions'),
            max_connexions=models.Max('nb_connexions'),
            min_connexions=models.Min('nb_connexions')
        )
        
        return stats_frequence
    
    def generate_rapport_complet(self, jours=30):
        """Génère un rapport complet d'analyse"""
        return {
            'statistiques_globales': self.statistiques_connexions_globales(jours),
            'evolution_quotidienne': self.evolution_connexions_quotidiennes(jours),
            'heures_pointe': self.heures_pointe_connexions(jours),
            'top_membres_actifs': self.top_membres_actifs(10, jours),
            'analyse_categories': self.analyse_par_categorie(jours),
            'types_sessions': self.sessions_longues_courtes(jours),
            'frequence_moyenne': self.frequence_connexion_moyenne(jours),
            'membres_inactifs': self.alertes_inactivite(30),
            'date_generation': timezone.now().isoformat(),
            'periode_analyse': f"{jours} jours"
        }


class VisualisationConnexions:
    """Classe pour générer des visualisations des données de connexion"""
    
    @staticmethod
    def create_connexions_chart(connexions_data):
        """Crée un graphique d'évolution des connexions"""
        try:
            dates = [item['date'] for item in connexions_data]
            counts = [item['count'] for item in connexions_data]
            
            plt.figure(figsize=(12, 6))
            plt.plot(dates, counts, marker='o', linewidth=2, markersize=4)
            plt.title('Évolution des Connexions Quotidiennes')
            plt.xlabel('Date')
            plt.ylabel('Nombre de Connexions')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            # Convertir en image base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            
            graphic = base64.b64encode(image_png).decode('utf-8')
            plt.close()
            
            return graphic
        except Exception as e:
            return None
    
    @staticmethod
    def create_heures_pointe_chart(heures_data):
        """Crée un graphique des heures de pointe"""
        try:
            heures = [f"{item['heure']}h" for item in heures_data]
            counts = [item['count'] for item in heures_data]
            
            plt.figure(figsize=(10, 6))
            plt.bar(heures, counts, color='skyblue', alpha=0.7)
            plt.title('Répartition des Connexions par Heure')
            plt.xlabel('Heure de la Journée')
            plt.ylabel('Nombre de Connexions')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            
            graphic = base64.b64encode(image_png).decode('utf-8')
            plt.close()
            
            return graphic
        except Exception as e:
            return None


# ==============================================================================
# VUES POUR L'INTERFACE D'ANALYSE
# ==============================================================================

def dashboard_analytics(request):
    """Tableau de bord d'analyse des connexions"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Accès non autorisé'}, status=403)
    
    analyseur = AnalyseConnexions()
    visualisateur = VisualisationConnexions()
    
    # Paramètres
    jours = int(request.GET.get('jours', 30))
    
    # Données
    rapport = analyseur.generate_rapport_complet(jours)
    chart_connexions = visualisateur.create_connexions_chart(rapport['evolution_quotidienne'])
    chart_heures = visualisateur.create_heures_pointe_chart(rapport['heures_pointe'])
    
    context = {
        'title': 'Analytics des Connexions',
        'rapport': rapport,
        'chart_connexions': chart_connexions,
        'chart_heures': chart_heures,
        'jours_selectionnes': jours,
        'date_actuelle': timezone.now().strftime("%d/%m/%Y %H:%M")
    }
    
    return render(request, 'membres/analytics_dashboard.html', context)


def api_analytics_data(request):
    """API pour les données d'analytics"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Accès non autorisé'}, status=403)
    
    analyseur = AnalyseConnexions()
    jours = int(request.GET.get('jours', 30))
    
    data_type = request.GET.get('type', 'global')
    
    if data_type == 'global':
        data = analyseur.statistiques_connexions_globales(jours)
    elif data_type == 'evolution':
        data = analyseur.evolution_connexions_quotidiennes(jours)
    elif data_type == 'heures':
        data = analyseur.heures_pointe_connexions(jours)
    elif data_type == 'top_membres':
        data = analyseur.top_membres_actifs(10, jours)
    elif data_type == 'inactifs':
        data = analyseur.alertes_inactivite(30)
    else:
        data = {'error': 'Type de données non supporté'}
    
    return JsonResponse(data, safe=False)


def export_analytics_excel(request):
    """Export des données d'analytics en Excel"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Accès non autorisé'}, status=403)
    
    analyseur = AnalyseConnexions()
    jours = int(request.GET.get('jours', 30))
    
    # Créer un fichier Excel avec plusieurs onglets
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        
        # Onglet 1: Statistiques globales
        stats_globales = analyseur.statistiques_connexions_globales(jours)
        df_global = pd.DataFrame([stats_globales])
        df_global.to_excel(writer, sheet_name='Statistiques Globales', index=False)
        
        # Onglet 2: Évolution quotidienne
        evolution = analyseur.evolution_connexions_quotidiennes(jours)
        df_evolution = pd.DataFrame(evolution)
        df_evolution.to_excel(writer, sheet_name='Évolution Quotidienne', index=False)
        
        # Onglet 3: Top membres actifs
        top_membres = analyseur.top_membres_actifs(50, jours)
        df_top = pd.DataFrame(top_membres)
        df_top.to_excel(writer, sheet_name='Top Membres Actifs', index=False)
        
        # Onglet 4: Membres inactifs
        inactifs = analyseur.alertes_inactivite(30)
        df_inactifs = pd.DataFrame(inactifs)
        df_inactifs.to_excel(writer, sheet_name='Membres Inactifs', index=False)
    
    output.seek(0)
    
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="analytics_connexions_{timezone.now().strftime("%Y%m%d_%H%M")}.xlsx"'
    
    return response