# corriger_affichage_details.py
import os

def corriger_affichage_details():
    """Corriger l'affichage des détails dans le template"""
    
    template_path = 'templates/communication/messagerie.html'
    
    with open(template_path, 'r') as f:
        contenu = f.read()
    
    print("🔧 CORRECTION AFFICHAGE DÉTAILS")
    print("=" * 50)
    
    # Vérifier et corriger l'affichage des messages
    if '{{ conversation.total_messages }}' in contenu:
        print("✅ L'affichage du total des messages est présent")
    else:
        print("❌ L'affichage du total des messages est manquant")
        
        # Ajouter l'affichage des messages
        if '{{ conversation.nb_messages_non_lus }}' in contenu:
            contenu = contenu.replace(
                '{{ conversation.nb_messages_non_lus }}',
                '{{ conversation.nb_messages_non_lus }} / {{ conversation.total_messages }}'
            )
            print("✅ Affichage des messages corrigé")
    
    # Vérifier l'affichage de la date d'activité
    if '{{ conversation.derniere_activite|timesince }}' in contenu:
        print("✅ L'affichage de la date d'activité est présent")
    else:
        print("❌ L'affichage de la date d'activité est manquant")
    
    # Écrire les modifications
    with open(template_path, 'w') as f:
        f.write(contenu)
    
    print("✅ Corrections des détails appliquées")

if __name__ == "__main__":
    corriger_affichage_details()