# gunicorn_config.py
import multiprocessing

# Configuration pour Render
bind = "0.0.0.0:8000"

# 1 worker seulement pour le plan gratuit (Render)
workers = 1

# Threads pour améliorer les performances
threads = 2

# TIMEOUT AUGMENTÉ À 120 SECONDES (ESSENTIEL !)
timeout = 120

# Keep-alive pour les connexions persistantes
keepalive = 2

# Nombre maximum de requêtes avant redémarrage
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Worker class optimisée pour Django
worker_class = "sync"

# Pré-chargement de l'application (accélère le démarrage)
preload_app = True

# Configuration spécifique pour éviter les timeouts
graceful_timeout = 30

# Nombre maximum de clients simultanés
worker_connections = 1000