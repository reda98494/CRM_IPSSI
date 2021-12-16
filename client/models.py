from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Client(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    nom = models.CharField(max_length=50, null=True)
    telephone = models.CharField(max_length=200, null=True)
    mail = models.EmailField(max_length=200, null=True)
    photo_profil = models.ImageField(default="strd.jpg", null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.nom
