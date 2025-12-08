import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def correction_definitive():
    """Correction définitive - API renvoie les champs à la racine comme attendu par le frontend"""
    print("🔧 CORRECTION DÉFINITIVE API")
    print("============================")
    
    vue_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'agents', 'views.py')
    
    if os.path.exists(vue_path):
        print("📁 Application de la correction définitive...")
        
        with open(vue_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Nouvelle version qui renvoie les champs à la racine
        nouvelle_fonction = '''
def details_bon_soin_api(request, bon_id):
    """API pour récupérer les détails d'un bon de soin - VERSION CORRIGÉE POUR LE FRONTEND"""
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
        
        # CRITIQUE: Renvoyer les champs À LA RACINE comme le frontend les attend
        # Le frontend ne regarde pas dans un objet "bon", mais directement à la racine
        data = {
            # Champs généraux - À LA RACINE
            'code': str(bon.id),
            'membre': bon.patient.nom_complet if bon.patient and hasattr(bon.patient, 'nom_complet') else 'Non spécifié',
            'montant_max': str(bon.montant) if bon.montant else '0',
            'statut': bon.statut.upper() if bon.statut else 'INDEFINI',
            
            # Dates - À LA RACINE
            'date_creation': bon.date_creation.strftime('%d/%m/%Y') if bon.date_creation else 'Non spécifiée',
            'date_expiration': date_expiration.strftime('%d/%m/%Y') if date_expiration else 'Non calculée',
            'temps_restant': f"{temps_restant} jours" if temps_restant > 0 else "Expiré",
            
            # Détails médicaux - À LA RACINE
            'motif': bon.symptomes or 'Non spécifié',
            'type_soin': bon.diagnostic or 'Consultation générale',
            'urgence': 'Normale',
            
            # Champs supplémentaires pour compatibilité
            'id': bon.id,
            'patient_nom': bon.patient.nom if bon.patient else '',
            'patient_prenom': bon.patient.prenom if bon.patient else '',
            'medecin': bon.medecin.get_full_name() if bon.medecin and hasattr(bon.medecin, 'get_full_name') else 'Non assigné',
            'symptomes': bon.symptomes or 'Non spécifiés',
            'diagnostic': bon.diagnostic or 'Non spécifié'
        }
        
        return JsonResponse(data)  # IMPORTANT: Renvoyer data directement, pas dans un objet 'bon'
        
    except BonDeSoin.DoesNotExist:
        from django.http import JsonResponse
        return JsonResponse({'success': False, 'error': 'Bon de soin non trouvé'}, status=404)
    except Exception as e:
        from django.http import JsonResponse
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
'''
        
        # Remplacer l'ancienne fonction
        if 'def details_bon_soin_api' in content:
            debut = content.find('def details_bon_soin_api')
            fin = content.find('def ', debut + 1)
            if fin == -1:
                fin = len(content)
            
            nouveau_content = content[:debut] + nouvelle_fonction + content[fin:]
            
            with open(vue_path, 'w', encoding='utf-8') as f:
                f.write(nouveau_content)
            
            print("✅ Correction définitive appliquée!")
            print("   📋 L'API renvoie maintenant les champs À LA RACINE")
            print("   🎯 Le frontend devrait maintenant trouver les données directement")
        else:
            print("❌ Fonction non trouvée")
    
    return True

if __name__ == "__main__":
    correction_definitive()
    print("\n🔁 Redémarrez le serveur pour appliquer les changements")