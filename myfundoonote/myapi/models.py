from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyUserManager(BaseUserManager):
    """
    Creating a class to create a manager for a custom user model
    """
    def create_user(self, email, username, first_name, last_name, password=None):
        """
        Creating method to creating user and also to check whether required fields are filled
        Else it will raise error
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not first_name:
            raise ValueError('Users must specify a first name')  
        if not last_name:
            raise ValueError('Users must specify a last name') 

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name,last_name, password):
        """
        Creating method for creating super user
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True #super user is set as admin,staff,superuser by default
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
 

class User(AbstractBaseUser):
    """
    Creating class for creating custom user model by inheriting AbstractBaseUser class
    """
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name' ,'last_name'] #these are the required fields while creating superuser

    objects = MyUserManager()

    def __str__(self):
    	return self.email

	# For checking permissions. 
    def has_perm(self, perm, obj=None):
    	return self.is_admin

	
    def has_module_perms(self, app_label):
    	return True
