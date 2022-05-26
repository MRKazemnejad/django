from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .models import Post,Relation
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostUpdateView,CommentFormView
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.


class HomeView(View):
    def get(self,request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts': posts})


class PostView(View):
    form_class=CommentFormView
    def setup(self,request,*args,**kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request,*args,**kwargs)

    def get(self,request,*args,**kwargs):
        # post=Post.objects.get(pk=post_id,slug=post_slug)
        # post=get_object_or_404(Post,pk=post_id,slug=post_slug)
        comments=self.post_instance.comment_post.filter(is_replay=False)
        return render(request,'home/post.html',{'post':self.post_instance,'comments':comments,'form':self.form_class})
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            new_form=form.save(commit=False)
            new_form.user=request.user
            new_form.post=self.post_instance
            new_form.save()
            messages.success(request,'your comments save successfully','success')
            return redirect('home:post',self.post_instance.id,self.post_instance.slug)

class DeleteView(LoginRequiredMixin,View):
    def get(self,request,*arge,**kwargs):
        post=Post.objects.get(pk=kwargs['post_id'])
        if post.user.id==request.user.id:
            post.delete()
            messages.success(request,'Your post deleted successfully','success')
        else:
            messages.error(request,'Your cann\'t delete this post')
        return redirect('home:home')


class UpdateView(LoginRequiredMixin,View):
    form_class=PostUpdateView

    def setup(self, request, *args, **kwargs):
        self.post_instans = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request,*args,**kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instans
        if not request.user.id == post.user.id:
            messages.error(request, 'you can not update post', 'error')
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request,*args,**kwargs):
        post=self.post_instans
        form=self.form_class(instance=post)
        return render(request,'home/update.html',{'form':form})

    def post(self,request,*args,**kwargs):
        post=self.post_instans
        form=self.form_class(request.POST,instance=post)
        if form.is_valid():
            new_data=form.save(commit=False)
            new_data.slug=slugify(form.cleaned_data['body'][:20])
            new_data.save()
            messages.success(request,'your post updated successfully','success')
            return redirect('home:home')
        else:
            messages.error(request,'wrong data','error')
            return redirect('home:home')



class FollowView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user=User.objects.get(pk=user_id)
        relation=Relation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            messages.error(request,'you followed this person before','error')
        else:
            Relation(from_user=request.user,to_user=user).save()
            messages.success(request,'you followed successfully')
        return redirect('home:home')


class UnFollowView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user=User.objects.get(pk=user_id)
        relation=Relation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request,'you unfollowed successfully','success')
        else:
            messages.error(request,'you did not follow this person yet!','error')
        return redirect('home:home')

