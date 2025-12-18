# test_env_vars.py
import os

print("🔍 VÉRIFICATION DES VARIABLES D'ENVIRONNEMENT")
print("="*60)

critical_vars = ['DEBUG', 'CSRF_TRUSTED_ORIGINS', 'SECRET_KEY']

for var in critical_vars:
    value = os.environ.get(var, 'NON DÉFINIE')
    print(f"{var}: {value}")
    
    if var == 'DEBUG':
        if value == 'NON DÉFINIE':
            print("  ❌ DEBUG n'est pas défini (doit être 'false')")
        elif value.lower() == 'true':
            print("  ⚠️  DEBUG=true (dangereux en production)")
        else:
            print("  ✅ DEBUG est désactivé")
    
    elif var == 'CSRF_TRUSTED_ORIGINS':
        if 'NON DÉFINIE' in value:
            print("  ❌ CSRF_TRUSTED_ORIGINS non défini")
        elif 'web-production-abe5.up.railway.app' in value:
            print("  ✅ Domaine Railway dans la liste")
        else:
            print("  ⚠️  Domaine Railway peut-être manquant")

print("\n" + "="*60)
print("📊 RÉSUMÉ :")
if all('NON DÉFINIE' not in os.environ.get(var, 'NON DÉFINIE') for var in critical_vars):
    print("✅ Toutes les variables critiques sont définies")
else:
    print("🚨 Certaines variables critiques manquent")
    print("   Ajoutez-les via l'interface web Railway")