from django.db import models
from client.models import Client
from produit.models import Produit


# Create your models here.


# Ici on a crée une relation 1 2 many de telle sorte qu'une commande peut contenir plusieurs produits et qu'un client
# peut avoir plusieures commandes


class Commande(models.Model):
    STATUS = (('en instance', 'en instance'),
              ('non livré', 'non livré'),
              ('livré', 'livré'))
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    produit = models.ForeignKey(Produit, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=50, null=True, choices=STATUS)
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
