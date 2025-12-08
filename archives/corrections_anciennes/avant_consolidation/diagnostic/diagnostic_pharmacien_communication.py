#!/usr/bin/env python3
"""
SCRIPT DE DIAGNOSTIC PHARMACIEN & COMMUNICATION
Diagnostique les problèmes de communication et pharmacien
"""

import os
import sys
import django
import json
import traceback
from pathlib import Path

# Ajouter le chemin du projet
PROJECT_DIR = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_DIR))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur lors du setup Django: {e}")
    sys.exit(1)

print("=" * 80)
print("🔍 DIAGNOSTIC COMPLET PHARMACIEN & COMMUNICATION")
print("=" * 80)

# ============================================================================
# 1. VÉRIFICATION DES MODÈLES
# ============================================================================
print("\n1. 🔧 VÉRIFICATION DES MODÈLES")
print("-" * 40)

try:
    from communication.models import Conversation, Message, Notification, PieceJointe
    from pharmacien.models import Pharmacien, BonDeSoin, Ordonnance, MedicamentPrescrit
    
    print("✅ Modèles communication importés")
    print("✅ Modèles pharmacien importés")
    
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print(traceback.format_exc())

# ============================================================================
# 2. VÉRIFICATION DES UTILISATEURS ET PERMISSIONS
# ============================================================================
print("\n2. 👥 VÉRIFICATION DES UTILISATEURS")
print("-" * 40)

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

try:
    # Comptage des utilisateurs
    total_users = User.objects.count()
    print(f"Total utilisateurs: {total_users}")
    
    # Utilisateurs avec rôle pharmacien
    pharmaciens = User.objects.filter(groups__name='Pharmacien')
    print(f"Pharmaciens: {pharmaciens.count()}")
    
    if pharmaciens.exists():
        print("📋 Liste des pharmaciens:")
        for pharma in pharmaciens[:5]:  # Limiter à 5
            print(f"  • {pharma.username} (ID: {pharma.id}) - {pharma.get_full_name()}")
    
    # Groupes et permissions
    print(f"\nGroupes existants: {Group.objects.count()}")
    for group in Group.objects.all():
        perms = group.permissions.count()
        users = group.user_set.count()
        print(f"  • {group.name}: {users} utilisateurs, {perms} permissions")
        
except Exception as e:
    print(f"❌ Erreur: {e}")

# ============================================================================
# 3. VÉRIFICATION DES CONVERSATIONS ET MESSAGES
# ============================================================================
print("\n3. 📨 VÉRIFICATION DES COMMUNICATIONS")
print("-" * 40)

try:
    # Statistiques générales
    total_conversations = Conversation.objects.count()
    total_messages = Message.objects.count()
    total_notifications = Notification.objects.count()
    
    print(f"Conversations totales: {total_conversations}")
    print(f"Messages totaux: {total_messages}")
    print(f"Notifications totales: {total_notifications}")
    
    # Dernières conversations
    recent_convs = Conversation.objects.order_by('-date_modification')[:5]
    if recent_convs.exists():
        print("\n📊 Dernières conversations:")
        for conv in recent_convs:
            participants = [p.username for p in conv.participants.all()]
            msgs = conv.messages.count()
            print(f"  • Conv {conv.id}: {', '.join(participants)} - {msgs} messages")
    
    # Messages non lus
    unread_messages = Message.objects.filter(est_lu=False)
    print(f"\n📫 Messages non lus: {unread_messages.count()}")
    
    # Par utilisateur
    from django.db.models import Count
    users_with_unread = User.objects.annotate(
        unread_count=Count('messages_recus', filter=models.Q(messages_recus__est_lu=False))
    ).filter(unread_count__gt=0)
    
    if users_with_unread.exists():
        print("Utilisateurs avec messages non lus:")
        for user in users_with_unread:
            print(f"  • {user.username}: {user.unread_count} messages non lus")
            
except Exception as e:
    print(f"❌ Erreur: {e}")

# ============================================================================
# 4. VÉRIFICATION PHARMACIEN
# ============================================================================
print("\n4. 💊 VÉRIFICATION PHARMACIEN")
print("-" * 40)

try:
    # Statistiques pharmacien
    total_pharmaciens = Pharmacien.objects.count()
    total_bons = BonDeSoin.objects.count()
    total_ordonnances = Ordonnance.objects.count()
    
    print(f"Pharmaciens enregistrés: {total_pharmaciens}")
    print(f"Bons de soin totaux: {total_bons}")
    print(f"Ordonnances totales: {total_ordonnances}")
    
    # Bons par statut
    from django.db.models import Count
    bons_by_status = BonDeSoin.objects.values('statut').annotate(count=Count('id'))
    
    if bons_by_status:
        print("\n📈 Bons de soin par statut:")
        for item in bons_by_status:
            print(f"  • {item['statut']}: {item['count']}")
    
    # Dernières ordonnances
    recent_ordonnances = Ordonnance.objects.select_related('medecin', 'patient').order_by('-date_creation')[:3]
    if recent_ordonnances.exists():
        print("\n💊 Dernières ordonnances:")
        for ord in recent_ordonnances:
            print(f"  • Ord {ord.id}: Dr. {ord.medecin.username} → {ord.patient.username}")
    
except Exception as e:
    print(f"❌ Erreur pharmacien: {e}")

# ============================================================================
# 5. VÉRIFICATION DES VUES ET URLS
# ============================================================================
print("\n5. 🌐 VÉRIFICATION DES VUES")
print("-" * 40)

try:
    from django.urls import reverse, NoReverseMatch
    from communication import views as comm_views
    from pharmacien import views as pharma_views
    
    # URLs à tester
    test_urls = [
        ('communication:envoyer_message_api', 'API Envoi Message'),
        ('communication:messages_liste', 'Liste Messages'),
        ('pharmacien:dashboard', 'Dashboard Pharmacien'),
        ('pharmacien:bons_soin_liste', 'Liste Bons'),
        ('pharmacien:ordonnances_liste', 'Liste Ordonnances'),
    ]
    
    print("🔗 Test des URLs:")
    for url_name, description in test_urls:
        try:
            url = reverse(url_name)
            print(f"  ✅ {description}: {url}")
        except NoReverseMatch:
            print(f"  ❌ {description}: URL non trouvée")
        except Exception as e:
            print(f"  ⚠️ {description}: Erreur - {e}")
    
    # Vérification des fonctions de vue
    print("\n🔍 Vérification des fonctions de vue:")
    
    # Communication
    comm_functions = [
        ('envoyer_message_api', comm_views),
        ('messages_liste', comm_views),
        ('details_conversation', comm_views),
    ]
    
    for func_name, module in comm_functions:
        if hasattr(module, func_name):
            func = getattr(module, func_name)
            print(f"  ✅ {func_name}: {func.__name__} (décorateurs: {func.__decorators__ if hasattr(func, '__decorators__') else 'N/A'})")
        else:
            print(f"  ❌ {func_name}: Non trouvée")
    
except Exception as e:
    print(f"❌ Erreur vérification vues: {e}")
    print(traceback.format_exc())

# ============================================================================
# 6. VÉRIFICATION DES TEMPLATES
# ============================================================================
print("\n6. 📄 VÉRIFICATION DES TEMPLATES")
print("-" * 40)

template_dirs = [
    PROJECT_DIR / 'communication' / 'templates',
    PROJECT_DIR / 'pharmacien' / 'templates',
    PROJECT_DIR / 'templates',
]

for tpl_dir in template_dirs:
    if tpl_dir.exists():
        templates = list(tpl_dir.rglob('*.html'))
        print(f"📁 {tpl_dir.relative_to(PROJECT_DIR)}: {len(templates)} templates")
        
        # Afficher quelques templates importants
        important_templates = ['messages', 'pharmacien', 'dashboard', 'liste', 'form']
        for template in templates[:3]:  # Limiter à 3
            print(f"  • {template.relative_to(tpl_dir)}")
    else:
        print(f"❌ Dossier manquant: {tpl_dir}")

# ============================================================================
# 7. VÉRIFICATION DES FORMULAIRES
# ============================================================================
print("\n7. 📝 VÉRIFICATION DES FORMULAIRES")
print("-" * 40)

try:
    from communication.forms import MessageForm
    from pharmacien.forms import BonDeSoinForm, OrdonnanceForm
    
    print("✅ MessageForm importé")
    print("✅ BonDeSoinForm importé")
    print("✅ OrdonnanceForm importé")
    
    # Vérifier les champs
    print("\n🔍 Champs MessageForm:")
    for field_name, field in MessageForm.base_fields.items():
        required = "🔴" if field.required else "🟢"
        print(f"  {required} {field_name}: {field.__class__.__name__}")
        
except ImportError as e:
    print(f"❌ Erreur import formulaires: {e}")

# ============================================================================
# 8. VÉRIFICATION DES SIGNALS
# ============================================================================
print("\n8. 🔔 VÉRIFICATION DES SIGNALS")
print("-" * 40)

try:
    # Vérifier les fichiers signals.py
    signals_files = [
        PROJECT_DIR / 'communication' / 'signals.py',
        PROJECT_DIR / 'pharmacien' / 'signals.py',
    ]
    
    for sig_file in signals_files:
        if sig_file.exists():
            print(f"✅ {sig_file.relative_to(PROJECT_DIR)} existe")
            # Lire pour voir les signaux définis
            with open(sig_file, 'r') as f:
                content = f.read()
                if '@receiver' in content:
                    print(f"  • Contient des signaux Django")
        else:
            print(f"⚠️ {sig_file.relative_to(PROJECT_DIR)} manquant")
            
except Exception as e:
    print(f"❌ Erreur vérification signals: {e}")

# ============================================================================
# 9. TEST DES FONCTIONNALITÉS CLÉS
# ============================================================================
print("\n9. 🧪 TEST DES FONCTIONNALITÉS")
print("-" * 40)

def test_message_sending():
    """Test l'envoi de message"""
    try:
        from django.test import RequestFactory
        from communication.views import envoyer_message_api
        from django.contrib.auth.models import User
        
        factory = RequestFactory()
        
        # Créer des utilisateurs de test si besoin
        test_users = User.objects.filter(id__in=[1, 28])
        if test_users.count() >= 2:
            user1, user2 = test_users[0], test_users[1]
            
            # Préparer la requête
            data = {
                'destinataire': user2.id,
                'contenu': 'Message test diagnostic',
                'titre': 'Test Diagnostic'
            }
            
            request = factory.post('/communication/envoyer-message-api/', data)
            request.user = user1
            
            response = envoyer_message_api(request)
            
            print(f"  • Test envoi message: Status {response.status_code}")
            
            if response.status_code == 200:
                print(f"    ✅ Succès: Message envoyé")
            else:
                print(f"    ❌ Échec: {response.content.decode()}")
                
    except Exception as e:
        print(f"  ❌ Erreur test message: {e}")

def test_pharmacien_dashboard():
    """Test l'accès au dashboard pharmacien"""
    try:
        from django.test import RequestFactory
        from pharmacien.views import dashboard
        from django.contrib.auth.models import User
        
        factory = RequestFactory()
        
        # Trouver un pharmacien
        pharmacien_user = User.objects.filter(groups__name='Pharmacien').first()
        if pharmacien_user:
            request = factory.get('/pharmacien/dashboard/')
            request.user = pharmacien_user
            
            response = dashboard(request)
            
            print(f"  • Test dashboard pharmacien: Status {response.status_code}")
            
        else:
            print("  ⚠️ Aucun utilisateur pharmacien trouvé")
            
    except Exception as e:
        print(f"  ❌ Erreur test dashboard: {e}")

# Exécuter les tests
test_message_sending()
test_pharmacien_dashboard()

# ============================================================================
# 10. RECOMMANDATIONS
# ============================================================================
print("\n10. 📋 RECOMMANDATIONS")
print("-" * 40)

recommendations = [
    "✅ Vérifier que les URLs sont bien configurées dans urls.py",
    "✅ S'assurer que les templates existent aux bons emplacements",
    "✅ Vérifier les permissions des groupes Pharmacien",
    "✅ Tester l'envoi de message via l'interface web",
    "✅ Vérifier les logs Django pour les erreurs 500",
    "✅ Tester avec différents utilisateurs (admin, pharmacien, membre)",
    "✅ Vérifier la base de données pour les conversations existantes",
    "✅ S'assurer que le middleware d'authentification fonctionne",
]

for i, rec in enumerate(recommendations, 1):
    print(f"{i:2}. {rec}")

# ============================================================================
# 11. RÉSUMÉ
# ============================================================================
print("\n" + "=" * 80)
print("📊 RÉSUMÉ DU DIAGNOSTIC")
print("=" * 80)

# Collecter les problèmes potentiels
issues = []

# Vérifier la base de données
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT sqlite_version()")
        db_version = cursor.fetchone()[0]
        print(f"📦 Base de données: SQLite {db_version}")
        
        # Vérifier les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%communication%' OR name LIKE '%pharmacien%'")
        tables = cursor.fetchall()
        
        comm_tables = [t[0] for t in tables if 'communication' in t[0]]
        pharma_tables = [t[0] for t in tables if 'pharmacien' in t[0]]
        
        print(f"   Tables communication: {len(comm_tables)}")
        print(f"   Tables pharmacien: {len(pharma_tables)}")
        
        if len(comm_tables) == 0:
            issues.append("❌ Aucune table communication trouvée")
        if len(pharma_tables) == 0:
            issues.append("❌ Aucune table pharmacien trouvée")
            
except Exception as e:
    print(f"❌ Erreur vérification base: {e}")

# Vérifier les migrations
try:
    from django.db.migrations.recorder import MigrationRecorder
    recorder = MigrationRecorder.MigrationRecorder(connection)
    applied = recorder.applied_migrations()
    
    comm_migrations = [m for m in applied if m[0] == 'communication']
    pharma_migrations = [m for m in applied if m[0] == 'pharmacien']
    
    print(f"📋 Migrations appliquées:")
    print(f"   Communication: {len(comm_migrations)}")
    print(f"   Pharmacien: {len(pharma_migrations)}")
    
except Exception as e:
    print(f"⚠️ Erreur vérification migrations: {e}")

# Afficher les issues
if issues:
    print("\n🚨 PROBLÈMES IDENTIFIÉS:")
    for issue in issues:
        print(f"  {issue}")
else:
    print("\n✅ Aucun problème majeur identifié")

print("\n" + "=" * 80)
print("✨ DIAGNOSTIC TERMINÉ")
print("=" * 80)

# Générer un rapport
report_file = PROJECT_DIR / 'diagnostic_rapport.json'
try:
    report_data = {
        'timestamp': django.utils.timezone.now().isoformat(),
        'total_users': total_users,
        'conversations': total_conversations,
        'messages': total_messages,
        'pharmaciens': total_pharmaciens,
        'issues': issues
    }
    
    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2, default=str)
    
    print(f"\n📄 Rapport sauvegardé: {report_file}")
    
except Exception as e:
    print(f"⚠️ Impossible de sauvegarder le rapport: {e}")