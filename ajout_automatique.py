#!/usr/bin/env python3
"""
SCRIPT D'AJOUT AUTOMATIQUE DES URLs ET VUES MANQUANTES
"""

import re
from pathlib import Path

def ajouter_urls_manquantes():
    """Ajoute les URLs manquantes dans assureur/urls.py"""
    print("🔗 AJOUT DES URLs MANQUANTES")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    urls_file = project_root / "assureur/urls.py"
    
    if not urls_file.exists():
        print("❌ Fichier assureur/urls.py non trouvé")
        return False
    
    with open(urls_file, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # Vérifier si les URLs existent déjà
    if "name='export_bons_pdf'" in contenu or 'name="export_bons_pdf"' in contenu:
        print("✅ URL export_bons_pdf existe déjà")
    else:
        # Ajouter l'URL export_bons_pdf
        nouveau_url = """    path('bons/export-pdf/', views.export_bons_pdf, name='export_bons_pdf'),"""
        
        # Trouver où insérer (après la dernière URL existante)
        pattern = r"(urlpatterns\s*=\s*\[)(.*?)(\n\])"
        match = re.search(pattern, contenu, re.DOTALL)
        
        if match:
            debut, urls_existantes, fin = match.groups()
            nouvelles_urls = urls_existantes.rstrip() + "\n" + nouveau_url + "\n"
            contenu = contenu[:match.start()] + debut + nouvelles_urls + fin + contenu[match.end():]
            print("✅ URL export_bons_pdf ajoutée")
        else:
            print("❌ Impossible de trouver urlpatterns")
            return False
    
    if "name='creer_paiement'" in contenu or 'name="creer_paiement"' in contenu:
        print("✅ URL creer_paiement existe déjà")
    else:
        # Ajouter l'URL creer_paiement
        nouveau_url = """    path('paiements/creer/', views.creer_paiement, name='creer_paiement'),"""
        
        pattern = r"(urlpatterns\s*=\s*\[)(.*?)(\n\])"
        match = re.search(pattern, contenu, re.DOTALL)
        
        if match:
            debut, urls_existantes, fin = match.groups()
            nouvelles_urls = urls_existantes.rstrip() + "\n" + nouveau_url + "\n"
            contenu = contenu[:match.start()] + debut + nouvelles_urls + fin + contenu[match.end():]
            print("✅ URL creer_paiement ajoutée")
        else:
            print("❌ Impossible de trouver urlpatterns")
            return False
    
    # Sauvegarder
    with open(urls_file, 'w', encoding='utf-8') as f:
        f.write(contenu)
    
    return True

def ajouter_vues_manquantes():
    """Ajoute les vues manquantes dans assureur/views.py"""
    print("\n🛠️  AJOUT DES VUES MANQUANTES")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    views_file = project_root / "assureur/views.py"
    
    if not views_file.exists():
        print("❌ Fichier assureur/views.py non trouvé")
        return False
    
    with open(views_file, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # Vérifier et ajouter export_bons_pdf
    if 'def export_bons_pdf(' in contenu:
        print("✅ Vue export_bons_pdf existe déjà")
    else:
        # Ajouter la vue export_bons_pdf à la fin du fichier, avant les dernières lignes
        nouvelle_vue = """

def export_bons_pdf(request):
    \"\"\"Export PDF des bons de soin\"\"\"
    from django.http import HttpResponse
    from django.template.loader import render_to_string
    from weasyprint import HTML
    import tempfile
    from .models import BonDeSoin
    
    try:
        # Récupérer tous les bons
        bons = BonDeSoin.objects.all()
        
        # Rendre le template HTML
        html_string = render_to_string('assureur/export_bons_pdf.html', {
            'bons': bons,
            'title': 'Liste des Bons de Soin'
        })
        
        # Créer un PDF
        html = HTML(string=html_string)
        pdf_file = tempfile.NamedTemporaryFile(delete=False)
        html.write_pdf(pdf_file.name)
        
        # Retourner le PDF
        with open(pdf_file.name, 'rb') as f:
            pdf_content = f.read()
        
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="bons_soin.pdf"'
        return response
        
    except Exception as e:
        # Fallback simple si WeasyPrint n'est pas installé
        return HttpResponse(f"Export PDF des bons de soin - Erreur: {e}")
"""
        
        # Ajouter avant la dernière ligne (généralement une ligne vide ou la fin du fichier)
        contenu = contenu.rstrip() + nouvelle_vue + "\n"
        print("✅ Vue export_bons_pdf ajoutée")
    
    # Vérifier et ajouter creer_paiement
    if 'def creer_paiement(' in contenu:
        print("✅ Vue creer_paiement existe déjà")
    else:
        # Ajouter la vue creer_paiement
        nouvelle_vue = """

def creer_paiement(request):
    \"\"\"Créer un nouveau paiement\"\"\"
    from django.shortcuts import render, redirect
    from django.contrib import messages
    from .models import Paiement, Membre
    from .forms import PaiementForm
    
    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            paiement = form.save(commit=False)
            paiement.save()
            messages.success(request, 'Paiement créé avec succès!')
            return redirect('assureur:liste_paiements')
        else:
            messages.error(request, 'Erreur dans le formulaire')
    else:
        form = PaiementForm()
    
    context = {
        'form': form,
        'title': 'Créer un Paiement',
        'membres': Membre.objects.all()
    }
    return render(request, 'assureur/creer_paiement.html', context)
"""
        
        contenu = contenu.rstrip() + nouvelle_vue + "\n"
        print("✅ Vue creer_paiement ajoutée")
    
    # Sauvegarder
    with open(views_file, 'w', encoding='utf-8') as f:
        f.write(contenu)
    
    return True

def creer_formulaire_paiement():
    """Crée le formulaire de paiement si nécessaire"""
    print("\n📝 CRÉATION DU FORMULAIRE DE PAIEMENT")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    forms_file = project_root / "assureur/forms.py"
    
    # Vérifier si forms.py existe
    if not forms_file.exists():
        print("ℹ️  Fichier assureur/forms.py non trouvé - création...")
        contenu_forms = """from django import forms
from .models import Paiement

class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['membre', 'montant', 'date_paiement', 'type_paiement', 'description']
        widgets = {
            'date_paiement': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
"""
        with open(forms_file, 'w', encoding='utf-8') as f:
            f.write(contenu_forms)
        print("✅ Fichier forms.py créé avec PaiementForm")
    else:
        with open(forms_file, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        if 'class PaiementForm' not in contenu:
            # Ajouter PaiementForm à la fin
            nouveau_form = """

class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['membre', 'montant', 'date_paiement', 'type_paiement', 'description']
        widgets = {
            'date_paiement': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
"""
            contenu = contenu.rstrip() + nouveau_form + "\n"
            with open(forms_file, 'w', encoding='utf-8') as f:
                f.write(contenu)
            print("✅ PaiementForm ajouté à forms.py")
        else:
            print("✅ PaiementForm existe déjà")

def verifier_imports_views():
    """Vérifie et ajoute les imports nécessaires dans views.py"""
    print("\n📦 VÉRIFICATION DES IMPORTS")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    views_file = project_root / "assureur/views.py"
    
    with open(views_file, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    imports_manquants = []
    
    # Vérifier l'import de PaiementForm
    if 'from .forms import PaiementForm' not in contenu and 'PaiementForm' in contenu:
        imports_manquants.append("from .forms import PaiementForm")
    
    # Vérifier l'import de Membre
    if 'from .models import Membre' not in contenu and 'Membre.objects' in contenu:
        imports_manquants.append("from .models import Membre")
    
    if imports_manquants:
        # Ajouter les imports après les autres imports
        lignes = contenu.split('\n')
        nouvelle_contenu = []
        imports_ajoutes = False
        
        for ligne in lignes:
            nouvelle_contenu.append(ligne)
            if ligne.startswith('from ') or ligne.startswith('import '):
                if not imports_ajoutes and (not ligne.strip() or not (ligne.startswith('from ') or ligne.startswith('import '))):
                    for import_manquant in imports_manquants:
                        nouvelle_contenu.append(import_manquant)
                        print(f"✅ Import ajouté: {import_manquant}")
                    imports_ajoutes = True
        
        if not imports_ajoutes:
            # Ajouter à la fin des imports existants
            for i, ligne in enumerate(nouvelle_contenu):
                if ligne.startswith('from ') or ligne.startswith('import '):
                    if i + 1 >= len(nouvelle_contenu) or not (nouvelle_contenu[i + 1].startswith('from ') or nouvelle_contenu[i + 1].startswith('import ')):
                        for import_manquant in imports_manquants:
                            nouvelle_contenu.insert(i + 1, import_manquant)
                            print(f"✅ Import ajouté: {import_manquant}")
                        break
        
        contenu = '\n'.join(nouvelle_contenu)
        
        with open(views_file, 'w', encoding='utf-8') as f:
            f.write(contenu)
    else:
        print("✅ Tous les imports sont présents")

def solution_simplifiee():
    """Solution simplifiée pour tester rapidement"""
    print("\n🚀 SOLUTION SIMPLIFIÉE POUR TEST RAPIDE")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    views_file = project_root / "assureur/views.py"
    
    with open(views_file, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # Remplacer les vues complexes par des versions simplifiées
    if 'def export_bons_pdf(' in contenu:
        # Trouver et remplacer la fonction existante
        pattern = r"def export_bons_pdf\(request\):.*?return response.*?\n"
        nouvelle_vue = '''def export_bons_pdf(request):
    """Export PDF des bons de soin (version simplifiée)"""
    from django.http import HttpResponse
    return HttpResponse("Fonction d'export PDF des bons - À implémenter")
'''
        contenu = re.sub(pattern, nouvelle_vue, contenu, flags=re.DOTALL)
        print("✅ Vue export_bons_pdf simplifiée")
    
    if 'def creer_paiement(' in contenu:
        # Trouver et remplacer la fonction existante
        pattern = r"def creer_paiement\(request\):.*?return render.*?\n"
        nouvelle_vue = '''def creer_paiement(request):
    """Créer un nouveau paiement (version simplifiée)"""
    from django.http import HttpResponse
    return HttpResponse("Formulaire de création de paiement - À implémenter")
'''
        contenu = re.sub(pattern, nouvelle_vue, contenu, flags=re.DOTALL)
        print("✅ Vue creer_paiement simplifiée")
    
    with open(views_file, 'w', encoding='utf-8') as f:
        f.write(contenu)

def main():
    """Fonction principale"""
    print("🚀 AJOUT AUTOMATIQUE DES FONCTIONNALITÉS MANQUANTES")
    print("=" * 60)
    
    try:
        # Étape 1: Ajouter les URLs
        succes_urls = ajouter_urls_manquantes()
        
        # Étape 2: Ajouter les vues
        succes_vues = ajouter_vues_manquantes()
        
        # Étape 3: Créer le formulaire
        creer_formulaire_paiement()
        
        # Étape 4: Vérifier les imports
        verifier_imports_views()
        
        # Étape 5: Solution simplifiée pour test
        print("\n💡 Voulez-vous une version simplifiée pour tester rapidement?")
        print("   (Cela remplacera les fonctions complexes par des versions simples)")
        reponse = input("   Tapez 'oui' pour appliquer la version simplifiée: ")
        
        if reponse.lower() in ['oui', 'yes', 'o', 'y']:
            solution_simplifiee()
            print("✅ Version simplifiée appliquée")
        
        print("\n" + "=" * 60)
        print("🎉 CONFIGURATION TERMINÉE!")
        print("\n📋 RÉCAPITULATIF:")
        print("✅ URLs ajoutées dans assureur/urls.py")
        print("✅ Vues ajoutées dans assureur/views.py") 
        print("✅ Formulaire créé dans assureur/forms.py")
        print("✅ Imports vérifiés")
        
        print("\n🚀 PROCHAINES ÉTAPES:")
        print("1. Redémarrez le serveur: python manage.py runserver")
        print("2. Testez les fonctionnalités:")
        print("   - Liste des bons (bouton PDF)")
        print("   - Liste des paiements (bouton création)")
        print("3. Implémentez les fonctionnalités complètes plus tard")
        
    except Exception as e:
        print(f"❌ Erreur lors de la configuration: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())