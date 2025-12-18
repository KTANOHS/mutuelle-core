import os
print("🔍 VARIABLES D'ENVIRONNEMENT :")
print(f"DEBUG: {os.environ.get('DEBUG', 'NON DÉFINI')}")
print(f"CSRF_TRUSTED_ORIGINS: {os.environ.get('CSRF_TRUSTED_ORIGINS', 'NON DÉFINI')}")
print(f"SECRET_KEY définie: {'OUI' if os.environ.get('SECRET_KEY') else 'NON'}")
