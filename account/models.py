from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class NewUser(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    age=models.PositiveSmallIntegerField(default=0)
    title=models.CharField(max_length=100)
