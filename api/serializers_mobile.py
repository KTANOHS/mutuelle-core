# api/serializers_mobile.py
from rest_framework import serializers
from membres.models import Membre, Bon
from soins.models import Soin
from paiements.models import Paiement
from notifications.models import Notification

class MobileMembreSerializer(serializers.ModelSerializer):
    """Serializer optimisé pour mobile"""
    nom_complet = serializers.SerializerMethodField()
    
    class Meta:
        model = Membre
        fields = [
            'id', 'numero_membre', 'nom_complet', 'statut', 
            'type_mutuelle', 'date_adhesion', 'solde'
        ]
    
    def get_nom_complet(self, obj):
        return f"{obj.prenom} {obj.nom}"

class MobileBonSerializer(serializers.ModelSerializer):
    """Serializer light pour mobile"""
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    
    class Meta:
        model = Bon
        fields = [
            'id', 'numero_bon', 'statut', 'statut_display', 
            'montant_total', 'date_creation', 'type_soin'
        ]

class MobileSoinSerializer(serializers.ModelSerializer):
    """Serializer optimisé pour les soins - mobile"""
    type_soin_nom = serializers.CharField(source='type_soin.nom', read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    
    class Meta:
        model = Soin
        fields = [
            'id', 'type_soin_nom', 'date_realisation', 'statut', 
            'statut_display', 'cout', 'description'
        ]

class MobilePaiementSerializer(serializers.ModelSerializer):
    """Serializer light pour les paiements - mobile"""
    mode_paiement_display = serializers.CharField(source='get_mode_paiement_display', read_only=True)
    
    class Meta:
        model = Paiement
        fields = [
            'id', 'montant', 'mode_paiement', 'mode_paiement_display',
            'statut', 'date_paiement', 'numero_transaction'
        ]

class MobileNotificationSerializer(serializers.ModelSerializer):
    """Serializer pour les notifications mobiles"""
    class Meta:
        model = Notification
        fields = [
            'id', 'titre', 'message', 'type_notification', 
            'lu', 'date_creation', 'lien'
        ]

class MobileDashboardSerializer(serializers.Serializer):
    """Serializer pour le dashboard mobile"""
    solde = serializers.DecimalField(max_digits=10, decimal_places=2)
    bons_actifs = serializers.IntegerField()
    bons_total = serializers.IntegerField()
    soins_en_attente = serializers.IntegerField()
    notifications_non_lues = serializers.IntegerField()
    prochain_rdv = serializers.DateTimeField(required=False, allow_null=True)