import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

def verification_correction_finale():
    print("🔍 VÉRIFICATION CORRECTION FINALE")
    print("=" * 50)
    
    # Vérifier le template corrigé
    template_path = 'templates/medecin/suivi_chronique/tableau_bord.html'
    
    if not os.path.exists(template_path):
        print("❌ Template non trouvé")
        return False
    
    # Lire le contenu
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("📄 Vérification extension:")
    if "{% extends 'medecin/base.html' %}" in content:
        print("✅ Utilise medecin/base.html")
    elif "{% extends 'medecin/base_medecin.html' %}" in content:
        print("❌ Utilise encore base_medecin.html")
        return False
    else:
        print("⚠️  Extension non standard")
    
    # Test Django
    try:
        django.setup()
        from django.template.loader import get_template
        
        print("\n🐍 TEST DJANGO:")
        try:
            template = get_template('medecin/suivi_chronique/tableau_bord.html')
            print("✅ Template chargé avec succès")
            
            # Test de rendu
            from django.contrib.auth.models import User
            user = User.objects.get(username='medecin_test')
            
            context = {
                'request': type('Request', (), {'user': user, 'path': '/medecin/suivi-chronique/'})(),
                'patients_suivis': 5,
                'accompagnements_actifs': 3,
                'alertes_en_cours': 2,
                'objectifs_atteints': 8,
                'accompagnements': [],
                'medecin': type('Medecin', (), {
                    'specialite': type('Specialite', (), {'nom': 'Généraliste'})(),
                    'etablissement': type('Etablissement', (), {'nom': 'Cabinet Test'})(),
                    'disponible': True
                })()
            }
            
            rendered = template.render(context)
            print(f"✅ Rendu réussi - {len(rendered)} caractères")
            
            # Vérifications du contenu rendu
            if "Suivi des Maladies Chroniques" in rendered:
                print("✅ Contenu spécifique présent")
            if "card border-left-primary" in rendered:
                print("✅ Cartes statistiques présentes")
                
            return True
            
        except Exception as e:
            print(f"❌ Erreur template: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur setup: {e}")
        return False

success = verification_correction_finale()

if success:
    print("\n🎉 CORRECTION RÉUSSIE!")
    print("📋 Le serveur devrait maintenant fonctionner sans erreur")
else:
    print("\n❌ Problème persistant")