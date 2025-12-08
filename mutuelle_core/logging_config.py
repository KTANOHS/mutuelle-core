# mutuelle_core/logging_config.py
import logging
import sys
from datetime import datetime
from django.utils import timezone

class BonLogger:
    """Logger spécialisé pour les opérations sur les bons"""
    
    def __init__(self, name=__name__):
        self.logger = logging.getLogger(name)
    
    def log_creation_success(self, bon_numero, membre_numero, username):
        """Log une création réussie de bon"""
        self.logger.info(
            f"BON_CREATED - Bon: {bon_numero}, "
            f"Membre: {membre_numero}, "
            f"User: {username}, "
            f"Time: {timezone.now().isoformat()}"
        )
    
    def log_creation_failed(self, membre_numero, username, error_msg):
        """Log un échec de création de bon"""
        self.logger.error(
            f"BON_CREATION_FAILED - "
            f"Membre: {membre_numero}, "
            f"User: {username}, "
            f"Error: {error_msg}, "
            f"Time: {timezone.now().isoformat()}"
        )
    
    def log_validation_error(self, membre_numero, username, validation_msg):
        """Log une erreur de validation"""
        self.logger.warning(
            f"BON_VALIDATION_FAILED - "
            f"Membre: {membre_numero}, "
            f"User: {username}, "
            f"Reason: {validation_msg}, "
            f"Time: {timezone.now().isoformat()}"
        )

# Instance globale
bon_logger = BonLogger('assureur.bons')