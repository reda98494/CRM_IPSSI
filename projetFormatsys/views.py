from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .decorators import unauthenticated_user, allowed_users
from .forms import CreationUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from client.forms import ClientForm


@unauthenticated_user
def inscription(request):
    form = CreationUserForm()
    if request.method == "POST":
        form = CreationUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            # Ancienne méthode avant de mettre en place le sys de signals
            # group = Group.objects.get(name='visiteurs')
            # user.groups.add(group)
            # Client.objects.create(
            #     user=user,
            #     nom=user.username,
            #     mail=user.email,
            # )
            messages.success(request, "Votre compte a bien été créé " + username)
            return redirect('connexion')
    contexte = {'form': form}
    return render(request, 'inscription.html', contexte)


@unauthenticated_user
def connexion(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, "Nom d'utilisateur ou mot de passe incorrect")
    return render(request, 'connexion.html')


def deconnexion(request):
    logout(request)
    return redirect('connexion')


@login_required(login_url='connexion')
@allowed_users(allowed_roles=['visiteurs'])
def utilisateur(request):
    commandes = request.user.client.commande_set.all()
    total_commandes = commandes.count()
    commandes_livrees = commandes.filter(status='livré').count()
    contexte = {'commandes': commandes, 'total_commandes': total_commandes, 'commandes_livrees': commandes_livrees}
    return render(request, 'utilisateur.html', contexte)


@login_required(login_url='connexion')
@allowed_users(allowed_roles=['visiteurs'])
def accountSettings(request):
    client = request.user.client
    form = ClientForm(instance=client)
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
    contexte = {'form': form}
    return render(request, 'account_settings.html', contexte)
