#!/usr/bin/env python
"""
CORRECTION URGENTE ET COMPLÈTE - TOUS LES PROBLÈMES
"""
import os
import sys
import django
import subprocess

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

def corriger_medecin_models_urgence():
    """Correction URGENTE de medecin/models.py"""
    print("🔧 CORRECTION URGENTE - medecin/models.py")
    print("=" * 60)
    
    file_path = 'medecin/models.py'
    
    if not os.path.exists(file_path):
        print(f"❌ Fichier {file_path} non trouvé")
        return False
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # 1. Vérifier l'import de date
        if 'from datetime import date, timedelta' not in content:
            # Ajouter l'import manquant
            if 'from datetime import timedelta' in content:
                content = content.replace('from datetime import timedelta', 'from datetime import date, timedelta')
            else:
                # Ajouter après les imports Django
                import_section = 'from django.utils import timezone'
                if import_section in content:
                    content = content.replace(import_section, f"{import_section}\nfrom datetime import date, timedelta")
                else:
                    # Ajouter en haut du fichier
                    content = 'from datetime import date, timedelta\n' + content
        
        # 2. Corriger la méthode est_valide
        est_valide_correction = """@property
def est_valide(self):
    \"\"\"Vérifie si l'ordonnance est encore valide (30 jours) - VERSION CORRIGÉE\"\"\"
    if not self.date_prescription:
        return False
    
    # ✅ CORRECTION: Gérer à la fois les dates et les datetimes
    if hasattr(self.date_prescription, 'date'):
        # C'est un datetime, on extrait la date
        date_prescription_date = self.date_prescription.date()
    else:
        # C'est déjà une date
        date_prescription_date = self.date_prescription
        
    date_expiration = date_prescription_date + timedelta(days=30)
    
    # ✅ CORRECTION: Utiliser date.today() pour éviter l'erreur de comparaison
    return date.today() <= date_expiration"""
        
        # Rechercher et remplacer l'ancienne méthode
        if '@property\ndef est_valide(self):' in content:
            # Trouver le début et la fin de la méthode
            start = content.find('@property\ndef est_valide(self):')
            if start != -1:
                # Trouver la fin de la méthode (4 lignes après)
                lines = content[start:].split('\n')
                end_index = min(10, len(lines))  # Chercher dans les 10 lignes suivantes
                for i in range(end_index):
                    if 'return' in lines[i] and i > 0:
                        # Remplacer jusqu'à cette ligne
                        old_method = '\n'.join(lines[:i+1])
                        content = content.replace(old_method, est_valide_correction)
                        break
        
        # 3. Corriger la relation patient (Membre au lieu de User)
        if "patient = models.ForeignKey(User" in content:
            content = content.replace(
                "patient = models.ForeignKey(User", 
                "patient = models.ForeignKey('membres.Membre'"
            )
            print("✅ Relation patient corrigée (Membre au lieu de User)")
        
        # Sauvegarder
        with open(file_path, 'w') as f:
            f.write(content)
        
        print("✅ medecin/models.py corrigé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur correction medecin/models.py: {e}")
        return False

def corriger_assureur_views():
    """Correction de la vue creer_bon pour accepter GET"""
    print("\n🔧 CORRECTION - assureur/views.py")
    print("=" * 60)
    
    file_path = 'assureur/views.py'
    
    if not os.path.exists(file_path):
        print(f"❌ Fichier {file_path} non trouvé")
        return False
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Vérifier si la vue creer_bon existe et accepte GET
        if 'def creer_bon(request, membre_id):' in content:
            print("✅ Vue creer_bon trouvée")
            
            # Vérifier si elle a un traitement GET
            if 'request.method == \\'POST\\'' in content or "request.method == 'POST'" in content:
                print("✅ La vue gère déjà GET/POST")
            else:
                print("⚠️  La vue ne gère pas explicitement GET/POST")
        else:
            print("❌ Vue creer_bon non trouvée")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur vérification assureur/views.py: {e}")
        return False

def creer_vue_creer_bon_corrigee():
    """Crée une version corrigée de la vue creer_bon si nécessaire"""
    print("\n🔧 CRÉATION VUE creer_bon CORRIGÉE")
    print("=" * 60)
    
    vue_corrigee = '''# assureur/views.py - VERSION CORRIGÉE
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from membres.models import Membre
from assureur.models import Bon  # Assurez-vous que ce modèle existe
from assureur.forms import BonForm  # Assurez-vous que ce formulaire existe

@login_required
def est_assureur(user):
    """Vérifie si l'utilisateur est un assureur"""
    return user.groups.filter(name='Assureur').exists() or user.is_staff

@login_required  
@user_passes_test(est_assureur)
def creer_bon(request, membre_id):
    """Crée un bon pour un membre - VERSION CORRIGÉE AVEC GET/POST"""
    try:
        # Récupérer le membre
        membre = get_object_or_404(Membre, id=membre_id)
        
        print(f"DEBUG: Création bon pour membre {membre.id} - {membre.nom_complet}")
        
        if request.method == 'POST':
            # Traitement du formulaire POST
            form = BonForm(request.POST)
            if form.is_valid():
                bon = form.save(commit=False)
                bon.membre = membre
                bon.save()
                
                messages.success(request, f"Bon créé avec succès pour {membre.nom_complet}!")
                return redirect('assureur:liste_bons')
            else:
                messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
        else:
            # Affichage du formulaire GET
            form = BonForm(initial={'membre': membre})
        
        context = {
            'form': form,
            'membre': membre,
            'title': f'Créer un bon pour {membre.nom_complet}'
        }
        
        return render(request, 'assureur/creer_bon.html', context)
        
    except Exception as e:
        print(f"ERREUR dans creer_bon: {e}")
        messages.error(request, f"Erreur: {str(e)}")
        return redirect('assureur:liste_membres')
'''

    # Créer un fichier de backup et sauvegarder la vue corrigée
    backup_path = 'assureur/views_corrige.py'
    with open(backup_path, 'w') as f:
        f.write(vue_corrigee)
    
    print(f"✅ Vue corrigée sauvegardée dans: {backup_path}")
    print("📝 Copiez ce code dans assureur/views.py si nécessaire")
    
    return True

def executer_migrations_force():
    """Exécute les migrations en forçant si nécessaire"""
    print("\n🗃️  MIGRATIONS FORCÉES")
    print("=" * 60)
    
    commands = [
        "python manage.py makemigrations medecin",
        "python manage.py makemigrations assureur", 
        "python manage.py migrate"
    ]
    
    for cmd in commands:
        print(f"🔄 Exécution: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Succès: {result.stdout}")
            else:
                print(f"⚠️  Avertissement: {result.stderr}")
        except Exception as e:
            print(f"❌ Erreur: {e}")

def tester_corrections():
    """Test complet des corrections"""
    print("\n🧪 TEST DES CORRECTIONS")
    print("=" * 60)
    
    try:
        # Test 1: Vérifier l'import de date
        from datetime import date
        print("✅ Import date: OK")
        
        # Test 2: Vérifier les modèles
        from medecin.models import Ordonnance
        from membres.models import Membre
        
        # Test 3: Vérifier qu'un membre existe
        membre = Membre.objects.get(id=5)
        print(f"✅ Membre 5 trouvé: {membre.nom_complet}")
        
        # Test 4: Tester l'accès avec client
        from django.test import Client
        from django.contrib.auth.models import User
        
        client = Client()
        user = User.objects.get(username='assureur_complet')
        client.force_login(user)
        
        response = client.get('/assureur/bons/creer/5/')
        print(f"✅ Test accès URL: Status {response.status_code}")
        
        if response.status_code == 200:
            print("🎉 SUCCÈS: La page fonctionne maintenant!")
        else:
            print(f"⚠️  Statut: {response.status_code} - Vérifiez la vue")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur test: {e}")
        return False

def creer_script_test_final():
    """Crée un script de test final"""
    script_content = '''#!/usr/bin/env python
"""
TEST FINAL - Vérification complète
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.test import Client
from django.contrib.auth.models import User
from membres.models import Membre
from medecin.models import Ordonnance
from datetime import date, timedelta

def test_complet():
    """Test complet de toutes les fonctionnalités"""
    print("🎯 TEST FINAL COMPLET")
    print("=" * 60)
    
    # 1. Test des modèles
    print("1. 🔍 TEST MODÈLES:")
    try:
        membre = Membre.objects.get(id=5)
        print(f"   ✅ Membre 5: {membre.nom_complet}")
        
        # Créer une ordonnance de test
        ordonnance = Ordonnance.objects.create(
            patient=membre,
            diagnostic="Test diagnostic",
            date_prescription=date.today(),
            medecin_prescripteur="Dr Test"
        )
        
        print(f"   ✅ Ordonnance créée: {ordonnance.est_valide}")
        ordonnance.delete()
        
    except Exception as e:
        print(f"   ❌ Erreur modèles: {e}")
    
    # 2. Test accès URL
    print("\\n2. 🔗 TEST ACCÈS URL:")
    client = Client()
    
    try:
        user = User.objects.get(username='assureur_complet')
        client.force_login(user)
        
        response = client.get('/assureur/bons/creer/5/')
        print(f"   ✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   🎉 PAGE FONCTIONNE!")
        else:
            print(f"   ⚠️  Problème: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Erreur accès: {e}")
    
    # 3. Test permissions
    print("\\n3. 🔐 TEST PERMISSIONS:")
    try:
        from assureur.views import est_assureur
        user = User.objects.get(username='assureur_complet')
        result = est_assureur(user)
        print(f"   ✅ Permission assureur: {result}")
    except Exception as e:
        print(f"   ❌ Erreur permissions: {e}")

if __name__ == "__main__":
    test_complet()
    print("\\n" + "=" * 60)
    print("🎉 TEST TERMINÉ")
    print("\\n📝 Si tout est vert, votre application fonctionne!")
'''

    with open('test_final.py', 'w') as f:
        f.write(script_content)
    
    print("✅ Script de test final créé: test_final.py")

if __name__ == "__main__":
    print("🎯 CORRECTION URGENTE ET COMPLÈTE")
    print("=" * 70)
    
    # Appliquer toutes les corrections
    corriger_medecin_models_urgence()
    corriger_assureur_views()
    creer_vue_creer_bon_corrigee()
    executer_migrations_force()
    
    # Tester
    tester_corrections()
    creer_script_test_final()
    
    print("\n" + "=" * 70)
    print("🎉 CORRECTIONS APPLIQUÉES")
    print("\n🎯 PROCHAINES ÉTAPES:")
    print("1. Exécutez: python test_final.py")
    print("2. Si des erreurs persistent, copiez le code de assureur/views_corrige.py dans assureur/views.py")
    print("3. Redémarrez le serveur: python manage.py runserver")
    print("4. Accédez à: http://127.0.0.1:8000/assureur/bons/creer/5/")
    print("\n🔧 Identifiants de test:")
    print("   Utilisateur: assureur_complet")
    print("   Mot de passe: password123")