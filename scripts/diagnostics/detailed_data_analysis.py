#!/usr/bin/env python3
"""
Vérification détaillée des données restantes après suppression
"""

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps
from django.db import connection
from django.contrib.auth import get_user_model

def detailed_data_analysis():
    """Analyse détaillée des données restantes"""
    print("🔍 ANALYSE DÉTAILLÉE DES DONNÉES RESTANTES")
    print("=" * 70)
    
    User = get_user_model()
    
    # 1. Analyse des utilisateurs
    print("\n👥 ANALYSE DES UTILISATEURS:")
    total_users = User.objects.count()
    staff_users = User.objects.filter(is_staff=True).count()
    active_users = User.objects.filter(is_active=True).count()
    
    print(f"   📊 Total: {total_users}")
    print(f"   👨‍💼 Staff: {staff_users}")
    print(f"   ✅ Actifs: {active_users}")
    
    # Derniers utilisateurs créés
    recent_users = User.objects.order_by('-date_joined')[:5]
    print("   🆕 Derniers utilisateurs:")
    for user in recent_users:
        print(f"     - {user.username} ({user.date_joined.date()})")
    
    # 2. Recherche de modèles spécifiques
    print("\n🔎 RECHERCHE DE MODÈLES MÉDICAUX:")
    
    medical_models = []
    for model in apps.get_models():
        model_name = model._meta.model_name.lower()
        if any(term in model_name for term in ['membre', 'medecin', 'patient', 'soin', 'ordonnance', 'paiement']):
            medical_models.append(model)
    
    for model in medical_models:
        count = model.objects.count()
        app_label = model._meta.app_label
        model_name = model._meta.model_name
        
        print(f"   🏥 {app_label}.{model_name}: {count}")
        
        if count > 0 and count <= 10:
            # Afficher les données restantes
            objects = model.objects.all()[:3]
            for obj in objects:
                print(f"     📝 {obj}")
    
    # 3. Vérification des relations brisées
    print("\n🔗 VÉRIFICATION DES RELATIONS:")
    check_broken_relations()
    
    # 4. État de la base de données
    print("\n🗄️  ÉTAT DE LA BASE DE DONNÉES:")
    with connection.cursor() as cursor:
        if 'sqlite' in connection.settings_dict['ENGINE']:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        else:
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        
        tables = [row[0] for row in cursor.fetchall()]
        medical_tables = [t for t in tables if any(term in t.lower() for term in ['membre', 'medecin', 'medical'])]
        
        print(f"   📋 Tables médicales: {len(medical_tables)}")
        for table in medical_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            print(f"     📊 {table}: {count}")

def check_broken_relations():
    """Vérifie les relations brisées"""
    try:
        # Cette vérification dépend de votre structure exacte
        # Adaptez selon vos modèles
        from django.db.models import Q
        
        # Exemple de vérification pour un modèle Membre hypothétique
        try:
            Membre = apps.get_model('membres', 'Membre')
            broken_membres = Membre.objects.filter(
                Q(user__isnull=True) | 
                Q(medecin_traitant__isnull=True)
            )
            if broken_membres.exists():
                print(f"   ⚠️  Membres avec relations brisées: {broken_membres.count()}")
        except LookupError:
            pass
            
    except Exception as e:
        print(f"   ❌ Erreur vérification relations: {e}")

def generate_recovery_sql():
    """Génère des commandes SQL pour l'analyse"""
    print("\n📝 COMMANDES SQL POUR ANALYSE:")
    
    sql_commands = [
        "-- Compter les données par table médicale",
        "SELECT 'membres_membre' as table, COUNT(*) as count FROM membres_membre UNION ALL",
        "SELECT 'medecins_medecin' as table, COUNT(*) as count FROM medecins_medecin UNION ALL", 
        "SELECT 'soins_soin' as table, COUNT(*) as count FROM soins_soin;",
        "",
        "-- Vérifier les dernières modifications",
        "SELECT * FROM django_migrations WHERE app IN ('membres', 'medecins') ORDER BY applied DESC LIMIT 5;"
    ]
    
    for cmd in sql_commands:
        print(f"   {cmd}")

def main():
    print("🩺 ANALYSE DÉTAILLÉE - DONNÉES MÉDICALES")
    print("=" * 70)
    
    detailed_data_analysis()
    generate_recovery_sql()
    
    print("\n🎯 RECOMMANDATIONS:")
    print("1. Vérifiez les sauvegardes automatiques")
    print("2. Consultez les logs Django des dernières 24h")
    print("3. Vérifiez l'historique des commandes manage.py")
    print("4. Contrôlez les migrations récentes")
    print("5. Examinez les éventuels scripts de nettoyage")

if __name__ == "__main__":
    main()