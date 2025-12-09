
# Mutuelle Core

Application Django de gestion de mutuelle de santé, optimisée pour déploiement sur Render.com.

## Fonctionnalités

- Gestion des membres
- Suivi des cotisations
- Interface médécin/pharmacien
- Système de bons de soins
- Dashboard agent/assureur
- API REST

## Déploiement sur Render.com

1. Cliquez sur "New +" → "Web Service"
2. Connectez votre repository GitHub
3. Render détectera automatiquement :
   - `render.yaml` (configuration)
   - `Procfile` (commande de démarrage)
   - `requirements.txt` (dépendances)

## Variables d'environnement requises

Sur Render, ces variables seront configurées automatiquement :
- `DATABASE_URL` (PostgreSQL fourni par Render)
- `SECRET_KEY` (générée automatiquement)

Variables optionnelles :
- `DJANGO_ENV` = `production` (défaut)
- `DEBUG` = `False` (défaut)

## Accès à l'application

Après déploiement, votre application sera disponible à :
`https://votre-nom-service.onrender.com`

## Développement local

```bash
# Installation
pip install -r requirements.txt

# Migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver