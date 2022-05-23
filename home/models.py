from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.CharField(max_length=300)
    slug=models.SlugField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse('home:post',kwargs={'post_id':self.id,'post_slug':self.slug})
