# api/views_mobile.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from django.utils import timezone

from .serializers_mobile import *
from membres.models import Membre, Bon
from soins.models import Soin
from paiements.models import Paiement
from notifications.models import Notification

class MobileMembreViewSet(viewsets.ReadOnlyModelViewSet):
    """API mobile pour les membres"""
    serializer_class = MobileMembreSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Membre.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Dashboard mobile personnalisé"""
        membre = self.get_queryset().first()
        if not membre:
            return Response(
                {'error': 'Profil membre non trouvé'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Calcul des statistiques
        bons = Bon.objects.filter(membre=membre)
        bons_actifs = bons.filter(statut='ACTIF').count()
        soins_en_attente = Soin.objects.filter(patient=request.user, statut='attente').count()
        notifications_non_lues = Notification.objects.filter(user=request.user, lu=False).count()
        
        dashboard_data = {
            'solde': membre.solde or 0,
            'bons_actifs': bons_actifs,
            'bons_total': bons.count(),
            'soins_en_attente': soins_en_attente,
            'notifications_non_lues': notifications_non_lues,
            'prochain_rdv': None
        }
        
        serializer = MobileDashboardSerializer(dashboard_data)
        return Response(serializer.data)

class MobileBonViewSet(viewsets.ReadOnlyModelViewSet):
    """API mobile pour les bons"""
    serializer_class = MobileBonSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Bon.objects.filter(membre__user=self.request.user).order_by('-date_creation')

class MobileNotificationViewSet(viewsets.ModelViewSet):
    """Gestion des notifications mobiles"""
    serializer_class = MobileNotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-date_creation')
    
    @action(detail=False, methods=['post'])
    def marquer_toutes_lues(self, request):
        """Marquer toutes les notifications comme lues"""
        updated = Notification.objects.filter(
            user=request.user, 
            lu=False
        ).update(lu=True)
        
        return Response({
            'status': 'success',
            'notifications_marquees': updated
        })
    
    @action(detail=True, methods=['post'])
    def marquer_lue(self, request, pk=None):
        """Marquer une notification comme lue"""
        notification = self.get_object()
        notification.marquer_comme_lu()
        return Response({'status': 'success'})

class MobileSoinViewSet(viewsets.ReadOnlyModelViewSet):
    """API mobile pour les soins"""
    serializer_class = MobileSoinSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Soin.objects.filter(patient=self.request.user).order_by('-date_realisation')

class MobilePaiementViewSet(viewsets.ReadOnlyModelViewSet):
    """API mobile pour les paiements"""
    serializer_class = MobilePaiementSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Paiement.objects.filter(bon__membre__user=self.request.user).order_by('-date_paiement')