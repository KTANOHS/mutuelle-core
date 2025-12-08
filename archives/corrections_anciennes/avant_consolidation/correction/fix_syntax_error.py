#!/usr/bin/env python
import os

def fix_syntax_error():
    """Corriger l'erreur de syntaxe dans agents/views.py"""
    
    file_path = 'agents/views.py'
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        print("🔍 RECHERCHE DE L'ERREUR DE SYNTAXE...")
        
        # Rechercher la ligne problématique
        problematic_lines = []
        for i, line in enumerate(lines, 1):
            if 'python final_validation.py' in line:
                problematic_lines.append((i, line.strip()))
                print(f"❌ Ligne {i}: {line.strip()}")
        
        if problematic_lines:
            print(f"\n🔧 SUPPRESSION DE {len(problematic_lines)} LIGNE(S) PROBLÉMATIQUE(S)...")
            
            # Créer un nouveau contenu sans les lignes problématiques
            new_lines = []
            for i, line in enumerate(lines, 1):
                if not any(prob_line[0] == i for prob_line in problematic_lines):
                    new_lines.append(line)
                else:
                    print(f"✅ Supprimé: '{line.strip()}'")
            
            # Écrire le fichier corrigé
            with open(file_path, 'w') as file:
                file.writelines(new_lines)
            
            print("\n🎯 ERREUR DE SYNTAXE CORRIGÉE!")
            return True
        else:
            print("✅ Aucune erreur de syntaxe trouvée")
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        return False

def verify_fix():
    """Vérifier que la correction a fonctionné"""
    
    file_path = 'agents/views.py'
    
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        if 'python final_validation.py' in content:
            print("❌ L'erreur de syntaxe est toujours présente")
            return False
        else:
            print("✅ Fichier agents/views.py maintenant syntaxiquement correct")
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

if __name__ == "__main__":
    print("🔄 CORRECTION DE L'ERREUR DE SYNTAXE DANS agents/views.py")
    print("=" * 60)
    
    if fix_syntax_error():
        print("\n🔍 VÉRIFICATION DE LA CORRECTION...")
        if verify_fix():
            print("\n🎉 CORRECTION RÉUSSIE!")
            print("💡 Vous pouvez maintenant relancer la validation:")
            print("   python final_validation.py")
        else:
            print("\n⚠️  La vérification a échoué")
            print("📋 Supprimez manuellement la ligne contenant 'python final_validation.py'")
    else:
        print("\n❌ La correction automatique a échoué")
        print("📋 Ouvrez agents/views.py et supprimez manuellement la ligne problématique")