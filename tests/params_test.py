import pytest
from django.contrib.auth.models import Group
from produit.models import *


@pytest.fixture
def valid_form_connect():
    return {
        'username': 'reda44',
        'password': 'reda123@'
    }


@pytest.fixture
def invalid_form_connect():
    return {
        'username': 'reda44',
        'password': '47485@'
    }


@pytest.fixture
def create_admin_groupe():
    admin_group = Group.objects.get_or_create(name='admin')
    return admin_group[0]


@pytest.fixture
def check_authenticated_client(client, django_user_model):
    username = "user_1"
    password = "user_1_password"
    user = django_user_model.objects.create_user(username=username, password=password)
    return user


@pytest.fixture
def check_authenticated_super_user(client, django_user_model, create_admin_groupe):
    username = "super_user_1"
    password = "super_user_1_password"
    groupe_user = create_admin_groupe
    user = django_user_model.objects.create_superuser(username=username, password=password)
    user.groups.add(groupe_user)
    return user


@pytest.fixture
def create_tag():
    tag = Tag(nom='Apple')
    tag.save()
    return tag
