
#!/usr/bin/env python3
import os
import sys
import re

# Chemin du fichier views.py
views_path = "pharmacien/views.py"

# Lire le contenu
with open(views_path, 'r') as f:
    content = f.read()

# Trouver et remplacer la fonction historique_validation
# Nouvelle version corrigée
new_function = '''@login_required
@pharmacien_required
@gerer_erreurs
def historique_validation(request):
    """Affiche l'historique des ordonnances validées par le pharmacien"""
    try:
        # Importer les modèles nécessaires
        from pharmacien.models import OrdonnancePharmacien, Pharmacien
        from django.core.paginator import Paginator
        from django.utils import timezone
        from datetime import timedelta
        import logging
        
        logger = logging.getLogger(__name__)
        
        # 1. Obtenir le profil Pharmacien de l'utilisateur
        try:
            pharmacien_profile = Pharmacien.objects.get(user=request.user)
        except Pharmacien.DoesNotExist:
            logger.error(f"Profil pharmacien non trouvé pour {request.user.username}")
            from django.contrib import messages
            messages.error(request, "Profil pharmacien introuvable.")
            return redirect('pharmacien:dashboard')
        
        # 2. Récupérer l'historique des validations
        # CORRECTION: utiliser pharmacien_validateur (Foreign Key vers User)
        validations_qs = OrdonnancePharmacien.objects.filter(
            pharmacien_validateur=request.user,  # CHANGÉ ICI: pharmacien_validateur est un ForeignKey vers User
            date_validation__isnull=False
        ).select_related(
            'ordonnance_medecin__patient',
            'ordonnance_medecin__medecin'
        ).order_by('-date_validation')
        
        # 3. Adapter les données pour le template
        validations_list = []
        for validation in validations_qs:
            if hasattr(validation, 'ordonnance_medecin') and validation.ordonnance_medecin:
                ordonnance = validation.ordonnance_medecin
                validations_list.append({
                    'ordonnance': {
                        'id': ordonnance.id if hasattr(ordonnance, 'id') else validation.id,
                        'ordonnance_medecin': {
                            'patient': getattr(ordonnance, 'patient', None),
                            'medecin': getattr(ordonnance, 'medecin', None),
                            'date_prescription': getattr(ordonnance, 'date_prescription', None),
                        }
                    },
                    'date_validation': validation.date_validation,
                })
        
        # 4. Pagination
        paginator = Paginator(validations_list, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # 5. Statistiques
        stats = {
            'total': len(validations_list),
            'mois_courant': validations_qs.filter(
                date_validation__month=timezone.now().month,
                date_validation__year=timezone.now().year
            ).count(),
            'semaine_courante': validations_qs.filter(
                date_validation__gte=timezone.now() - timedelta(days=7)
            ).count(),
        }
        
        # 6. Contexte
        context = {
            'validations': page_obj,
            'stats': stats,
            'title': 'Historique des validations',
            'pharmacien_profile': pharmacien_profile,
        }
        return render(request, 'pharmacien/historique.html', context)
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Erreur dans historique_validation : {e}")
        from django.contrib import messages
        messages.error(request, "Erreur lors du chargement de l'historique.")
        return redirect('pharmacien:dashboard')'''

# Remplacer la fonction existante
# Chercher la fonction par pattern
pattern = r'@login_required\s*\n@pharmacien_required\s*\n@gerer_erreurs\s*\ndef historique_validation\(request\).*?(?=\n@|\ndef |\Z)'
new_content = re.sub(pattern, new_function, content, flags=re.DOTALL)

# Écrire le fichier corrigé
with open(views_path, 'w') as f:
    f.write(new_content)

print("✓ Vue historique_validation corrigée avec succès")
print("\nCHANGEMENTS APPLIQUÉS:")
print("1. Remplacement de 'pharmacien__user=request.user' par 'pharmacien_validateur=request.user'")
print("2. Ajout de la récupération du profil Pharmacien")
print("3. Amélioration de la gestion d'erreurs")
print("\nRedémarrez le serveur pour appliquer les changements.")
