#!/usr/bin/env python
import os

def fix_final_urls():
    """Vérifier et corriger les 2 URLs manquantes dans agents/urls.py"""
    
    file_path = 'agents/urls.py'
    
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        print("🔍 VÉRIFICATION DES URLs DANS agents/urls.py...")
        
        # Vérifier la présence des URLs manquantes
        missing_urls = {
            'creer_bon_soin_membre': "path('creer-bon-soin/<int:membre_id>/', views.creer_bon_soin_membre, name='creer_bon_soin_membre')",
            'confirmation_bon_soin': "path('confirmation-bon-soin/<int:bon_id>/', views.confirmation_bon_soin, name='confirmation_bon_soin')"
        }
        
        found_urls = []
        missing_urls_list = []
        
        for url_name, url_pattern in missing_urls.items():
            if url_pattern in content:
                found_urls.append(url_name)
                print(f"✅ {url_name} - PRÉSENT")
            else:
                missing_urls_list.append(url_pattern)
                print(f"❌ {url_name} - MANQUANT")
        
        if not missing_urls_list:
            print("\n🎯 TOUTES LES URLs SONT PRÉSENTES DANS LE FICHIER!")
            return True
        else:
            print(f"\n🔧 AJOUT DES {len(missing_urls_list)} URLs MANQUANTES...")
            
            # Trouver la section des bons de soin
            section_marker = "# =========================================================================\n# URLs GESTION BONS DE SOIN"
            section_pos = content.find(section_marker)
            
            if section_pos != -1:
                # Trouver la fin de la section
                end_section_pos = content.find("# =========================================================================\n#", section_pos + 100)
                
                if end_section_pos == -1:
                    end_section_pos = content.find("]", section_pos)
                
                # Insérer les URLs manquantes dans la section
                if end_section_pos != -1:
                    insertion_point = end_section_pos
                    new_urls = "\n    " + "\n    ".join(missing_urls_list)
                    new_content = content[:insertion_point] + new_urls + "\n    " + content[insertion_point:]
                    
                    with open(file_path, 'w') as file:
                        file.write(new_content)
                    
                    print("✅ URLs manquantes ajoutées avec succès!")
                    return True
            else:
                print("❌ Impossible de trouver la section des bons de soin")
                return False
                
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def verify_urls_in_views():
    """Vérifier que les vues existent dans agents/views.py"""
    
    file_path = 'agents/views.py'
    
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        print("\n🔍 VÉRIFICATION DES VUES DANS agents/views.py...")
        
        required_views = [
            'def creer_bon_soin_membre(',
            'def confirmation_bon_soin('
        ]
        
        for view in required_views:
            if view in content:
                print(f"✅ {view.split('(')[0]} - PRÉSENTE")
            else:
                print(f"❌ {view.split('(')[0]} - MANQUANTE")
        
        return all(view in content for view in required_views)
        
    except Exception as e:
        print(f"❌ Erreur vérification vues: {e}")
        return False

if __name__ == "__main__":
    print("🎯 CORRECTION FINALE POUR ATTEINDRE 100%")
    print("=" * 50)
    
    # Vérifier les URLs
    urls_ok = fix_final_urls()
    
    # Vérifier les vues
    views_ok = verify_urls_in_views()
    
    if urls_ok and views_ok:
        print("\n🎉 TOUTES LES CORRECTIONS SONT EN PLACE!")
        print("💡 Relancez la validation pour voir le score de 100%:")
        print("   python final_validation.py")
    else:
        print("\n⚠️  Il reste quelques corrections à faire manuellement")
        print("📋 Vérifiez que ces lignes sont dans agents/urls.py:")
        print("   path('creer-bon-soin/<int:membre_id>/', views.creer_bon_soin_membre, name='creer_bon_soin_membre')")
        print("   path('confirmation-bon-soin/<int:bon_id>/', views.confirmation_bon_soin, name='confirmation_bon_soin')")