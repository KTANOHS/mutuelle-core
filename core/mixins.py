from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import PartageAutomatique

class PartageAutomatiqueMixin:
    """Mixin pour vérifier l'accès aux documents partagés"""
    
    def get_document_partage(self, type_document, document_id):
        """Récupère un document si l'utilisateur y a accès"""
        # Vérifier si le document est partagé avec l'utilisateur
        if PartageAutomatique.objects.filter(
            type_document=type_document,
            document_id=document_id,
            visible_par=self.request.user
        ).exists():
            
            # Récupérer le document selon son type
            if type_document == PartageAutomatique.ORDONNANCE:
                from medecin.models import Ordonnance
                return get_object_or_404(Ordonnance, id=document_id)
            elif type_document == PartageAutomatique.BON:
                from assureur.models import Bon
                return get_object_or_404(Bon, id=document_id)
        
        raise PermissionDenied("Vous n'avez pas accès à ce document")

class FiltreParPartageMixin:
    """Mixin pour filtrer les querysets par documents partagés"""
    
    def get_queryset_ordonnances(self):
        """Retourne les ordonnances accessibles à l'utilisateur"""
        from medecin.models import Ordonnance
        ordonnances_partagees = PartageAutomatique.objects.filter(
            type_document=PartageAutomatique.ORDONNANCE,
            visible_par=self.request.user
        ).values_list('document_id', flat=True)
        
        return Ordonnance.objects.filter(id__in=ordonnances_partagees)
    
    def get_queryset_bons(self):
        """Retourne les bons accessibles à l'utilisateur"""
        from assureur.models import Bon
        bons_partages = PartageAutomatique.objects.filter(
            type_document=PartageAutomatique.BON,
            visible_par=self.request.user
        ).values_list('document_id', flat=True)
        
        return Bon.objects.filter(id__in=bons_partages)