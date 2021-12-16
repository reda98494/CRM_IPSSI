from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('afficher_produit', views.afficher_produit, name='afficher_produit'),
    path('ajouter_produit', views.ajouter_produit, name='ajouter_produit'),
    path('modifier_produit/<str:pk>', views.modifier_produit, name='modifier_produit'),
    path('supprimer_produit/<str:pk>', views.supprimer_produit, name='supprimer_produit'),

]
