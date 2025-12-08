# PATCH URGENCE - Correction champ est_actif
# Ajoutez ce code au début de agents/views.py

import sys
from membres.models import Membre

# Monkey patch pour intercepter les appels à est_actif
_original_filter = Membre.objects.filter

def _patched_filter(**kwargs):
    if 'est_actif' in kwargs:
        value = kwargs.pop('est_actif')
        kwargs['statut'] = 'ACTIF' if value else 'INACTIF'
    return _original_filter(**kwargs)

Membre.objects.filter = _patched_filter

print("✅ Patch urgence appliqué - est_actif redirigé vers statut")
