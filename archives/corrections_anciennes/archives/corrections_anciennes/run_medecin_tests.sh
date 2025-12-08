#!/bin/bash
echo "🧪 LANCEMENT DES TESTS MÉDECIN - STRUCTURE EXISTANTE"
echo "======================================================"

echo "1. Application des migrations..."
python manage.py migrate

echo "2. Création des groupes si nécessaire..."
python manage.py create_groups

echo "3. Tests unitaires..."
python manage.py test medecin.tests.test_connexion -v 2

echo "4. Test manuel complet..."
python scripts/test_connexion_medecin_corrige.py

echo "5. Vérification de la structure..."
echo "======================================================"
echo "✅ TOUS LES TESTS ONT ÉTÉ EXÉCUTÉS"