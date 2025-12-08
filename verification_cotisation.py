#!/usr/bin/env python
"""
Script de vérification du modèle Cotisation
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db import connection
from django.apps import apps

print("🔍 VÉRIFICATION DU MODÈLE COTISATION")
print("=" * 50)

# 1. Vérifier si la table existe
tables = connection.introspection.table_names()
table_name = 'assureur_cotisation'  # Nom typique de la table

if table_name in tables:
    print(f"✅ La table '{table_name}' existe dans la base de données")
    
    # Afficher les colonnes
    with connection.cursor() as cursor:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print(f"📋 Colonnes de la table {table_name}:")
        for col in columns:
            print(f"  - {col[1]}: {col[2]} (Nullable: {col[3]})")
else:
    print(f"❌ La table '{table_name}' n'existe pas dans la base")

# 2. Vérifier si le modèle est chargé
try:
    Cotisation = apps.get_model('assureur', 'Cotisation')
    print(f"✅ Modèle Cotisation chargé avec succès")
    
    # Compter les enregistrements
    count = Cotisation.objects.count()
    print(f"📊 Nombre de cotisations en base : {count}")
    
    # Afficher les premiers enregistrements
    if count > 0:
        print(f"\n📄 Premières cotisations :")
        for cotisation in Cotisation.objects.all()[:5]:
            print(f"  - {cotisation.reference}: {cotisation.montant} FCFA ({cotisation.statut})")
except LookupError:
    print(f"❌ Modèle Cotisation non trouvé dans l'application 'assureur'")
except Exception as e:
    print(f"⚠️ Erreur avec le modèle Cotisation: {e}")

print("\n" + "=" * 50)

# 3. Options pour créer le modèle si nécessaire
print("\n🔧 OPTIONS SI LE MODÈLE N'EXISTE PAS :")
print("1. Créer une migration pour le modèle Cotisation")
print("2. Utiliser une structure simplifiée si non nécessaire")
print("3. Modifier les vues pour gérer l'absence du modèle")