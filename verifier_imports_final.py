
#!/usr/bin/env python3
"""
Vérification finale des imports
"""
import subprocess
import sys

def tester_import_direct():
    """Tester l'import direct"""
    try:
        from utilitaires.affichage_unifie import afficher_fiche_cotisation_unifiee
        print("✅ Import direct depuis utilitaires.affichage_unifie: OK")
        return True
    except ImportError as e:
        print(f"❌ Import direct échoué: {e}")
        return False

def tester_import_alias():
    """Tester l'import via l'alias"""
    try:
        import affichage_unifie
        print("✅ Import via alias affichage_unifie: OK")
        return True
    except ImportError as e:
        print(f"⚠️  Import via alias échoué: {e}")
        return False

def tester_django_check():
    """Tester la commande Django check"""
    print("\n🧪 Test Django check...")
    result = subprocess.run(
        [sys.executable, 'manage.py', 'check'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Django check: PASS")
        return True
    else:
        print(f"❌ Django check: FAIL")
        print(f"Erreur: {result.stderr}")
        return False

def main():
    print("🔍 Vérification finale des imports")
    print("=" * 50)
    
    tests = [
        ("Import direct", tester_import_direct),
        ("Import alias", tester_import_alias),
        ("Django check", tester_django_check)
    ]
    
    résultats = []
    for nom_test, fonction_test in tests:
        print(f"\n📋 {nom_test}:")
        try:
            résultat = fonction_test()
            résultats.append((nom_test, résultat))
        except Exception as e:
            print(f"  ❌ Exception: {e}")
            résultats.append((nom_test, False))
    
    # Afficher le résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ:")
    
    succès = sum(1 for _, résultat in résultats if résultat)
    total = len(résultats)
    
    for nom_test, résultat in résultats:
        statut = "✅ PASS" if résultat else "❌ FAIL"
        print(f"{statut} {nom_test}")
    
    if succès == total:
        print(f"\n🎉 Tous les tests passent ({succès}/{total})")
        print("\n✅ Le projet est prêt! Vous pouvez démarrer le serveur:")
        print("   python manage.py runserver")
        return 0
    else:
        print(f"\n⚠️  {succès}/{total} tests passés")
        print("\n🔧 Solutions possibles:")
        print("1. Vérifiez que utilitaires/__init__.py existe")
        print("2. Vérifiez que utilitaires/affichage_unifie.py existe")
        print("3. Créez un lien symbolique: ln -sf utilitaires/affichage_unifie.py affichage_unifie.py")
        print("4. Vérifiez les imports dans agents/views.py")
        return 1

if __name__ == "__main__":
    sys.exit(main())


