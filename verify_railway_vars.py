import os

print("=== VÉRIFICATION DES VARIABLES RAILWAY ===")
print(f"RAILWAY: {os.getenv('RAILWAY')}")
print(f"CSRF_TRUSTED_ORIGINS: {os.getenv('CSRF_TRUSTED_ORIGINS')}")
print(f"ALLOWED_HOSTS: {os.getenv('ALLOWED_HOSTS')}")

# Vérifier si c'est correct
csrf = os.getenv('CSRF_TRUSTED_ORIGINS', '')
allowed = os.getenv('ALLOWED_HOSTS', '')

issues = []
if '*.web-production-' in csrf:
    issues.append("❌ CSRF_TRUSTED_ORIGINS contient '*.web-production-' (incorrect)")
if '*.railway.app' not in allowed:
    issues.append("❌ ALLOWED_HOSTS ne contient pas '*.railway.app'")

if issues:
    print("\n🚨 PROBLÈMES DÉTECTÉS :")
    for issue in issues:
        print(issue)
    
    print("\n🎯 CORRECTIONS REQUISES :")
    print("1. Allez sur https://railway.app")
    print("2. Projet → marvelous-light → Variables")
    print("3. Supprimez CSRF_TRUSTED_ORIGINS et ALLOWED_HOSTS")
    print("4. Recréez avec ces valeurs :")
    print("   CSRF_TRUSTED_ORIGINS = https://*.railway.app,https://*.up.railway.app,https://web-production-abe5.up.railway.app")
    print("   ALLOWED_HOSTS = *.railway.app,*.up.railway.app,localhost,127.0.0.1,web-production-abe5.up.railway.app")
else:
    print("\n✅ Variables correctement configurées !")