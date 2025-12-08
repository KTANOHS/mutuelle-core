# 📋 Checklist de Déploiement

## ✅ Pré-déploiement
- [ ] Tests passent: `python manage.py test`
- [ ] Vérifications: `python manage.py check --deploy`
- [ ] Fichiers statiques collectés
- [ ] Migrations appliquées
- [ ] Backup de la base de données

## 🔧 Configuration Serveur
- [ ] Python 3.11+ installé
- [ ] PostgreSQL installé et configuré
- [ ] Redis installé (optionnel)
- [ ] Nginx installé et configuré
- [ ] Gunicorn installé

## 📁 Structure de Dossiers
- [ ] /var/www/mutuelle/ créé
- [ ] Permissions configurées (www-data:www-data)
- [ ] Logs: /var/www/mutuelle/logs/
- [ ] Static: /var/www/mutuelle/staticfiles/
- [ ] Media: /var/www/mutuelle/media/

## 🔐 Sécurité
- [ ] DEBUG=False
- [ ] SECRET_KEY généré
- [ ] ALLOWED_HOSTS configuré
- [ ] HTTPS configuré (Let's Encrypt)
- [ ] Firewall configuré (UFW)

## 🚀 Déploiement
- [ ] Code déployé (Git clone/pull)
- [ ] Environnement virtuel créé
- [ ] Requirements installés
- [ ] .env configuré
- [ ] Migrations appliquées
- [ ] Superutilisateur créé
- [ ] Services démarrés (Gunicorn, Nginx)

## 📊 Post-déploiement
- [ ] Site accessible via HTTPS
- [ ] Static files servis
- [ ] Media files accessibles
- [ ] Logs monitorés
- [ ] Backup automatique configuré
- [ ] Monitoring (optional)

## �� Dépannage
- [ ] Vérifier logs: `sudo journalctl -u mutuelle`
- [ ] Vérifier Nginx: `sudo nginx -t`
- [ ] Tester connexion DB
- [ ] Tester static files
