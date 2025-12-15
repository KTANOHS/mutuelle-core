# api/views.py - VERSION SIMPLIFIÉE ET FONCTIONNELLE

import os
import sys
from datetime import timedelta

# =============================================================================
# 1. CONFIGURER DJANGO (nécessaire pour les imports)
# =============================================================================

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    import django
    django.setup()
    print("✅ Django configuré")
except Exception as e:
    print(f"⚠️  Erreur configuration Django: {e}")

# =============================================================================
# 2. api_health - DÉFINIE EN PREMIER (fonction simple)
# =============================================================================

from django.http import JsonResponse
from django.utils import timezone

def api_health(request):
    """Endpoint de santé de l'API"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'Mutuelle Core API',
        'version': '1.0.0',
        'timestamp': timezone.now().isoformat(),
        'message': 'API en fonctionnement'
    })

# =============================================================================
# 3. IMPORTER DRF ET DÉCORER api_health
# =============================================================================

try:
    from rest_framework.decorators import api_view
    # Décorer la fonction existante
    api_health = api_view(['GET'])(api_health)
    print("✅ api_health décorée avec @api_view")
except ImportError as e:
    print(f"⚠️  DRF non disponible: {e}")

# =============================================================================
# 4. ESSAYER D'IMPORTER LES MODÈLES (avec gestion d'erreurs)
# =============================================================================

try:
    from .serializers import *
    from soins.models import Soin, TypeSoin, Prescription
    from medecin.models import Medecin, Ordonnance
    from assureur.models import BonPriseEnCharge, Membre
    from paiements.models import Paiement
    MODELS_AVAILABLE = True
    print("✅ Modèles importés")
except ImportError as e:
    MODELS_AVAILABLE = False
    print(f"⚠️  Modèles non disponibles: {e}")
    # Classes vides pour éviter les erreurs
    class Soin: objects = None
    class TypeSoin: objects = None
    class Prescription: objects = None
    class Medecin: objects = None
    class Ordonnance: objects = None
    class BonPriseEnCharge: objects = None
    class Membre: objects = None
    class Paiement: objects = None

# =============================================================================
# 5. IMPORTER DRF COMPLET (si disponible)
# =============================================================================

try:
    from rest_framework import viewsets, generics, status
    from rest_framework.decorators import action
    from rest_framework.response import Response
    from rest_framework.permissions import IsAuthenticated
    from rest_framework.exceptions import PermissionDenied
    from django_filters.rest_framework import DjangoFilterBackend
    from rest_framework.filters import SearchFilter, OrderingFilter
    from django.db.models import Sum, Avg
    
    DRF_AVAILABLE = True
    print("✅ DRF importé")
except ImportError as e:
    DRF_AVAILABLE = False
    print(f"⚠️  DRF non disponible: {e}")
    
    # Définir des classes vides
    class viewsets:
        class ModelViewSet: pass
        class ReadOnlyModelViewSet: pass
    class generics:
        class GenericAPIView: pass
    class Response:
        def __init__(self, data=None, status=None):
            self.data = data
            self.status_code = status
    class PermissionDenied(Exception): pass
    DjangoFilterBackend = None
    SearchFilter = None
    OrderingFilter = None

# =============================================================================
# 6. VIEWSETS CONDITIONNELS (uniquement si DRF et modèles disponibles)
# =============================================================================

if DRF_AVAILABLE and MODELS_AVAILABLE:
    
    class TypeSoinViewSet(viewsets.ModelViewSet):
        queryset = TypeSoin.objects.filter(actif=True)
        serializer_class = TypeSoinSerializer
        permission_classes = [IsAuthenticated]
        filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
        search_fields = ['nom', 'description']
        ordering_fields = ['nom', 'cout_reference']


    class SoinViewSet(viewsets.ModelViewSet):
        queryset = Soin.objects.all()
        permission_classes = [IsAuthenticated]
        filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
        filterset_fields = ['statut', 'type_soin', 'medecin']
        search_fields = ['patient__username', 'patient__first_name', 'patient__last_name', 'description']
        ordering_fields = ['date_realisation', 'date_creation', 'cout']

        def get_serializer_class(self):
            if self.action in ['create', 'update', 'partial_update']:
                return SoinCreateSerializer
            return SoinSerializer


    class PrescriptionViewSet(viewsets.ModelViewSet):
        queryset = Prescription.objects.all()
        serializer_class = PrescriptionSerializer
        permission_classes = [IsAuthenticated]
        filter_backends = [DjangoFilterBackend, SearchFilter]
        filterset_fields = ['soin', 'date_prescription']
        search_fields = ['medicament']


    class MedecinViewSet(viewsets.ReadOnlyModelViewSet):
        queryset = Medecin.objects.filter(actif=True).select_related('user')
        serializer_class = MedecinSerializer
        permission_classes = [IsAuthenticated]
        filter_backends = [SearchFilter, OrderingFilter]
        search_fields = ['user__first_name', 'user__last_name', 'specialite']
        ordering_fields = ['user__last_name', 'specialite']


    class MembreViewSet(viewsets.ModelViewSet):
        queryset = Membre.objects.filter(statut='actif')
        serializer_class = MembreSerializer
        permission_classes = [IsAuthenticated]
        filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
        filterset_fields = ['type_mutuelle', 'statut']
        search_fields = ['user__first_name', 'user__last_name', 'numero_membre']
        ordering_fields = ['user__last_name', 'date_adhesion']


    class BonPriseEnChargeViewSet(viewsets.ModelViewSet):
        queryset = BonPriseEnCharge.objects.all()
        serializer_class = BonPriseEnChargeSerializer
        permission_classes = [IsAuthenticated]
        filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
        filterset_fields = ['statut', 'membre']
        search_fields = ['numero_bon', 'membre__user__first_name', 'membre__user__last_name']
        ordering_fields = ['date_creation', 'montant_prise_en_charge']


    class PaiementViewSet(viewsets.ModelViewSet):
        queryset = Paiement.objects.all()
        serializer_class = PaiementSerializer
        permission_classes = [IsAuthenticated]
        filter_backends = [DjangoFilterBackend, OrderingFilter]
        filterset_fields = ['statut', 'mode_paiement']
        ordering_fields = ['date_paiement', 'montant']


    class OrdonnanceViewSet(viewsets.ModelViewSet):
        queryset = Ordonnance.objects.all()
        serializer_class = OrdonnanceSerializer
        permission_classes = [IsAuthenticated]
        filter_backends = [DjangoFilterBackend, OrderingFilter]
        filterset_fields = ['est_valide', 'medecin', 'patient']
        ordering_fields = ['date_ordonnance']


    class StatistiquesAPIView(generics.GenericAPIView):
        permission_classes = [IsAuthenticated]

        def get(self, request):
            user = request.user
            date_30j = timezone.now().date() - timedelta(days=30)

            if hasattr(user, 'profile'):
                if user.profile.role == 'ASSUREUR':
                    data = self.get_statistiques_assureur()
                elif user.profile.role == 'MEDECIN':
                    data = self.get_statistiques_medecin(user)
                elif user.profile.role == 'MEMBRE':
                    data = self.get_statistiques_membre(user)
                else:
                    data = self.get_statistiques_generales()
            else:
                data = self.get_statistiques_generales()

            return Response(data)

        def get_statistiques_assureur(self):
            soins_30j = Soin.objects.filter(date_realisation__gte=timezone.now().date() - timedelta(days=30))
            
            return {
                'soins': {
                    'total': Soin.objects.count(),
                    'total_30j': soins_30j.count(),
                    'valides': Soin.objects.filter(statut='valide').count(),
                    'attente': Soin.objects.filter(statut='attente').count(),
                    'rejetes': Soin.objects.filter(statut='rejete').count(),
                    'cout_total': Soin.objects.aggregate(Sum('cout'))['cout__sum'] or 0,
                    'cout_moyen': Soin.objects.aggregate(Avg('cout'))['cout__avg'] or 0,
                },
                'membres': {
                    'total': Membre.objects.filter(statut='actif').count(),
                    'nouveaux_30j': Membre.objects.filter(
                        date_adhesion__gte=timezone.now().date() - timedelta(days=30)
                    ).count(),
                },
                'paiements': {
                    'total': Paiement.objects.count(),
                    'montant_total': Paiement.objects.aggregate(Sum('montant'))['montant__sum'] or 0,
                }
            }

        def get_statistiques_medecin(self, user):
            soins_medecin = Soin.objects.filter(medecin__user=user)
            soins_30j = soins_medecin.filter(date_realisation__gte=timezone.now().date() - timedelta(days=30))

            return {
                'soins': {
                    'total': soins_medecin.count(),
                    'total_30j': soins_30j.count(),
                    'valides': soins_medecin.filter(statut='valide').count(),
                    'attente': soins_medecin.filter(statut='attente').count(),
                    'cout_total': soins_medecin.aggregate(Sum('cout'))['cout__sum'] or 0,
                },
                'ordonnances': {
                    'total': Ordonnance.objects.filter(medecin__user=user).count(),
                    'validees': Ordonnance.objects.filter(medecin__user=user, est_valide=True).count(),
                }
            }

        def get_statistiques_membre(self, user):
            soins_membre = Soin.objects.filter(patient=user)
            
            return {
                'soins': {
                    'total': soins_membre.count(),
                    'valides': soins_membre.filter(statut='valide').count(),
                    'attente': soins_membre.filter(statut='attente').count(),
                },
                'bons': {
                    'total': BonPriseEnCharge.objects.filter(membre__user=user).count(),
                    'actifs': BonPriseEnCharge.objects.filter(membre__user=user, statut='ACTIF').count(),
                }
            }

        def get_statistiques_generales(self):
            return {
                'soins_total': Soin.objects.count(),
                'membres_total': Membre.objects.filter(statut='actif').count(),
                'medecins_total': Medecin.objects.filter(actif=True).count(),
            }

else:
    print("⚠️  DRF ou modèles non disponibles - ViewSets désactivés")
    
    # Définir des classes vides pour éviter les erreurs d'import
    class TypeSoinViewSet: pass
    class SoinViewSet: pass
    class PrescriptionViewSet: pass
    class MedecinViewSet: pass
    class MembreViewSet: pass
    class BonPriseEnChargeViewSet: pass
    class PaiementViewSet: pass
    class OrdonnanceViewSet: pass
    class StatistiquesAPIView: pass