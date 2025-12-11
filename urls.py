# Ajoutez cette route à vos urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... vos autres URLs ...
    
    # Diagnostic (protégé)
    path('admin/diagnostic/', views.RenderDiagnosticView.as_view(), name='render_diagnostic'),
    
    # Version publique simplifiée
    path('api/health/', views.health_check, name='health_check'),
]

# Dans views.py, ajoutez:
def health_check(request):
    """Endpoint de santé simple pour Render"""
    import socket
    from django.db import connection
    from django.http import JsonResponse
    
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "mutuelle-core",
        "checks": {
            "database": False,
            "filesystem": False,
            "cache": False,
        }
    }
    
    # Vérifier la base de données
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_data["checks"]["database"] = True
    except:
        health_data["checks"]["database"] = False
        health_data["status"] = "degraded"
    
    # Vérifier le système de fichiers
    try:
        import tempfile
        with tempfile.NamedTemporaryFile(delete=True) as f:
            health_data["checks"]["filesystem"] = True
    except:
        health_data["checks"]["filesystem"] = False
        health_data["status"] = "degraded"
    
    # Si toutes les vérifications échouent
    if not any(health_data["checks"].values()):
        health_data["status"] = "unhealthy"
    
    return JsonResponse(health_data, status=200 if health_data["status"] == "healthy" else 500)