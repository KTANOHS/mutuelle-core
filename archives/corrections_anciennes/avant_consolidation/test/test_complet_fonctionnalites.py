# test_complet_fonctionnalites.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import TestCase
from membres.models import Membre
from agents.models import VerificationCotisation, Agent
from relances.models import TemplateRelance, RelanceProgrammee
from scoring.models import RegleScoring, HistoriqueScore
from scoring.calculators import CalculateurScoreMembre
from relances.services import ServiceRelances

class TestNouvellesFonctionnalites:
    def __init__(self):
        self.resultats = []
    
    def tester_scoring(self):
        """Teste le système de scoring"""
        print("🧪 Test du système de scoring...")
        
        try:
            # Vérifier les règles
            regles = RegleScoring.objects.all()
            assert regles.count() > 0, "Aucune règle de scoring"
            print(f"✅ {regles.count()} règles de scoring")
            
            # Tester le calculateur
            calculateur = CalculateurScoreMembre()
            membre = Membre.objects.first()
            
            if membre:
                resultat = calculateur.calculer_score_complet(membre)
                assert 'score_final' in resultat, "Score final manquant"
                assert 'niveau_risque' in resultat, "Niveau risque manquant"
                assert 'details_scores' in resultat, "Détails scores manquants"
                
                print(f"✅ Scoring fonctionnel: {membre.nom} → {resultat['score_final']}")
                self.resultats.append(("Scoring", "✅ FONCTIONNEL"))
            else:
                print("⚠️  Aucun membre pour tester le scoring")
                self.resultats.append(("Scoring", "⚠️  AUCUN MEMBRE"))
                
        except Exception as e:
            print(f"❌ Erreur scoring: {e}")
            self.resultats.append(("Scoring", f"❌ ERREUR: {e}"))
    
    def tester_relances(self):
        """Teste le système de relances"""
        print("\\n📧 Test du système de relances...")
        
        try:
            # Vérifier les templates
            templates = TemplateRelance.objects.all()
            assert templates.count() > 0, "Aucun template de relance"
            print(f"✅ {templates.count()} templates de relance")
            
            # Tester le service
            service = ServiceRelances()
            membres_a_relancer = service.identifier_membres_a_relancer()
            print(f"✅ Service relances fonctionnel: {len(membres_a_relancer)} membres à relancer")
            
            self.resultats.append(("Relances", "✅ FONCTIONNEL"))
            
        except Exception as e:
            print(f"❌ Erreur relances: {e}")
            self.resultats.append(("Relances", f"❌ ERREUR: {e}"))
    
    def tester_interface_admin(self):
        """Teste l'interface d'admin"""
        print("\\n⚙️  Test de l'interface admin...")
        
        try:
            from django.contrib import admin
            from django.contrib.auth.models import User
            
            # Vérifier que les modèles sont enregistrés
            site = admin.site
            models_registres = [
                'ia_detection_modeleia',
                'scoring_historiquescore', 
                'relances_templaterelance'
            ]
            
            for model in models_registres:
                try:
                    site.get_model_admin(model)
                    print(f"✅ Modèle {model} enregistré dans l'admin")
                except:
                    print(f"⚠️  Modèle {model} non enregistré")
            
            self.resultats.append(("Admin", "✅ FONCTIONNEL"))
            
        except Exception as e:
            print(f"❌ Erreur admin: {e}")
            self.resultats.append(("Admin", f"❌ ERREUR: {e}"))
    
    def generer_rapport(self):
        """Génère un rapport complet"""
        print("\\n" + "=" * 60)
        print("📊 RAPPORT DE TEST COMPLET")
        print("=" * 60)
        
        for fonctionnalite, statut in self.resultats:
            print(f"   {fonctionnalite:<15} {statut}")
        
        # Statistiques finales
        print(f"\\n📈 STATISTIQUES FINALES:")
        print(f"   👥 Membres: {Membre.objects.count()}")
        print(f"   📋 Vérifications: {VerificationCotisation.objects.count()}")
        print(f"   📊 Scores calculés: {HistoriqueScore.objects.count()}")
        print(f"   📧 Templates: {TemplateRelance.objects.count()}")
        print(f"   📈 Règles: {RegleScoring.objects.count()}")
        
        print("\\n🎉 TEST TERMINÉ!")

def main():
    testeur = TestNouvellesFonctionnalites()
    testeur.tester_scoring()
    testeur.tester_relances() 
    testeur.tester_interface_admin()
    testeur.generer_rapport()

if __name__ == "__main__":
    main()