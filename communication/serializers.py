# communication/serializers.py
from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    expediteur_username = serializers.ReadOnlyField(source='expediteur.username')
    destinataire_username = serializers.ReadOnlyField(source='destinataire.username')
    
    class Meta:
        model = Message
        fields = ['id', 'contenu', 'expediteur_username', 'destinataire_username', 'date_envoi', 'est_lu']