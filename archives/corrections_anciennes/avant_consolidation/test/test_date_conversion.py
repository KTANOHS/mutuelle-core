# Créez un fichier de test

import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def normaliser_periode(periode_input):
    """Même fonction que ci-dessus"""
    if not periode_input:
        return datetime.now().strftime('%Y-%m')
    
    if '-' in periode_input and len(periode_input) == 7:
        try:
            datetime.strptime(periode_input, '%Y-%m')
            return periode_input
        except:
            pass
    
    if '/' in periode_input:
        try:
            if len(periode_input.split('/')) == 3:
                date_obj = datetime.strptime(periode_input, '%d/%m/%Y')
                return date_obj.strftime('%Y-%m')
            elif len(periode_input.split('/')) == 2:
                date_obj = datetime.strptime(periode_input, '%m/%Y')
                return date_obj.strftime('%Y-%m')
        except:
            pass
    
    if '-' in periode_input and len(periode_input.split('-')) == 2:
        try:
            date_obj = datetime.strptime(periode_input, '%m-%Y')
            return date_obj.strftime('%Y-%m')
        except:
            pass
    
    return datetime.now().strftime('%Y-%m')

# Tests
test_cases = [
    '2025-12',
    '01/12/2025',
    '12/2025',
    '12-2025',
    'invalid',
    '',
    '2025/12',
    '25-12',
]

print("=== TESTS DE CONVERSION DE PÉRIODE ===")
for test in test_cases:
    result = normaliser_periode(test)
    print(f"'{test}' -> '{result}'")


