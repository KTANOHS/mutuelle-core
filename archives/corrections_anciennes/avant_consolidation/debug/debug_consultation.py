#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.template.loader import get_template
from django.urls import reverse, resolve
from medecin.models import Consultation, Medecin
from membres.models import Membre
from django.contrib.auth.models import User

def debug_consultation_error():
    """
    Script de diagnostic pour l'erreur de création de consultation
    """
    print("=" * 60)
    print("🔍 DIAGNOSTIC ERREUR CREATION CONSULTATION")
    print("=" * 60)
    
    # 1. Vérifier les templates
    print("\n1. ✅ VÉRIFICATION DES TEMPLATES")
    try:
        template = get_template('medecin/creer_consultation.html')
        print("   ✓ Template creer_consultation.html trouvé")
    except Exception as e:
        print(f"   ✗ ERREUR Template: {e}")
    
    try:
        template = get_template('base_medecin.html')
        print("   ✓ Template base_medecin.html trouvé")
    except Exception as e:
        print(f"   ✗ ERREUR Template base: {e}")
    
    # 2. Vérifier les URLs
    print("\n2. ✅ VÉRIFICATION DES URLs")
    try:
        url = reverse('medecin:creer_consultation')
        print(f"   ✓ URL creer_consultation: {url}")
    except Exception as e:
        print(f"   ✗ ERREUR URL: {e}")
    
    # 3. Vérifier les modèles
    print("\n3. ✅ VÉRIFICATION DES MODÈLES")
    try:
        medecin_count = Medecin.objects.count()
        print(f"   ✓ Modèle Medecin: {medecin_count} instances")
    except Exception as e:
        print(f"   ✗ ERREUR Modèle Medecin: {e}")
    
    try:
        patients_count = Membre.objects.filter(statut='ACTIF').count()
        print(f"   ✓ Modèle Membre (patients): {patients_count} actifs")
    except Exception as e:
        print(f"   ✗ ERREUR Modèle Membre: {e}")
    
    try:
        consultations_count = Consultation.objects.count()
        print(f"   ✓ Modèle Consultation: {consultations_count} instances")
        
        # Vérifier la structure du modèle
        consultation_fields = [f.name for f in Consultation._meta.get_fields()]
        print(f"   ✓ Champs Consultation: {', '.join(consultation_fields)}")
    except Exception as e:
        print(f"   ✗ ERREUR Modèle Consultation: {e}")
    
    # 4. Vérifier un utilisateur médecin de test
    print("\n4. ✅ VÉRIFICATION UTILISATEURS MÉDECINS")
    try:
        medecins = Medecin.objects.select_related('user').all()[:5]
        if medecins:
            print("   ✓ Médecins trouvés:")
            for med in medecins:
                print(f"     - {med.user.username} ({med.user.get_full_name()})")
        else:
            print("   ⚠ Aucun médecin trouvé dans la base")
    except Exception as e:
        print(f"   ✗ ERREUR Médecins: {e}")
    
    # 5. Vérifier les permissions
    print("\n5. ✅ VÉRIFICATION DES PERMISSIONS")
    try:
        from django.contrib.auth.models import Group
        medecin_group = Group.objects.filter(name='MEDECIN').first()
        if medecin_group:
            print(f"   ✓ Groupe MEDECIN trouvé: {medecin_group.user_set.count()} utilisateurs")
        else:
            print("   ⚠ Groupe MEDECIN non trouvé")
    except Exception as e:
        print(f"   ✗ ERREUR Permissions: {e}")
    
    # 6. Vérifier la structure de la base de données
    print("\n6. ✅ VÉRIFICATION STRUCTURE BD")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            # Vérifier si la table consultation existe
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='medecin_consultation'")
            table_exists = cursor.fetchone()
            if table_exists:
                print("   ✓ Table medecin_consultation existe")
                
                # Vérifier les colonnes
                cursor.execute("PRAGMA table_info(medecin_consultation)")
                columns = [col[1] for col in cursor.fetchall()]
                print(f"   ✓ Colonnes: {', '.join(columns)}")
            else:
                print("   ✗ Table medecin_consultation n'existe pas")
    except Exception as e:
        print(f"   ✗ ERREUR Structure BD: {e}")
    
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ DU DIAGNOSTIC")
    print("=" * 60)

if __name__ == "__main__":
    debug_consultation_error()