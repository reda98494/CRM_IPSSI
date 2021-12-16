# Generated by Django 3.1.4 on 2020-12-29 10:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0004_client_mail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='mail',
            field=models.EmailField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='photo_profil',
            field=models.ImageField(blank=True, default='strd.jpg', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='client',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
