from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from .managers import UserManager


class Organisation(models.Model):
    name = models.CharField(max_length=220)

    def __str__(self):
        return self.name


class ToDoList(models.Model):
    name = models.CharField(max_length=220)
    organization = models.ForeignKey(Organisation, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.organization.name, self.name)


class ToDo(models.Model):
    description = models.TextField()
    list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.description


class CustomAuthToken(TokenAuthentication):
    keyword = 'Bearer'


class User(AbstractUser):
    username = None
    organizations = models.ManyToManyField(Organisation, blank=True)
    active_organization = models.ForeignKey(Organisation, blank=True, null=True, on_delete=models.SET_NULL,
                                            related_name='active_organization')
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

