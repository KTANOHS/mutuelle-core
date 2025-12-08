# correcteur_sync_urgence.py
import os
import sys
import django
from pathlib import Path
from django.db import transaction

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from django.contrib.auth.models import User
from membres.models import Membre
from django.db.models import Q

print("🔧 CORRECTEUR DE SYNCHRONISATION URGENCE")
print("=" * 50)

class CorrecteurSynchronisation:
    def __init__(self, mode_test=True):
        self.mode_test = mode_test
        self.actions = []
        self.corrections_appliquees = 0
    
    def corriger_tous_problemes(self):
        """Corrige tous les problèmes identifiés"""
        print("🎯 CORRECTION DES PROBLÈMES DE SYNCHRO...")
        
        try:
            with transaction.atomic():
                if self.mode_test:
                    transaction.set_rollback(True)
                    print("⚠️  MODE TEST - Aucune modification en base")
                
                # 1. Corriger les membres sans user
                self._corriger_membres_sans_user()
                
                # 2. Vérifier et corriger les numéros uniques
                self._corriger_numeros_uniques()
                
                # 3. Synchroniser utilisateurs-membres
                self._synchroniser_utilisateurs_membres()
                
                # Résumé
                self._afficher_resume()
                
        except Exception as e:
            print(f"❌ Erreur lors des corrections: {e}")
    
    def _corriger_membres_sans_user(self):
        """Corrige les membres sans utilisateur associé"""
        print("\n1. 🔗 CORRECTION MEMBRES SANS USER...")
        
        membres_sans_user = Membre.objects.filter(user__isnull=True)
        count = membres_sans_user.count()
        
        if count == 0:
            print("   ✅ Aucun membre sans user - rien à corriger")
            return
        
        print(f"   🔍 {count} membres sans user trouvés")
        
        for membre in membres_sans_user:
            # Stratégie de correction : chercher un user par email ou créer un nouveau
            user_trouve = None
            
            # Chercher par email si disponible
            if hasattr(membre, 'email') and membre.email:
                try:
                    user_trouve = User.objects.filter(email=membre.email).first()
                except:
                    pass
            
            # Chercher par nom/prénom
            if not user_trouve and hasattr(membre, 'prenom') and hasattr(membre, 'nom'):
                try:
                    users_possibles = User.objects.filter(
                        first_name__icontains=membre.prenom,
                        last_name__icontains=membre.nom
                    )
                    if users_possibles.exists():
                        user_trouve = users_possibles.first()
                except:
                    pass
            
            # Créer un user si nécessaire (en mode réel seulement)
            if not user_trouve and not self.mode_test:
                username_base = f"membre_{membre.id}"
                if hasattr(membre, 'prenom') and hasattr(membre, 'nom'):
                    username_base = f"{membre.prenom.lower()}.{membre.nom.lower()}"
                
                # S'assurer que le username est unique
                username = username_base
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{username_base}{counter}"
                    counter += 1
                
                user_trouve = User.objects.create_user(
                    username=username,
                    email=getattr(membre, 'email', f"{username}@mutuelle.local"),
                    password='password123',
                    first_name=getattr(membre, 'prenom', ''),
                    last_name=getattr(membre, 'nom', '')
                )
                action = f"CRÉÉ user {username} pour membre {membre.id}"
            elif user_trouve:
                action = f"ASSOCIÉ user {user_trouve.username} à membre {membre.id}"
            else:
                action = f"ARCHIVÉ membre {membre.id} (aucun user trouvé/créé)"
            
            # Appliquer la correction
            if user_trouve and not self.mode_test:
                membre.user = user_trouve
                membre.save()
                self.corrections_appliquees += 1
            
            self.actions.append(action)
            print(f"   ✅ {action}")
    
    def _corriger_numeros_uniques(self):
        """Vérifie et corrige les numéros uniques"""
        print("\n2. 🔢 VÉRIFICATION NUMÉROS UNIQUES...")
        
        try:
            # Vérifier les doublons sur numero_unique
            from django.db.models import Count
            
            doublons = Membre.objects.values('numero_unique').annotate(
                count=Count('id')
            ).filter(count__gt=1, numero_unique__isnull=False)
            
            if doublons.exists():
                print(f"   ⚠️  {doublons.count()} numéros uniques en double")
                
                for doublon in doublons:
                    numero = doublon['numero_unique']
                    membres = Membre.objects.filter(numero_unique=numero).order_by('date_inscription')
                    
                    # Garder le premier, corriger les autres
                    membre_reference = membres.first()
                    
                    for membre in membres[1:]:
                        nouveau_numero = f"{numero}_DUPL_{membre.id}"
                        
                        if self.mode_test:
                            action = f"TEST: Renommer {numero} → {nouveau_numero}"
                        else:
                            membre.numero_unique = nouveau_numero
                            membre.save()
                            action = f"RENOMMÉ {numero} → {nouveau_numero}"
                            self.corrections_appliquees += 1
                        
                        self.actions.append(action)
                        print(f"   ✅ {action}")
            else:
                print("   ✅ Aucun numéro unique en double")
                
        except Exception as e:
            print(f"   ⚠️  Vérification numéros: {e}")
        
        # Vérifier les membres sans numéro unique
        try:
            membres_sans_numero = Membre.objects.filter(
                Q(numero_unique__isnull=True) | Q(numero_unique='')
            )
            
            if membres_sans_numero.exists():
                print(f"   ⚠️  {membres_sans_numero.count()} membres sans numéro unique")
                
                for membre in membres_sans_numero:
                    # Générer un numéro unique basé sur l'ID
                    nouveau_numero = f"MEM{str(membre.id).zfill(4)}"
                    
                    if self.mode_test:
                        action = f"TEST: Attribuer numéro {nouveau_numero} à membre {membre.id}"
                    else:
                        membre.numero_unique = nouveau_numero
                        membre.save()
                        action = f"ATTRIBUÉ numéro {nouveau_numero} à membre {membre.id}"
                        self.corrections_appliquees += 1
                    
                    self.actions.append(action)
                    print(f"   ✅ {action}")
            else:
                print("   ✅ Tous les membres ont un numéro unique")
                
        except Exception as e:
            print(f"   ⚠️  Correction numéros manquants: {e}")
    
    def _synchroniser_utilisateurs_membres(self):
        """Synchronise les utilisateurs et membres"""
        print("\n3. 🔄 SYNCHRONISATION UTILISATEURS-MEMBRES...")
        
        # Compter les users sans membre
        users_sans_membre = User.objects.filter(
            is_staff=False, 
            is_superuser=False
        ).exclude(
            id__in=Membre.objects.filter(user__isnull=False).values('user_id')
        )
        
        count_users_sans_membre = users_sans_membre.count()
        print(f"   🔍 {count_users_sans_membre} utilisateurs sans membre associé")
        
        if count_users_sans_membre > 0 and not self.mode_test:
            print("   💡 Création automatique des membres pour les users...")
            
            for user in users_sans_membre[:10]:  # Limiter à 10 pour éviter la surcharge
                try:
                    # Vérifier si un membre existe déjà pour cet user
                    membre_existant = Membre.objects.filter(user=user).exists()
                    if not membre_existant:
                        # Créer le membre
                        numero_unique = f"USER{str(user.id).zfill(4)}"
                        
                        membre = Membre.objects.create(
                            user=user,
                            numero_unique=numero_unique,
                            prenom=user.first_name,
                            nom=user.last_name,
                            email=user.email
                        )
                        
                        action = f"CRÉÉ membre {numero_unique} pour user {user.username}"
                        self.actions.append(action)
                        self.corrections_appliquees += 1
                        print(f"   ✅ {action}")
                        
                except Exception as e:
                    print(f"   ❌ Erreur création membre pour {user.username}: {e}")
        elif self.mode_test:
            print("   ⚠️  MODE TEST: Créerait des membres pour les users sans membre")
    
    def _afficher_resume(self):
        """Affiche le résumé des corrections"""
        print("\n" + "=" * 50)
        print("📋 RÉSUMÉ DES CORRECTIONS")
        print("=" * 50)
        
        if self.mode_test:
            print("🔬 MODE TEST - Simulations seulement")
        else:
            print("🔧 MODE RÉEL - Modifications appliquées")
        
        print(f"✅ Corrections appliquées: {self.corrections_appliquees}")
        print(f"📝 Actions: {len(self.actions)}")
        
        if self.actions:
            print("\n📋 DÉTAIL DES ACTIONS:")
            for action in self.actions[:10]:  # Afficher les 10 premières
                print(f"   • {action}")
            if len(self.actions) > 10:
                print(f"   ... et {len(self.actions) - 10} autres actions")
        
        # Statistiques finales
        membres_avec_user = Membre.objects.filter(user__isnull=False).count()
        total_membres = Membre.objects.count()
        pourcentage_corrige = (membres_avec_user / total_membres * 100) if total_membres > 0 else 0
        
        print(f"\n📊 STATISTIQUES FINALES:")
        print(f"   👤 Membres avec user: {membres_avec_user}/{total_membres} ({pourcentage_corrige:.1f}%)")
        
        if not self.mode_test and pourcentage_corrige < 100:
            print(f"\n💡 RECOMMANDATION: Exécutez à nouveau en mode réel pour compléter la synchronisation")

# Exécution
if __name__ == "__main__":
    print("🔧 Ce correcteur va résoudre les problèmes de synchronisation.")
    print("💡 Il fonctionne en deux modes: TEST (sans modification) et RÉEL (avec modification)")
    
    mode = input("Choisir le mode [T]est ou [R]éel? (T/R): ").strip().upper()
    
    if mode == 'R':
        confirm = input("⚠️  MODE RÉEL - Les modifications seront appliquées. Confirmer? (O/N): ").strip().upper()
        if confirm == 'O':
            correcteur = CorrecteurSynchronisation(mode_test=False)
        else:
            print("🚫 Annulé - Passage en mode TEST")
            correcteur = CorrecteurSynchronisation(mode_test=True)
    else:
        correcteur = CorrecteurSynchronisation(mode_test=True)
    
    correcteur.corriger_tous_problemes()