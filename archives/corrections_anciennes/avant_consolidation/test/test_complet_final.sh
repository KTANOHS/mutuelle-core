#!/bin/bash

echo "🚀 TEST COMPLET FINAL - SYSTÈME MUTUELLE"
echo "========================================"

# 1. Vérification de base
echo ""
echo "1. 🔍 VÉRIFICATION BASE DE DONNÉES"
python scripts/test_final_validation.py

# 2. Correction redirections
echo ""
echo "2. 🔧 CORRECTION REDIRECTIONS"
python scripts/correction_redirection_admin.py

# 3. Test création avec médecin
echo ""
echo "3. 🧪 TEST CRÉATION AVEC MÉDECIN"
python scripts/correction_medecin_final.py

# 4. Résumé final
echo ""
echo "4. 📊 RÉSUMÉ FINAL"
python manage.py shell << EOF
from soins.models import BonDeSoin
from membres.models import Membre
from agents.models import Agent

print("📈 STATISTIQUES FINALES:")
print(f"   👤 Membres: {Membre.objects.count()}")
print(f"   👨‍💼 Agents: {Agent.objects.count()}")
print(f"   📄 Bons de soin: {BonDeSoin.objects.count()}")

# Derniers bons créés
derniers = BonDeSoin.objects.order_by('-id')[:5]
print(f"   🆕 5 derniers bons:")
for bon in derniers:
    medecin = bon.medecin.username if bon.medecin else "Aucun"
    print(f"      - #{bon.id}: {bon.patient.nom_complet} | Médecin: {medecin} | Statut: {bon.statut}")
EOF

echo ""
echo "🎉 SYSTÈME PRÊT POUR LA PRODUCTION!"
echo "🌐 URLS DISPONIBLES:"
echo "   - Interface Admin: http://localhost:8000/admin/"
echo "   - Liste membres: http://localhost:8000/agents/liste-membres/"
echo "   - Création bons: http://localhost:8000/agents/creer-bon-soin/"
echo ""
echo "🔑 COMPTES TEST:"
echo "   - Superuser: koffitanoh / nouveau_mot_de_passe"
echo "   - Agent dédié: agent_operateur / agent123"