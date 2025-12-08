# diagnostic_final_conversations.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostic_complet():
    print("🔍 DIAGNOSTIC FINAL DES CONVERSATIONS")
    print("=" * 60)
    
    from django.test import Client
    from django.contrib.auth.models import User
    from communication.models import Conversation
    
    try:
        # Se connecter
        pharmacien = User.objects.get(username='test_pharmacien')
        client = Client()
        client.force_login(pharmacien)
        
        # Faire une requête
        response = client.get('/communication/')
        content = response.content.decode('utf-8')
        
        print(f"📊 Statut: {response.status_code}")
        
        # Analyser le contenu HTML pour comprendre ce qui s'affiche
        print("\n📄 ANALYSE DU CONTENU HTML:")
        
        # Chercher où apparaissent test_agent et test_medecin
        for nom in ['test_agent', 'test_medecin']:
            index = content.find(nom)
            if index != -1:
                # Extraire le contexte autour du nom
                debut = max(0, index - 200)
                fin = min(len(content), index + 200)
                contexte = content[debut:fin]
                print(f"\n🔍 Contexte autour de '{nom}':")
                print("..." + contexte + "...")
        
        # Vérifier la présence de balises spécifiques
        balises_importantes = {
            'conversation-item': 'conversation-item' in content,
            'alert alert-success': 'alert alert-success' in content,
            'flex-grow-1': 'flex-grow-1' in content,
            'badge bg-secondary': 'badge bg-secondary' in content,
            'btn btn-primary': 'btn btn-primary' in content
        }
        
        print(f"\n🎯 BALISES HTML TROUVÉES:")
        for balise, presente in balises_importantes.items():
            status = "✅" if presente else "❌"
            print(f"   {status} {balise}: {'PRÉSENTE' if presente else 'ABSENTE'}")
        
        # Vérifier si les données sont dans le contexte mais mal affichées
        print(f"\n🧪 TEST DES DONNÉES DIRECTES:")
        conversations = Conversation.objects.filter(participants=pharmacien)
        print(f"   - Conversations en base: {conversations.count()}")
        
        for conv in conversations:
            participants = list(conv.participants.all())
            autres = [p for p in participants if p != pharmacien]
            print(f"   - Conversation {conv.id}: {len(autres)} autre(s) participant(s)")
            for p in autres:
                print(f"     → {p.username} (ID: {p.id})")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

def corriger_affichage_conversations():
    """Corriger l'affichage des conversations dans le template"""
    
    template_path = 'templates/communication/messagerie.html'
    
    with open(template_path, 'r') as f:
        contenu = f.read()
    
    print(f"\n🔧 CORRECTION DE L'AFFICHAGE DES CONVERSATIONS")
    print("=" * 50)
    
    # Vérifier si le problème est dans la condition {% if conversations %}
    if '{% if conversations %}' in contenu and '{% else %}' in contenu:
        print("✅ Structure conditionnelle trouvée")
        
        # Remplacer par une version plus robuste
        ancienne_structure = '''{% if conversations %}
                <div class="alert alert-success">
                    <i class="fas fa-check-circle me-2"></i>
                    {{ conversations.count }} conversation(s) trouvée(s) dans la base de données
                </div>'''
        
        nouvelle_structure = '''{% if conversations %}
                <div class="alert alert-success">
                    <i class="fas fa-check-circle me-2"></i>
                    <strong>DEBUG:</strong> {{ conversations.count }} conversation(s) trouvée(s) | 
                    Affichage de {{ conversations|length }} conversation(s) dans le template
                </div>'''
        
        if ancienne_structure in contenu:
            contenu = contenu.replace(ancienne_structure, nouvelle_structure)
            print("✅ Structure conditionnelle renforcée")
    
    # Ajouter du debug dans la boucle des conversations
    if '{% for conversation in conversations %}' in contenu:
        ancienne_boucle = '''{% for conversation in conversations %}
                <div class="conversation-item border rounded p-3 mb-3 bg-light">'''
        
        nouvelle_boucle = '''{% for conversation in conversations %}
                <!-- DEBUG: Conversation {{ conversation.id }} -->
                <div class="conversation-item border rounded p-3 mb-3 bg-light" data-conv-id="{{ conversation.id }}">'''
        
        if ancienne_boucle in contenu:
            contenu = contenu.replace(ancienne_boucle, nouvelle_boucle)
            print("✅ Debug ajouté dans la boucle des conversations")
    
    # Écrire le template corrigé
    with open(template_path, 'w') as f:
        f.write(contenu)
    
    print("✅ Corrections appliquées au template")

if __name__ == "__main__":
    diagnostic_complet()
    corriger_affichage_conversations()
    
    print(f"\n🎯 PROCHAINES ÉTAPES:")
    print("1. Le diagnostic va montrer OÙ apparaissent test_agent et test_medecin")
    print("2. Les corrections vont ajouter du debug pour voir les conversations")
    print("3. Testez à nouveau: http://127.0.0.1:8000/communication/")