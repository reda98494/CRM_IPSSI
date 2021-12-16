from django.shortcuts import render, redirect
from .forms import ClientForm
from .models import Client
from commande.filters import CommandeFiltre
from commande.models import Commande
from django.contrib.auth.decorators import login_required
from projetFormatsys.decorators import allowed_users, admin_only


# Create your views here.


@login_required(login_url='connexion')
@admin_only
def afficher_client(request):
    clients = Client.objects.all()
    contexte = {'clients': clients}
    return render(request, 'client/clients.html', contexte)


@login_required(login_url='connexion')
@admin_only
def list_client(request, pk):
    client = Client.objects.get(id=pk)
    commandes = client.commande_set.all()
    commandes_total = commandes.count()
    myFilter = CommandeFiltre(request.GET, queryset=commandes)
    commandes = myFilter.qs
    context = {'client': client, 'commandes': commandes, 'commandes_total': commandes_total,'myFilter': myFilter}
    return render(request, 'client/list_client.html', context)


@login_required(login_url='connexion')
@admin_only
def ajouter_client(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    contexte = {'form': form}
    return render(request, 'client/ajouter_client.html', contexte)


@login_required(login_url='connexion')
@admin_only
def modifier_client(request, pk):
    client = Client.objects.get(id=pk)
    # client = Client.objects.all()
    form = ClientForm(instance=client)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('/')
    contexte = {'form': form}
    return render(request, 'client/ajouter_client.html', contexte)


@login_required(login_url='connexion')
@admin_only
def supprimer_client(request, pk):
    client = Client.objects.get(id=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('/')
    contexte = {'item': client}
    return render(request, 'client/supprimer_client.html', contexte)



