#!/usr/bin/env python3
"""
Vérification de sécurité de l'administration Django
"""

import os
import django
from django.apps import apps
from django.contrib import admin

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'votre_projet.settings')
django.setup()

class AdminSecurityChecker:
    """Vérificateur de sécurité de l'admin"""
    
    def check_security(self):
        """Vérifie les aspects sécurité"""
        print("🔒 VÉRIFICATION DE SÉCURITÉ ADMIN")
        print("=" * 50)
        
        checks = [
            self.check_permission_methods,
            self.check_sensitive_fields,
            self.check_admin_authentication,
            self.check_custom_actions
        ]
        
        for check in checks:
            check()
    
    def check_permission_methods(self):
        """Vérifie les méthodes de permission"""
        print("\n🔐 VÉRIFICATION DES PERMISSIONS")
        print("-" * 30)
        
        for model, model_admin in admin.site._registry.items():
            model_name = f"{model._meta.app_label}.{model.__name__}"
            
            has_custom_permissions = (
                hasattr(model_admin, 'has_add_permission') or
                hasattr(model_admin, 'has_change_permission') or
                hasattr(model_admin, 'has_delete_permission') or
                hasattr(model_admin, 'has_view_permission')
            )
            
            status = "✅" if has_custom_permissions else "⚠️"
            print(f"{status} {model_name}: Permissions personnalisées: {'OUI' if has_custom_permissions else 'NON'}")
    
    def check_sensitive_fields(self):
        """Vérifie les champs sensibles"""
        print("\n🚨 CHAMPS SENSIBLES")
        print("-" * 30)
        
        sensitive_keywords = ['password', 'secret', 'token', 'key', 'auth']
        
        for model in apps.get_models():
            for field in model._meta.fields:
                if any(keyword in field.name.lower() for keyword in sensitive_keywords):
                    print(f"⚠️  {model._meta.app_label}.{model.__name__}.{field.name}: Champ sensible détecté")
    
    def check_admin_authentication(self):
        """Vérifie la configuration d'authentification"""
        print("\n🔑 CONFIGURATION AUTHENTIFICATION")
        print("-" * 30)
        
        from django.conf import settings
        
        # Vérifier les settings de sécurité
        security_settings = [
            ('DEBUG', not settings.DEBUG, "DEBUG devrait être False en production"),
            ('ALLOWED_HOSTS', bool(settings.ALLOWED_HOSTS), "ALLOWED_HOSTS devrait être configuré"),
        ]
        
        for setting, condition, message in security_settings:
            status = "✅" if condition else "❌"
            print(f"{status} {setting}: {message}")

def main():
    """Fonction principale"""
    checker = AdminSecurityChecker()
    checker.check_security()

if __name__ == "__main__":
    main()