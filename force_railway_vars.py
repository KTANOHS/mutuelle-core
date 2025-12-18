# force_railway_vars.py
import os

# Variables CRITIQUES pour Railway
RAILWAY_VARS = {
    'DEBUG': 'false',
    'SECRET_KEY': '*ut#lmdlu*r&jr&%*6de=k_e1u9r)@exjifan1y%c9^jyd$br5',
    'CSRF_TRUSTED_ORIGINS': 'https://web-production-abe5.up.railway.app,https://*.railway.app',
    'CSRF_COOKIE_SECURE': 'true',
    'SESSION_COOKIE_SECURE': 'true',
    'SECURE_SSL_REDIRECT': 'true',
}

print("🚨 FORÇAGE DES VARIABLES RAILWAY")
print("="*50)

# Ajouter aux variables d'environnement
for key, value in RAILWAY_VARS.items():
    os.environ[key] = value
    print(f"✅ {key} = {value}")

print("\n" + "="*50)
print("📝 Redéployez maintenant :")
print("railway up")
print("\n🔗 Testez ensuite :")
print("open https://web-production-abe5.up.railway.app/admin/")