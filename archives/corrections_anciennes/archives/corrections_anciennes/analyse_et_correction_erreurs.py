# analyse_et_correction_erreurs.py
import os
import re
import django
from pathlib import Path
import sys

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Configuration Django chargée")
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

def analyser_modele_soin():
    """Analyse le modèle Soin existant"""
    print("\n🔍 ANALYSE DU MODÈLE SOIN")
    print("=" * 50)
    
    try:
        from soins.models import Soin
        champs = [f.name for f in Soin._meta.get_fields()]
        print(f"✅ Modèle Soin trouvé avec {len(champs)} champs:")
        for champ in champs:
            print(f"   📌 {champ}")
        return champs
    except Exception as e:
        print(f"❌ Erreur analyse modèle Soin: {e}")
        return []

def analyser_formulaire_soin():
    """Analyse le formulaire SoinForm"""
    print("\n🔍 ANALYSE DU FORMULAIRE SOIN")
    print("=" * 50)
    
    try:
        # Lire le fichier forms.py
        with open('soins/forms.py', 'r') as f:
            content = f.read()
        
        # Extraire les champs du formulaire SoinForm
        match = re.search(r'class SoinForm.*?fields\s*=\s*\[(.*?)\]', content, re.DOTALL)
        if match:
            champs_form = [champ.strip().strip("'\"") for champ in match.group(1).split(',')]
            print(f"✅ Formulaire SoinForm trouvé avec {len(champs_form)} champs:")
            for champ in champs_form:
                print(f"   📌 {champ}")
            return champs_form, content
        else:
            print("❌ Impossible de trouver la définition des champs dans SoinForm")
            return [], content
    except Exception as e:
        print(f"❌ Erreur analyse formulaire Soin: {e}")
        return [], ""

def identifier_champs_manquants(champs_modele, champs_formulaire):
    """Identifie les champs du formulaire qui n'existent pas dans le modèle"""
    print("\n🔍 IDENTIFICATION DES CHAMPS MANQUANTS")
    print("=" * 50)
    
    champs_manquants = [champ for champ in champs_formulaire if champ not in champs_modele]
    
    if champs_manquants:
        print(f"❌ {len(champs_manquants)} champs manquants dans le modèle:")
        for champ in champs_manquants:
            print(f"   🚫 {champ}")
    else:
        print("✅ Aucun champ manquant détecté")
    
    return champs_manquants

def corriger_formulaire_soin(champs_manquants, contenu_original):
    """Corrige le formulaire SoinForm en supprimant les champs manquants"""
    print("\n🔧 CORRECTION DU FORMULAIRE SOIN")
    print("=" * 50)
    
    # Extraire la liste des champs actuels
    pattern = r'(fields\s*=\s*\[)(.*?)(\])'
    match = re.search(pattern, contenu_original, re.DOTALL)
    
    if not match:
        print("❌ Impossible de trouver la liste des champs à corriger")
        return False
    
    champs_actuels = match.group(2)
    champs_liste = [champ.strip().strip("'\"") for champ in champs_actuels.split(',') if champ.strip()]
    
    # Filtrer les champs existants
    champs_corriges = [champ for champ in champs_liste if champ not in champs_manquants]
    
    # Reconstruire le contenu
    nouvelle_liste = ",\n        ".join([f"'{champ}'" for champ in champs_corriges])
    nouveau_contenu = re.sub(pattern, f'\\1{nouvelle_liste}\\3', contenu_original, flags=re.DOTALL)
    
    # Sauvegarder la correction
    with open('soins/forms.py', 'w') as f:
        f.write(nouveau_contenu)
    
    print(f"✅ Formulaire corrigé : {len(champs_corriges)} champs conservés")
    print(f"✅ {len(champs_manquants)} champs supprimés: {', '.join(champs_manquants)}")
    
    return True

def completer_modele_soin(champs_manquants):
    """Complète le modèle Soin avec les champs manquants"""
    print("\n🔧 COMPLÉTION DU MODÈLE SOIN")
    print("=" * 50)
    
    try:
        # Lire le modèle actuel
        with open('soins/models.py', 'r') as f:
            contenu_modele = f.read()
        
        # Trouver la classe Soin
        class_match = re.search(r'(class Soin\(.*?\):.*?)(\n\n|\Z)', contenu_modele, re.DOTALL)
        
        if not class_match:
            print("❌ Impossible de trouver la classe Soin dans models.py")
            return False
        
        classe_soin = class_match.group(1)
        
        # Définitions des champs manquants
        definitions_champs = {
            'duree_sejour': "    duree_sejour = models.IntegerField(help_text='Durée en jours', blank=True, null=True)",
            'diagnostic': "    diagnostic = models.TextField(blank=True)",
            'taux_prise_charge': "    taux_prise_charge = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text='Taux de prise en charge en %')",
            'cout_estime': "    cout_estime = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text='Coût estimé avant validation')",
            'observations': "    observations = models.TextField(blank=True, help_text='Observations médicales')"
        }
        
        # Ajouter les champs manquants
        nouvelle_classe = classe_soin
        for champ in champs_manquants:
            if champ in definitions_champs:
                # Trouver où insérer (avant les champs de relation)
                if 'ForeignKey' in classe_soin or 'OneToOneField' in classe_soin or 'ManyToManyField' in classe_soin:
                    # Insérer avant le premier champ de relation
                    pattern = r'(\s+)(valide_par|created_by|ForeignKey|OneToOneField|ManyToManyField)'
                    match_rel = re.search(pattern, nouvelle_classe)
                    if match_rel:
                        nouvelle_classe = nouvelle_classe[:match_rel.start()] + definitions_champs[champ] + '\n' + nouvelle_classe[match_rel.start():]
                    else:
                        # Insérer à la fin de la classe (avant la méthode __str__ ou la fin)
                        if 'def __str__' in nouvelle_classe:
                            nouvelle_classe = nouvelle_classe.replace('def __str__', definitions_champs[champ] + '\n\n    def __str__')
                        else:
                            nouvelle_classe += '\n\n    ' + definitions_champs[champ]
                else:
                    # Insérer avant les méthodes
                    if 'def ' in nouvelle_classe:
                        nouvelle_classe = nouvelle_classe.replace('def ', definitions_champs[champ] + '\n\n    def ')
                    else:
                        nouvelle_classe += '\n\n    ' + definitions_champs[champ]
                
                print(f"✅ Champ ajouté: {champ}")
        
        # Remplacer la classe dans le contenu
        nouveau_contenu = contenu_modele.replace(classe_soin, nouvelle_classe)
        
        # Sauvegarder
        with open('soins/models.py', 'w') as f:
            f.write(nouveau_contenu)
        
        print("✅ Modèle Soin complété avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la complétion du modèle: {e}")
        return False

def creer_migrations():
    """Crée et applique les migrations"""
    print("\n🔄 CRÉATION DES MIGRATIONS")
    print("=" * 50)
    
    try:
        import subprocess
        
        # Créer les migrations
        result = subprocess.run(['python', 'manage.py', 'makemigrations', 'soins'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Migrations créées avec succès")
            print(result.stdout)
        else:
            print("❌ Erreur création migrations:")
            print(result.stderr)
            return False
        
        # Appliquer les migrations
        result = subprocess.run(['python', 'manage.py', 'migrate'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Migrations appliquées avec succès")
            print(result.stdout)
            return True
        else:
            print("❌ Erreur application migrations:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors des migrations: {e}")
        return False

def verifier_correction():
    """Vérifie que la correction a fonctionné"""
    print("\n✅ VÉRIFICATION DE LA CORRECTION")
    print("=" * 50)
    
    try:
        # Réimporter après corrections
        from soins.models import Soin
        from soins.forms import SoinForm
        
        champs_modele = [f.name for f in Soin._meta.get_fields()]
        soin_form = SoinForm()
        
        print("✅ Modèle Soin importé avec succès")
        print("✅ Formulaire SoinForm importé avec succès")
        print(f"✅ Modèle contient maintenant {len(champs_modele)} champs")
        
        # Vérifier que manage.py check fonctionne
        import subprocess
        result = subprocess.run(['python', 'manage.py', 'check'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ System check OK - Aucune erreur détectée")
            return True
        else:
            print("❌ System check échoué:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔧 SCRIPT DE CORRECTION AUTOMATIQUE DES ERREURS")
    print("=" * 60)
    
    # Étape 1: Analyse
    champs_modele = analyser_modele_soin()
    champs_formulaire, contenu_form = analyser_formulaire_soin()
    
    if not champs_modele or not champs_formulaire:
        print("❌ Impossible de procéder à l'analyse")
        return
    
    # Étape 2: Identification des problèmes
    champs_manquants = identifier_champs_manquants(champs_modele, champs_formulaire)
    
    if not champs_manquants:
        print("\n🎉 Aucune correction nécessaire!")
        return
    
    # Étape 3: Correction
    print("\n🎯 STRATÉGIE DE CORRECTION:")
    print("   1. Compléter le modèle Soin avec les champs manquants")
    print("   2. Créer et appliquer les migrations")
    print("   3. Vérifier la correction")
    
    # Demander confirmation
    reponse = input("\n❓ Voulez-vous procéder à la correction? (o/N): ")
    if reponse.lower() not in ['o', 'oui', 'y', 'yes']:
        print("❌ Correction annulée")
        return
    
    # Correction
    if completer_modele_soin(champs_manquants):
        if creer_migrations():
            if verifier_correction():
                print("\n🎉 CORRECTION TERMINÉE AVEC SUCCÈS!")
                print("📱 L'API mobile est maintenant opérationnelle")
            else:
                print("\n⚠️  Correction partielle - Vérification échouée")
        else:
            print("\n❌ Correction échouée - Problème de migrations")
    else:
        print("\n❌ Correction échouée - Impossible de compléter le modèle")

if __name__ == "__main__":
    main()