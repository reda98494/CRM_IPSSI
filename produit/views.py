from django.shortcuts import render, redirect
from commande.models import Commande
from client.models import Client
from projetFormatsys.decorators import allowed_users, admin_only
from .forms import ProduitForm
from .models import Produit
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='connexion')
@admin_only
def home(request):
    commandes = Commande.objects.all()
    clients = Client.objects.all()
    context = {'commandes': commandes, 'clients': clients}
    return render(request, 'produit/acceuil.html', context)


@login_required(login_url='connexion')
@allowed_users(allowed_roles=['admin'])
def afficher_produit(request):
    produits = Produit.objects.all()
    contexte = {'produits': produits}
    return render(request, 'produit/afficher_produit.html', contexte)


@login_required(login_url='connexion')
@allowed_users(allowed_roles=['admin'])
def ajouter_produit(request):
    form = ProduitForm()
    if request.method == "POST":
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    contexte = {'form': form}
    return render(request, 'produit/ajouter_produit.html', contexte)


@login_required(login_url='connexion')
@allowed_users(allowed_roles=['admin'])
def modifier_produit(request, pk):
    produit = Produit.objects.get(id=pk)
    form = ProduitForm(instance=produit)
    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('/')

    contexte = {'form': form}
    return render(request, 'produit/ajouter_produit.html', contexte)


@login_required(login_url='connexion')
@allowed_users(allowed_roles=['admin'])
def supprimer_produit(request, pk):
    produit = Produit.objects.get(id=pk)
    if request.method == 'POST':
        produit.delete()
        return redirect('/')
    contexte = {'item': produit}
    return render(request, 'produit/supprimer_produit.html', contexte)
