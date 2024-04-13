from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    phone = models.CharField(max_length=12)
    email = models.EmailField(_('email address'), unique=True)
    username = None
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups", 
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_user_permissions", 
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="details")
    age = models.IntegerField()
    dob = models.DateTimeField()
    profession = models.CharField(max_length=240)
    address = models.CharField(max_length=240)
    hobby = models.CharField(max_length=240)
