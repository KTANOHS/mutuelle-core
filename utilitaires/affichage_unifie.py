# affichage_unifie.py - VERSION CORRIGÉE
import logging
from django.utils import timezone
from datetime import datetime, timedelta

logger = logging.getLogger('affichage_unifie')

def determiner_statut_cotisation(verification):
    """Détermine le statut de cotisation avec gestion robuste des None"""
    try:
        if not verification:
            return "Non vérifié", "⚪", "statut-non-verifie"
        
        # Vérification sécurisée des attributs
        statut = getattr(verification, 'statut_cotisation', 'non_verifie')
        
        if statut == 'a_jour':
            return "À jour", "🟢", "statut-a-jour"
        elif statut == 'en_retard':
            return "En retard", "🔴", "statut-en-retard"
        else:
            return "Non vérifié", "⚪", "statut-non-verifie"
            
    except Exception as e:
        logger.error(f"Erreur détermination statut: {e}")
        return "Erreur", "⚫", "statut-erreur"

def afficher_fiche_cotisation_unifiee(membre, verification, cotisation):
    """Génère une fiche de cotisation unifiée avec gestion robuste des erreurs"""
    try:
        # Gestion des objets None
        if not membre:
            return "❌ Membre non spécifié"
        
        # Récupération des données avec valeurs par défaut
        nom_complet = f"{getattr(membre, 'prenom', '')} {getattr(membre, 'nom', '')}".strip()
        if not nom_complet or nom_complet == " ":
            nom_complet = "Membre non identifié"
            
        numero_unique = getattr(membre, 'numero_unique', 'N/A')
        telephone = getattr(membre, 'telephone', 'Non renseigné')
        
        # Détermination du statut
        libelle_statut, emoji_statut, classe_statut = determiner_statut_cotisation(verification)
        
        # CORRECTION : Gestion sécurisée de montant_dette_str
        montant_dette = "0 FCFA"
        prochaine_echeance = "Non définie"
        dernier_paiement = "Aucun"
        date_verification = "Non vérifié"
        
        if verification:
            # CORRECTION : Vérifier l'existence de l'attribut avant de l'utiliser
            montant_dette = getattr(verification, 'montant_dette_str', '0 FCFA')
            
            if hasattr(verification, 'prochaine_echeance') and verification.prochaine_echeance:
                try:
                    prochaine_echeance = verification.prochaine_echeance.strftime('%d/%m/%Y')
                except (AttributeError, ValueError):
                    prochaine_echeance = "Date invalide"
            
            if hasattr(verification, 'date_dernier_paiement') and verification.date_dernier_paiement:
                try:
                    dernier_paiement = verification.date_dernier_paiement.strftime('%d/%m/%Y')
                except (AttributeError, ValueError):
                    dernier_paiement = "Date invalide"
            
            if hasattr(verification, 'date_verification') and verification.date_verification:
                try:
                    date_verification = verification.date_verification.strftime('%d/%m/%Y')
                except (AttributeError, ValueError):
                    date_verification = "Date invalide"
        
        # Informations de la cotisation actuelle
        cotisation_actuelle = "Aucune"
        if cotisation:
            if hasattr(cotisation, 'date_debut') and cotisation.date_debut:
                try:
                    date_debut = cotisation.date_debut.strftime('%d/%m/%Y')
                    date_fin = getattr(cotisation, 'date_fin', '').strftime('%d/%m/%Y') if getattr(cotisation, 'date_fin', None) else 'Non définie'
                    cotisation_actuelle = f"Du {date_debut} au {date_fin}"
                except (AttributeError, ValueError):
                    cotisation_actuelle = "Période invalide"
        
        # Calcul des jours de retard (simulation)
        jours_retard = 0
        if verification and hasattr(verification, 'jours_retard'):
            jours_retard = getattr(verification, 'jours_retard', 0)
        
        # Génération de la fiche HTML
        fiche_html = f"""
        <div class="fiche-cotisation {classe_statut}">
            <div class="fiche-header">
                <h2>📊 FICHE COTISATION UNIFIÉE</h2>
                <div class="statut-badge {classe_statut}">
                    {emoji_statut} {libelle_statut}
                </div>
            </div>
            
            <div class="fiche-body">
                <div class="section">
                    <h3>👤 INFORMATIONS MEMBRE</h3>
                    <div class="grid-2">
                        <div class="info-item">
                            <label>Nom complet:</label>
                            <span>{nom_complet}</span>
                        </div>
                        <div class="info-item">
                            <label>Numéro unique:</label>
                            <span>{numero_unique}</span>
                        </div>
                        <div class="info-item">
                            <label>Téléphone:</label>
                            <span>{telephone}</span>
                        </div>
                        <div class="info-item">
                            <label>Statut:</label>
                            <span class="statut {classe_statut}">{libelle_statut}</span>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h3>💰 SITUATION FINANCIÈRE</h3>
                    <div class="grid-2">
                        <div class="info-item">
                            <label>Montant dû:</label>
                            <span class="montant-dette">{montant_dette}</span>
                        </div>
                        <div class="info-item">
                            <label>Dernier paiement:</label>
                            <span>{dernier_paiement}</span>
                        </div>
                        <div class="info-item">
                            <label>Prochaine échéance:</label>
                            <span>{prochaine_echeance}</span>
                        </div>
                        <div class="info-item">
                            <label>Jours de retard:</label>
                            <span>{jours_retard} jours</span>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h3>📋 HISTORIQUE RÉCENT</h3>
                    <div class="historique">
                        <div class="historique-item">
                            <span class="date">{timezone.now().strftime('%d/%m/%Y %H:%M')}</span>
                            <span class="action">Fiche générée</span>
                        </div>
                        <div class="historique-item">
                            <span class="date">{date_verification}</span>
                            <span class="action">Dernière vérification</span>
                        </div>
                        <div class="historique-item">
                            <span class="date">Cotisation actuelle</span>
                            <span class="action">{cotisation_actuelle}</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="fiche-footer">
                <div class="timestamp">
                    Généré le {timezone.now().strftime('%d/%m/%Y à %H:%M')}
                </div>
            </div>
        </div>
        
        <style>
        .fiche-cotisation {{
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .fiche-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }}
        .fiche-header h2 {{
            margin: 0;
            color: #2c3e50;
            font-size: 1.5rem;
        }}
        .statut-badge {{
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 14px;
        }}
        .statut-a-jour {{ background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }}
        .statut-en-retard {{ background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }}
        .statut-non-verifie {{ background: #fff3cd; color: #856404; border: 1px solid #ffeaa7; }}
        .statut-erreur {{ background: #f8f9fa; color: #6c757d; border: 1px solid #e9ecef; }}
        .section {{ margin-bottom: 25px; }}
        .section h3 {{
            color: #34495e;
            border-left: 4px solid #3498db;
            padding-left: 10px;
            margin-bottom: 15px;
            font-size: 1.2rem;
        }}
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }}
        .info-item {{
            display: flex;
            flex-direction: column;
            padding: 12px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 3px solid #3498db;
        }}
        .info-item label {{
            font-weight: bold;
            color: #7f8c8d;
            font-size: 12px;
            margin-bottom: 5px;
            text-transform: uppercase;
        }}
        .montant-dette {{
            font-weight: bold;
            color: #e74c3c;
            font-size: 1.1em;
        }}
        .historique-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px;
            border-bottom: 1px solid #ecf0f1;
            background: #fafafa;
            margin-bottom: 5px;
            border-radius: 5px;
        }}
        .historique-item:last-child {{ border-bottom: none; }}
        .historique-item .date {{
            font-weight: bold;
            color: #2c3e50;
        }}
        .historique-item .action {{
            color: #7f8c8d;
        }}
        .fiche-footer {{
            border-top: 1px solid #f0f0f0;
            padding-top: 15px;
            margin-top: 20px;
            text-align: center;
            color: #7f8c8d;
            font-size: 12px;
        }}
        @media (max-width: 768px) {{
            .grid-2 {{ grid-template-columns: 1fr; }}
            .fiche-header {{ flex-direction: column; align-items: flex-start; }}
            .fiche-header h2 {{ margin-bottom: 10px; }}
        }}
        </style>
        """
        
        return fiche_html
        
    except Exception as e:
        logger.error(f"Erreur génération fiche unifiée: {e}")
        return f"""
        <div class="alert alert-danger">
            <h4>❌ Erreur de génération</h4>
            <p>Impossible de générer la fiche de cotisation.</p>
            <small>Erreur: {str(e)}</small>
        </div>
        """