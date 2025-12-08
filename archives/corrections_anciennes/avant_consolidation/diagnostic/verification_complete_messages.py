# verification_complete_messages.py
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def verifier_tous_les_messages():
    """Vérifie que tous les messages spécifiques sont présents"""
    
    print("=" * 60)
    print("VÉRIFICATION COMPLÈTE DES MESSAGES")
    print("=" * 60)
    
    # Récupérer tous les messages
    url = f"{BASE_URL}/communication/api/public/conversations/5/messages/"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            messages = data.get('messages', [])
            
            print(f"📊 Total de messages dans la réponse: {len(messages)}")
            
            # Liste des messages à vérifier
            messages_a_verifier = [
                {"recherche": "Test diagnostique", "trouve": False, "ids": []},
                {"recherche": "Test API diagnostique", "trouve": False, "ids": []},
                {"recherche": "Test API", "trouve": False, "ids": []},
                {"recherche": "Shell Test", "trouve": False, "ids": []},
                {"recherche": "Test Diagnostic", "trouve": False, "ids": []},
                {"recherche": "CAPTURE", "trouve": False, "ids": []},
                {"recherche": "Message via API", "trouve": False, "ids": []},
            ]
            
            print("\n🔍 Recherche dans tous les messages...")
            
            for msg in messages:
                titre = msg.get('titre', '')
                contenu = msg.get('contenu', '')
                
                for recherche in messages_a_verifier:
                    if (recherche['recherche'] in titre or 
                        recherche['recherche'] in contenu):
                        recherche['trouve'] = True
                        recherche['ids'].append(msg['id'])
            
            # Afficher les résultats
            print("\n" + "=" * 60)
            print("📋 RÉSULTATS DE LA VÉRIFICATION")
            print("=" * 60)
            
            trouves = 0
            for recherche in messages_a_verifier:
                if recherche['trouve']:
                    print(f"✅ '{recherche['recherche']}' - TROUVÉ (IDs: {recherche['ids']})")
                    trouves += 1
                else:
                    print(f"❌ '{recherche['recherche']}' - NON TROUVÉ")
            
            print(f"\n📈 Total trouvé: {trouves}/{len(messages_a_verifier)}")
            
            # Afficher tous les messages avec leurs IDs
            print("\n" + "=" * 60)
            print("📨 LISTE COMPLÈTE DES MESSAGES")
            print("=" * 60)
            
            for msg in messages:
                print(f"ID {msg['id']:2}: {msg['titre']}")
                print(f"    Contenu: {msg['contenu'][:50]}...")
                print(f"    De: {msg['expediteur']['username']} → À: {msg['destinataire']['username']}")
                print()
                
        else:
            print(f"❌ Erreur {response.status_code}: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def exporter_messages_json():
    """Exporte les messages en JSON formaté"""
    
    print("\n" + "=" * 60)
    print("💾 EXPORT DES MESSAGES EN JSON")
    print("=" * 60)
    
    url = f"{BASE_URL}/communication/api/public/conversations/5/messages/"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Sauvegarder dans un fichier
            with open('messages_conversation_5.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print("✅ Fichier sauvegardé: messages_conversation_5.json")
            
            # Afficher un extrait
            print("\n📄 Extrait du JSON:")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
            
        else:
            print(f"❌ Erreur lors de l'export: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def creer_rapport_html():
    """Crée un rapport HTML des messages"""
    
    print("\n" + "=" * 60)
    print("🌐 CRÉATION D'UN RAPPORT HTML")
    print("=" * 60)
    
    url = f"{BASE_URL}/communication/api/public/conversations/5/messages/"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            messages = data.get('messages', [])
            
            # Créer le HTML
            html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport - Conversation 5</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .message {{ border: 1px solid #ddd; margin: 15px 0; padding: 15px; border-radius: 5px; background: #f9f9f9; }}
        .message-header {{ display: flex; justify-content: space-between; background: #e8f4fc; padding: 10px; border-radius: 3px; }}
        .message-id {{ font-weight: bold; color: #2980b9; }}
        .message-titre {{ font-size: 1.2em; color: #2c3e50; }}
        .message-contenu {{ margin: 10px 0; padding: 10px; background: white; border-left: 3px solid #3498db; }}
        .message-metadata {{ display: flex; justify-content: space-between; font-size: 0.9em; color: #7f8c8d; }}
        .statistics {{ background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .success {{ color: #27ae60; }}
        .warning {{ color: #f39c12; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📨 Rapport - Conversation 5</h1>
        
        <div class="statistics">
            <h2>📊 Statistiques</h2>
            <p><strong>Total des messages:</strong> {len(messages)}</p>
            <p><strong>Date de génération:</strong> {data.get('timestamp', 'N/A')}</p>
            <p><strong>ID de la conversation:</strong> {data.get('conversation_id', 'N/A')}</p>
            <p><strong>Statut:</strong> <span class="success">✅ API fonctionnelle</span></p>
        </div>
        
        <h2>📝 Liste des messages</h2>
"""
            
            for msg in messages:
                expediteur = msg.get('expediteur', {}).get('username', 'Inconnu')
                destinataire = msg.get('destinataire', {}).get('username', 'Inconnu')
                date = msg.get('date_envoi', 'N/A')
                est_lu = "✅ Lu" if msg.get('est_lu') else "📨 Non lu"
                
                html += f"""
        <div class="message">
            <div class="message-header">
                <span class="message-id">ID {msg.get('id')}</span>
                <span class="message-titre">{msg.get('titre', 'Sans titre')}</span>
                <span>{est_lu}</span>
            </div>
            <div class="message-contenu">
                {msg.get('contenu', '')}
            </div>
            <div class="message-metadata">
                <span>👤 De: {expediteur}</span>
                <span>👥 À: {destinataire}</span>
                <span>📅 {date}</span>
            </div>
        </div>
"""
            
            html += """
    </div>
</body>
</html>"""
            
            # Sauvegarder le fichier HTML
            with open('rapport_conversation_5.html', 'w', encoding='utf-8') as f:
                f.write(html)
            
            print("✅ Rapport HTML créé: rapport_conversation_5.html")
            print("   Ouvrez ce fichier dans votre navigateur pour voir le rapport.")
            
        else:
            print(f"❌ Erreur lors de la création du rapport: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    """Fonction principale"""
    
    print("🔍 VÉRIFICATION ET EXPORT DES MESSAGES")
    print("=" * 60)
    
    # 1. Vérifier tous les messages
    verifier_tous_les_messages()
    
    # 2. Exporter en JSON
    exporter_messages_json()
    
    # 3. Créer un rapport HTML
    creer_rapport_html()
    
    print("\n" + "=" * 60)
    print("🎯 OPÉRATION TERMINÉE AVEC SUCCÈS !")
    print("=" * 60)
    print("\n📁 FICHIERS CRÉÉS :")
    print("   1. messages_conversation_5.json - Export JSON complet")
    print("   2. rapport_conversation_5.html - Rapport HTML formaté")
    print("\n🌐 URL DE L'API :")
    print("   http://127.0.0.1:8000/communication/api/public/conversations/5/messages/")
    print("\n🔧 COMMANDES DE TEST :")
    print("   curl http://127.0.0.1:8000/communication/api/public/conversations/5/messages/")
    print("   python -m json.tool < messages_conversation_5.json")

if __name__ == "__main__":
    main()