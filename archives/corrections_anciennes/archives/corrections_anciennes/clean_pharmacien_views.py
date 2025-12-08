# verify_pharmacien_setup.py
from pathlib import Path

def verify_pharmacien_setup():
    """Vérifie la cohérence de l'application pharmacien"""
    
    print("🔍 VÉRIFICATION DE L'APPLICATION PHARMACIEN")
    print("=" * 50)
    
    # Vérifier l'existence des fichiers
    files_to_check = [
        ('pharmacien/views.py', 'Vues'),
        ('pharmacien/urls.py', 'URLs'),
        ('pharmacien/models.py', 'Modèles'),
        ('templates/pharmacien/dashboard.html', 'Template Dashboard'),
    ]
    
    for file_path, description in files_to_check:
        if Path(file_path).exists():
            print(f"✅ {description}: EXISTE")
        else:
            print(f"❌ {description}: MANQUANT")
    
    # Vérifier les URLs dans le template base.html
    base_template = Path('templates/base.html')
    if base_template.exists():
        with open(base_template, 'r', encoding='utf-8') as f:
            content = f.read()
            
        urls_to_check = [
            'pharmacien:dashboard',
            'pharmacien:liste_ordonnances_attente', 
            'pharmacien:profil_pharmacien',
            'pharmacien:stock'
        ]
        
        print("\n📋 URLs référencées dans base.html:")
        for url in urls_to_check:
            if url in content:
                print(f"  ✅ {url}")
            else:
                print(f"  ❌ {url} (non référencée)")
    
    print("\n💡 RECOMMANDATIONS:")
    print("1. Exécutez: python clean_pharmacien_views.py")
    print("2. Vérifiez que pharmacien/urls.py existe")
    print("3. Testez: python manage.py check")

if __name__ == '__main__':
    verify_pharmacien_setup()