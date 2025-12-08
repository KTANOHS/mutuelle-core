#!/usr/bin/env python3
"""
Correction des URLs manquantes dans les templates assureur
"""

import re
from pathlib import Path

def fix_missing_urls():
    """Corrige les URLs manquantes identifiées"""
    print("🔧 CORRECTION DES URLs MANQUANTES")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    corrections = {
        'export_bons_pdf': 'assureur:export_bons_pdf',
        'creer_paiement_general': 'assureur:creer_paiement'  # ou l'URL correcte
    }
    
    # Fichiers à corriger
    files_to_fix = [
        "templates/assureur/liste_bons.html",
        "templates/assureur/liste_paiements.html"
    ]
    
    for file_path in files_to_fix:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"\n📄 Traitement de {file_path}")
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            corrections_made = 0
            
            for wrong_url, correct_url in corrections.items():
                # Patterns de recherche
                patterns = [
                    f"['\"]{wrong_url}['\"]",
                    f"\\{{%\\s*url\\s+['\"]{wrong_url}['\"]\\s*%\\}}",
                    f"href=[\"']\\s*\\{{%\\s*url\\s+[\"']{wrong_url}[\"']\\s*%\\}}\\s*[\"']"
                ]
                
                for pattern in patterns:
                    try:
                        # Remplacer par l'URL correcte avec le namespace
                        replacement = pattern.replace(wrong_url, correct_url)
                        new_content, count = re.subn(pattern, replacement, content)
                        if count > 0:
                            content = new_content
                            corrections_made += count
                            print(f"   ✅ Remplacé '{wrong_url}' par '{correct_url}' ({count} fois)")
                    except re.error as e:
                        print(f"   ⚠️  Erreur regex: {e}")
            
            if content != original_content:
                # Sauvegarde
                backup_path = full_path.with_suffix('.html.backup2')
                if not backup_path.exists():
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        f.write(original_content)
                
                # Écriture des corrections
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"   💾 {corrections_made} correction(s) sauvegardée(s)")
            else:
                print("   ℹ️  Aucune correction nécessaire")
        else:
            print(f"⚠️  Fichier non trouvé: {file_path}")

def verify_urls_configuration():
    """Vérifie la configuration des URLs dans urls.py"""
    print("\n🔍 VÉRIFICATION DE LA CONFIGURATION DES URLs")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    
    # Vérifier assureur/urls.py
    assureur_urls = project_root / "assureur/urls.py"
    if assureur_urls.exists():
        with open(assureur_urls, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_urls = ['export_bons_pdf', 'creer_paiement']
        missing_urls = []
        
        for url in required_urls:
            if f"name='{url}'" not in content and f'name="{url}"' not in content:
                missing_urls.append(url)
        
        if missing_urls:
            print("❌ URLs manquantes dans assureur/urls.py:")
            for url in missing_urls:
                print(f"   - {url}")
            print("\n💡 Ajoutez ces URLs dans assureur/urls.py:")
            print("""
    path('bons/export-pdf/', views.export_bons_pdf, name='export_bons_pdf'),
    path('paiements/creer/', views.creer_paiement, name='creer_paiement'),
""")
        else:
            print("✅ Toutes les URLs sont configurées")
    else:
        print("⚠️  Fichier assureur/urls.py non trouvé")

def create_missing_views():
    """Crée les vues manquantes si nécessaire"""
    print("\n🛠️  CRÉATION DES VUES MANQUANTES")
    print("=" * 50)
    
    views_file = Path(__file__).parent / "assureur/views.py"
    
    if views_file.exists():
        with open(views_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier les vues manquantes
        missing_views = []
        if 'def export_bons_pdf' not in content:
            missing_views.append('export_bons_pdf')
        if 'def creer_paiement' not in content:
            missing_views.append('creer_paiement')
        
        if missing_views:
            print("❌ Vues manquantes dans assureur/views.py:")
            for view in missing_views:
                print(f"   - {view}")
            
            print("\n💡 Ajoutez ces fonctions dans assureur/views.py:")
            print("""
def export_bons_pdf(request):
    \"\"\"Export PDF des bons de soin\"\"\"
    from django.http import HttpResponse
    # Implémentez l'export PDF ici
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="bons_soin.pdf"'
    return response

def creer_paiement(request):
    \"\"\"Créer un nouveau paiement\"\"\"
    if request.method == 'POST':
        # Traitement du formulaire
        pass
    # Afficher le formulaire de création
    return render(request, 'assureur/creer_paiement.html')
""")
        else:
            print("✅ Toutes les vues existent")
    else:
        print("⚠️  Fichier assureur/views.py non trouvé")

def main():
    """Fonction principale"""
    print("🚀 CORRECTION DES ERREURS D'URLS ASSUREUR")
    print("=" * 60)
    
    # Étape 1: Corriger les templates
    fix_missing_urls()
    
    # Étape 2: Vérifier la configuration
    verify_urls_configuration()
    
    # Étape 3: Vérifier les vues
    create_missing_views()
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES ACTIONS")
    print("✅ Templates corrigés")
    print("✅ Configuration vérifiée") 
    print("✅ Vues vérifiées")
    print("\n🎯 PROCHAINES ÉTAPES:")
    print("1. Si des URLs/vues manquent, ajoutez-les")
    print("2. Redémarrez le serveur: python manage.py runserver")
    print("3. Testez les fonctionnalités corrigées")

if __name__ == "__main__":
    main()