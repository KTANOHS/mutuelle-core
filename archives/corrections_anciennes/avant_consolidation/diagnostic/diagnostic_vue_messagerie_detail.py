# diagnostic_vue_messagerie_detail.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyser_vue_messagerie():
    """Analyser en détail la vue messagerie"""
    
    print("🔍 ANALYSE DÉTAILLÉE DE LA VUE MESSAGERIE")
    print("=" * 60)
    
    # Lire le fichier views.py
    with open('communication/views.py', 'r') as f:
        contenu = f.read()
    
    # Extraire la fonction messagerie
    debut = contenu.find('def messagerie(request):')
    if debut == -1:
        print("❌ Fonction messagerie non trouvée dans views.py")
        return
    
    fin = contenu.find('def ', debut + 1)
    if fin == -1:
        fin = len(contenu)
    
    fonction_messagerie = contenu[debut:fin]
    print("📝 CODE DE LA VUE MESSAGERIE:")
    print("-" * 40)
    print(fonction_messagerie)
    print("-" * 40)
    
    # Vérifications
    verifications = {
        "return render avec context": "return render(request, 'communication/messagerie.html', context)" in fonction_messagerie,
        "context défini": "context = {" in fonction_messagerie,
        "conversations dans context": "'conversations'" in fonction_messagerie,
        "form dans context": "'form'" in fonction_messagerie,
        "gestion des erreurs": "except Exception as e:" in fonction_messagerie
    }
    
    print("\n✅ VÉRIFICATIONS:")
    for check, result in verifications.items():
        status = "✅" if result else "❌"
        print(f"   {status} {check}")
    
    return fonction_messagerie

def tester_vue_messagerie_direct():
    """Tester la vue messagerie directement"""
    print("\n🧪 TEST DIRECT DE LA VUE MESSAGERIE")
    print("=" * 60)
    
    from communication.views import messagerie
    from django.test import RequestFactory
    from django.contrib.auth.models import User
    
    try:
        # Créer une requête simulée
        factory = RequestFactory()
        request = factory.get('/communication/')
        
        # Utiliser un utilisateur existant
        pharmacien = User.objects.get(username='test_pharmacien')
        request.user = pharmacien
        
        # Appeler la vue
        response = messagerie(request)
        
        print(f"📊 Statut HTTP: {response.status_code}")
        print(f"📝 Template: {getattr(response, 'template_name', 'Non défini')}")
        
        # Vérifier le contexte
        if hasattr(response, 'context_data'):
            context = response.context_data
            print(f"📦 Contexte disponible: {len(context)} éléments")
            for key, value in context.items():
                print(f"   - {key}: {type(value)}")
        else:
            print("❌ Aucun contexte_data disponible")
            
        # Vérifier le contenu de la réponse
        content = response.content.decode('utf-8')
        if 'conversations' in content.lower() or 'message' in content.lower():
            print("✅ Contenu HTML semble contenir des données de messagerie")
        else:
            print("❌ Contenu HTML ne semble pas contenir de données de messagerie")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

def verifier_template_messagerie():
    """Vérifier le template messagerie.html"""
    print("\n📄 VÉRIFICATION DU TEMPLATE MESSAGERIE.HTML")
    print("=" * 60)
    
    template_path = 'templates/communication/messagerie.html'
    
    if not os.path.exists(template_path):
        print(f"❌ Template non trouvé: {template_path}")
        return
    
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    verifications_template = {
        "Utilise conversations": "conversations" in template_content,
        "Utilise messages_recents": "messages_recents" in template_content,
        "Boucle sur conversations": "for conversation in conversations" in template_content,
        "Affiche le formulaire": "form" in template_content,
        "Gère le cas vide": "empty" in template_content or "Aucun" in template_content
    }
    
    print("✅ VÉRIFICATIONS TEMPLATE:")
    for check, result in verifications_template.items():
        status = "✅" if result else "❌"
        print(f"   {status} {check}")
    
    # Afficher un extrait du template
    print(f"\n📋 Extrait du template (premières 500 caractères):")
    print(template_content[:500] + "..." if len(template_content) > 500 else template_content)

if __name__ == "__main__":
    analyser_vue_messagerie()
    tester_vue_messagerie_direct()
    verifier_template_messagerie()
    
    print("\n🎯 SOLUTIONS POTENTIELLES:")
    print("1. Vérifiez que le template affiche bien les données")
    print("2. Testez l'URL alternative: http://127.0.0.1:8000/communication/messages/")
    print("3. Vérifiez les logs Django pour des erreurs supplémentaires")