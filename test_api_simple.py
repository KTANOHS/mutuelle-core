#!/usr/bin/env python3
# test_api_simple.py - Test simplifié de l'API
import requests
import json
import sys

def test_api():
    base_url = "http://127.0.0.1:8000"
    
    # Test 1: JSON
    print("\n🔍 Test 1: Envoi JSON")
    url = f"{base_url}/communication/envoyer-message-api/"
    data = {
        "destinataire_id": 1,
        "contenu": "Test message via JSON API",
        "titre": "Test API"
    }
    
    try:
        response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Succès: {response.json()}")
        else:
            print(f"   ❌ Erreur: {response.text[:200]}")
    except Exception as e:
        print(f"   💥 Exception: {str(e)}")
    
    # Test 2: Form-Data
    print("\n🔍 Test 2: Envoi Form-Data")
    data_form = {
        "destinataire": 1,
        "contenu": "Test message via Form-Data",
        "titre": "Test Form"
    }
    
    try:
        response = requests.post(url, data=data_form)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Succès: {response.json()}")
        else:
            print(f"   ❌ Erreur: {response.text[:200]}")
    except Exception as e:
        print(f"   💥 Exception: {str(e)}")

if __name__ == "__main__":
    test_api()
