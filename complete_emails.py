#!/usr/bin/env python3
"""
Script final pour compléter les templates d'email
"""

from pathlib import Path

def complete_email_templates():
    email_templates = {
        'emails/remboursement_demande.html': """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Demande de Remboursement</title>
</head>
<body>
    <h2>Demande de Remboursement Reçue</h2>
    <p>Bonjour {{ membre.nom }},</p>
    <p>Votre demande de remboursement pour le soin "{{ soin.libelle }}" a été reçue.</p>
    <p><strong>Montant:</strong> {{ montant }} €</p>
    <p><strong>Statut:</strong> En traitement</p>
    <p>Cordialement,<br>L'équipe Mutuelle</p>
</body>
</html>""",

        'emails/paiement_annule.html': """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Paiement Annulé</title>
</head>
<body>
    <h2>Paiement Annulé</h2>
    <p>Bonjour {{ membre.nom }},</p>
    <p>Votre paiement du {{ date_paiement }} a été annulé.</p>
    <p><strong>Raison:</strong> {{ raison }}</p>
    <p>Pour toute question, contactez notre service client.</p>
    <p>Cordialement,<br>L'équipe Mutuelle</p>
</body>
</html>""",

        'emails/bordereau_paiement.html': """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Bordereau de Paiement</title>
</head>
<body>
    <h2>Bordereau de Paiement</h2>
    <p><strong>Référence:</strong> {{ reference }}</p>
    <p><strong>Date:</strong> {{ date }}</p>
    <p><strong>Montant:</strong> {{ montant }} €</p>
    <p><strong>Bénéficiaire:</strong> {{ beneficiaire }}</p>
    <p><strong>Description:</strong> {{ description }}</p>
    <p>Cordialement,<br>Service Paiements</p>
</body>
</html>""",

        'emails/rappel_paiement.html': """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Rappel de Paiement</title>
</head>
<body>
    <h2>Rappel de Paiement</h2>
    <p>Bonjour {{ membre.nom }},</p>
    <p>Nous vous rappelons que votre paiement de {{ montant }} € est dû depuis le {{ date_echeance }}.</p>
    <p>Merci de régulariser votre situation au plus vite.</p>
    <p>Cordialement,<br>Service Financier</p>
</body>
</html>"""
    }

    templates_dir = Path("templates")
    
    for file_path, content in email_templates.items():
        full_path = templates_dir / file_path
        full_path.write_text(content, encoding='utf-8')
        print(f"✅ Complété: {file_path}")

if __name__ == "__main__":
    print("📧 Complétion des templates d'email...")
    complete_email_templates()
    print("🎉 Tous les templates sont maintenant complets!")