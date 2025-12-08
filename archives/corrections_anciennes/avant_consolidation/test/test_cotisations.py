# test_cotisations.py
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_preview_generation():
    """Test de l'API de prévisualisation"""
    url = f"{BASE_URL}/assureur/cotisations/preview/"
    params = {"periode": "2024-12"}
    
    try:
        response = requests.get(url, params=params)
        print(f"Status: {response.status_code}")
        print(f"Contenu: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("✓ Prévisualisation OK")
        else:
            print("✗ Erreur prévisualisation")
    except Exception as e:
        print(f"✗ Exception: {e}")

def test_generate_cotisations():
    """Test de la génération de cotisations"""
    url = f"{BASE_URL}/assureur/cotisations/generer/"
    data = {
        "periode": "2024-12",
        "csrfmiddlewaretoken": "get_from_browser"
    }
    
    # Note: Vous devez d'abord vous connecter pour obtenir le token CSRF
    # Ce test nécessite une session authentifiée
    
    print("Note: Ce test nécessite une session authentifiée")
    print("Testez manuellement via le formulaire web")

def test_list_cotisations():
    """Test de la liste des cotisations"""
    url = f"{BASE_URL}/assureur/cotisations/"
    
    try:
        response = requests.get(url)
        print(f"Liste cotisations - Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Liste des cotisations accessible")
        else:
            print("✗ Erreur liste des cotisations")
    except Exception as e:
        print(f"✗ Exception: {e}")

def test_statistiques():
    """Test des statistiques"""
    url = f"{BASE_URL}/assureur/statistiques/"
    
    try:
        response = requests.get(url)
        print(f"Statistiques - Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Statistiques accessibles")
        else:
            print("✗ Erreur statistiques")
    except Exception as e:
        print(f"✗ Exception: {e}")

if __name__ == "__main__":
    print("=== TESTS COTISATIONS ASSUREUR ===\n")
    
    print("1. Test prévisualisation:")
    test_preview_generation()
    
    print("\n2. Test liste des cotisations:")
    test_list_cotisations()
    
    print("\n3. Test statistiques:")
    test_statistiques()
    
    print("\n4. Test génération (à faire manuellement):")
    print("   Accédez à: http://127.0.0.1:8000/assureur/cotisations/generer/")
    print("   Connectez-vous en tant qu'assureur")
    print("   Sélectionnez une période")
    print("   Cliquez sur 'Générer les cotisations'")