import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def corriger_champs_api():
    """Corriger les champs de l'API pour qu'ils correspondent au frontend"""
    print("🔧 CORRECTION CHAMPS API")
    print("=======================")
    
    # Chemin vers le fichier de vues
    vue_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'agents', 'views.py')
    
    if os.path.exists(vue_path):
        print("📁 Modification de la vue API...")
        
        with open(vue_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Trouver et remplacer la fonction details_bon_soin_api
        if 'def details_bon_soin_api' in content:
            # Nouvelle version de la fonction avec les champs attendus par le frontend
            nouvelle_fonction = '''
def details_bon_soin_api(request, bon_id):
    """API pour récupérer les détails d'un bon de soin - Version corrigée pour le frontend"""
    try:
        from soins.models import BonDeSoin
        from django.utils import timezone
        from datetime import timedelta
        
        bon = BonDeSoin.objects.select_related('patient', 'medecin').get(id=bon_id)
        
        # Calculer la date d'expiration (30 jours après la création)
        date_expiration = bon.date_creation + timedelta(days=30) if bon.date_creation else None
        temps_restant = (date_expiration - timezone.now().date()).days if date_expiration else 0
        
        # Formater les données selon ce que le frontend attend
        data = {
            # Champs généraux attendus par le frontend
            'code': bon.id,  # Utiliser l'ID comme code
            'membre': bon.patient.nom_complet if bon.patient else 'Non spécifié',
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
            
            # Informations supplémentaires (au cas où)
            'patient_complet': {
                'nom': bon.patient.nom if bon.patient else '',
                'prenom': bon.patient.prenom if bon.patient else '',
                'numero': bon.patient.numero_unique if bon.patient else ''
            },
            'medecin': bon.medecin.get_full_name() if bon.medecin else 'Non assigné',
            'symptomes': bon.symptomes or 'Non spécifiés',
            'diagnostic': bon.diagnostic or 'Non spécifié'
        }
        
        from django.http import JsonResponse
        return JsonResponse({'success': True, 'bon': data})
        
    except BonDeSoin.DoesNotExist:
        from django.http import JsonResponse
        return JsonResponse({'success': False, 'error': 'Bon de soin non trouvé'}, status=404)
    except Exception as e:
        from django.http import JsonResponse
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
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
                
                print("✅ Fonction API mise à jour avec les bons champs")
            else:
                print("❌ Impossible de trouver la fonction à remplacer")
        else:
            print("❌ Fonction details_bon_soin_api non trouvée")
    
    return True

if __name__ == "__main__":
    success = corriger_champs_api()
    
    if success:
        print("\n🎉 CHAMPS API CORRIGÉS!")
        print("🔁 Redémarrez le serveur pour appliquer les changements")
    else:
        print("\n⚠️  CORRECTION ÉCHOUÉE")