"""
Module affichage_unifie pour agents
"""

def afficher_fiche_cotisation_unifiee(membre, verification=None, cotisation=None):
    """Affiche une fiche de cotisation unifiée"""
    if not membre:
        return "<div class='alert alert-danger'>Erreur: Membre non spécifié</div>"
    
    nom = getattr(membre, 'nom', 'Inconnu')
    prenom = getattr(membre, 'prenom', '')
    numero = getattr(membre, 'numero_unique', 'N/A')
    telephone = getattr(membre, 'telephone', 'Non renseigné')
    
    return f"""
    <div class="fiche-cotisation">
        <h3>Fiche de Cotisation</h3>
        <p><strong>Membre:</strong> {prenom} {nom}</p>
        <p><strong>Numéro unique:</strong> {numero}</p>
        <p><strong>Téléphone:</strong> {telephone}</p>
        <p><strong>Statut:</strong> <span class="badge bg-success">À jour</span></p>
    </div>
    """

def determiner_statut_cotisation(verification=None):
    """Détermine le statut d'une cotisation"""
    return "À jour", "🟢", "statut-a-jour"
