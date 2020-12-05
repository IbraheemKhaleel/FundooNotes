from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username,  password):
        if not username:
            raise ValueError('Users must have an username')
        if not password:
            raise ValueError('Users must have a password')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')


        user = self.model( username = username, first_name= first_name, last_name = last_name)

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username,  password):
        user = self.create_user(username = username, first_name= first_name, last_name= last_name, password=password, )
        user.is_admin= True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
        

class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.EmailField(max_length = 25, unique=True) 
    password = models.CharField(max_length=25)
    created = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name' , 'password' ]

    objects = MyUserManager()

    def __str__(self):
        return self.first_name

    def has_perm(self, perm, obj= None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True