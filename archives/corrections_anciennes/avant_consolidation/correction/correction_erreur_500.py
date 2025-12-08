import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def corriger_erreur_500():
    """Corriger l'erreur 500 dans l'API details_bon_soin_api"""
    print("🔧 CORRECTION ERREUR 500")
    print("=======================")
    
    # Chemin vers le fichier de vues
    vue_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'agents', 'views.py')
    
    if os.path.exists(vue_path):
        print("📁 Correction de la vue API...")
        
        with open(vue_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier si la fonction existe et la corriger
        if 'def details_bon_soin_api' in content:
            # Nouvelle version CORRIGÉE de la fonction
            nouvelle_fonction = '''
def details_bon_soin_api(request, bon_id):
    """API pour récupérer les détails d'un bon de soin - Version corrigée pour le frontend"""
    try:
        from soins.models import BonDeSoin
        from django.utils import timezone
        from datetime import timedelta
        from django.http import JsonResponse
        
        bon = BonDeSoin.objects.select_related('patient', 'medecin').get(id=bon_id)
        
        # Calculer la date d'expiration (30 jours après la création)
        date_expiration = None
        temps_restant = 0
        
        if bon.date_creation:
            # Convertir en date si c'est un datetime
            if hasattr(bon.date_creation, 'date'):
                date_creation = bon.date_creation.date()
            else:
                date_creation = bon.date_creation
                
            date_expiration = date_creation + timedelta(days=30)
            aujourd_hui = timezone.now().date()
            temps_restant = (date_expiration - aujourd_hui).days
        
        # Formater les données selon ce que le frontend attend
        data = {
            # Champs généraux attendus par le frontend
            'code': str(bon.id),  # Utiliser l'ID comme code (convertir en string)
            'membre': bon.patient.nom_complet if bon.patient and hasattr(bon.patient, 'nom_complet') else 'Non spécifié',
            'montant_max': str(bon.montant) if bon.montant else '0',
            'statut': bon.statut.upper() if bon.statut else 'INDEFINI',
            
            # Dates
            'date_creation': bon.date_creation.strftime('%d/%m/%Y') if bon.date_creation else 'Non spécifiée',
            'date_expiration': date_expiration.strftime('%d/%m/%Y') if date_expiration else 'Non calculée',
            'temps_restant': f"{temps_restant} jours" if temps_restant > 0 else "Expiré",
            
            # Détails médicaux
            'motif': bon.symptomes or 'Non spécifié',
            'type_soin': bon.diagnostic or 'Consultation générale',
            'urgence': 'Normale',  # Valeur par défaut
            
            # Informations supplémentaires
            'medecin': bon.medecin.get_full_name() if bon.medecin and hasattr(bon.medecin, 'get_full_name') else 'Non assigné',
            'symptomes': bon.symptomes or 'Non spécifiés',
            'diagnostic': bon.diagnostic or 'Non spécifié'
        }
        
        return JsonResponse({'success': True, 'bon': data})
        
    except BonDeSoin.DoesNotExist:
        from django.http import JsonResponse
        return JsonResponse({'success': False, 'error': 'Bon de soin non trouvé'}, status=404)
    except Exception as e:
        from django.http import JsonResponse
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ Erreur dans details_bon_soin_api: {e}")
        print(f"📋 Détails: {error_details}")
        return JsonResponse({'success': False, 'error': str(e), 'details': error_details}, status=500)
'''
            
            # Remplacer l'ancienne fonction par la nouvelle
            debut_fonction = content.find('def details_bon_soin_api')
            if debut_fonction != -1:
                # Trouver la fin de la fonction (prochaine fonction ou fin de fichier)
                fin_fonction = content.find('def ', debut_fonction + 1)
                if fin_fonction == -1:
                    fin_fonction = len(content)
                
                # Remplacer
                nouveau_content = content[:debut_fonction] + nouvelle_fonction + content[fin_fonction:]
                
                with open(vue_path, 'w', encoding='utf-8') as f:
                    f.write(nouveau_content)
                
                print("✅ Fonction API corrigée (gestion d'erreurs améliorée)")
            else:
                print("❌ Impossible de trouver la fonction à remplacer")
        else:
            print("❌ Fonction details_bon_soin_api non trouvée")
    
    return True

if __name__ == "__main__":
    success = corriger_erreur_500()
    
    if success:
        print("\n🎉 CORRECTION APPLIQUÉE!")
        print("🔁 Redémarrez le serveur pour appliquer les changements")
    else:
        print("\n⚠️  CORRECTION ÉCHOUÉE")