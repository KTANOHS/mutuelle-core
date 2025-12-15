#!/bin/bash
# monitor_railway.sh

echo "🚂 SURVEILLANCE DU DÉPLOIEMENT RAILWAY"
echo "======================================"

# Attendez quelques minutes pour le déploiement
echo "⏳ Attente du déploiement Railway (30 secondes)..."
sleep 30

# Générer une URL de test (vous devrez la remplacer par la vraie)
RAILWAY_URL="https://votre-projet.railway.app"

echo -e "\n🌐 Test de l'application déployée..."

# Test 1: Endpoint health
echo "1. Test de l'endpoint /api/health/:"
curl -s --max-time 10 "$RAILWAY_URL/api/health/" || echo "❌ Impossible d'atteindre l'application"

# Test 2: Admin (devrait rediriger)
echo -e "\n2. Test de l'admin:"
curl -I --max-time 10 "$RAILWAY_URL/admin/" 2>/dev/null | head -1 || echo "❌ Erreur"

# Test 3: Logs récents (simulation)
echo -e "\n📋 Derniers messages de log attendus:"
echo "   ✅ Build réussi"
echo "   ✅ Migrations appliquées"
echo "   ✅ Gunicorn démarré"
echo "   ✅ Application Django prête"

echo -e "\n🔧 Si vous voyez des erreurs:"
echo "1. Allez sur https://railway.app"
echo "2. Sélectionnez votre projet"
echo "3. Cliquez sur 'Logs'"
echo "4. Vérifiez les dernières erreurs"

echo -e "\n🎯 URL de votre application: $RAILWAY_URL"