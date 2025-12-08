from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.sessions.models import Session as DefaultSession
from .models import Session, User

# Enregistrer le modèle proxy Session
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'expire_date']
    search_fields = ['session_key']
#     readonly_fields = ['session_key', 'session_data', 'expire_date']  # ⚠️ COMMENTÉ - vérifier les champs
#     list_filter = ['expire_date']
    
    def has_add_permission(self, request):
        return False

# Enregistrer le modèle proxy User
@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    # Utilise la même configuration que UserAdmin par défaut
    pass

# Optionnel: Désenregistrer les modèles originaux si vous voulez n'utiliser que les proxies
# admin.site.unregister(DefaultSession)
# admin.site.unregister(DefaultUser)
