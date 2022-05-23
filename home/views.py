from django.shortcuts import render,redirect
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# Create your views here.


class HomeView(View):
    def get(self,request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts': posts})


class PostView(View):
    def get(self,request,post_id,post_slug):
        post=Post.objects.get(pk=post_id,slug=post_slug)
        return render(request,'home/post.html',{'post':post})

class DeleteView(LoginRequiredMixin,View):
    def get(self,request,*arge,**kwargs):
        post=Post.objects.get(pk=kwargs['post_id'])
        if post.user.id==request.user.id:
            post.delete()
            messages.success(request,'Your post deleted successfully','success')
        else:
            messages.error(request,'Your cann\'t delete this post')
        return redirect('home:home')
    def post(self,request,*arge,**kwargs):
        pass



