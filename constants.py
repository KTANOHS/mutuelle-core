"""
Constantes pour l'application mutuelle_core
"""

# Statuts des membres
class StatutMembre:
    ACTIF = 'ACTIF'
    INACTIF = 'INACTIF'
    SUSPENDU = 'SUSPENDU'
    CHOICES = [
        (ACTIF, 'Actif'),
        (INACTIF, 'Inactif'),
        (SUSPENDU, 'Suspendu'),
    ]

# Catégories de membres
class CategorieMembre:
    STANDARD = 'STANDARD'
    PREMIUM = 'PREMIUM'
    FAMILLE = 'FAMILLE'
    CHOICES = [
        (STANDARD, 'Standard'),
        (PREMIUM, 'Premium'),
        (FAMILLE, 'Famille'),
    ]

# Configuration de l'application
class Config:
    # Taux de remboursement par défaut
    TAUX_REMBOURSEMENT_DEFAULT = 80
    
    # Durée de validité des bons (en jours)
    DUREE_VALIDITE_BON = 30
    
    # Montant minimum de cotisation
    COTISATION_MINIMUM = 5000
    
    # Devise
    DEVISE = 'FCFA'

# URLs des dashboards
DASHBOARD_URLS = {
    'assureur': '/assureur-dashboard/',
    'medecin': '/medecin-dashboard/',
    'pharmacien': '/pharmacien-dashboard/',
    'membre': '/membre-dashboard/',
    'generic': '/generic-dashboard/',
}