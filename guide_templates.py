# guide_templates.py
def generer_guide_templates():
    """
    Génère un guide pour utiliser les URLs dans les templates
    """
    print("GUIDE D'UTILISATION DANS LES TEMPLATES")
    print("=" * 50)
    
    print("\n📝 COMMENT UTILISER LES URLs AVEC PARAMÈTRES:")
    print("-" * 40)
    
    exemples = {
        'medecin:detail_consultation': 
            "{% url 'medecin:detail_consultation' consultation.id %}",
        
        'medecin:detail_ordonnance': 
            "{% url 'medecin:detail_ordonnance' ordonnance.id %}",
        
        'medecin:modifier_consultation': 
            "{% url 'medecin:modifier_consultation' consultation.id %}",
        
        'medecin:valider_bon': 
            "{% url 'medecin:valider_bon' bon.id %}",
        
        'medecin:modifier_statut_rdv': 
            "{% url 'medecin:modifier_statut_rdv' consultation.id %}"
    }
    
    print("Dans vos templates Django, utilisez:")
    for url_name, exemple in exemples.items():
        print(f"\n🔗 {url_name}:")
        print(f"   → {exemple}")
    
    print("\n💡 CONSEILS:")
    print("1. Passez les objets complets dans le contexte")
    print("2. Utilisez .id pour obtenir l'identifiant")
    print("3. Vérifiez que l'objet existe avant de créer le lien")
    print("4. Testez chaque lien dans l'interface utilisateur")

if __name__ == "__main__":
    generer_guide_templates()