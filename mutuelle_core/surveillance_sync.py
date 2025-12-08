# surveillance_sync.py
import os
import sys
import django
import json
from datetime import datetime, timedelta
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from django.contrib.auth.models import User
from membres.models import Membre
from django.db.models import Count, Q

class SurveillantSynchronisation:
    def __init__(self):
        self.rapport = {
            'timestamp': datetime.now().isoformat(),
            'alertes': [],
            'statistiques': {},
            'recommandations': []
        }
    
    def verifier_synchronisation(self):
        """Vérifie l'état de la synchronisation"""
        print("🔍 VÉRIFICATION DE LA SYNCHRONISATION")
        print("=" * 50)
        
        # Statistiques de base
        total_users = User.objects.count()
        total_membres = Membre.objects.count()
        membres_avec_user = Membre.objects.filter(user__isnull=False).count()
        
        self.rapport['statistiques'] = {
            'utilisateurs': total_users,
            'membres': total_membres,
            'membres_avec_user': membres_avec_user,
            'taux_synchronisation': (membres_avec_user / total_membres * 100) if total_membres > 0 else 0
        }
        
        print(f"📊 Utilisateurs: {total_users}")
        print(f"📊 Membres: {total_membres}")
        print(f"📊 Membres synchronisés: {membres_avec_user}/{total_membres} ({self.rapport['statistiques']['taux_synchronisation']:.1f}%)")
        
        # Vérifications critiques
        if membres_avec_user < total_membres:
            self.rapport['alertes'].append({
                'niveau': 'CRITIQUE',
                'message': f'{total_membres - membres_avec_user} membres sans user associé',
                'action': 'Exécuter le correcteur de synchronisation'
            })
            print("🚨 ALERTE: Membres non synchronisés détectés!")
        
        # Vérifier les numéros uniques
        try:
            doublons = Membre.objects.values('numero_unique').annotate(
                count=Count('id')
            ).filter(count__gt=1, numero_unique__isnull=False)
            
            if doublons.exists():
                self.rapport['alertes'].append({
                    'niveau': 'MOYEN',
                    'message': f'{doublons.count()} numéros uniques en double',
                    'action': 'Corriger les doublons de numéros'
                })
                print("⚠️  ALERTE: Doublons de numéros détectés")
        except Exception as e:
            print(f"⚠️  Vérification doublons: {e}")
        
        # Vérifier les données manquantes
        try:
            sans_numero = Membre.objects.filter(
                Q(numero_unique__isnull=True) | Q(numero_unique='')
            ).count()
            
            if sans_numero > 0:
                self.rapport['alertes'].append({
                    'niveau': 'MOYEN',
                    'message': f'{sans_numero} membres sans numéro unique',
                    'action': 'Attribuer des numéros uniques'
                })
        except Exception as e:
            print(f"⚠️  Vérification numéros manquants: {e}")
        
        # Générer recommandations
        self._generer_recommandations()
        
        return self.rapport
    
    def _generer_recommandations(self):
        """Génère des recommandations basées sur l'état actuel"""
        stats = self.rapport['statistiques']
        
        if stats['taux_synchronisation'] < 100:
            self.rapport['recommandations'].append(
                "Exécuter le correcteur de synchronisation immédiatement"
            )
        
        if stats['membres'] > 50:
            self.rapport['recommandations'].append(
                "Planifier une maintenance des performances (indexes, pagination)"
            )
        
        # Recommandation de maintenance préventive
        self.rapport['recommandations'].append(
            "Exécuter cette surveillance hebdomadairement"
        )
    
    def sauvegarder_rapport(self):
        """Sauvegarde le rapport de surveillance"""
        nom_fichier = f"surveillance_sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(nom_fichier, 'w', encoding='utf-8') as f:
            json.dump(self.rapport, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Rapport sauvegardé: {nom_fichier}")
        return nom_fichier
    
    def afficher_resume(self):
        """Affiche un résumé du rapport"""
        print("\n" + "=" * 50)
        print("📋 RAPPORT DE SURVEILLANCE")
        print("=" * 50)
        
        stats = self.rapport['statistiques']
        print(f"🎯 État: {'✅ OPTIMAL' if stats['taux_synchronisation'] == 100 else '⚠️  ATTENTION'}")
        print(f"📊 Taux synchronisation: {stats['taux_synchronisation']:.1f}%")
        
        if self.rapport['alertes']:
            print(f"\n🚨 ALERTES ({len(self.rapport['alertes'])}):")
            for alerte in self.rapport['alertes']:
                print(f"   {alerte['niveau']}: {alerte['message']}")
                print(f"   💡 Action: {alerte['action']}")
        else:
            print("\n✅ Aucune alerte - Synchronisation optimale")
        
        if self.rapport['recommandations']:
            print(f"\n💡 RECOMMANDATIONS:")
            for reco in self.rapport['recommandations']:
                print(f"   • {reco}")
        
        print("=" * 50)

# Exécution
if __name__ == "__main__":
    surveillant = SurveillantSynchronisation()
    rapport = surveillant.verifier_synchronisation()
    surveillant.sauvegarder_rapport()
    surveillant.afficher_resume()