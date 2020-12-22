from django.db import models
from django.utils import timezone


# Create your models here.
class Label(models.Model):
    """
    Created a model class for labelling notes
    """
    name = models.CharField(max_length = 130, null = True , unique = True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default = False)

    def __str__(self):
        return self.name

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()    

       

  