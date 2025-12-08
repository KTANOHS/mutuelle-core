import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

django.setup()

def verifier_urls_medecin():
    print("🔗 VÉRIFICATION DES URLS MÉDECIN")
    print("=" * 40)
    
    # Vérifier le fichier urls.py de l'application medecin
    urls_path = os.path.join(os.path.dirname(__file__), 'medecin', 'urls.py')
    
    if os.path.exists(urls_path):
        print("✅ Fichier medecin/urls.py existe")
        with open(urls_path, 'r') as f:
            content = f.read()
            print("📄 Contenu de medecin/urls.py:")
            print("-" * 30)
            for line in content.split('\n'):
                if line.strip() and not line.strip().startswith('#'):
                    print(f"  {line}")
            print("-" * 30)
    else:
        print("❌ Fichier medecin/urls.py n'existe pas")
    
    # Vérifier les URLs dans le projet principal
    projet_urls_path = os.path.join(os.path.dirname(__file__), 'votre_projet', 'urls.py')
    if os.path.exists(projet_urls_path):
        print("\n📋 URLs dans le projet principal:")
        with open(projet_urls_path, 'r') as f:
            content = f.read()
            if 'medecin' in content:
                print("✅ Application medecin incluse dans les URLs principales")
            else:
                print("❌ Application medecin NON incluse dans les URLs principales")
    
    # Tester l'accès via le resolver Django
    print("\n🌐 URLs disponibles via Django:")
    from django.urls import get_resolver
    resolver = get_resolver()
    
    def extract_urls(patterns, prefix=''):
        urls = []
        for pattern in patterns:
            if hasattr(pattern, 'pattern'):
                current_pattern = str(pattern.pattern)
                if hasattr(pattern, 'url_patterns'):
                    # C'est un include
                    urls.extend(extract_urls(pattern.url_patterns, prefix + current_pattern))
                else:
                    # C'est un pattern simple
                    if hasattr(pattern, 'name') and pattern.name:
                        urls.append(f"{prefix + current_pattern} -> {pattern.name}")
                    else:
                        urls.append(prefix + current_pattern)
        return urls
    
    try:
        all_urls = extract_urls(resolver.url_patterns)
        medecin_urls = [url for url in all_urls if 'medecin' in url.lower()]
        
        if medecin_urls:
            print("✅ URLs medecin trouvées:")
            for url in medecin_urls:
                print(f"   📍 {url}")
        else:
            print("❌ Aucune URL medecin trouvée")
            
    except Exception as e:
        print(f"❌ Erreur extraction URLs: {e}")

verifier_urls_medecin()