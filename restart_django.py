#!/usr/bin/env python3
"""
Redémarrage complet du cache Django
"""

import os
import django
from django.core.management import call_command

def restart_django():
    print("🔄 REDÉMARRAGE DU CACHE DJANGO")
    print("=" * 40)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    
    try:
        django.setup()
        
        # Vider le cache des templates
        from django.template import engines
        for engine in engines.all():
            if hasattr(engine, 'engine'):
                if hasattr(engine.engine, 'template_cache'):
                    engine.engine.template_cache.clear()
                    print("✅ Cache des templates vidé")
        
        # Vider le cache général
        from django.core.cache import cache
        cache.clear()
        print("✅ Cache général vidé")
        
        print("🎯 Redémarrage réussi - Le serveur devrait maintenant fonctionner")
        
    except Exception as e:
        print(f"❌ Erreur lors du redémarrage: {e}")

if __name__ == "__main__":
    restart_django()