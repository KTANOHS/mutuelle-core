import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

def verification_template_complet():
    print("🔍 VÉRIFICATION DU TEMPLATE COMPLET")
    print("=" * 50)
    
    # Vérifier le template
    template_path = 'templates/medecin/suivi_chronique/tableau_bord.html'
    
    if not os.path.exists(template_path):
        print("❌ Template non trouvé")
        return False
    
    print("✅ Template trouvé")
    
    # Analyser le contenu
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📏 Taille: {len(content)} caractères")
    print(f"📄 Lignes: {len(content.splitlines())}")
    
    # Vérifier les éléments clés
    elements = [
        ("Extension base", "{% extends 'medecin/base_medecin.html' %}" in content),
        ("Titre", "Suivi des Maladies Chroniques" in content),
        ("Cartes statistiques", "card border-left-primary" in content),
        ("Tableau accompagnements", "table table-hover" in content),
        ("Bouton création", "Créer un Accompagnement" in content)
    ]
    
    print("\n🔍 Éléments détectés:")
    for element, present in elements:
        status = "✅" if present else "❌"
        print(f"   {status} {element}")
    
    # Test Django
    try:
        django.setup()
        from django.template.loader import get_template
        
        template = get_template('medecin/suivi_chronique/tableau_bord.html')
        print("\n✅ Django peut charger le template complet")
        
        # Test de rendu avec contexte
        context = {
            'patients_suivis': 5,
            'accompagnements_actifs': 3,
            'alertes_en_cours': 2,
            'objectifs_atteints': 8,
            'accompagnements': []
        }
        
        rendered = template.render(context)
        print(f"✅ Rendu avec contexte réussi ({len(rendered)} caractères)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

success = verification_template_complet()

if success:
    print("\n🎉 TEMPLATE COMPLET VALIDÉ!")
    print("📋 Redémarrez le serveur pour voir la nouvelle interface")
else:
    print("\n❌ Problème avec le template")