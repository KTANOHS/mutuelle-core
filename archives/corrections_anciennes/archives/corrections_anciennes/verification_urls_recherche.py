# verification_urls_recherche.py
import os
import django
import sys

sys.path.append('/Users/koffitanohsoualiho/Documents/projet')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.urls import reverse, get_resolver

def analyser_urls_recherche():
    print("🔗 ANALYSE DES URLs DE RECHERCHE")
    print("=" * 50)
    
    resolver = get_resolver()
    
    # Chercher toutes les URLs contenant 'recherche'
    urls_recherche = []
    
    def find_urls(urlpatterns, prefix=''):
        for pattern in urlpatterns:
            if hasattr(pattern, 'pattern'):
                full_pattern = prefix + str(pattern.pattern)
                if hasattr(pattern, 'name') and pattern.name:
                    if 'recherche' in pattern.name.lower():
                        urls_recherche.append((pattern.name, full_pattern))
                if hasattr(pattern, 'url_patterns'):
                    find_urls(pattern.url_patterns, prefix + str(pattern.pattern))
    
    find_urls(resolver.url_patterns)
    
    if urls_recherche:
        print("URLs de recherche trouvées:")
        for nom, pattern in urls_recherche:
            print(f"  🔗 {nom:20} -> {pattern}")
            
            # Tester si l'URL fonctionne
            try:
                url = reverse(nom)
                print(f"      ✅ URL générée: {url}")
            except Exception as e:
                print(f"      ❌ Erreur: {e}")
    else:
        print("❌ Aucune URL de recherche trouvée")

if __name__ == "__main__":
    analyser_urls_recherche()