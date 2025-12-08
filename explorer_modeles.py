#!/usr/bin/env python
"""
SCRIPT D'EXPLORATION - Découvrez vos modèles Django
Usage: python explorer_modeles.py
"""

import os
import sys
import django

def setup_django():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.abspath(os.path.join(current_dir, '..'))
        sys.path.append(project_dir)
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        django.setup()
        print("✅ Django configuré avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def explorer_modeles():
    """Explorer tous les modèles disponibles"""
    from django.apps import apps
    
    print("\n" + "="*80)
    print("🔍 EXPLORATION DES MODÈLES DJANGO")
    print("="*80)
    
    # Lister toutes les applications
    print("\n📦 APPLICATIONS INSTALLÉES:")
    for app_config in apps.get_app_configs():
        print(f"   • {app_config.name} ({app_config.verbose_name})")
    
    # Détecter les modèles liés aux membres
    print("\n👥 MODÈLES DE MEMBRES (potentiels):")
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            model_name = model.__name__.lower()
            if any(keyword in model_name for keyword in ['membre', 'user', 'client', 'patient', 'person']):
                count = model.objects.count()
                print(f"   • {model.__name__:25} (app: {app_config.name:15}) : {count:4} enregistrements")
    
    # Détecter les modèles financiers
    print("\n💰 MODÈLES FINANCIERS (potentiels):")
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            model_name = model.__name__.lower()
            if any(keyword in model_name for keyword in ['cotisation', 'paiement', 'payment', 'facture', 'invoice']):
                count = model.objects.count()
                print(f"   • {model.__name__:25} (app: {app_config.name:15}) : {count:4} enregistrements")
    
    # Détecter les modèles médicaux
    print("\n🏥 MODÈLES MÉDICAUX (potentiels):")
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            model_name = model.__name__.lower()
            if any(keyword in model_name for keyword in ['soin', 'medicament', 'ordonnance', 'consultation', 'doctor']):
                count = model.objects.count()
                print(f"   • {model.__name__:25} (app: {app_config.name:15}) : {count:4} enregistrements")
    
    # Afficher tous les modèles avec leurs champs
    print("\n📋 TOUS LES MODÈLES (avec champs):")
    for app_config in apps.get_app_configs():
        if app_config.models:  # Vérifier si l'app a des modèles
            print(f"\n📁 Application: {app_config.name}")
            for model in app_config.get_models():
                count = model.objects.count()
                fields = [f.name for f in model._meta.fields]
                print(f"   ├─ {model.__name__} ({count} enregistrements)")
                print(f"   └─ Champs: {', '.join(fields[:5])}{'...' if len(fields) > 5 else ''}")

def afficher_stats():
    """Afficher les statistiques de base"""
    from django.apps import apps
    
    print("\n" + "="*80)
    print("📊 STATISTIQUES DE BASE")
    print("="*80)
    
    total_enregistrements = 0
    model_stats = []
    
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            count = model.objects.count()
            total_enregistrements += count
            if count > 0:
                model_stats.append({
                    'app': app_config.name,
                    'model': model.__name__,
                    'count': count,
                    'verbose': model._meta.verbose_name_plural
                })
    
    # Trier par nombre d'enregistrements
    model_stats.sort(key=lambda x: x['count'], reverse=True)
    
    print(f"\n📈 TOTAL D'ENREGISTREMENTS: {total_enregistrements:,}")
    print(f"📦 MODÈLES AVEC DONNÉES: {len(model_stats)}")
    
    print(f"\n🏆 TOP 10 DES MODÈLES:")
    for i, stat in enumerate(model_stats[:10], 1):
        print(f"   {i:2}. {stat['verbose']:30} ({stat['model']:20}) : {stat['count']:6,} (app: {stat['app']})")
    
    # Suggestions basées sur les données
    print(f"\n💡 SUGGESTIONS:")
    
    # Chercher un modèle Membre
    for stat in model_stats:
        if 'membre' in stat['model'].lower():
            print(f"   • Modèle Membre trouvé: {stat['model']} ({stat['count']} membres)")
            break
    else:
        print("   • ❌ Aucun modèle Membre trouvé")
    
    # Chercher des modèles financiers
    model_financiers = [s for s in model_stats if any(
        keyword in s['model'].lower() for keyword in 
        ['cotisation', 'paiement', 'payment']
    )]
    
    if model_financiers:
        print(f"   • Modèles financiers trouvés: {len(model_financiers)}")
        for mf in model_financiers[:3]:
            print(f"     - {mf['model']}: {mf['count']} enregistrements")
    else:
        print("   • ❌ Aucun modèle financier trouvé")

def main():
    """Fonction principale"""
    if not setup_django():
        return
    
    explorer_modeles()
    afficher_stats()
    
    print("\n" + "="*80)
    print("✅ EXPLORATION TERMINÉE")
    print("="*80)
    print("\n📝 INSTRUCTIONS:")
    print("1. Identifiez le nom exact de votre modèle Membre")
    print("2. Identifiez le nom exact de votre modèle Cotisation")
    print("3. Identifiez le nom exact de votre modèle Paiement")
    print("4. Utilisez ces noms pour corriger les scripts existants")

if __name__ == "__main__":
    main()