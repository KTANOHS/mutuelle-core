
#!/usr/bin/env python3
"""
AMÉLIORATION DU MODÈLE PIECEJOINTE
Ajoute les champs manquants identifiés par l'analyse
"""

from pathlib import Path

def ameliorer_piece_jointe():
    communication_path = Path('communication')
    models_file = communication_path / 'models.py'
    
    if not models_file.exists():
        print("❌ models.py non trouvé")
        return
    
    with open(models_file, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # Trouver la classe PieceJointe
    if 'class PieceJointe' not in contenu:
        print("❌ Classe PieceJointe non trouvée")
        return
    
    # Nouvelle version améliorée de PieceJointe
    nouvelle_piece_jointe = '''class PieceJointe(models.Model):
    """Modèle pour gérer les pièces jointes des messages"""
    TYPES_FICHIERS = [
        ('PDF', 'Document PDF'),
        ('IMAGE', 'Image'),
        ('DOCUMENT', 'Document Word/Excel'),
        ('AUTRE', 'Autre type'),
    ]
    
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='pieces_jointes')
    fichier = models.FileField(upload_to='pieces_jointes/%Y/%m/%d/')
    nom_original = models.CharField(max_length=255)
    type_fichier = models.CharField(max_length=20, choices=TYPES_FICHIERS, default='AUTRE')
    taille = models.BigIntegerField(default=0, help_text="Taille en octets")
    date_upload = models.DateTimeField(auto_now_add=True)
    est_valide = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Pièce jointe"
        verbose_name_plural = "Pièces jointes"
        ordering = ['-date_upload']
    
    def __str__(self):
        return f"{self.nom_original} ({self.get_taille_lisible()})"
    
    def get_taille_lisible(self):
        """Retourne la taille dans un format lisible"""
        if self.taille < 1024:
            return f"{self.taille} o"
        elif self.taille < 1024 * 1024:
            return f"{self.taille / 1024:.1f} Ko"
        else:
            return f"{self.taille / (1024 * 1024):.1f} Mo"
    
    def save(self, *args, **kwargs):
        """Surcharge pour calculer automatiquement la taille et le type"""
        if self.fichier:
            # Calculer la taille si le fichier est nouveau
            if not self.pk and self.fichier.size:
                self.taille = self.fichier.size
            
            # Déterminer le type de fichier basé sur l'extension
            nom_fichier = self.fichier.name.lower()
            if nom_fichier.endswith(('.pdf',)):
                self.type_fichier = 'PDF'
            elif nom_fichier.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                self.type_fichier = 'IMAGE'
            elif nom_fichier.endswith(('.doc', '.docx', '.xls', '.xlsx')):
                self.type_fichier = 'DOCUMENT'
        
        super().save(*args, **kwargs)
    
    def peut_etre_visualise(self):
        """Vérifie si le fichier peut être visualisé directement"""
        return self.type_fichier in ['PDF', 'IMAGE']'''
    
    # Remplacer l'ancienne classe PieceJointe
    import re
    pattern = r'class PieceJointe\([^)]+\):.*?(?=class|\Z)'
    
    nouvelle_contenu = re.sub(pattern, nouvelle_piece_jointe, contenu, flags=re.DOTALL)
    
    if nouvelle_contenu != contenu:
        # Sauvegarder backup
        backup_file = communication_path / 'models_backup_pieces_jointes.py'
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(contenu)
        
        # Écrire la nouvelle version
        with open(models_file, 'w', encoding='utf-8') as f:
            f.write(nouvelle_contenu)
        
        print("✅ PieceJointe amélioré avec succès!")
        print("📊 Nouvelles fonctionnalités ajoutées:")
        print("   • Gestion des types de fichiers")
        print("   • Calcul automatique de la taille")
        print("   • Méthode de formatage de taille")
        print("   • Validation des types visualisables")
        print(f"   • Backup sauvegardé: {backup_file.name}")
    else:
        print("❌ Aucun changement effectué")

if __name__ == '__main__':
    print("🚀 AMÉLIORATION DU MODÈLE PIECEJOINTE")
    print("=" * 45)
    ameliorer_piece_jointe()


