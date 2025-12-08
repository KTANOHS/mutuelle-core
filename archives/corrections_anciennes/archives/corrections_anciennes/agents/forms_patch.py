
# PATCH IMMÉDIAT - À ajouter au début de agents/forms.py
from membres.models import Membre

# Redéfinition temporaire pour contourner l'erreur
_original_membre_filter = Membre.objects.filter

def _membre_filter_patch(*args, **kwargs):
    """Patch pour rediriger est_actif vers statut"""
    if 'est_actif' in kwargs:
        est_actif = kwargs.pop('est_actif')
        kwargs['statut'] = 'ACTIF' if est_actif else 'INACTIF'
    return _original_membre_filter(*args, **kwargs)

Membre.objects.filter = _membre_filter_patch
print("🔧 Patch Membre.filter appliqué")
