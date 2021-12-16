from django.shortcuts import render, redirect

from projetFormatsys.decorators import admin_only
from .forms import CommandeForm
from .models import Commande
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='connexion')
@admin_only
def list_commande(request):
    commandes = Commande.objects.all()
    contexte = {'commandes': commandes}
    return render(request, 'commande/list_commande.html', contexte)


@login_required(login_url='connexion')
@admin_only
def ajouter_commande(request):
    form = CommandeForm()
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    contexte = {'form': form}
    return render(request, 'commande/ajouter_commande.html', contexte)


@login_required(login_url='connexion')
@admin_only
def modifier_commande(request, pk):
    commande = Commande.objects.get(id=pk)
    form = CommandeForm(instance=commande)
    if request.method == 'POST':
        form = CommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            return redirect('/')
    contexte = {'form': form}
    return render(request,'commande/ajouter_commande.html', contexte)


@login_required(login_url='connexion')
@admin_only
def supprimer_commande(request, pk):
    commande = Commande.objects.get(id=pk)
    if request.method == 'POST':
        commande.delete()
        return redirect('/')
    contexte = {'item': commande}
    return render(request, 'commande/supprimer_commande.html', contexte)