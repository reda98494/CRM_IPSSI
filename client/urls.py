from django.urls import path
from . import views

urlpatterns = [
    path('<str:pk>/', views.list_client, name="list_client"),
    path('afficher_client', views.afficher_client, name="afficher_client"),
    path('ajouter_client', views.ajouter_client, name="ajouter_client"),
    path('modifier_client/<str:pk>', views.modifier_client, name="modifier_client"),
    path('supprimer_client/<str:pk>', views.supprimer_client, name="supprimer_client"),

]
