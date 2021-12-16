# Generated by Django 3.1.4 on 2020-12-16 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('en instance', 'en instance'), ('non livré', 'non livré'), ('livré', 'livré')], max_length=50, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
