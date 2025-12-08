#!/usr/bin/env python
"""
DIAGNOSTIC TEMPLATE MÉDECIN
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def diagnostic_template():
    client = Client()
    client.login(username='medecin_test', password='pass123')
    
    response = client.get('/medecin/ordonnances/')
    print("🔍 DIAGNOSTIC TEMPLATE:")
    print(f"Status: {response.status_code}")
    print(f"Template utilisé: {response.template_name}")
    print(f"Contenu (extrait): {response.content[:500]}...")

if __name__ == "__main__":
    diagnostic_template()