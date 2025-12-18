import os

print("=== Script de correction Railway ===")
print("Problèmes identifiés :")
print("1. CSRF_TRUSTED_ORIGINS contient '*.web-production-' (incorrect)")
print("2. ALLOWED_HOSTS incomplet")

print("\n=== Valeurs CORRECTES à configurer ===")
print("CSRF_TRUSTED_ORIGINS = https://*.railway.app,https://*.up.railway.app,https://web-production-abe5.up.railway.app")
print("ALLOWED_HOSTS = *.railway.app,*.up.railway.app,localhost,127.0.0.1,web-production-abe5.up.railway.app")

print("\n=== Instructions ===")
print("1. Allez sur https://railway.app")
print("2. Projet → marvelous-light → Variables")
print("3. Supprimez CSRF_TRUSTED_ORIGINS et ALLOWED_HOSTS")
print("4. Recréez-les avec les valeurs ci-dessus")