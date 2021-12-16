from django.urls import reverse
from .params_test import *
from client.models import *
from commande.models import *

"""Test 1er exemple"""


@pytest.mark.django_db
def test_user_create():
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    assert User.objects.count() == 1


def test_with_authenticated_client(check_authenticated_client, client):
    username = check_authenticated_client.username
    password = "user_1_password"
    is_super_user = check_authenticated_client.is_superuser
    current_user_loged_in = client.login(username=username, password=password)
    print("\t user: {}, is_superuser: {} , TEST OK ACCES AUTORISE A UN COMPTE CLIENT AVEC DES LOGINS & PASSWORD CLIENT \t".format(username, check_authenticated_client.is_superuser))
    assert is_super_user == False
    response = client.get('/utilisateur/')
    assert response.status_code == 200


"""
Invalide authentification, tentative d'accès au pannel réservé au super user
Redirection vers la page /utilisateur/ réservée à un simple user
"""


def test_invalid_with_authenticated_client(check_authenticated_client, client):
    username = check_authenticated_client.username
    password = "user_1_password"
    is_super_user = check_authenticated_client.is_superuser
    current_user_loged_in = client.login(username=username, password=password)
    print("\t user: {}, is_superuser: {} , TEST OK ACCES NON AUTORISE A UN COMPTE ADMIN AVEC DES LOGINS & PASSWORD CLIENT NON ADMIN \t".format(username, check_authenticated_client.is_superuser))
    assert is_super_user == False
    response = client.get('/')
    assert response.status_code == 302


def test_with_authenticated_super_user(check_authenticated_super_user, client):
    username = check_authenticated_super_user.username
    password = "super_user_1_password"
    is_super_user = check_authenticated_super_user.is_superuser
    current_super_user_loged_in = client.login(username=username, password=password)
    url = reverse(
        'home',
    )
    print("\t user: {}, is_superuser: {} , TEST OK ACCES AUTORISE A UN COMPTE ADMIN AVEC DES LOGINS & PASSWORD ADMIN \t".format(username, check_authenticated_super_user.is_superuser))
    assert is_super_user
    response = client.get('/')
    assert response.status_code == 200


"""
Invalide authentification, tentative d'accès au pannel réservé aux clients
Renvoie un message d'erreur comme quoi l'accès n'est pas autorisé
"""


def test_invalid_with_authenticated_super_user(check_authenticated_super_user, client):
    username = check_authenticated_super_user.username
    password = "super_user_1_password"
    is_super_user = check_authenticated_super_user.is_superuser
    current_super_user_loged_in = client.login(username=username, password=password)
    url = reverse(
        'home',
    )
    print("\t user: {}, is_superuser: {} , TEST OK ACCES NON AUTORISE A UN COMPTE CLIENT AVEC DES LOGINS & PASSWORD ADMIN, ERROR MESSAGE EN RETOUR \t".format(username, check_authenticated_super_user.is_superuser))
    assert is_super_user
    response = client.get('/utilisateur/')
    assert response.status_code == 200
    assert "Vous n'avez le droit d'y accéder" in response.content.decode("utf-8")


"""
Création de Produit, check authentification & ALLOWED_USERS = [admin_only]
"""


def test_product_create(check_authenticated_super_user, client):
    username = check_authenticated_super_user.username
    password = "super_user_1_password"
    is_super_user = check_authenticated_super_user.is_superuser
    current_super_user_loged_in = client.login(username=username, password=password)
    url = reverse(
        'home',
    )
    print("\t user: {}, is_superuser: {} , TEST OK AUTORISATION DE CREATION D'UN PRODUIT SSI AUTHENTIFIER AVEC UN COMPTE ADMIN \t".format(username, check_authenticated_super_user.is_superuser))
    assert is_super_user
    response = client.get('/')
    assert response.status_code == 200
    assert ' <a class="nav-link" href="/afficher_produit">Produits</a>' in response.content.decode("utf-8")
    products_response = client.get('/afficher_produit')
    assert products_response.status_code == 200
    assert '<a class="btn btn-primary  btn-sm btn-block" href="/ajouter_produit">Ajouter un produit</a>' in products_response.content.decode(
        "utf-8")
    add_product_response = client.get('/ajouter_produit')
    assert add_product_response.status_code == 200
    response_off = client.post('/ajouter_produit', data={"nom": 'tv11', 'prix': '2.99', 'tag': 'Apple'})
    assert response_off.status_code == 200 or response_off.status_code == 302
    response_acceuill = client.get('/')
    assert response_acceuill.status_code == 200


"""
Invalide tentative de création de produit, si authentitifé & qu'il n'est pas admin
"""


def test_invalid_product_create_not_admin(check_authenticated_client, client):
    username = check_authenticated_client.username
    password = "user_1_password"
    is_super_user = check_authenticated_client.is_superuser
    current_user_loged_in = client.login(username=username, password=password)
    print("\t user: {}, is_superuser: {} , TEST OK AUTORISATION REFUSEE DE CREATION D'UN PRODUIT SI AUTHENTIFIER AVEC UN COMPTE NON ADMIN, REDIRECTION A UNE PAGE AUTHORISEE D'ACCESS DEPUIS UN COMPTE CLIENT \t".format(username, check_authenticated_client.is_superuser))
    assert is_super_user == False
    response = client.get('/')
    assert response.status_code == 302
    redirect_response = client.get('/utilisateur/')
    assert redirect_response.status_code == 200
    assert ' <a class="nav-link" href="/afficher_produit">Produits</a>' not in redirect_response.content.decode("utf-8")


"""
Création de client, check authentification & ALLOWED_USERS = [admin_only]
"""


def test_client_create(check_authenticated_super_user, client):
    username = check_authenticated_super_user.username
    password = "super_user_1_password"
    is_super_user = check_authenticated_super_user.is_superuser
    current_super_user_loged_in = client.login(username=username, password=password)
    url = reverse(
        'home',
    )
    print("\t user: {}, is_superuser: {} , TEST OK AUTORISATION DE CREATION D'UN CLIENT SSI AUTHENTIFIER AVEC UN COMPTE ADMIN \t".format(username, check_authenticated_super_user.is_superuser))
    assert is_super_user
    response = client.get('/')
    assert response.status_code == 200
    assert '<a class="nav-link" href="/client/afficher_client">Clients</a>' in response.content.decode("utf-8")
    clients_response = client.get('/client/afficher_client')
    assert clients_response.status_code == 200
    assert '<a class="btn btn-primary  btn-sm btn-block" href="/client/ajouter_client">Créer Un Client</a>' in clients_response.content.decode(
        "utf-8")
    add_client_response = client.get('/client/ajouter_client')
    assert add_client_response.status_code == 200
    response_off = client.post('/client/ajouter_client',
                               data={"nom": 'john', "telephone": '03426965233', "mail": 'john@gmail.com', "user": '1'})
    assert response_off.status_code == 200 or response_off.status_code == 302
    response_acceuill = client.get('/')
    assert response_acceuill.status_code == 200


"""
Invalide tentative de création de client, si authentitifé & qu'il n'est pas admin
"""


def test_invalid_client_create_not_admin(check_authenticated_client, client):
    username = check_authenticated_client.username
    password = "user_1_password"
    is_super_user = check_authenticated_client.is_superuser
    current_user_loged_in = client.login(username=username, password=password)
    print("\t user: {}, is_superuser: {} , TEST OK AUTORISATION REFUSEE DE CREATION D'UN CLIENT SI AUTHENTIFIER AVEC UN COMPTE NON ADMIN, REDIRECTION A UNE PAGE AUTHORISEE D'ACCESS DEPUIS UN COMPTE CLIENT \t".format(username, check_authenticated_client.is_superuser))
    assert is_super_user == False
    response = client.get('/')
    assert response.status_code == 302
    redirect_response = client.get('/utilisateur/')
    assert redirect_response.status_code == 200
    assert ' <a class="nav-link" href="/afficher_produit">Produits</a>' not in redirect_response.content.decode("utf-8")


"""
Création de commande, check authentification & ALLOWED_USERS = [admin_only]
"""


def test_order_create(check_authenticated_super_user, client, create_tag):
    product = Produit(nom="tv_HD", prix=2.99)
    product.save()
    product.tag.add(create_tag)
    product.save()
    username = check_authenticated_super_user.username
    password = "super_user_1_password"
    is_super_user = check_authenticated_super_user.is_superuser
    current_super_user_loged_in = client.login(username=username, password=password)
    url = reverse(
        'home',
    )
    print("\t user: {}, is_superuser: {} , TEST OK AUTORISATION DE CREATION D'UNE COMMANDE SSI AUTHENTIFIER AVEC UN COMPTE ADMIN \t".format(check_authenticated_super_user.username, check_authenticated_super_user.is_superuser))

    assert is_super_user
    response = client.get('/')
    assert response.status_code == 200
    assert '<a class="nav-link" href="/commande/afficher_commande">Commandes</a>' in response.content.decode("utf-8")
    commandes_response = client.get('/commande/afficher_commande')
    assert commandes_response.status_code == 200
    assert '<a class="btn btn-primary  btn-sm btn-block" href="/commande/ajouter_commande/">Ajouter une Commande</a>' in commandes_response.content.decode(
        "utf-8")
    add_commande_response = client.get('/commande/ajouter_commande/')
    assert add_commande_response.status_code == 200
    response_off = client.post('/commande/ajouter_commande/',
                               data={"status": 'livré', "produit": product, "client": check_authenticated_super_user})
    assert response_off.status_code == 200 or response_off.status_code == 302
    response_acceuill = client.get('/')
    assert response_acceuill.status_code == 200


"""
Invalide tentative de création de commande, si authentitifé & qu'il n'est pas admin
"""


def test_invalid_order_create_not_admin(check_authenticated_client, client):
    username = check_authenticated_client.username
    password = "user_1_password"
    is_super_user = check_authenticated_client.is_superuser
    current_user_loged_in = client.login(username=username, password=password)
    print("\t user: {}, is_superuser: {} , TEST OK AUTORISATION REFUSEE DE CREATION D'UNE COMMANDE SI AUTHENTIFIER AVEC UN COMPTE NON ADMIN, REDIRECTION A UNE PAGE AUTHORISEE D'ACCESS DEPUIS UN COMPTE CLIENT \t".format(username, check_authenticated_client.is_superuser))

    assert is_super_user == False
    response = client.get('/')
    assert response.status_code == 302
    redirect_response = client.get('/utilisateur/')
    assert redirect_response.status_code == 200
    assert ' <a class="nav-link" href="/commande/afficher_commande">Commandes</a>' not in redirect_response.content.decode(
        "utf-8")


"""
Affichage du dashboard d'un client authentifié, avec touts ses commandes en cours, passées ...etc
"""


def test_orders_client(check_authenticated_client, client, create_tag):
    product = Produit(nom="tv_HD", prix=2.99)
    product.save()
    product.tag.add(create_tag)
    product.save()
    cli = Client.objects.get(user=check_authenticated_client)
    commande = Commande(status='livré', client=cli, produit=product)
    commande.save()
    username = check_authenticated_client.username
    password = "user_1_password"
    is_super_user = check_authenticated_client.is_superuser
    current_user_loged_in = client.login(username=username, password=password)
    print("\t user: {}, is_superuser: {} , TEST OK AUTORISATION ACCEES A SON COMPTE SSI AUTHENTIFIER AVEC UN COMPTE CLIENT, AFFICHAGE DU DASHBOARD AVEC TOUTES LES COAMMNDES \t".format(username, check_authenticated_client.is_superuser))

    assert is_super_user == False
    response = client.get('/utilisateur/')
    assert response.status_code == 200
    assert '<th>tv_HD</th>' in response.content.decode("utf-8")


"""
Update du profile d'un client, une fois connecté sur son propre compte
"""


def test_update_client_profile(check_authenticated_client, client):
    username = check_authenticated_client.username
    password = "user_1_password"
    is_super_user = check_authenticated_client.is_superuser
    cli = Client.objects.get(user=check_authenticated_client)
    cli.nom = 'user1'
    cli.telephone = '023569963'
    cli.mail = 'user1@gmail.com'
    cli.save(update_fields=['nom', 'telephone', 'mail'])
    current_user_loged_in = client.login(username=username, password=password)
    print("\t user: {}, is_superuser: {} , TEST OK AUTORISATION ACCEES A SON COMPTE SSI AUTHENTIFIER AVEC UN COMPTE CLIENT, UPDATE AUTHORISER DES SES INFORMATIONS PERSONNELLES \t".format(username, check_authenticated_client.is_superuser))
    assert is_super_user == False
    response = client.get('/utilisateur/')
    assert response.status_code == 200
    assert ' <a class="nav-link" href="/compte/">Mon profil</a>' in response.content.decode("utf-8")
    profil_response = client.get('/compte/')
    assert profil_response.status_code == 200
    response_off = client.post('/compte/', data={"nom": 'USER1', "telephone": '0758963623'})
    assert response_off.status_code == 200
