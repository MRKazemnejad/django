from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='pro')
    age=models.PositiveSmallIntegerField(default=0)
    title=models.CharField(max_length=100,null=True,blank=True)
