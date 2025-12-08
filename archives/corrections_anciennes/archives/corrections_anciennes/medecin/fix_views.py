# medecin/fix_views.py
import os
import re

def corriger_vues_automatiquement():
    """Corrige automatiquement les vues sans décorateurs"""
    
    views_path = 'medecin/views.py'
    
    if not os.path.exists(views_path):
        print(f"❌ Fichier {views_path} non trouvé")
        return
    
    with open(views_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Liste des vues à corriger
    vues_a_corriger = [
        'liste_bons_attente',
        'historiques_ordonnances', 
        'mes_rendez_vous',
        'profil_medecin',
        'statistiques_medecin',
        'creer_ordonnance',
        'detail_bon',
        'creer_rendez_vous',
        'modifier_statut_rdv',
        'api_statistiques',
        'api_toggle_disponibilite',
        'ajouter_medicament'
    ]
    
    modifications = 0
    
    for vue in vues_a_corriger:
        # Pattern pour trouver la définition de la vue
        pattern = r'def ' + vue + r'\(request[^)]*\):'
        
        # Vérifier si les décorateurs sont déjà présents
        if f'@login_required\ndef {vue}(' in content or f'@medecin_required\ndef {vue}(' in content:
            print(f"✅ {vue} a déjà les décorateurs")
            continue
        
        # Trouver la ligne de définition
        match = re.search(pattern, content)
        if match:
            ligne_vue = match.group()
            nouvelle_ligne = f'@login_required\n@medecin_required\n{ligne_vue}'
            content = content.replace(ligne_vue, nouvelle_ligne)
            modifications += 1
            print(f"✅ {vue} corrigée")
        else:
            print(f"❌ {vue} non trouvée")
    
    if modifications > 0:
        # Sauvegarder le fichier corrigé
        with open(views_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n🎉 {modifications} vues corrigées avec succès!")
        print("🔄 Redémarrez le serveur Django")
    else:
        print("\nℹ️  Aucune correction nécessaire")

# Exécution:
# python manage.py shell
# >>> from medecin.fix_views import corriger_vues_automatiquement
# >>> corriger_vues_automatiquement()