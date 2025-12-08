# test_sans_erreurs.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

# Désactiver temporairement le signal problématique
from django.db.models import signals
from django.contrib.auth.models import User
from assureur.models import creer_profil_assureur
from medecin.models import creer_profil_medecin
from pharmacien.models import creer_profil_pharmacien

# Désactiver les signaux
signals.post_save.disconnect(creer_profil_assureur, sender=User)
signals.post_save.disconnect(creer_profil_medecin, sender=User)
signals.post_save.disconnect(creer_profil_pharmacien, sender=User)

# Maintenant exécutez votre test
from django.test import Client

client = Client()
client.login(username='admin', password='admin123')

# ... le reste de votre test ...