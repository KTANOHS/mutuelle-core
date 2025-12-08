
#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group

print("🔧 CORRECTION DES ASSUREURS (is_staff=False)")
print("=" * 40)

# Récupérer tous les assureurs
assureurs = User.objects.filter(groups__name='Assureur')

print(f"🔍 {assureurs.count()} assureur(s) trouvé(s):")
print("-" * 30)

for assureur in assureurs:
    print(f"\n👤 {assureur.username}:")
    print(f"   AVANT: is_staff={assureur.is_staff}, is_superuser={assureur.is_superuser}")
    
    # Corriger: mettre is_staff = False pour tous les assureurs
    assureur.is_staff = False
    assureur.save()
    
    print(f"   APRÈS: is_staff={assureur.is_staff}")

# Vérifier la configuration
print("\n📋 CONFIGURATION FINALE:")
print("-" * 30)

for assureur in assureurs:
    print(f"• {assureur.username}: staff={assureur.is_staff}, superuser={assureur.is_superuser}")

print("\n✅ Correction appliquée")
print("\n💡 Les assureurs ne seront plus redirigés vers /admin/")


