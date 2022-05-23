from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegistrationForm,UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post

# Create your views here.


class UserRegisterView(View):
    form_name=UserRegistrationForm
    template_name='account/register_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        return render(request,self.template_name,{'form':self.form_name})

    def post(self,request):
        form=self.form_name(request.POST)
        if form.is_valid():
           cd=form.cleaned_data
           User.objects.create_user(cd['username'],cd['email'],cd['password1'])
           messages.success(request,'Your account created successfully','success')
           return redirect('home:home')
        return render(request,self.template_name,{'form':form})

class UserLoginView(View):

    form_name=UserLoginForm
    template_name='account/login_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        return render(request,self.template_name,{'form':self.form_name})
    def post(self,request):
        form=self.form_name(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(username=cd['username'],password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'You login successfully','success')
                return redirect('home:home')
            messages.error(request,'username or passwor is wrong','error')
        return render(request,self.template_name,{'form':form})

class UserLogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,'You logout successfully','success')
        return redirect('home:home')

class UserProfileView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user=User.objects.get(pk=user_id)
        post=Post.objects.filter(user=user)
        return render(request,'account/profile.html',{'user':user,'posts':post})











