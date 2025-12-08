#!/usr/bin/env python
"""
TROUVER ET CORRIGER LA VUE DE CRÉATION DE BONS
"""

import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Django configuré")
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

def trouver_fichier_vue():
    """Trouve le fichier contenant la vue de création de bons"""
    print("🔍 RECHERCHE DE LA VUE...")
    
    dossiers_a_chercher = ['assureur', 'membres', 'core', 'soins']
    
    for dossier in dossiers_a_chercher:
        chemin_views = os.path.join(os.path.dirname(__file__), dossier, 'views.py')
        if os.path.exists(chemin_views):
            print(f"✅ Fichier views.py trouvé dans: {dossier}/")
            
            # Lire le contenu
            with open(chemin_views, 'r') as f:
                contenu = f.read()
                
            # Chercher la fonction de création de bons
            if 'creer_bon' in contenu or 'bondesoin' in contenu.lower():
                print(f"🎯 Vue de création de bons trouvée dans: {dossier}/views.py")
                return chemin_views, dossier, contenu
    
    print("❌ Vue non trouvée automatiquement")
    return None, None, None

def corriger_vue(chemin_views, app_name):
    """Corrige la vue pour retourner JsonResponse"""
    print(f"\n🔧 CORRECTION DE LA VUE DANS {chemin_views}...")
    
    # Code de vue corrigé
    code_corrige = '''
def creer_bon(request, membre_id):
    """
    Vue corrigée pour la création de bons
    IMPORTANT: Retourne TOUJOURS JsonResponse, jamais de dict
    """
    from django.http import JsonResponse
    import json
    from django.utils import timezone
    from membres.models import Membre, Bon
    
    try:
        if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Charger les données JSON
            data = json.loads(request.body)
            
            # Récupérer le membre
            try:
                membre = Membre.objects.get(numero_unique=membre_id)
            except Membre.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': f'Membre {membre_id} non trouvé'
                }, status=404)
            
            # CRÉATION DU BON
            numero_bon = f"BON_{membre.numero_unique}_{timezone.now().strftime('%Y%m%d_%H%M%S')}"
            
            bon = Bon.objects.create(
                numero_bon=numero_bon,
                membre=membre,
                type_soin=data.get('type_soin', 'Consultation générale'),
                description=data.get('description', ''),
                lieu_soins=data.get('lieu_soins', 'Hôpital Central'),
                date_soins=data.get('date_soins', timezone.now().date()),
                medecin_traitant=data.get('medecin_traitant', 'Dr. Smith'),
                numero_ordonnance=data.get('numero_ordonnance', ''),
                montant_total=float(data.get('montant_total', 0)),
                taux_remboursement=float(data.get('taux_remboursement', 70)),
                montant_rembourse=0,
                frais_dossier=0,
                statut='en_attente',
                date_creation=timezone.now(),
                date_emission=timezone.now().date()
            )
            
            # RETOURNER JsonResponse, PAS de dict
            return JsonResponse({
                'success': True,
                'message': 'Bon créé avec succès',
                'bon_id': bon.id,
                'numero_bon': bon.numero_bon,
                'membre': f"{membre.nom} {membre.prenom}",
                'statut': bon.statut
            })
            
        else:
            return JsonResponse({
                'success': False,
                'message': 'Méthode non autorisée'
            }, status=405)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erreur: {str(e)}'
        }, status=500)
'''

    # Lire le fichier actuel
    with open(chemin_views, 'r') as f:
        ancien_contenu = f.read()
    
    # Remplacer la fonction existante ou l'ajouter
    if 'def creer_bon(' in ancien_contenu:
        # Trouver et remplacer la fonction existante
        lines = ancien_contenu.split('\n')
        new_lines = []
        in_function = False
        replaced = False
        
        for line in lines:
            if line.strip().startswith('def creer_bon('):
                in_function = True
                if not replaced:
                    new_lines.append(code_corrige)
                    replaced = True
                continue
                
            if in_function and line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                in_function = False
                
            if not in_function:
                new_lines.append(line)
        
        nouveau_contenu = '\n'.join(new_lines)
    else:
        # Ajouter la fonction à la fin
        nouveau_contenu = ancien_contenu + '\n\n' + code_corrige
    
    # Sauvegarder
    with open(chemin_views, 'w') as f:
        f.write(nouveau_contenu)
    
    print("✅ Vue corrigée avec succès!")
    return True

def main():
    print("🛠️  CORRECTION DE LA VUE DE CRÉATION DE BONS")
    print("=" * 50)
    
    chemin_views, app_name, contenu = trouver_fichier_vue()
    
    if not chemin_views:
        print("\n❌ Vue non trouvée. Création d'une nouvelle vue...")
        # Créer la vue dans assureur/views.py
        chemin_assureur = os.path.join(os.path.dirname(__file__), 'assureur')
        if not os.path.exists(chemin_assureur):
            os.makedirs(chemin_assureur)
        
        chemin_views = os.path.join(chemin_assureur, 'views.py')
        with open(chemin_views, 'w') as f:
            f.write('''"""
Vues pour l'application assureur
"""

from django.http import JsonResponse
import json
from django.utils import timezone
from membres.models import Membre, Bon

''')
        app_name = 'assureur'
    
    # Corriger la vue
    if corriger_vue(chemin_views, app_name):
        print(f"\n✅ Vue corrigée dans: {chemin_views}")
        print("\n🎯 Redémarrez le serveur et relancez les tests!")
    else:
        print("❌ Échec de la correction")

if __name__ == "__main__"
    main()