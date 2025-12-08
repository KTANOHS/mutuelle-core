# correction_ciblee.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def corriger_est_valide_urgence():
    """Correction URGENTE de la propriété est_valide"""
    print("🚨 CORRECTION URGENTE - est_valide retourne None")
    
    file_path = 'medecin/models.py'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Rechercher la propriété est_valide actuelle
        lines = content.split('\n')
        new_lines = []
        in_est_valide = False
        indent_level = 0
        
        for i, line in enumerate(lines):
            if 'def est_valide' in line and '(self):' in line:
                in_est_valide = True
                indent_level = len(line) - len(line.lstrip())
                new_lines.append(line)
                # REMPLACER COMPLÈTEMENT le contenu de la propriété
                new_lines.append(' ' * (indent_level + 4) + '"""Vérifie si l\'ordonnance est encore valide"""')
                new_lines.append(' ' * (indent_level + 4) + 'if not self.date_prescription:')
                new_lines.append(' ' * (indent_level + 8) + 'return False')
                new_lines.append(' ' * (indent_level + 4) + '')
                new_lines.append(' ' * (indent_level + 4) + '# Validité de 3 mois (90 jours)')
                new_lines.append(' ' * (indent_level + 4) + 'from datetime import timedelta')
                new_lines.append(' ' * (indent_level + 4) + 'from django.utils import timezone')
                new_lines.append(' ' * (indent_level + 4) + '')
                new_lines.append(' ' * (indent_level + 4) + 'duree_validite = timedelta(days=90)')
                new_lines.append(' ' * (indent_level + 4) + 'date_expiration = self.date_prescription + duree_validite')
                new_lines.append(' ' * (indent_level + 4) + '')
                new_lines.append(' ' * (indent_level + 4) + '# Retourne True si pas expirée')
                new_lines.append(' ' * (indent_level + 4) + 'return timezone.now().date() <= date_expiration')
                continue
            
            if in_est_valide:
                # Ignorer les anciennes lignes jusqu'à la prochaine méthode
                if line.strip() and len(line) - len(line.lstrip()) <= indent_level and not line.startswith(' ' * (indent_level + 4)):
                    in_est_valide = False
                    new_lines.append(line)
                continue
            else:
                new_lines.append(line)
        
        content = '\n'.join(new_lines)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ est_valide CORRIGÉ URGENCE - Retourne maintenant un booléen")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

def corriger_nom_complet_urgence():
    """Correction URGENTE de nom_complet"""
    print("🚨 CORRECTION URGENTE - nom_complet retourne ' '")
    
    file_path = 'membres/models.py'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        new_lines = []
        in_nom_complet = False
        indent_level = 0
        
        for i, line in enumerate(lines):
            if 'def nom_complet' in line and '(self):' in line:
                in_nom_complet = True
                indent_level = len(line) - len(line.lstrip())
                new_lines.append(line)
                # REMPLACER COMPLÈTEMENT
                new_lines.append(' ' * (indent_level + 4) + '"""Retourne le nom complet du membre"""')
                new_lines.append(' ' * (indent_level + 4) + 'try:')
                new_lines.append(' ' * (indent_level + 8) + 'if self.user.first_name and self.user.last_name:')
                new_lines.append(' ' * (indent_level + 12) + 'return f"{self.user.last_name} {self.user.first_name}"')
                new_lines.append(' ' * (indent_level + 8) + 'elif self.user.get_full_name():')
                new_lines.append(' ' * (indent_level + 12) + 'return self.user.get_full_name()')
                new_lines.append(' ' * (indent_level + 8) + 'else:')
                new_lines.append(' ' * (indent_level + 12) + 'return self.user.username')
                new_lines.append(' ' * (indent_level + 4) + 'except:')
                new_lines.append(' ' * (indent_level + 8) + 'return self.user.username')
                continue
            
            if in_nom_complet:
                if line.strip() and len(line) - len(line.lstrip()) <= indent_level and not line.startswith(' ' * (indent_level + 4)):
                    in_nom_complet = False
                    new_lines.append(line)
                continue
            else:
                new_lines.append(line)
        
        content = '\n'.join(new_lines)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ nom_complet CORRIGÉ URGENCE")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

def corriger_vue_mes_ordonnances_urgence():
    """Correction URGENTE de la vue mes_ordonnances"""
    print("🚨 CORRECTION URGENTE - Vue mes_ordonnances")
    
    vue_code = '''
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from medecin.models import Ordonnance

@login_required
def mes_ordonnances(request):
    """Affiche les ordonnances du membre connecté"""
    # Récupérer TOUTES les ordonnances pour debug
    toutes_ordonnances = Ordonnance.objects.all()
    print(f"DEBUG: {toutes_ordonnances.count()} ordonnances totales dans la base")
    
    for ord in toutes_ordonnances:
        print(f"DEBUG - Ordonnance {ord.id}: patient={ord.patient}, diagnostic={ord.diagnostic}")
    
    # Récupérer les ordonnances du membre connecté
    ordonnances = Ordonnance.objects.filter(patient=request.user)
    print(f"DEBUG: {ordonnances.count()} ordonnances pour l'utilisateur {request.user}")
    
    context = {
        'ordonnances': ordonnances
    }
    return render(request, 'membres/mes_ordonnances.html', context)
'''
    
    file_path = 'membres/views.py'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer toute la fonction
        lines = content.split('\n')
        new_lines = []
        in_function = False
        function_indent = ''
        
        for line in lines:
            if 'def mes_ordonnances' in line and '(request):' in line:
                in_function = True
                function_indent = line.split('def')[0]
                # Ajouter la nouvelle fonction
                for vue_line in vue_code.strip().split('\n'):
                    new_lines.append(vue_line)
                continue
            
            if in_function:
                # Ignorer l'ancien contenu jusqu'à la fin
                if line.strip() and len(line) - len(line.lstrip()) <= len(function_indent) and not line.startswith(function_indent + '    '):
                    in_function = False
                    new_lines.append(line)
                continue
            else:
                new_lines.append(line)
        
        content = '\n'.join(new_lines)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Vue mes_ordonnances CORRIGÉE URGENCE")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

def creer_test_manuel():
    """Créer un script de test manuel"""
    print("🔧 Création d'un test manuel...")
    
    test_code = '''import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_est_valide():
    """Test manuel de est_valide"""
    from medecin.models import Ordonnance
    from django.utils import timezone
    
    print("🧪 TEST MANUEL - est_valide")
    print("=" * 50)
    
    ordonnance = Ordonnance.objects.first()
    if ordonnance:
        print(f"Ordonnance ID: {ordonnance.id}")
        print(f"Date prescription: {ordonnance.date_prescription}")
        print(f"Type date_prescription: {type(ordonnance.date_prescription)}")
        print(f"Est valide: {ordonnance.est_valide}")
        print(f"Type est_valide: {type(ordonnance.est_valide)}")
        print(f"Date maintenant: {timezone.now().date()}")
    else:
        print("❌ Aucune ordonnance trouvée")

def test_nom_complet():
    """Test manuel de nom_complet"""
    from membres.models import Membre
    
    print("\\n🧪 TEST MANUEL - nom_complet")
    print("=" * 50)
    
    membre = Membre.objects.first()
    if membre:
        print(f"Membre ID: {membre.id}")
        print(f"User: {membre.user}")
        print(f"First name: '{membre.user.first_name}'")
        print(f"Last name: '{membre.user.last_name}'")
        print(f"Nom complet: '{membre.nom_complet}'")
    else:
        print("❌ Aucun membre trouvé")

def test_vue_ordonnances():
    """Test manuel de la vue mes_ordonnances"""
    from django.test import RequestFactory
    from membres.views import mes_ordonnances
    from django.contrib.auth.models import User
    
    print("\\n🧪 TEST MANUEL - Vue mes_ordonnances")
    print("=" * 50)
    
    factory = RequestFactory()
    request = factory.get('/membres/mes_ordonnances/')
    
    # Trouver un utilisateur membre
    membre_user = User.objects.filter(groups__name='Membres').first()
    if membre_user:
        request.user = membre_user
        print(f"Utilisateur test: {membre_user}")
        
        response = mes_ordonnances(request)
        print(f"Status code: {response.status_code}")
        
        ordonnances = response.context_data.get('ordonnances', [])
        print(f"Ordonnances dans contexte: {len(ordonnances)}")
        
        for ord in ordonnances:
            print(f"  - Ordonnance {ord.id}: {ord.diagnostic}")
    else:
        print("❌ Aucun utilisateur membre trouvé")

if __name__ == "__main__":
    test_est_valide()
    test_nom_complet() 
    test_vue_ordonnances()
    print("\\n🎉 TESTS MANUELS TERMINÉS")
'''
    
    with open('test_manuel.py', 'w', encoding='utf-8') as f:
        f.write(test_code)
    print("✅ Test manuel créé: test_manuel.py")

def main():
    """Application des corrections URGENTES"""
    print("🚨 CORRECTIONS URGENTES - DÉMARRAGE")
    print("=" * 50)
    
    # 1. Correction CRITIQUE - est_valide
    corriger_est_valide_urgence()
    
    # 2. Correction CRITIQUE - nom_complet
    corriger_nom_complet_urgence()
    
    # 3. Correction CRITIQUE - vue mes_ordonnances
    corriger_vue_mes_ordonnances_urgence()
    
    # 4. Créer un test manuel
    creer_test_manuel()
    
    print("=" * 50)
    print("🎉 CORRECTIONS URGENTES APPLIQUÉES!")
    print("\\n🔍 EXÉCUTEZ MAINTENANT:")
    print("python test_manuel.py")
    print("\\n📋 PUIS TESTEZ AVEC:")
    print("python manage.py test medecin.tests.MedecinTests.test_ordonnance_est_valide --settings=mutuelle_core.settings")

if __name__ == "__main__":
    main()