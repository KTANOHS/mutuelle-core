#!/usr/bin/env python3
"""
Script de diagnostic et correction du profil médecin
"""

import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.apps import apps

User = get_user_model()

def diagnose_medecin_issue():
    print("🔍 Diagnostic du problème Profil Médecin")
    print("=" * 50)
    
    # 1. Vérifier si le modèle Médecin existe
    try:
        Medecin = apps.get_model('votre_app', 'Medecin')
        print("✅ Modèle Médecin trouvé")
        
        # Compter les médecins
        medecin_count = Medecin.objects.count()
        print(f"📊 Nombre de médecins en base: {medecin_count}")
        
    except LookupError:
        print("❌ Modèle Médecin non trouvé")
        print("   Vérifiez le nom de l'application dans models.py")
        return False
    
    # 2. Vérifier l'utilisateur connecté
    print("\n👤 Vérification de l'utilisateur:")
    
    # Récupérer le dernier utilisateur avec des privilèges médecin (pour test)
    try:
        # Chercher un utilisateur avec des permissions médecin
        medecin_users = User.objects.filter(
            groups__name__icontains='medecin'
        ) | User.objects.filter(
            user_permissions__codename__icontains='medecin'
        )
        
        if medecin_users.exists():
            print(f"✅ Utilisateurs médecin trouvés: {medecin_users.count()}")
            for user in medecin_users[:3]:  # Afficher les 3 premiers
                print(f"   - {user.username} ({user.get_full_name()})")
        else:
            print("❌ Aucun utilisateur avec rôle médecin trouvé")
            
    except Exception as e:
        print(f"⚠️  Erreur vérification utilisateurs: {e}")
    
    # 3. Vérifier les URLs médecin
    print("\n🌐 Vérification des URLs médecin:")
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        
        medecin_urls = []
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'url_patterns'):
                for subpattern in pattern.url_patterns:
                    if 'medecin' in str(subpattern.pattern):
                        medecin_urls.append(str(subpattern.pattern))
            elif 'medecin' in str(pattern.pattern):
                medecin_urls.append(str(pattern.pattern))
        
        if medecin_urls:
            print("✅ URLs médecin trouvées:")
            for url in medecin_urls[:5]:  # Afficher les 5 premières
                print(f"   - {url}")
        else:
            print("❌ Aucune URL médecin trouvée")
            
    except Exception as e:
        print(f"⚠️  Erreur vérification URLs: {e}")
    
    # 4. Vérifier les vues médecin
    print("\n📋 Vérification des vues médecin:")
    try:
        from django.core.management import call_command
        from io import StringIO
        
        # Capturer la sortie de show_urls
        output = StringIO()
        call_command('show_urls', stdout=output)
        urls_output = output.getvalue()
        
        medecin_views = [line for line in urls_output.split('\n') if 'medecin' in line.lower()]
        
        if medecin_views:
            print("✅ Vues médecin trouvées:")
            for view in medecin_views[:5]:
                print(f"   - {view}")
        else:
            print("❌ Aucune vue médecin trouvée")
            
    except Exception as e:
        print(f"⚠️  Erreur vérification vues: {e}")
    
    return True

def check_medecin_profile_setup():
    """Vérifie la configuration du profil médecin"""
    print("\n🔧 Vérification configuration profil médecin:")
    
    # Vérifier les templates médecin
    template_paths = [
        'templates/medecin/profil_medecin.html',
        'templates/medecin/base_medecin.html',
        'templates/medecin/dashboard.html'
    ]
    
    for template_path in template_paths:
        if os.path.exists(template_path):
            print(f"✅ Template trouvé: {template_path}")
        else:
            print(f"❌ Template manquant: {template_path}")
    
    # Vérifier les URLs
    try:
        from votre_app.urls import urlpatterns
        medecin_urls = [p for p in urlpatterns if 'medecin' in str(p.pattern)]
        print(f"📊 URLs médecin dans urls.py: {len(medecin_urls)}")
        
    except ImportError:
        print("⚠️  Impossible d'importer les URLs")

def quick_fix_suggestions():
    """Suggestions de correction rapide"""
    print("\n💡 SOLUTIONS RAPIDES:")
    print("1. Créer un profil médecin manuellement:")
    print("""
from votre_app.models import Medecin
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(username='votre_medecin')
medecin, created = Medecin.objects.get_or_create(
    user=user,
    defaults={
        'specialite': 'Médecine Générale',
        'numero_ordre': '12345',
        'est_actif': True
    }
)
print(f"Profil médecin {'créé' if created else 'existe déjà'}")
""")
    
    print("\n2. Vérifier les permissions:")
    print("""
from django.contrib.auth.models import Group, Permission

# Créer groupe médecin si nécessaire
group, created = Group.objects.get_or_create(name='Medecin')
if created:
    print("Groupe Medecin créé")
    
# Ajouter l'utilisateur au groupe
user.groups.add(group)
print("Utilisateur ajouté au groupe Medecin")
""")

def main():
    print("🩺 Diagnostic Profil Médecin")
    print("=" * 50)
    
    success = diagnose_medecin_issue()
    check_medecin_profile_setup()
    quick_fix_suggestions()
    
    print("\n🎯 Étapes suivantes:")
    print("1. Vérifiez que l'utilisateur a un profil médecin associé")
    print("2. Vérifiez les permissions et groupes")
    print("3. Testez l'accès au dashboard médecin")
    print("4. Consultez les logs Django pour plus de détails")

if __name__ == "__main__":
    main()