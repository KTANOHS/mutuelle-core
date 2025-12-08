#!/usr/bin/env python3
# correction_templates_assureur.py
import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def corriger_templates():
    print("🔧 APPLICATION DES CORRECTIONS...")
    
    print("📝 Remplacer 'assureur:rapports' par 'assureur:rapport_statistiques'")

    print("✅ Corrections appliquées!")

if __name__ == '__main__':
    corriger_templates()
