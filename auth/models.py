from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, password=None):
        if not email:
            raise ValueError('Not a valid email')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.TextField()
    last_name = models.TextField()
    phone = models.CharField(max_length=15, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    date_of_birth = models.DateField()
    profession = models.CharField(max_length=100)
    address = models.TextField()
    hobby = models.CharField(max_length=100)