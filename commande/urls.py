from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_commande, name="list_commande"),
    path('afficher_commande', views.list_commande, name="afficher_commande"),
    path('ajouter_commande/', views.ajouter_commande, name="ajouter_commande"),
    path('modifier_commande/<str:pk>', views.modifier_commande, name="modifier_commande"),
    path('supprimer_commande/<str:pk>', views.supprimer_commande, name="supprimer_commande"),

]
