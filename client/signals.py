from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Client


def client_profil(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get_or_create(name='visiteurs')[0]
        # Ajouter ce client a son groupe "visiteurs en mettenat instance.
        instance.groups.add(group)
        Client.objects.create(
            user=instance,
            nom=instance.username,
            mail=instance.email,
        )


post_save.connect(client_profil, sender=User)
