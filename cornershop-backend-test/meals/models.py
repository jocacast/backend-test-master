from django.db import models
from django.db.models.fields import CharField
import uuid

# Create your models here.

class Meal (models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200, blank = True, null=True)    
    description = models.TextField(null=False, blank=False)   
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


