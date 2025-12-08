# correction_recherche.py
import os
import django
import sys

sys.path.append('/Users/koffitanohsoualiho/Documents/projet')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def corriger_vue_recherche():
    print("🔧 CORRECTION DE LA VUE RECHERCHE")
    print("=" * 50)
    
    chemin_vue = "/Users/koffitanohsoualiho/Documents/projet/assureur/views.py"
    
    try:
        with open(chemin_vue, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        # Vérifier si la vue recherche_membre existe
        if 'def recherche_membre' not in contenu:
            print("❌ La vue recherche_membre n'existe pas dans views.py")
            return False
        
        # Compter les occurrences du champ problématique
        occurrences = contenu.count('numero_assurance')
        print(f"📊 Occurrences de 'numero_assurance' trouvées: {occurrences}")
        
        if occurrences == 0:
            print("✅ Aucune occurrence de 'numero_assurance' trouvée")
            print("ℹ️  Le problème peut être ailleurs")
            return True
        
        # Remplacer numero_assurance par numero_membre
        nouveau_contenu = contenu.replace('numero_assurance', 'numero_membre')
        
        # Sauvegarder
        with open(chemin_vue, 'w', encoding='utf-8') as f:
            f.write(nouveau_contenu)
        
        print("✅ Correction appliquée: 'numero_assurance' → 'numero_membre'")
        
        # Vérifier la correction
        with open(chemin_vue, 'r', encoding='utf-8') as f:
            contenu_corrige = f.read()
            if 'numero_assurance' not in contenu_corrige:
                print("✅ Vérification: 'numero_assurance' a été supprimé")
            else:
                print("❌ Vérification: 'numero_assurance' est toujours présent")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        return False

def creer_vue_recherche_corrigee():
    """Crée une version corrigée de la vue recherche si nécessaire"""
    print("\n🔄 CRÉATION D'UNE VUE RECHERCHE CORRIGÉE")
    print("=" * 50)
    
    code_corrige = '''
def recherche_membre(request):
    """
    Vue corrigée pour la recherche de membres
    """
    from django.db.models import Q
    from .models import Membre
    
    query = request.GET.get('q', '').strip()
    
    if not query:
        # Si pas de recherche, retourner tous les membres ou une page vide
        membres = Membre.objects.all()[:50]  # Limiter à 50 résultats
        message = "Veuillez entrer un terme de recherche"
    else:
        # Rechercher dans les champs existants
        membres = Membre.objects.filter(
            Q(nom__icontains=query) |
            Q(prenom__icontains=query) |
            Q(numero_membre__icontains=query) |
            Q(email__icontains=query) |
            Q(telephone__icontains=query) |
            Q(numero_contrat__icontains=query)
        ).distinct()
        message = f"Résultats pour : {query}"
    
    context = {
        'membres': membres,
        'query': query,
        'message': message,
        'total_resultats': membres.count()
    }
    
    return render(request, 'assureur/recherche_membre.html', context)
'''
    
    print("📝 Code de la vue corrigée prêt")
    return code_corrige

if __name__ == "__main__":
    succes = corriger_vue_recherche()
    
    if not succes:
        print("\n🔄 Application de la correction alternative...")
        code_corrige = creer_vue_recherche_corrigee()
        print("Code de remplacement généré")