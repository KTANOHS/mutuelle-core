# api/views.py - CORRECTION COMPLÈTE AVEC QUERYSETS
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta

from .serializers import *
from soins.models import Soin, TypeSoin, Prescription
from medecin.models import Medecin, Ordonnance
from assureur.models import BonPriseEnCharge, Membre
from paiements.models import Paiement


class TypeSoinViewSet(viewsets.ModelViewSet):
    queryset = TypeSoin.objects.filter(actif=True)
    serializer_class = TypeSoinSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['nom', 'description']
    ordering_fields = ['nom', 'cout_reference']


class SoinViewSet(viewsets.ModelViewSet):
    # AJOUT: queryset de base pour le routeur
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

    def get_queryset(self):
        user = self.request.user
        queryset = Soin.objects.all().select_related(
            'patient', 'medecin', 'type_soin', 'valide_par'
        )

        # Filtrage selon le rôle
        if hasattr(user, 'profile'):
            if user.profile.role == 'MEDECIN':
                queryset = queryset.filter(medecin__user=user)
            elif user.profile.role == 'MEMBRE':
                queryset = queryset.filter(patient=user)
            # ASSUREUR voit tous les soins

        return queryset

    def perform_create(self, serializer):
        # Seuls les médecins peuvent créer des soins
        if hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'MEDECIN':
            serializer.save(medecin=self.request.user.medecin, created_by=self.request.user)
        else:
            raise PermissionDenied("Seuls les médecins peuvent créer des soins")

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def valider(self, request, pk=None):
        soin = self.get_object()
        if request.user.profile.role != 'ASSUREUR':
            return Response({'error': 'Seuls les assureurs peuvent valider les soins'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        soin.statut = 'valide'
        soin.valide_par = request.user
        soin.date_validation = timezone.now()
        soin.save()
        
        return Response({'status': 'soin validé'})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def rejeter(self, request, pk=None):
        soin = self.get_object()
        if request.user.profile.role != 'ASSUREUR':
            return Response({'error': 'Seuls les assureurs peuvent rejeter les soins'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        motif = request.data.get('motif_rejet', '')
        soin.statut = 'rejete'
        soin.valide_par = request.user
        soin.date_validation = timezone.now()
        soin.motif_rejet = motif
        soin.save()
        
        return Response({'status': 'soin rejeté'})


class PrescriptionViewSet(viewsets.ModelViewSet):
    # AJOUT: queryset de base pour le routeur
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['soin', 'date_prescription']
    search_fields = ['medicament']

    def get_queryset(self):
        user = self.request.user
        queryset = Prescription.objects.all().select_related('soin')

        if hasattr(user, 'profile'):
            if user.profile.role == 'MEDECIN':
                queryset = queryset.filter(soin__medecin__user=user)
            elif user.profile.role == 'MEMBRE':
                queryset = queryset.filter(soin__patient=user)

        return queryset


class MedecinViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Medecin.objects.filter(actif=True).select_related('user')
    serializer_class = MedecinSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__first_name', 'user__last_name', 'specialite']
    ordering_fields = ['user__last_name', 'specialite']


class MembreViewSet(viewsets.ModelViewSet):
    # AJOUT: queryset de base pour le routeur
    queryset = Membre.objects.filter(statut='actif')
    serializer_class = MembreSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type_mutuelle', 'statut']
    search_fields = ['user__first_name', 'user__last_name', 'numero_membre']
    ordering_fields = ['user__last_name', 'date_adhesion']

    def get_queryset(self):
        user = self.request.user
        queryset = Membre.objects.filter(statut='actif').select_related('user')

        if hasattr(user, 'profile') and user.profile.role == 'MEMBRE':
            queryset = queryset.filter(user=user)

        return queryset


class BonPriseEnChargeViewSet(viewsets.ModelViewSet):
    # AJOUT: queryset de base pour le routeur
    queryset = BonPriseEnCharge.objects.all()
    serializer_class = BonPriseEnChargeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['statut', 'membre']
    search_fields = ['numero_bon', 'membre__user__first_name', 'membre__user__last_name']
    ordering_fields = ['date_creation', 'montant_prise_en_charge']

    def get_queryset(self):
        user = self.request.user
        queryset = BonPriseEnCharge.objects.all().select_related('membre', 'soin', 'created_by')

        if hasattr(user, 'profile'):
            if user.profile.role == 'MEMBRE':
                queryset = queryset.filter(membre__user=user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PaiementViewSet(viewsets.ModelViewSet):
    # AJOUT: queryset de base pour le routeur
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['statut', 'mode_paiement']
    ordering_fields = ['date_paiement', 'montant']

    def get_queryset(self):
        user = self.request.user
        queryset = Paiement.objects.all().select_related('bon', 'created_by')

        if hasattr(user, 'profile') and user.profile.role == 'MEMBRE':
            queryset = queryset.filter(bon__membre__user=user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class OrdonnanceViewSet(viewsets.ModelViewSet):
    # AJOUT: queryset de base pour le routeur
    queryset = Ordonnance.objects.all()
    serializer_class = OrdonnanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['est_valide', 'medecin', 'patient']
    ordering_fields = ['date_ordonnance']

    def get_queryset(self):
        user = self.request.user
        queryset = Ordonnance.objects.all().select_related('medecin', 'patient')

        if hasattr(user, 'profile'):
            if user.profile.role == 'MEDECIN':
                queryset = queryset.filter(medecin__user=user)
            elif user.profile.role == 'MEMBRE':
                queryset = queryset.filter(patient=user)

        return queryset


# Vues pour les statistiques
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