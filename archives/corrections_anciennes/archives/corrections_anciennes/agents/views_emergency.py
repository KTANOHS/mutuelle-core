
# agents/views_emergency.py
from django.http import HttpResponse
from django.shortcuts import render

def emergency_dashboard(request):
    return HttpResponse('''
    <html>
    <head><title>MAINTENANCE AGENT</title></head>
    <body style="background: red; color: white; text-align: center; padding: 50px;">
        <h1>🚨 ESPACE AGENT EN MAINTENANCE</h1>
        <p>L'espace agent est temporairement indisponible.</p>
        <p>Raison: Templates manquants</p>
        <p>Veuillez contacter l'administrateur.</p>
    </body>
    </html>
    ''', status=503)
