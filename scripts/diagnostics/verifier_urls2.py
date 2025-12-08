#!/usr/bin/env python
"""
SCRIPT DE VÉRIFICATION DES URLs - VERSION CORRIGÉE
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.urls import reverse, NoReverseMatch  # ✅ CORRECTION: urls au lieu de core.urlresolvers
from django.test import Client

def verifier_urls_assureur():
    """Vérifie toutes les URLs de l'application assureur"""
    print("🔗 VÉRIFICATION DES URLs ASSUREUR")
    print("=" * 60)
    
    urls_a_verifier = [
        'assureur:liste_bons',
        'assureur:creer_bon',
        'assureur:liste_membres',
        'assureur:detail_membre',
        'assureur:dashboard',
    ]
    
    client = Client()
    
    # Tester avec un utilisateur anonyme d'abord
    print("\n🔍 TEST UTILISATEUR ANONYME:")
    for url_name in urls_a_verifier:
        try:
            if 'creer_bon' in url_name:
                url = reverse(url_name, kwargs={'membre_id': 5})
            elif 'detail_membre' in url_name:
                url = reverse(url_name, kwargs={'membre_id': 5})
            else:
                url = reverse(url_name)
            
            response = client.get(url)
            print(f"   {url_name:25} -> {response.status_code} ({url})")
            
        except NoReverseMatch:
            print(f"   {url_name:25} -> ❌ URL NON CONFIGURÉE")
        except Exception as e:
            print(f"   {url_name:25} -> ❌ ERREUR: {e}")
    
    # Maintenant tester en se connectant
    print("\n🔐 TEST AVEC CONNEXION ASSUREUR:")
    
    from django.contrib.auth.models import User
    try:
        # Essayer de se connecter avec un utilisateur assureur
        user = User.objects.get(username='assureur_complet')
        client.force_login(user)
        
        for url_name in urls_a_verifier:
            try:
                if 'creer_bon' in url_name:
                    url = reverse(url_name, kwargs={'membre_id': 5})
                elif 'detail_membre' in url_name:
                    url = reverse(url_name, kwargs={'membre_id': 5})
                else:
                    url = reverse(url_name)
                
                response = client.get(url)
                status = "✅" if response.status_code == 200 else f"❌ {response.status_code}"
                print(f"   {url_name:25} -> {status} ({url})")
                
            except NoReverseMatch:
                print(f"   {url_name:25} -> ❌ URL NON CONFIGURÉE")
            except Exception as e:
                print(f"   {url_name:25} -> ❌ ERREUR: {e}")
                
    except User.DoesNotExist:
        print("❌ Utilisateur assureur_complet non trouvé")

def verifier_structure_urls():
    """Vérifie la structure des URLs dans les fichiers de configuration"""
    print("\n📁 STRUCTURE DES FICHIERS URLs:")
    
    urls_files = [
        'mutuelle_core/urls.py',
        'assureur/urls.py'
    ]
    
    for file_path in urls_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} existe")
            # Lire le fichier pour vérifier la configuration
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    if 'assureur' in content and 'bons/creer' in content:
                        print(f"   → Contient la configuration assureur/bons")
                    else:
                        print(f"   ⚠️  Configuration assureur manquante")
            except Exception as e:
                print(f"   ❌ Erreur lecture: {e}")
        else:
            print(f"❌ {file_path} n'existe pas")

if __name__ == "__main__":
    verifier_urls_assureur()
    verifier_structure_urls()
    
    print("\n" + "=" * 60)
    print("🎯 SOLUTIONS:")
    print("1. Utilisez les identifiants: assureur_complet / password123")
    print("2. Vérifiez que l'URL est correcte dans assureur/urls.py")
    print("3. Vérifiez les permissions dans la vue creer_bon")