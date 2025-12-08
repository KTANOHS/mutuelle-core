"""
Module de nettoyage
"""
import os
import shutil
from pathlib import Path

class Cleaner:
    """Nettoyeur de projet"""
    
    def __init__(self, project_path):
        self.project_path = Path(project_path)
    
    def clean_pycache(self):
        """Nettoie les dossiers __pycache__"""
        deleted = []
        for root, dirs, files in os.walk(self.project_path):
            if '__pycache__' in root:
                shutil.rmtree(root)
                deleted.append(root)
        return deleted
    
    def clean_backup_files(self, patterns=['.bak', '.backup', '~']):
        """Nettoie les fichiers de backup"""
        deleted = []
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if any(file.endswith(pattern) for pattern in patterns):
                    file_path = Path(root) / file
                    os.remove(file_path)
                    deleted.append(str(file_path))
        return deleted
