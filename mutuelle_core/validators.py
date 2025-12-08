"""
Validateurs pour l'application mutuelle_core
"""
import re
from django.core.exceptions import ValidationError
from datetime import datetime, date

def validate_phone_number(value):
    """
    Valide un numéro de téléphone
    """
    pattern = r'^\+?[0-9]{10,15}$'
    if not re.match(pattern, value):
        raise ValidationError('Numéro de téléphone invalide')

def validate_date_not_future(value):
    """
    Valide qu'une date n'est pas dans le futur
    """
    if value > date.today():
        raise ValidationError('La date ne peut pas être dans le futur')

def validate_age_minimum(value, min_age=18):
    """
    Valide qu'une date de naissance correspond à un âge minimum
    """
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < min_age:
        raise ValidationError(f'L\'âge minimum requis est {min_age} ans')

def validate_percentage(value):
    """
    Valide qu'une valeur est un pourcentage valide (0-100)
    """
    if value < 0 or value > 100:
        raise ValidationError('Le pourcentage doit être entre 0 et 100')

def validate_positive_number(value):
    """
    Valide qu'un nombre est positif
    """
    if value < 0:
        raise ValidationError('Le montant doit être positif')