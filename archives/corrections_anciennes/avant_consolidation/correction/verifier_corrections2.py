# verifier_corrections.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_corrections():
    print("🔍 VÉRIFICATION DES CORRECTIONS APPLIQUÉES")
    print("=" * 50)
    
    # Vérifier le template
    template_path = 'templates/communication/messagerie.html'
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    verifs_template = [
        "for conversation in conversations" in template_content,
        "if conversations" in template_content,
        "conversation.participants.all" in template_content
    ]
    
    print("✅ TEMPLATE:")
    for i, check in enumerate(verifs_template, 1):
        status = "✅" if check else "❌"
        print(f"   {status} Vérification {i}: {'OK' if check else 'NOK'}")
    
    # Vérifier la vue
    vue_path = 'communication/views.py'
    with open(vue_path, 'r') as f:
        vue_content = f.read()
    
    verifs_vue = [
        "messages_recents" in vue_content,
        "page_title" in vue_content,
        "total_conversations" in vue_content
    ]
    
    print("\n✅ VUE:")
    for i, check in enumerate(verifs_vue, 1):
        status = "✅" if check else "❌"
        print(f"   {status} Vérification {i}: {'OK' if check else 'NOK'}")
    
    if all(verifs_template) and all(verifs_vue):
        print("\n🎉 TOUTES LES CORRECTIONS ONT ÉTÉ APPLIQUÉES AVEC SUCCÈS !")
        print("🌐 Testez maintenant: http://127.0.0.1:8000/communication/")
    else:
        print("\n⚠️  Certaines corrections n'ont pas été appliquées")

if __name__ == "__main__":
    verifier_corrections()