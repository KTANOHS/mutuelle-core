#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

# Configuration Django
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_compatibilite_documents():
    """Vérifie la compatibilité avec le nouveau système de documents"""
    from membres.models import Membre
    
    print("🔍 VÉRIFICATION DE COMPATIBILITÉ DOCUMENTS")
    print("=" * 50)
    
    # Statistiques des documents
    total_membres = Membre.objects.count()
    membres_avec_documents = Membre.objects.exclude(
        piece_identite_recto=''
    ).exclude(
        photo_identite=''
    ).count()
    
    print(f"📊 Statistiques documents:")
    print(f"   Total membres: {total_membres}")
    print(f"   Avec documents: {membres_avec_documents}")
    print(f"   Sans documents: {total_membres - membres_avec_documents}")
    print(f"   Taux complétion: {(membres_avec_documents/total_membres)*100:.1f}%")
    
    # Statut des documents
    from django.db.models import Count
    statuts = Membre.objects.values('statut_documents').annotate(
        count=Count('id')
    ).order_by('statut_documents')
    
    print(f"\n📋 Répartition statuts documents:")
    for statut in statuts:
        print(f"   - {statut['statut_documents']}: {statut['count']} membres")

def generer_plan_migration():
    """Génère un plan de migration pour les documents"""
    print("\n📋 PLAN DE MIGRATION DOCUMENTS")
    print("=" * 50)
    
    plan = [
        "1. Sauvegarde de la base de données",
        "2. Migration des champs documents (première phase - optionnels)",
        "3. Script de population des données existantes",
        "4. Migration des champs documents (deuxième phase - obligatoires)",
        "5. Vérification de l'intégrité des données",
        "6. Tests de régression",
        "7. Déploiement en production"
    ]
    
    for etape in plan:
        print(f"   {etape}")

def verifier_dependances():
    """Vérifie les dépendances entre applications"""
    print("\n🔗 VÉRIFICATION DES DÉPENDANCES")
    print("=" * 50)
    
    apps_dependantes = [
        ('inscription', 'Création de membres'),
        ('paiements', 'Vérification cotisations'),
        ('agents', 'Validation documents et création bons'),
        ('soins', 'Utilisation des membres pour les soins'),
        ('assureur', 'Gestion des assurances')
    ]
    
    for app, description in apps_dependantes:
        try:
            __import__(f"{app}.models")
            print(f"   ✅ {app}: {description}")
        except ImportError:
            print(f"   ❌ {app}: NON TROUVÉE")

if __name__ == "__main__":
    verifier_compatibilite_documents()
    verifier_dependances()
    generer_plan_migration()