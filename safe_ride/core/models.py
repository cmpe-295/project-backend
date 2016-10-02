from __future__ import unicode_literals

from django.db import models

from .managers import SiteUserManager

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class SiteUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = SiteUserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Driver(models.Model):
    user = models.OneToOneField(SiteUser, related_name='driver')


class Client(models.Model):
    user = models.OneToOneField(SiteUser, related_name='client')
    sjsu_id = models.CharField(max_length=15)
    email_verified = models.BooleanField(default=False)
