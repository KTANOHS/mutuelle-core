# debug_middleware.py
import os
import sys
import django

sys.path.append('/Users/koffitanohsoualiho/Documents/projet')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

django.setup()

from mutuelle_core.middlewares import AuthRedirectMiddleware

print("🔍 ANALYSE DU MIDDLEWARE AuthRedirectMiddleware")
print("=" * 50)

# Vérifiez le code source du middleware
try:
    import inspect
    source = inspect.getsource(AuthRedirectMiddleware)
    print("Code du middleware:")
    print("-" * 30)
    print(source)
except Exception as e:
    print(f"❌ Impossible d'analyser le middleware: {e}")