from colorfield.fields import ColorField
from django.db import models
from django.utils import timezone
from myfundooNotes.models import User
from Label.models import Label


class Note(models.Model):
    """
    Created a model class for Notes to store respective fields
    
    """
    user = models.ForeignKey(User , on_delete = models.CASCADE , related_name = 'author', null = True) #name of user
    deleted_at = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length = 50, blank = True)
    description = models.TextField(blank = True)
    reminder = models.DateTimeField(null = True, blank = True)
    color = ColorField(default='#FFFFFF')
    image = models.ImageField(upload_to = 'notes/', null = True,blank = True)
    collaborators = models.ManyToManyField(User , related_name = 'collaborator',  blank = True)#It connects with User model class we defined in myfundooNotes file
    labels = models.ManyToManyField(Label, blank= True) #This connects Label model class we defined above 
    is_archived = models.BooleanField(default = False, blank = True)
    is_deleted = models.BooleanField(default = False)
    is_pinned = models.BooleanField(default = False, blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()    

    
