# inspect_models.py
import os
import django
import sys

sys.path.append('/Users/koffitanohsoualiho/Documents/projet')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

# Désactiver temporairement le chargement des modèles pour inspection
os.environ['DJANGO_SETTINGS_MODULE'] = ''

# Lire directement le fichier models.py
try:
    with open('/Users/koffitanohsoualiho/Documents/projet/medecin/models.py', 'r') as f:
        content = f.read()
        print("📄 CONTENU ACTUEL de medecin/models.py:")
        print("=" * 50)
        
        # Afficher les lignes contenant "class" pour voir les modèles définis
        lines = content.split('\n')
        class_lines = [line for line in lines if line.strip().startswith('class ')]
        
        if class_lines:
            print("🧩 Classes trouvées:")
            for line in class_lines:
                print(f"   {line.strip()}")
        else:
            print("❌ Aucune classe trouvée dans models.py")
            
        print("\n🔍 Recherche spécifique des modèles d'ordonnance:")
        if 'class Ordonnance' in content:
            print("✅ 'class Ordonnance' trouvé")
            # Extraire la définition de la classe Ordonnance
            start = content.find('class Ordonnance')
            end = content.find('\nclass', start) if content.find('\nclass', start) != -1 else len(content)
            ordonnance_class = content[start:end]
            print("Définition Ordonnance:")
            print(ordonnance_class[:500] + "..." if len(ordonnance_class) > 500 else ordonnance_class)
        else:
            print("❌ 'class Ordonnance' NON trouvé")
            
        if 'class Medicament' in content:
            print("✅ 'class Medicament' trouvé")
        else:
            print("❌ 'class Medicament' NON trouvé")
            
        if 'class LigneOrdonnance' in content:
            print("✅ 'class LigneOrdonnance' trouvé")
        else:
            print("❌ 'class LigneOrdonnance' NON trouvé")
            
except Exception as e:
    print(f"❌ Erreur: {e}")