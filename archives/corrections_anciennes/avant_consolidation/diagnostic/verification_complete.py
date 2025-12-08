# verification_complete.py
import os
import sys
import django
from django.db.models import Q

# Configuration Django
projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("="*80)
print("🔍 VERIFICATION COMPLÈTE DU SYSTÈME MEMBRES")
print("="*80)

def verifier_imports():
    """Vérifie les imports dans assureur/views.py"""
    print("\n📋 1. VÉRIFICATION DES IMPORTS DANS assureur/views.py")
    print("-"*50)
    
    try:
        with open('assureur/views.py', 'r') as f:
            content = f.read()
            
        # Chercher les imports de Membre
        import_lines = []
        for line in content.split('\n'):
            if 'Membre' in line and ('import' in line or 'from' in line):
                import_lines.append(line.strip())
        
        if import_lines:
            for line in import_lines:
                print(f"  ✅ Trouvé: {line}")
                
                # Extraire le module source
                if 'from' in line:
                    module = line.split('from')[1].split('import')[0].strip()
                    print(f"     → Module: {module}")
        else:
            print("  ❌ Aucun import de 'Membre' trouvé dans assureur/views.py")
            
    except Exception as e:
        print(f"  ❌ Erreur: {e}")

def verifier_modeles():
    """Compare les deux modèles Membre"""
    print("\n📋 2. COMPARAISON DES MODÈLES MEMBRE")
    print("-"*50)
    
    try:
        # Essayer d'importer les deux modèles
        from agents.models import Membre as MembreAgents
        print("  ✅ agents.models.Membre importé")
        
        from assureur.models import Membre as MembreAssureur
        print("  ✅ assureur.models.Membre importé")
        
        # Compter les données
        count_agents = MembreAgents.objects.count()
        count_assureur = MembreAssureur.objects.count()
        
        print(f"\n  📊 STATISTIQUES DE DONNÉES:")
        print(f"     • agents.models.Membre: {count_agents} membres")
        print(f"     • assureur.models.Membre: {count_assureur} membres")
        
        # Comparer les champs
        print("\n  🔄 COMPARAISON DES CHAMPS:")
        
        # Champs agents.models.Membre
        fields_agents = {f.name for f in MembreAgents._meta.fields}
        print(f"     • agents.models.Membre: {len(fields_agents)} champs")
        
        # Champs assureur.models.Membre
        fields_assureur = {f.name for f in MembreAssureur._meta.fields}
        print(f"     • assureur.models.Membre: {len(fields_assureur)} champs")
        
        # Champs communs
        common_fields = fields_agents.intersection(fields_assureur)
        print(f"     • Champs communs: {len(common_fields)}")
        
        # Champs spécifiques
        agents_only = fields_agents - fields_assureur
        assureur_only = fields_assureur - fields_agents
        
        if agents_only:
            print(f"\n  📌 CHAMPS UNIQUES À agents.models.Membre:")
            for field in sorted(agents_only):
                print(f"     • {field}")
        
        if assureur_only:
            print(f"\n  📌 CHAMPS UNIQUES À assureur.models.Membre:")
            for field in sorted(assureur_only):
                print(f"     • {field}")
                
        return MembreAgents, MembreAssureur
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return None, None

def verifier_vue_liste_membres():
    """Analyse la vue liste_membres"""
    print("\n📋 3. ANALYSE DE LA VUE liste_membres")
    print("-"*50)
    
    try:
        with open('assureur/views.py', 'r') as f:
            content = f.read()
        
        # Trouver la fonction liste_membres
        start = content.find('def liste_membres')
        if start == -1:
            print("  ❌ Fonction liste_membres non trouvée")
            return
        
        # Trouver la fin de la fonction (prochaine fonction)
        next_def = content.find('\ndef ', start + 1)
        if next_def == -1:
            function_text = content[start:]
        else:
            function_text = content[start:next_def]
        
        print(f"  ✅ Fonction liste_membres trouvée ({len(function_text)} caractères)")
        
        # Vérifier les points clés
        checks = {
            'order_by': "'date_inscription'" in function_text or "'date_adhesion'" in function_text,
            'search_filter': 'Q(' in function_text and 'icontains' in function_text,
            'pagination': 'Paginator' in function_text,
            'statut_filter': "statut" in function_text.lower(),
        }
        
        for check, result in checks.items():
            status = "✅" if result else "❌"
            print(f"     {status} {check}")
            
    except Exception as e:
        print(f"  ❌ Erreur: {e}")

def verifier_template():
    """Vérifie le template liste_membres.html"""
    print("\n📋 4. VÉRIFICATION DU TEMPLATE")
    print("-"*50)
    
    template_path = 'assureur/templates/assureur/liste_membres.html'
    
    try:
        with open(template_path, 'r') as f:
            content = f.read()
        
        print(f"  ✅ Template trouvé: {template_path}")
        
        # Vérifier les variables utilisées
        variables = [
            ('page_obj', 'Objet de pagination'),
            ('stats_membres', 'Statistiques'),
            ('filters', 'Filtres'),
            ('statut_choices', 'Choix de statut'),
        ]
        
        for var, desc in variables:
            if var in content:
                print(f"     ✅ Variable '{var}' ({desc}) utilisée")
            else:
                print(f"     ❌ Variable '{var}' ({desc}) non trouvée")
        
        # Vérifier les champs de membre
        member_fields = [
            ('numero_unique', 'Numéro unique'),
            ('numero_membre', 'Numéro membre'),
            ('date_inscription', 'Date inscription'),
            ('date_adhesion', 'Date adhésion'),
            ('nom', 'Nom'),
            ('prenom', 'Prénom'),
            ('email', 'Email'),
            ('telephone', 'Téléphone'),
            ('statut', 'Statut'),
            ('est_femme_enceinte', 'Femme enceinte'),
        ]
        
        print("\n  🔍 CHAMPS DE MEMBRE DANS LE TEMPLATE:")
        for field, desc in member_fields:
            if field in content:
                print(f"     ✅ Champ '{field}' ({desc}) référencé")
        
    except FileNotFoundError:
        print(f"  ❌ Template non trouvé: {template_path}")
    except Exception as e:
        print(f"  ❌ Erreur: {e}")

def tester_recherche():
    """Teste la recherche de membres"""
    print("\n📋 5. TEST DE RECHERCHE")
    print("-"*50)
    
    try:
        from agents.models import Membre
        
        # Tests de recherche
        tests = [
            ('ASIA', 'Recherche "ASIA"'),
            ('Jean', 'Recherche "Jean"'),
            ('0500', 'Recherche "0500" (téléphone)'),
            ('test', 'Recherche "test" (email)'),
            ('', 'Recherche vide'),
        ]
        
        for search_term, description in tests:
            if search_term:
                results = Membre.objects.filter(
                    Q(nom__icontains=search_term) |
                    Q(prenom__icontains=search_term) |
                    Q(numero_unique__icontains=search_term) |
                    Q(email__icontains=search_term) |
                    Q(telephone__icontains=search_term)
                )
            else:
                results = Membre.objects.all()
            
            print(f"  {description}: {results.count()} résultat(s)")
            
            if results.count() <= 5 and results.count() > 0:
                for m in results:
                    print(f"     • {m.nom} {m.prenom} (ID: {m.id})")
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")

def verifier_urls():
    """Vérifie les URLs de l'application assureur"""
    print("\n📋 6. VÉRIFICATION DES URLs")
    print("-"*50)
    
    try:
        with open('assureur/urls.py', 'r') as f:
            content = f.read()
        
        # Chercher les URLs de membres
        if 'membres/' in content:
            print("  ✅ URLs pour membres trouvées")
            
            # Extraire les URLs spécifiques
            lines = content.split('\n')
            for line in lines:
                if 'membres' in line and 'path(' in line:
                    print(f"     • {line.strip()}")
        else:
            print("  ❌ Aucune URL pour membres trouvée")
            
    except Exception as e:
        print(f"  ❌ Erreur: {e}")

def generer_rapport():
    """Génère un rapport de recommandations"""
    print("\n" + "="*80)
    print("📊 RAPPORT DE RECOMMANDATIONS")
    print("="*80)
    
    recommendations = []
    
    # 1. Vérifier l'import
    try:
        with open('assureur/views.py', 'r') as f:
            content = f.read()
        
        if 'from agents.models import Membre' in content:
            recommendations.append("✅ L'import utilise agents.models.Membre (bon choix)")
        elif 'from assureur.models import Membre' in content:
            recommendations.append("⚠️  L'import utilise assureur.models.Membre (seulement 3 membres)")
        else:
            recommendations.append("❌ Import de Membre non trouvé")
    except:
        pass
    
    # 2. Vérifier les données
    try:
        from agents.models import Membre as MembreAgents
        from assureur.models import Membre as MembreAssureur
        
        if MembreAgents.objects.count() > MembreAssureur.objects.count():
            recommendations.append(f"✅ agents.models.Membre a plus de données ({MembreAgents.objects.count()} vs {MembreAssureur.objects.count()})")
        else:
            recommendations.append(f"⚠️  assureur.models.Membre a peu de données ({MembreAssureur.objects.count()} membres)")
    except:
        pass
    
    # 3. Vérifier le template
    try:
        with open('assureur/templates/assureur/liste_membres.html', 'r') as f:
            content = f.read()
        
        if 'numero_unique' in content and 'date_inscription' in content:
            recommendations.append("✅ Template utilise les champs de agents.models.Membre")
        elif 'numero_membre' in content and 'date_adhesion' in content:
            recommendations.append("⚠️  Template utilise les champs de assureur.models.Membre")
    except:
        pass
    
    # Afficher les recommandations
    print("\n💡 RECOMMANDATIONS:")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")
    
    print("\n🚀 ACTIONS RECOMMANDÉES:")
    print("  1. Vérifier que assureur/views.py utilise 'from agents.models import Membre'")
    print("  2. Vérifier que le template utilise 'numero_unique' et 'date_inscription'")
    print("  3. Supprimer les références à 'type_contrat' (n'existe pas dans agents.models.Membre)")
    print("  4. Redémarrer le serveur et tester la recherche")

def verifier_donnees_exemple():
    """Affiche des exemples de données"""
    print("\n📋 7. EXEMPLES DE DONNÉES")
    print("-"*50)
    
    try:
        from agents.models import Membre
        
        print("  📋 10 PREMIERS MEMBRES (agents.models.Membre):")
        for m in Membre.objects.all()[:10]:
            print(f"     • ID: {m.id}")
            print(f"       Nom: {m.nom} {m.prenom}")
            print(f"       Numéro: {m.numero_unique}")
            print(f"       Téléphone: {m.telephone}")
            print(f"       Email: {m.email}")
            print(f"       Statut: {m.statut}")
            print(f"       Date inscription: {m.date_inscription}")
            print()
            
    except Exception as e:
        print(f"  ❌ Erreur: {e}")

# Exécuter toutes les vérifications
def main():
    verifier_imports()
    verifier_modeles()
    verifier_vue_liste_membres()
    verifier_template()
    tester_recherche()
    verifier_urls()
    verifier_donnees_exemple()
    generer_rapport()
    
    print("\n" + "="*80)
    print("✅ VÉRIFICATION TERMINÉE")
    print("="*80)

if __name__ == "__main__":
    main()