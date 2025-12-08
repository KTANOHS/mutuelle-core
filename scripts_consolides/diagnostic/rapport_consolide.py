"""
FICHIER CONSOLIDÉ: rapport
Catégorie: diagnostic
Fusion de 4 fichiers
Date de consolidation: 2025-12-06 13:55:44
"""

import sys
import os
from pathlib import Path

# =============================================================================
# FICHIERS D'ORIGINE CONSOLIDÉS
# =============================================================================

# ============================================================
# ORIGINE 1: rapport_diagnostic_assureur.txt (2025-12-05)
# ============================================================

Rapport de diagnostic - 2025-12-05 23:33:19.084043
================================================================================

# ============================================================
# ORIGINE 2: rapport_verifications_20251130_2031.txt (2025-11-30)
# ============================================================

================================================================================
📊 TABLEAU DE BORD COMPLET - VÉRIFICATIONS COTISATIONS
================================================================================
🎯 MÉTRIQUES GLOBALES
────────────────────────────────────────
👥 Membres totaux: 15
✅ Vérifications créées: 15
📋 Vérifications complétées: 15
⏳ Taux complétion: 100.0%

📈 RÉPARTITION DES STATUTS:
  - a_jour: 15 (100.0%)

────────────────────────────────────────────────────────────────────────────────
👨‍💼 PERFORMANCE DES AGENTS
────────────────────────────────────────
Agent        Vérif. Total   Complétées   Taux %   Retard Moy   Dette Total
────────────────────────────────────────────────────────────────────────────────
AG001        7              7            100.0  % 0.0         312.63      €
AG002        2              2            100.0  % 0.0         57.47       €
AG003        6              6            100.0  % 0.0         175.85      €

────────────────────────────────────────────────────────────────────────────────
🚨 ALERTES ET ANOMALIES
────────────────────────────────────────

🔵 INFORMATION:
  • 1 échéances dans les 7 prochains jours

────────────────────────────────────────────────────────────────────────────────
📈 STATISTIQUES AVANCÉES
────────────────────────────────────────
📊 Retard moyen: 0.0 jours
📊 Retard maximum: 0.0 jours

💰 DISTRIBUTION DES DETTES:
  - 0-50€: 9 membres (60.0%)
  - 51-200€: 6 membres (40.0%)
  - 201-500€: 0 membres (0.0%)
  - 500+€: 0 membres (0.0%)

🎯 TAUX DE RÉSOLUTION PAR AGENT:
  - AG001: 100.0% de résolution
  - AG002: 100.0% de résolution
  - AG003: 100.0% de résolution

# ============================================================
# ORIGINE 3: rapport_analyse_projet_resume.txt (2025-11-19)
# ============================================================

================================================================================
RAPPORT D'ANALYSE DU PROJET DJANGO
================================================================================

📋 INFORMATIONS GÉNÉRALES
----------------------------------------
Projet: mutuelle_core
Fichiers Python: 25
Templates: 0
Fichiers statiques: 2
Migrations: 0

📱 APPLICATIONS DJANGO
----------------------------------------
🎯 MODULE AGENTS - ANALYSE DÉTAILLÉE
----------------------------------------
Modèles: 0
Vues: 0
URLs: 0
Templates: 0

📊 COUVERTURE FONCTIONNELLE:

💡 RECOMMANDATIONS
----------------------------------------
• 🔧 Module agents: Implémenter la gestion complète des membres
• 🔧 Module agents: Ajouter le système de communication
• 🔧 Module agents: Développer les fonctionnalités de reporting

================================================================================
Rapport généré le: 2025-11-19T14:42:09.217875
================================================================================

# ============================================================
# ORIGINE 4: rapport_analyse_projet.json (2025-11-19)
# ============================================================

{
  "timestamp": "2025-11-19T14:42:09.217875",
  "project_info": {
    "project_name": "mutuelle_core",
    "total_size": 420586,
    "python_files": 25,
    "template_files": 0,
    "static_files": 2,
    "database_files": 0,
    "migration_files": 0
  },
  "apps_analysis": {},
  "models_analysis": {},
  "views_analysis": {},
  "urls_analysis": {},
  "templates_analysis": {},
  "static_analysis": {},
  "security_analysis": {
    "issues": []
  },
  "performance_analysis": {
    "total_models": 0,
    "total_views": 0,
    "total_templates": 0,
    "large_models": 0,
    "complex_views": 0
  },
  "agents_module_analysis": {
    "error": "Module agents non trouvé"
  },
  "issues": [],
  "recommendations": [
    "🔧 Module agents: Implémenter la gestion complète des membres",
    "🔧 Module agents: Ajouter le système de communication",
    "🔧 Module agents: Développer les fonctionnalités de reporting"
  ]
}

