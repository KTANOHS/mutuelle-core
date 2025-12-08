
🎯 GUIDE DE TEST MANUEL - MESSAGERIE AGENT

🚀 DÉMARRAGE:
1. Lancez le serveur: python manage.py runserver
2. Ouvrez: http://localhost:8000/

🔑 CONNEXION AGENT:
1. Connectez-vous avec un compte agent
2. Ou créez un agent de test:
   - Username: agent_test
   - Email: agent@test.com  
   - Password: test123
   - Groupe: Agent

📊 TEST DASHBOARD:
1. Allez sur: http://localhost:8000/agents/dashboard/
2. VÉRIFIEZ:
   ✅ Carte "Messagerie" dans les statistiques
   ✅ Section "Centre de Messagerie" 
   ✅ Boutons "Boîte de réception" et "Nouveau message"
   ✅ Compteur de messages non lus

📁 TEST NAVIGATION:
1. Dans la sidebar, VÉRIFIEZ:
   ✅ Lien "Messagerie" dans le menu
   ✅ Badge avec nombre de messages
   ✅ Accès en un clic

📨 TEST MESSAGERIE:
1. Cliquez sur "Messagerie" dans la sidebar
2. Allez sur: http://localhost:8000/communication/agent/messagerie/
3. VÉRIFIEZ:
   ✅ Interface qui s'affiche sans erreur
   ✅ Liste des messages/conversations
   ✅ Possibilité d'envoyer un message
   ✅ Navigation entre les conversations

🔄 TEST FONCTIONNEL:
1. Envoyez un message test à un autre utilisateur
2. Vérifiez la réception du message
3. Testez la réponse aux messages
4. Vérifiez les notifications

🚨 PROBLÈMES COURANTS À VÉRIFIER:

❌ ERREUR 404:
   - Vérifiez les URLs dans communication/urls.py
   - Vérifiez les vues dans communication/views.py

❌ ERREUR TEMPLATE:
   - Vérifiez {% load static %} dans les templates
   - Vérifiez les balises Django correctes

❌ ACCÈS REFUSÉ:
   - Vérifiez les permissions agent
   - Vérifiez les groupes utilisateur

✅ SIGNES DE SUCCÈS:

• Dashboard affiche la messagerie
• Navigation fonctionnelle  
• Interface messagerie accessible
• Envoi/réception de messages opérationnel
• Aucune erreur dans la console

📞 SUPPORT:
Si problèmes persistants, vérifiez:
1. Fichier communication/urls.py
2. Fichier communication/views.py  
3. Fichier communication/models.py
4. Logs Django dans la console
