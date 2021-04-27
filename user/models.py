from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django import forms
# Create your models here.

class CustomUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, phone_num, address, password=None,):
        if not email:
            raise ValueError("Users must have an email!")
        if not first_name:
            raise ValueError("Users must have a first name!")
        if not last_name:
            raise ValueError("Users must have a last name!")
        if not phone_num:
            raise ValueError("Users must have a phone number!")
        if not address:
            raise ValueError("Users must have an address!")

        user = self.model(
            email=self.normalize_email(email),
            first_name= first_name,
            last_name = last_name,
            phone_num = phone_num,
            address = address
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, first_name, last_name, phone_num, address):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name= first_name,
            last_name = last_name,
            phone_num = phone_num,
            address = address,
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    username = None
    email = models.EmailField(verbose_name="email", unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=15)
    address = models.CharField(max_length=1000, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_num', 'address']

    def __str__(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_num', 'address']