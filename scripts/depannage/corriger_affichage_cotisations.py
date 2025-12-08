# corriger_affichage_cotisations.py
import os
import sys
import django
from pathlib import Path
from datetime import datetime, date, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from membres.models import Membre
from agents.models import VerificationCotisation
from django.db.models import Q

print("🔧 CORRECTION AFFICHAGE COTISATIONS")
print("=" * 50)

class CorrecteurAffichage:
    def __init__(self):
        self.rapport = {
            'timestamp': datetime.now().isoformat(),
            'corrections_appliquees': [],
            'membres_verifies': 0
        }
    
    def corriger_incoherences_dates_paiement(self):
        """Corrige les incohérences de dates de paiement"""
        print("\n1. 📅 CORRECTION INCOHÉRENCES DATES PAIEMENT...")
        
        # Vérifications avec date dernier paiement = aujourd'hui mais pas de paiement réel
        verifs_dates_incoherentes = VerificationCotisation.objects.filter(
            date_dernier_paiement=date.today(),
            montant_dernier_paiement=0
        )
        
        corrections = 0
        for verif in verifs_dates_incoherentes:
            # Si montant est 0, c'est qu'il n'y a pas eu de vrai paiement aujourd'hui
            verif.date_dernier_paiement = None
            verif.save()
            
            self.rapport['corrections_appliquees'].append({
                'type': 'DATE_PAIEMENT_INCOHERENTE',
                'verification_id': verif.id,
                'membre': f"{verif.membre.nom_complet}",
                'ancienne_date': date.today(),
                'nouvelle_date': None,
                'description': "Date dernier paiement réinitialisée car montant = 0"
            })
            corrections += 1
            print(f"   ✅ {verif.membre.numero_unique}: Date paiement réinitialisée (montant=0)")
        
        print(f"   📊 {corrections} dates de paiement corrigées")
    
    def mettre_a_jour_statuts_cotisations(self):
        """Met à jour les statuts des cotisations basés sur les données réelles"""
        print("\n2. 🏷️ MISE À JOUR STATUTS COTISATIONS...")
        
        # Récupérer toutes les vérifications
        verifications = VerificationCotisation.objects.all()
        
        for verif in verifications:
            ancien_statut = verif.statut_cotisation
            
            # Déterminer le statut réel
            nouveau_statut = self.determiner_statut_reel(verif)
            
            if ancien_statut != nouveau_statut:
                verif.statut_cotisation = nouveau_statut
                verif.save()
                
                self.rapport['corrections_appliquees'].append({
                    'type': 'MISE_A_JOUR_STATUT',
                    'verification_id': verif.id,
                    'membre': f"{verif.membre.nom_complet}",
                    'ancien_statut': ancien_statut,
                    'nouveau_statut': nouveau_statut,
                    'description': f"Statut mis à jour selon données réelles"
                })
                print(f"   ✅ {verif.membre.numero_unique}: '{ancien_statut}' → '{nouveau_statut}'")
    
    def determiner_statut_reel(self, verification):
        """Détermine le statut réel basé sur tous les critères"""
        aujourdhui = date.today()
        
        # Critère 1: Montant dû
        if verification.montant_dette > 0:
            return "en_retard"
        
        # Critère 2: Échéance dépassée
        if verification.prochaine_echeance and verification.prochaine_echeance < aujourdhui:
            return "en_retard"
        
        # Critère 3: Pas de date de dernier paiement (nouveau membre)
        if not verification.date_dernier_paiement:
            return "a_verifier"
        
        # Tous les critères sont bons
        return "a_jour"
    
    def generer_template_unifie(self):
        """Génère un template unifié pour l'affichage"""
        print("\n3. 📋 GÉNÉRATION TEMPLATE UNIFIÉ...")
        
        template_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Fiche Cotisation - {{ membre.numero_unique }}</title>
    <style>
        .fiche-cotisation {
            border: 2px solid #3498db;
            border-radius: 12px;
            padding: 20px;
            margin: 15px auto;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 450px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .header {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 20px;
        }
        .section {
            margin-bottom: 18px;
            padding-bottom: 15px;
            border-bottom: 1px solid #dee2e6;
        }
        .section-title {
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .info-line {
            margin: 8px 0;
            padding: 5px 0;
            display: flex;
            align-items: center;
        }
        .info-icon {
            margin-right: 10px;
            font-size: 16px;
            width: 20px;
            text-align: center;
        }
        .info-content {
            flex: 1;
        }
        .statut-ajour { 
            color: #27ae60; 
            font-weight: 700;
            background: #d5f4e6;
            padding: 8px 12px;
            border-radius: 6px;
            text-align: center;
        }
        .statut-retard { 
            color: #e74c3c; 
            font-weight: 700;
            background: #fadbd8;
            padding: 8px 12px;
            border-radius: 6px;
            text-align: center;
        }
        .statut-a-verifier { 
            color: #f39c12; 
            font-weight: 700;
            background: #fdebd0;
            padding: 8px 12px;
            border-radius: 6px;
            text-align: center;
        }
        .montant-du {
            color: #e74c3c;
            font-weight: 600;
        }
        .montant-zero {
            color: #27ae60;
            font-weight: 600;
        }
        .footer {
            text-align: center;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #dee2e6;
            font-size: 12px;
            color: #7f8c8d;
        }
        .badge {
            background: #3498db;
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 11px;
            margin-left: 5px;
        }
    </style>
</head>
<body>
    <div class="fiche-cotisation">
        <div class="header">
            <h2 style="margin: 0; font-size: 18px;">📊 FICHE COTISATION</h2>
            <small style="opacity: 0.9;">Système Mutuelle - {{ date_jour }}</small>
        </div>
        
        <!-- Informations Membre -->
        <div class="section">
            <div class="section-title">👤 INFORMATIONS MEMBRE</div>
            <div class="info-line">
                <span class="info-icon">👤</span>
                <div class="info-content">
                    <strong>{{ membre.nom_complet }}</strong>
                    <span class="badge">{{ membre.get_categorie_display }}</span>
                </div>
            </div>
            <div class="info-line">
                <span class="info-icon">#️⃣</span>
                <div class="info-content">
                    <strong>{{ membre.numero_unique }}</strong>
                </div>
            </div>
            <div class="info-line">
                <span class="info-icon">📞</span>
                <div class="info-content">
                    {{ membre.telephone|default:"<em>Non renseigné</em>" }}
                </div>
            </div>
            <div class="info-line">
                <span class="info-icon">📧</span>
                <div class="info-content">
                    {{ membre.email|default:"<em>Non renseigné</em>" }}
                </div>
            </div>
        </div>
        
        <!-- État des Cotisations -->
        <div class="section">
            <div class="section-title">💰 ÉTAT DES COTISATIONS</div>
            <div class="{{ statut_classe }}">
                {{ statut_icone }} {{ statut_message }}
            </div>
        </div>
        
        <!-- Détails Financiers -->
        <div class="section">
            <div class="section-title">💳 DÉTAILS FINANCIERS</div>
            {% if dernier_paiement %}
            <div class="info-line">
                <span class="info-icon">💰</span>
                <div class="info-content">
                    Dernier paiement: <strong>{{ dernier_paiement }}</strong>
                </div>
            </div>
            {% endif %}
            <div class="info-line">
                <span class="info-icon">📅</span>
                <div class="info-content">
                    Prochaine échéance: <strong>{{ prochaine_echeance }}</strong>
                </div>
            </div>
            <div class="info-line">
                <span class="info-icon">💸</span>
                <div class="info-content">
                    Montant dû: 
                    <strong class="{{ montant_classe }}">{{ montant_du }} FCFA</strong>
                </div>
            </div>
            {% if jours_retard > 0 %}
            <div class="info-line">
                <span class="info-icon">⏰</span>
                <div class="info-content">
                    Jours de retard: <strong>{{ jours_retard }} jours</strong>
                </div>
            </div>
            {% endif %}
        </div>
        
        <!-- Cotisation Active -->
        {% if cotisation_active %}
        <div class="section">
            <div class="section-title">📄 COTISATION ACTIVE</div>
            <div class="info-line">
                <span class="info-icon">📋</span>
                <div class="info-content">
                    Référence: <strong>{{ cotisation_active.reference }}</strong>
                </div>
            </div>
            <div class="info-line">
                <span class="info-icon">💵</span>
                <div class="info-content">
                    Montant: <strong>{{ cotisation_active.montant }} FCFA</strong>
                </div>
            </div>
            <div class="info-line">
                <span class="info-icon">📅</span>
                <div class="info-content">
                    Échéance: <strong>{{ cotisation_active.date_echeance }}</strong>
                </div>
            </div>
            <div class="info-line">
                <span class="info-icon">🏷️</span>
                <div class="info-content">
                    Statut: <strong>{{ cotisation_active.get_statut_display }}</strong>
                </div>
            </div>
        </div>
        {% endif %}
        
        <!-- Métadonnées -->
        <div class="footer">
            <div>🔍 Vérification: #{{ verification.id }}</div>
            <div>🕐 Dernière mise à jour: {{ date_maj }}</div>
            <div style="margin-top: 8px; font-size: 10px;">
                Généré automatiquement par le Système Mutuelle
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        with open('template_affichage_unifie.html', 'w', encoding='utf-8') as f:
            f.write(template_html)
        
        print("   ✅ Template HTML unifié généré: template_affichage_unifie.html")
        
        # Template texte pour affichage console/export
        template_texte = """
┌────────────────────────────────────────────────┐
│              FICHE COTISATION                 │
├────────────────────────────────────────────────┤
│ 📊 Système Mutuelle - {date_jour}             │
│                                                │
│ 👤 INFORMATIONS MEMBRE                         │
│    • Nom: {nom_complet}                        │
│    • Numéro: {numero_unique}                   │
│    • Téléphone: {telephone}                    │
│    • Catégorie: {categorie}                    │
│                                                │
│ 💰 ÉTAT DES COTISATIONS                        │
│    {statut_icone} {statut_message}             │
│                                                │
│ 💳 DÉTAILS FINANCIERS                          │
│    • Dernier paiement: {dernier_paiement}      │
│    • Prochaine échéance: {prochaine_echeance}  │
│    • Montant dû: {montant_du} FCFA             │
{jours_retard_ligne}
│                                                │
│ 📄 COTISATION ACTIVE                           │
│    • Référence: {reference_cotisation}         │
│    • Montant: {montant_cotisation} FCFA        │
│    • Échéance: {echeance_cotisation}           │
│    • Statut: {statut_cotisation}               │
│                                                │
│ 🔍 Vérification: #{verification_id}            │
│ 🕐 Dernière mise à jour: {date_maj}            │
└────────────────────────────────────────────────┘
        """
        
        with open('template_affichage_texte.txt', 'w', encoding='utf-8') as f:
            f.write(template_texte)
        
        print("   ✅ Template texte généré: template_affichage_texte.txt")
    
    def creer_fonction_affichage_unifie(self):
        """Crée une fonction Python pour l'affichage unifié"""
        print("\n4. 🐍 CRÉATION FONCTION AFFICHAGE UNIFIÉ...")
        
        fonction_python = """
def afficher_fiche_cotisation_unifiee(membre, verification, cotisation_active=None):
    \"\"\"
    Affiche une fiche de cotisation unifiée et cohérente
    
    Args:
        membre: Instance Membre
        verification: Instance VerificationCotisation
        cotisation_active: Instance Cotisation (optionnelle)
    \"\"\"
    from datetime import date
    
    # Déterminer le statut réel
    statut_reel, icone, classe = determiner_statut_cotisation(verification)
    
    # Formater les dates
    dernier_paiement = verification.date_dernier_paiement.strftime('%d/%m/%Y') if verification.date_dernier_paiement else 'Aucun paiement'
    prochaine_echeance = verification.prochaine_echeance.strftime('%d/%m/%Y') if verification.prochaine_echeance else 'Non définie'
    
    # Déterminer la classe CSS pour le montant dû
    montant_classe = 'montant-zero' if verification.montant_dette == 0 else 'montant-du'
    
    # Préparer la ligne jours de retard
    jours_retard_ligne = ''
    if verification.jours_retard > 0:
        jours_retard_ligne = f\"    • Jours de retard: {verification.jours_retard} jours\\\\n\"
    
    # Template texte unifié
    template = f\"\"\"
┌────────────────────────────────────────────────┐
│              FICHE COTISATION                 │
├────────────────────────────────────────────────┤
│ 📊 Système Mutuelle - {date.today().strftime('%d/%m/%Y')}
│                                                │
│ 👤 INFORMATIONS MEMBRE                         │
│    • Nom: {membre.nom_complet}
│    • Numéro: {membre.numero_unique}
│    • Téléphone: {membre.telephone or 'Non renseigné'}
│    • Catégorie: {membre.get_categorie_display()}
│                                                │
│ 💰 ÉTAT DES COTISATIONS                        │
│    {icone} {statut_reel}
│                                                │
│ 💳 DÉTAILS FINANCIERS                          │
│    • Dernier paiement: {dernier_paiement}
│    • Prochaine échéance: {prochaine_echeance}
│    • Montant dû: {verification.montant_dette} FCFA
{jours_retard_ligne}
\"\"\"
    
    # Ajouter section cotisation active si disponible
    if cotisation_active:
        template += f\"\"\"
│ 📄 COTISATION ACTIVE                           │
│    • Référence: {cotisation_active.reference}
│    • Montant: {cotisation_active.montant} FCFA
│    • Échéance: {cotisation_active.date_echeance.strftime('%d/%m/%Y')}
│    • Statut: {cotisation_active.get_statut_display()}
│                                                │
\"\"\"
    
    # Footer
    template += f\"\"\"
│ 🔍 Vérification: #{verification.id}
│ 🕐 Dernière mise à jour: {verification.date_verification.strftime('%d/%m/%Y %H:%M')}
└────────────────────────────────────────────────┘
\"\"\"
    
    return template

def determiner_statut_cotisation(verification):
    \"\"\"Détermine le statut réel de la cotisation\"\"\"
    from datetime import date
    
    aujourdhui = date.today()
    
    # 1. Vérifier le montant dû
    if verification.montant_dette > 0:
        return \"En retard de paiement\", \"🔴\", \"statut-retard\"
    
    # 2. Vérifier l'échéance dépassée
    if verification.prochaine_echeance and verification.prochaine_echeance < aujourdhui:
        jours_retard = (aujourdhui - verification.prochaine_echeance).days
        return f\"Échéance dépassée (+{jours_retard}j)\", \"🟡\", \"statut-retard\"
    
    # 3. Vérifier si pas de date de paiement (nouveau membre)
    if not verification.date_dernier_paiement:
        return \"À vérifier\", \"🟠\", \"statut-a-verifier\"
    
    # 4. Vérifier échéance proche (7 jours)
    if verification.prochaine_echeance:
        jours_restants = (verification.prochaine_echeance - aujourdhui).days
        if 0 <= jours_restants <= 7:
            return f\"Échéance proche ({jours_restants}j)\", \"🟠\", \"statut-a-verifier\"
    
    # Tout est bon
    return \"À jour des cotisations\", \"✅\", \"statut-ajour\"
"""
        
        with open('affichage_unifie.py', 'w', encoding='utf-8') as f:
            f.write(fonction_python)
        
        print("   ✅ Fonction Python générée: affichage_unifie.py")
    
    def executer_corrections_completes(self):
        """Exécute toutes les corrections"""
        print("🎯 LANCEMENT DES CORRECTIONS COMPLÈTES...")
        
        try:
            self.corriger_incoherences_dates_paiement()
            self.mettre_a_jour_statuts_cotisations()
            self.generer_template_unifie()
            self.creer_fonction_affichage_unifie()
            
            print(f"\n✅ CORRECTIONS TERMINÉES AVEC SUCCÈS")
            print(f"📊 {len(self.rapport['corrections_appliquees'])} corrections appliquées")
            print(f"📁 Fichiers générés:")
            print(f"   • template_affichage_unifie.html")
            print(f"   • template_affichage_texte.txt") 
            print(f"   • affichage_unifie.py")
            
        except Exception as e:
            print(f"❌ Erreur lors des corrections: {str(e)}")

# Exécution
if __name__ == "__main__":
    correcteur = CorrecteurAffichage()
    correcteur.executer_corrections_completes()