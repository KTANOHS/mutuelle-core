# core/constants.py
"""
CONSTANTES METIER POUR MEDISYSTEM
Centralise tous les noms de groupes, permissions et paramètres
Terminologie corrigée : MEMBRES au lieu de ADHERENTS
VERSION COMPLÈTE AVEC GROUPE MEMBRE
"""

# ==============================================================================
# 1. GROUPES UTILISATEURS - VERSION COMPLÈTE
# ==============================================================================
class UserGroups:
    # Groupes principaux
    ASSUREUR = "assureur"  # ✅ Changé en minuscules (standard Django)
    MEDECIN = "medecin"    # ✅ Changé en minuscules
    PHARMACIEN = "pharmacien"  # ✅ Changé en minuscules
    MEMBRE = "membre"      # ✅ AJOUT CRITIQUE - Groupe pour les membres
    ADMIN = "admin"        # ✅ Changé en minuscules
    
    CHOICES = [
        (ASSUREUR, "Assureur"),
        (MEDECIN, "Médecin"),
        (PHARMACIEN, "Pharmacien"),
        (MEMBRE, "Membre"),        # ✅ AJOUT
        (ADMIN, "Administrateur système"),
    ]
    
    # Mapping groupe -> URL de redirection (URLs absolues)
    REDIRECT_MAPPING = {
        ASSUREUR: "/assureur/dashboard/",
        MEDECIN: "/medecin/dashboard/",
        PHARMACIEN: "/pharmacien/dashboard/", 
        MEMBRE: "/membres/dashboard/",        # ✅ AJOUT CRITIQUE
        ADMIN: "/admin/",
    }

# ==============================================================================
# 2. PERMISSIONS METIER (CORRIGÉES - TERMINOLOGIE MEMBRES)
# ==============================================================================
class Permissions:
    """Permissions spécifiques à l'application"""
    
    # Assureurs - Gestion des MEMBRES
    VIEW_MEMBRES = "gestion.view_membre"
    ADD_MEMBRE = "gestion.add_membre"
    CHANGE_MEMBRE = "gestion.change_membre"
    DELETE_MEMBRE = "gestion.delete_membre"
    VALIDATE_BONS = "gestion.validate_bon"
    VIEW_STATISTIQUES = "gestion.view_stats"
    
    # Médecins - Consultations et patients
    CREATE_CONSULTATION = "gestion.add_rendezvous"
    PRESCRIRE_MEDICAMENT = "gestion.add_ordonnance"
    VIEW_DOSSIER_MEDICAL = "gestion.view_dossier"
    VIEW_PATIENTS = "gestion.view_patient"
    
    # Pharmaciens - Ordonnances et médicaments
    DISPENSE_MEDICAMENT = "gestion.dispense_medicament"
    MANAGE_STOCK = "gestion.manage_stock"
    VALIDATE_ORDONNANCE = "gestion.validate_ordonnance"
    VIEW_MEDICAMENTS = "gestion.view_medicament"
    
    # ✅ AJOUT: Permissions spécifiques pour les MEMBRES
    VIEW_OWN_PROFILE = "gestion.view_own_profile"
    EDIT_OWN_PROFILE = "gestion.edit_own_profile"
    VIEW_OWN_FACTURES = "gestion.view_own_factures"
    VIEW_OWN_REMBOURSEMENTS = "gestion.view_own_remboursements"

# ==============================================================================
# 3. PARAMETRES APPLICATION - VERSION CORRIGÉE
# ==============================================================================
class AppConfig:
    """Configuration de l'application"""
    ITEMS_PER_PAGE = 20
    SESSION_TIMEOUT = 3600  # 1 heure
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
    PAGINATION_DEFAULT = 15
    
    # ✅ AJOUT: Configuration spécifique membres
    COTISATION_MENSUELLE = 5000  # 5000 FCFA/mois
    COUVERTURE_MEDICALE = 100    # 100% soins médicaux
    COUVERTURE_CHIRURGIE = 65    # 65% chirurgie
    DELAI_REMBOURSEMENT = 48     # 48h pour remboursement

# ==============================================================================
# 4. MESSAGES ET TEXTES - NOUVEAU
# ==============================================================================
class Messages:
    """Messages système standardisés"""
    LOGIN_SUCCESS = "Connexion réussie. Redirection..."
    LOGIN_ERROR = "Nom d'utilisateur ou mot de passe incorrect"
    PERMISSION_DENIED = "Vous n'avez pas la permission d'accéder à cette page"
    GROUP_REQUIRED = "Cette page est réservée aux {group}"
    
    # Messages spécifiques membres
    MEMBER_WELCOME = "Bienvenue dans votre espace membre"
    COTISATION_INFO = "Cotisation: {price} FCFA/mois - {medical}% soins - {surgery}% chirurgie"

# ==============================================================================
# 5. URLS PRINCIPALES - NOUVEAU
# ==============================================================================
class Urls:
    """URLs principales de l'application"""
    HOME = "/"
    LOGIN = "/accounts/login/"
    LOGOUT = "/accounts/logout/"
    DASHBOARD = "/dashboard/"
    
    # URLs par groupe
    ASSUREUR_DASHBOARD = "/assureur/dashboard/"
    MEDECIN_DASHBOARD = "/medecin/dashboard/"
    PHARMACIEN_DASHBOARD = "/pharmacien/dashboard/"
    MEMBRE_DASHBOARD = "/membres/dashboard/"  # ✅ AJOUT
    ADMIN_DASHBOARD = "/admin/"
    
    # Inscription
    REGISTER = "/register/"
    DEVENIR_MEMBRE = "/devenir-membre/"