# test_vues_rapide.py
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("🔍 TEST RAPIDE DES VUES MEMBRES")
print("=" * 40)

try:
    from membres.views import creer_membre, liste_membres_agent, upload_documents_membre
    print("✅ SUCCÈS: Toutes les vues importées")
    
    # Test des URLs
    from django.urls import reverse
    print("📋 URLs configurées:")
    print(f"  • creer_membre: {reverse('membres:creer_membre')}")
    print(f"  • liste_membres_agent: {reverse('membres:liste_membres_agent')}")
    print(f"  • upload_documents: {reverse('membres:upload_documents', args=[1])}")
    
    # Test des formulaires
    from membres.forms import MembreCreationForm, MembreDocumentForm
    print("✅ Formulaires importés")
    
    # Test des modèles
    from membres.models import Membre
    from agents.models import Agent
    print(f"📊 Données: {Membre.objects.count()} membres, {Agent.objects.count()} agents")
    
    print("\n🎉 SYSTÈME PRÊT !")
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()