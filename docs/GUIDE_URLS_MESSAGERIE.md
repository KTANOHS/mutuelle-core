
📋 GUIDE DES URLs DE MESSAGERIE
================================

🌐 URLs PRINCIPALES:
-------------------
• http://localhost:8000/communication/membre/messagerie/
• http://localhost:8000/communication/assureur/messagerie/  
• http://localhost:8000/communication/medecin/messagerie/
• http://localhost:8000/communication/agent/messagerie/
• http://localhost:8000/communication/test-messagerie/

🔗 NOMS DES URLs (pour reverse()):
---------------------------------
• communication:messagerie_membre
• communication:messagerie_assureur
• communication:messagerie_medecin  
• communication:messagerie_agent
• communication:test_messagerie

🚀 POUR TESTER:
--------------
1. Démarrez le serveur:
   python manage.py runserver

2. Testez les URLs directement:
   http://localhost:8000/communication/test-messagerie/

3. Ou testez chaque interface individuellement

📝 DANS LES TEMPLATES:
---------------------
Utilisez:
{% url 'communication:messagerie_membre' %}
{% url 'communication:messagerie_assureur' %}
etc.

🐛 EN CAS DE PROBLÈME:
---------------------
• Vérifiez que communication/urls.py existe
• Vérifiez l'inclusion dans mutuelle_core/urls.py
• Redémarrez le serveur Django
