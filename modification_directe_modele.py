# modification_directe_modele.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def modifier_modele_membre_directement():
    """Modifie directement le modèle Membre pour ajouter les champs"""
    print("🔧 Modification directe du modèle Membre...")
    
    modele_path = 'membres/models.py'
    
    try:
        with open(modele_path, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        # Vérifier si les champs existent déjà
        if 'score_risque' in contenu:
            print("✅ Les champs existent déjà dans le modèle")
            return True
        
        # Trouver la classe Membre et ajouter les champs avant la fermeture
        lignes = contenu.split('\n')
        nouvelle_contenu = []
        dans_classe_membre = False
        champs_ajoutes = False
        
        for ligne in lignes:
            nouvelle_contenu.append(ligne)
            
            if 'class Membre' in ligne:
                dans_classe_membre = True
            
            # Ajouter après le dernier champ existant, avant les méthodes
            if dans_classe_membre and ligne.strip().startswith('def ') and not champs_ajoutes:
                # Insérer les nouveaux champs avant la méthode
                nouveaux_champs = '''
    # NOUVEAUX CHAMPS POUR LE SCORING
    score_risque = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=50.00,
        verbose_name="Score de risque"
    )
    niveau_risque = models.CharField(
        max_length=20,
        choices=[
            ('faible', '🟢 Faible risque'),
            ('modere', '🟡 Risque modéré'), 
            ('eleve', '🟠 Risque élevé'),
            ('tres_eleve', '🔴 Risque très élevé'),
        ],
        default='faible'
    )
    fraude_suspectee = models.BooleanField(
        default=False,
        verbose_name="Fraude suspectée par IA"
    )
    date_dernier_score = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Date du dernier calcul de score"
    )
    date_derniere_analyse_ia = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Dernière analyse IA"
    )
'''
                # Retirer la dernière ligne ajoutée (la méthode)
                derniere_ligne = nouvelle_contenu.pop()
                nouvelle_contenu.append(nouveaux_champs)
                nouvelle_contenu.append(derniere_ligne)
                champs_ajoutes = True
                dans_classe_membre = False
        
        # Réécrire le fichier
        with open(modele_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(nouvelle_contenu))
        
        print("✅ Modèle Membre modifié avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur modification modèle: {e}")
        return False

def forcer_migration():
    """Force la création et l'application des migrations"""
    print("\\n🚀 Forçage des migrations...")
    
    from django.core.management import call_command
    try:
        call_command('makemigrations', 'membres')
        call_command('migrate', 'membres')
        print("✅ Migrations forcées avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur migrations: {e}")
        return False

if __name__ == "__main__":
    print("🚀 MODIFICATION DIRECTE DU MODÈLE MEMBRE")
    print("=" * 50)
    
    if modifier_modele_membre_directement():
        if forcer_migration():
            print("\\n🎉 MODIFICATION RÉUSSIE!")
            print("\\n📋 Redémarrez le serveur et testez:")
            print("   python manage.py runserver")
            print("   python test_simplifie.py")