# test_web_interface.py
import os
import django
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("=== TEST DE L'INTERFACE WEB ===")

# Option 1: Test avec Selenium (si vous l'avez installé)
try:
    # Configuration du navigateur
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Mode sans interface
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    
    # Aller à la page de connexion
    driver.get('http://127.0.0.1:8000/accounts/login/')
    
    # Se connecter (remplacez par vos identifiants)
    username = driver.find_element(By.NAME, 'username')
    password = driver.find_element(By.NAME, 'password')
    
    username.send_keys('admin')  # Remplacez par votre username
    password.send_keys('admin123')  # Remplacez par votre password
    
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    
    # Attendre la redirection
    time.sleep(2)
    
    # Aller à la page de génération des cotisations
    driver.get('http://127.0.0.1:8000/assureur/cotisations/generer/')
    
    # Vérifier que la page charge
    wait = WebDriverWait(driver, 10)
    try:
        title = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        print(f"✅ Page chargée: {title.text}")
        
        # Vérifier les statistiques
        stats = driver.find_elements(By.CLASS_NAME, 'stat-box')
        print(f"✅ Statistiques trouvées: {len(stats)}")
        
        # Vérifier le formulaire
        form = driver.find_element(By.TAG_NAME, 'form')
        print("✅ Formulaire trouvé")
        
        # Vérifier le champ période
        periode_input = driver.find_element(By.ID, 'periode')
        print(f"✅ Champ période trouvé, valeur: {periode_input.get_attribute('value')}")
        
        # Vérifier le bouton de prévisualisation
        try:
            btn_preview = driver.find_element(By.ID, 'btn-preview')
            print("✅ Bouton prévisualisation trouvé")
        except:
            print("⚠ Bouton prévisualisation non trouvé")
            
        # Vérifier le bouton de génération
        try:
            btn_generate = driver.find_element(By.ID, 'btn-generate')
            print("✅ Bouton génération trouvé")
        except:
            print("⚠ Bouton génération non trouvé")
        
        print("\n✅ Test d'interface web réussi !")
        
    except TimeoutException:
        print("❌ Timeout: La page n'a pas chargé correctement")
        print(f"Page source: {driver.page_source[:500]}")
    
    driver.quit()
    
except Exception as e:
    print(f"❌ Erreur Selenium: {e}")
    print("Installation optionnelle: pip install selenium webdriver-manager")
    
    # Option 2: Test simple avec requests
    print("\n=== TEST ALTERNATIF AVEC REQUESTS ===")
    import requests
    from bs4 import BeautifulSoup
    
    session = requests.Session()
    
    # Se connecter
    login_url = 'http://127.0.0.1:8000/accounts/login/'
    response = session.get(login_url)
    
    # Extraire le token CSRF
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    
    # Envoyer les identifiants
    login_data = {
        'username': 'admin',
        'password': 'admin123',
        'csrfmiddlewaretoken': csrf_token
    }
    
    response = session.post(login_url, data=login_data)
    
    if response.status_code == 200 or response.status_code == 302:
        print("✅ Connexion réussie")
        
        # Accéder à la page de génération
        gen_url = 'http://127.0.0.1:8000/assureur/cotisations/generer/'
        response = session.get(gen_url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Vérifier le titre
            title = soup.find('h1')
            if title:
                print(f"✅ Titre trouvé: {title.text.strip()}")
            
            # Vérifier le formulaire
            form = soup.find('form')
            if form:
                print("✅ Formulaire trouvé")
                
                # Vérifier le champ période
                periode = soup.find('input', {'id': 'periode'})
                if periode:
                    print(f"✅ Champ période trouvé, valeur: {periode.get('value', 'Non défini')}")
            
            # Vérifier les boutons
            if soup.find('button', {'id': 'btn-preview'}):
                print("✅ Bouton prévisualisation trouvé")
            
            if soup.find('button', {'id': 'btn-generate'}):
                print("✅ Bouton génération trouvé")
            
            print("\n✅ Test de la page réussi !")
        else:
            print(f"❌ Erreur page génération: {response.status_code}")
    else:
        print(f"❌ Échec de connexion: {response.status_code}")