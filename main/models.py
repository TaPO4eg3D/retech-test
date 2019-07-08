from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class Organisation(models.Model):
    name = models.CharField(max_length=220)

    def __str__(self):
        return self.name


class ToDoList(models.Model):
    organization = models.ForeignKey(Organisation, on_delete=models.CASCADE)

    def __str__(self):
        return self.organization.name


class ToDo(models.Model):
    name = models.CharField(max_length=220)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = None
    organization = models.ManyToManyField(Organisation, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

