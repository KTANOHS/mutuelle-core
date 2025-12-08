from django.db import models
from django.contrib.sessions.models import Session as BaseSession

# Modèle proxy pour Session avec méthode __str__
class Session(BaseSession):
    """Modèle proxy pour Session"""
    
    class Meta:
        proxy = True
        app_label = 'mutuelle_core'
        
    def __str__(self):
        if self.expire_date:
            return f"Session {self.session_key} - {self.expire_date.strftime('%Y-%m-%d %H:%M')}"
        return f"Session {self.session_key}"


from django.contrib.auth.models import User as DefaultUser

# Modèle proxy pour User avec méthode __str__ améliorée
class User(DefaultUser):
    """Modèle proxy pour User"""
    
    class Meta:
        proxy = True
        app_label = 'mutuelle_core'
        
    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} ({self.username})"
        elif self.email:
            return f"{self.username} ({self.email})"
        else:
            return self.username
