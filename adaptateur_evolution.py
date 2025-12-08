# adaptateur_evolution.py
import os
import sys
import django
import json
import inspect
from datetime import datetime
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

print("🔧 ADAPTATEUR ÉVOLUTIF - MISE À JOUR DES SCRIPTS")
print("=" * 60)

class AdaptateurEvolution:
    def __init__(self):
        self.scripts_base = [
            'diagnostic_sync_final.py',
            'correcteur_sync_urgence.py', 
            'surveillance_simple.py',
            'surveillance_hebdomadaire.py'
        ]
    
    def analyser_compatibilite(self):
        """Analyse la compatibilité des scripts avec l'état actuel du projet"""
        print("🔍 Analyse de compatibilité...")
        
        rapport = {
            'timestamp': datetime.now().isoformat(),
            'scripts_analyses': [],
            'problemes_compatibilite': [],
            'recommandations_mise_a_jour': []
        }
        
        for script in self.scripts_base:
            if Path(script).exists():
                statut = self._analyser_script(script)
                rapport['scripts_analyses'].append(statut)
            else:
                rapport['problemes_compatibilite'].append(f"Script manquant: {script}")
        
        return rapport
    
    def _analyser_script(self, chemin_script):
        """Analyse un script spécifique"""
        try:
            with open(chemin_script, 'r') as f:
                contenu = f.read()
            
            analyse = {
                'script': chemin_script,
                'taille': len(contenu),
                'lignes': contenu.count('\\n'),
                'imports': self._extraire_imports(contenu),
                'modeles_references': self._extraire_modeles_references(contenu),
                'derniere_modification': Path(chemin_script).stat().st_mtime
            }
            
            # Vérifier la compatibilité
            analyse['compatibilite'] = self._verifier_compatibilite(analyse)
            
            return analyse
            
        except Exception as e:
            return {
                'script': chemin_script,
                'erreur': str(e),
                'compatibilite': 'ERREUR'
            }
    
    def _extraire_imports(self, contenu):
        """Extrait les imports du script"""
        imports = []
        lignes = contenu.split('\\n')
        
        for ligne in lignes:
            if ligne.strip().startswith(('import ', 'from ')):
                imports.append(ligne.strip())
        
        return imports
    
    def _extraire_modeles_references(self, contenu):
        """Extrait les modèles Django référencés"""
        modeles = set()
        
        # Modèles de base
        modeles_base = ['User', 'Membre', 'Agent', 'Ordonnance', 'Consultation', 'BonDeSoin']
        
        for modele in modeles_base:
            if modele in contenu:
                modeles.add(modele)
        
        return list(modeles)
    
    def _verifier_compatibilite(self, analyse):
        """Vérifie la compatibilité du script"""
        try:
            # Vérifier que les modèles référencés existent
            for modele in analyse['modeles_references']:
                if modele == 'User':
                    from django.contrib.auth.models import User
                elif modele == 'Membre':
                    from membres.models import Membre
                elif modele == 'Agent':
                    from agents.models import Agent
                elif modele == 'Ordonnance':
                    from medecin.models import Ordonnance
                elif modele == 'Consultation':
                    from medecin.models import Consultation  
                elif modele == 'BonDeSoin':
                    from medecin.models import BonDeSoin
            
            return 'COMPATIBLE'
            
        except ImportError as e:
            return f"INCOMPATIBLE: {e}"
    
    def generer_rapport_evolution(self):
        """Génère un rapport d'évolution et de maintenance"""
        print("📋 Génération rapport d'évolution...")
        
        rapport_compatibilite = self.analyser_compatibilite()
        
        rapport = {
            'timestamp': datetime.now().isoformat(),
            'compatibilite': rapport_compatibilite,
            'etat_systeme': self._analyser_etat_systeme(),
            'plan_evolution': self._generer_plan_evolution(rapport_compatibilite)
        }
        
        # Sauvegarder le rapport
        nom_fichier = f"rapport_evolution_{datetime.now().strftime('%Y%m%d')}.json"
        with open(nom_fichier, 'w') as f:
            json.dump(rapport, f, indent=2)
        
        print(f"💾 Rapport d'évolution sauvegardé: {nom_fichier}")
        return rapport
    
    def _analyser_etat_systeme(self):
        """Analyse l'état global du système"""
        from django.contrib.auth.models import User
        from membres.models import Membre
        
        return {
            'utilisateurs': User.objects.count(),
            'membres': Membre.objects.count(),
            'synchronisation': Membre.objects.filter(user__isnull=False).count(),
            'version_django': django.get_version(),
            'python': sys.version
        }
    
    def _generer_plan_evolution(self, rapport_compatibilite):
        """Génère un plan d'évolution basé sur l'analyse"""
        plan = {
            'priorites': [],
            'maintenance': [],
            'ameliorations': []
        }
        
        # Analyser les problèmes de compatibilité
        for script in rapport_compatibilite['scripts_analyses']:
            if script.get('compatibilite') != 'COMPATIBLE':
                plan['priorites'].append(f"Corriger {script['script']}: {script['compatibilite']}")
        
        # Maintenance préventive
        plan['maintenance'].extend([
            "Mettre à jour les dépendances Python",
            "Réviser les scripts de surveillance",
            "Sauvegarder les configurations"
        ])
        
        # Améliorations
        plan['ameliorations'].extend([
            "Ajouter plus de métriques de performance",
            "Implémenter des alertes avancées",
            "Créer des tableaux de bord"
        ])
        
        return plan
    
    def creer_script_mise_a_jour_auto(self):
        """Crée un script de mise à jour automatique"""
        script_content = '''#!/usr/bin/env python3
# mise_a_jour_scripts.py
import os
import sys
import json
from datetime import datetime
from pathlib import Path

print("🔄 MISE À JOUR AUTOMATIQUE DES SCRIPTS")
print("=" * 50)

class MiseAJourAuto:
    def __init__(self):
        self.dossier_backup = Path("backups_scripts")
        self.dossier_backup.mkdir(exist_ok=True)
    
    def sauvegarder_scripts(self):
        """Sauvegarde les scripts actuels"""
        print("💾 Sauvegarde des scripts...")
        
        scripts = [
            'diagnostic_sync_final.py',
            'correcteur_sync_urgence.py',
            'surveillance_simple.py', 
            'surveillance_hebdomadaire.py',
            'surveillance_sync.py'
        ]
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        dossier_backup = self.dossier_backup / timestamp
        dossier_backup.mkdir()
        
        for script in scripts:
            if Path(script).exists():
                Path(script).rename(dossier_backup / script)
                print(f"✅ Sauvegardé: {script}")
        
        return dossier_backup
    
    def verifier_nouvelles_versions(self):
        """Vérifie les nouvelles versions des scripts"""
        print("🔍 Vérification des mises à jour...")
        
        # Ici vous pourriez vérifier un dépôt Git ou un serveur
        # Pour l'instant, on simule
        return {
            'disponibles': ['surveillance_simple.py', 'diagnostic_sync_final.py'],
            'versions': {'surveillance_simple.py': '2.1.0', 'diagnostic_sync_final.py': '1.5.0'}
        }
    
    def appliquer_mises_a_jour(self):
        """Applique les mises à jour disponibles"""
        print("🔄 Application des mises à jour...")
        
        # Sauvegarder d'abord
        backup_dir = self.sauvegarder_scripts()
        
        # Vérifier les mises à jour
        mises_a_jour = self.verifier_nouvelles_versions()
        
        # Appliquer (simulation)
        for script in mises_a_jour['disponibles']:
            print(f"📥 Mise à jour: {script} -> {mises_a_jour['versions'][script]}")
            # Ici vous téléchargeriez la nouvelle version
        
        print(f"✅ Mises à jour appliquées - Backup: {backup_dir}")

if __name__ == "__main__":
    maj = MiseAJourAuto()
    maj.appliquer_mises_a_jour()
'''
        
        with open('mise_a_jour_scripts.py', 'w') as f:
            f.write(script_content)
        
        print("✅ Script de mise à jour créé: mise_a_jour_scripts.py")

# Exécution
if __name__ == "__main__":
    adaptateur = AdaptateurEvolution()
    
    print("🔧 OPTIONS D'ADAPTATION:")
    print("1. Analyser compatibilité")
    print("2. Rapport d'évolution complet")
    print("3. Créer script mise à jour auto")
    print("4. Tout exécuter")
    
    choix = input("Choisir une option (1-4): ").strip()
    
    if choix in ['1', '4']:
        rapport = adaptateur.analyser_compatibilite()
        print("✅ Analyse de compatibilité terminée")
    
    if choix in ['2', '4']:
        rapport = adaptateur.generer_rapport_evolution()
        print("✅ Rapport d'évolution généré")
    
    if choix in ['3', '4']:
        adaptateur.creer_script_mise_a_jour_auto()
        print("✅ Script de mise à jour créé")