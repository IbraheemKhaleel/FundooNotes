from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


class MyUserManager(BaseUserManager):

    def create_superuser(self, first_name, last_name, user_name, email, password, **other_fields):
        """
        takes details of the user as input and if all details are valid then it will create superuser profile
        """
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(first_name= first_name, last_name=last_name, user_name=user_name, email=email, password=password, **other_fields)

    def create_user(self, email, first_name, last_name, user_name, password, **other_fields):
        """
        takes details of the user as input and if all credentials are valid then it will create user
        """
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, user_name=user_name, email=email,
                          password=password, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    user_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'