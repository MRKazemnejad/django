from django.shortcuts import render
from django.views import View
from .models import Post

# Create your views here.


class HomeView(View):
    def get(self,request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts': posts})


class PostView(View):
    def get(self,request,post_id,post_slug):
        post=Post.objects.get(pk=post_id,slug=post_slug)
        return render(request,'home/post.html',{'post':post})
