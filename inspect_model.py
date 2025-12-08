#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from communication.models import Message
import inspect

print("🔍 INSPECTION DU MODÈLE MESSAGE")
print("=" * 60)

# 1. Voir les champs
print("Champs du modèle:")
for field in Message._meta.fields:
    print(f"  - {field.name}: {field.__class__.__name__} {'(NOT NULL)' if not field.null else ''}")

# 2. Voir la définition de la classe
print("\nDéfinition de la classe:")
try:
    source = inspect.getsource(Message)
    print(source[:500] + "..." if len(source) > 500 else source)
except:
    print("Impossible d'obtenir le source")

# 3. Voir un exemple de création
print("\nExemple de création:")
print("Message.objects.create(")
for field in Message._meta.fields:
    if field.name == 'id':
        continue
    if not field.null and field.name != 'conversation' and field.name != 'expediteur':
        print(f"    {field.name}=...,  # Requis")
