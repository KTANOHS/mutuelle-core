

# Create your views here.
# pharmacie_public/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import CreateView
from django.db.models import Q

from .models import PharmaciePublic, MedicamentPublic, CommandePublic, LigneCommandePublic
from .forms import InscriptionPharmaciePublicForm, RecherchePharmacieForm

class InscriptionPharmaciePublicView(CreateView):
    model = PharmaciePublic
    form_class = InscriptionPharmaciePublicForm
    template_name = 'pharmacie_public/inscription.html'
    
    def get_success_url(self):
        return '/pharmacie-public/inscription/success/'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 
            "✅ Votre inscription a été envoyée avec succès! "
            "Notre équipe la validera sous 48 heures. "
            "Vous recevrez un email de confirmation.")
        return response

def inscription_success(request):
    return render(request, 'pharmacie_public/inscription_success.html')

def liste_pharmacies(request):
    """Page publique de recherche de pharmacies"""
    form = RecherchePharmacieForm(request.GET or None)
    pharmacies = PharmaciePublic.objects.filter(statut='actif')
    
    if form.is_valid():
        ville = form.cleaned_data.get('ville')
        code_postal = form.cleaned_data.get('code_postal')
        type_pharmacie = form.cleaned_data.get('type_pharmacie')
        de_garde = form.cleaned_data.get('de_garde')
        partenaire_mutuelle = form.cleaned_data.get('partenaire_mutuelle')
        
        if ville:
            pharmacies = pharmacies.filter(ville__icontains=ville)
        if code_postal:
            pharmacies = pharmacies.filter(code_postal__icontains=code_postal)
        if type_pharmacie:
            pharmacies = pharmacies.filter(type_pharmacie=type_pharmacie)
        if de_garde:
            pharmacies = pharmacies.filter(est_de_garde=True)
        if partenaire_mutuelle:
            pharmacies = pharmacies.filter(partenaire_mutuelle=True)
    
    # Pharmacies de garde pour affichage spécial
    pharmacies_garde = pharmacies.filter(est_de_garde=True)
    
    context = {
        'pharmacies': pharmacies,
        'pharmacies_garde': pharmacies_garde,
        'form': form,
        'total_pharmacies': pharmacies.count(),
    }
    return render(request, 'pharmacie_public/liste_pharmacies.html', context)

def detail_pharmacie(request, pk):
    """Page publique de détail d'une pharmacie"""
    pharmacie = get_object_or_404(PharmaciePublic, pk=pk, statut='actif')
    medicaments = MedicamentPublic.objects.filter(pharmacie=pharmacie, stock__gt=0)
    
    context = {
        'pharmacie': pharmacie,
        'medicaments': medicaments,
    }
    return render(request, 'pharmacie_public/detail_pharmacie.html', context)

def pharmacies_garde(request):
    """Page dédiée aux pharmacies de garde"""
    pharmacies = PharmaciePublic.objects.filter(
        statut='actif',
        est_de_garde=True
    )
    
    context = {
        'pharmacies': pharmacies,
        'title': 'Pharmacies de Garde'
    }
    return render(request, 'pharmacie_public/pharmacies_garde.html', context)

@login_required
def passer_commande(request, pharmacie_id):
    """Passer une commande (nécessite connexion)"""
    pharmacie = get_object_or_404(PharmaciePublic, id=pharmacie_id, statut='actif')
    
    if request.method == 'POST':
        medicaments_ids = request.POST.getlist('medicament_id')
        quantites = request.POST.getlist('quantite')
        
        if medicaments_ids and quantites:
            # Créer la commande
            commande = CommandePublic.objects.create(
                client=request.user,
                pharmacie=pharmacie,
                statut='en_attente'
            )
            
            # Ajouter les lignes de commande
            montant_total = 0
            for med_id, quantite in zip(medicaments_ids, quantites):
                if quantite and int(quantite) > 0:
                    try:
                        medicament = MedicamentPublic.objects.get(id=med_id, pharmacie=pharmacie)
                        if medicament.stock >= int(quantite):
                            ligne = LigneCommandePublic.objects.create(
                                commande=commande,
                                medicament=medicament,
                                quantite=int(quantite),
                                prix_unitaire=medicament.prix
                            )
                            montant_total += ligne.sous_total
                            
                            # Mettre à jour le stock
                            medicament.stock -= int(quantite)
                            medicament.save()
                        else:
                            messages.warning(request, f"Stock insuffisant pour {medicament.nom}")
                    except MedicamentPublic.DoesNotExist:
                        messages.error(request, "Médicament non trouvé")
            
            commande.montant_total = montant_total
            commande.save()
            
            messages.success(request, f"✅ Commande #{commande.numero_commande} passée avec succès!")
            return redirect('pharmacie_public:mes_commandes')
        else:
            messages.error(request, "Veuillez sélectionner au moins un médicament")
    
    medicaments = MedicamentPublic.objects.filter(pharmacie=pharmacie, stock__gt=0)
    return render(request, 'pharmacie_public/passer_commande.html', {
        'pharmacie': pharmacie,
        'medicaments': medicaments
    })

@login_required
def mes_commandes(request):
    """Voir ses commandes"""
    commandes = CommandePublic.objects.filter(client=request.user).order_by('-date_commande')
    return render(request, 'pharmacie_public/mes_commandes.html', {
        'commandes': commandes
    })

# API pour applications mobiles
def api_pharmacies_garde(request):
    """API JSON des pharmacies de garde"""
    pharmacies = PharmaciePublic.objects.filter(
        statut='actif',
        est_de_garde=True
    ).values('id', 'nom_pharmacie', 'adresse', 'ville', 'telephone', 'horaires_ouverture')
    
    return JsonResponse(list(pharmacies), safe=False)

# pharmacie_public/views_dashboard.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import PharmaciePublic, CommandePublic

@login_required
def dashboard_pharmacie(request):
    """Tableau de bord pour les pharmaciens"""
    try:
        pharmacie = PharmaciePublic.objects.get(user=request.user)
    except PharmaciePublic.DoesNotExist:
        return redirect('pharmacie_public:inscription')
    
    # Statistiques
    commandes = CommandePublic.objects.filter(pharmacie=pharmacie)
    stats = {
        'total_commandes': commandes.count(),
        'commandes_attente': commandes.filter(statut='en_attente').count(),
        'chiffre_affaires': sum(c.montant_total for c in commandes.filter(statut='retiree')),
        'medicaments_stock': pharmacie.medicaments.count(),
    }
    
    # Commandes récentes
    commandes_recentes = commandes.order_by('-date_commande')[:10]
    
    context = {
        'pharmacie': pharmacie,
        'stats': stats,
        'commandes_recentes': commandes_recentes,
    }
    return render(request, 'pharmacie_public/dashboard_pharmacie.html', context)