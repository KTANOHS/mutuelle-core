# pharmacie_public/api_views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PharmaciePublic, MedicamentPublic, CommandePublic
from .serializers import PharmaciePublicSerializer, MedicamentPublicSerializer

class PharmaciePublicViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les pharmacies publiques"""
    queryset = PharmaciePublic.objects.filter(statut='actif')
    serializer_class = PharmaciePublicSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['GET'])
def api_pharmacies_proches(request):
    """API pour trouver les pharmacies proches"""
    latitude = request.GET.get('lat')
    longitude = request.GET.get('lng')
    rayon = request.GET.get('rayon', 10)  # 10km par défaut
    
    # Implémentation de la géolocalisation
    pharmacies = PharmaciePublic.objects.filter(statut='actif')
    
    # Filtrage par distance (implémentation simplifiée)
    if latitude and longitude:
        # Ici vous intégreriez un service de géolocalisation
        pass
        
    serializer = PharmaciePublicSerializer(pharmacies, many=True)
    return Response(serializer.data)