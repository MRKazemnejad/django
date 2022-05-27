from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegistrationForm,UserLoginForm,EditUserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
from home.models import Relation

# Create your views here.


class UserRegisterView(View):
    form_name=UserRegistrationForm
    template_name='account/register_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,{'form':self.form_name})

    def post(self,request,*args,**kwargs):
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
    def setup(self, request, *args, **kwargs):
        self.next=request.GET.get('next')
        return super().setup(request,*args,**kwargs)

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
                if self.next:
                    return redirect(self.next)
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
        is_following=False
        user=User.objects.get(pk=user_id)
        # post=Post.objects.filter(user=user)
        #using related_name
        post=user.posts.all()
        relation=Relation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            is_following=True
        return render(request,'account/profile.html',{'user':user,'posts':post,'is_following':is_following})



class UserEmailReset(auth_view.PasswordResetView):
    template_name='account/password_reset_form.html'
    success_url=reverse_lazy('account:reset_done')
    email_template_name='account/password_reset_template.html'

class UserPasswordResetDone(auth_view.PasswordResetDoneView):
    template_name='account/password_reset_done.html'


class UserPasswordResetConfirm(auth_view.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_complete')


class UserPasswordResetComplete(auth_view.PasswordResetCompleteView):
    template_name='account/password_reset_complete.html'


class EditUserProfileView(LoginRequiredMixin, View):
    form_class=EditUserProfile
    def get(self, request):
        form=self.form_class(instance=request.user.pro,initial={'email':request.user.email})
        return render(request,'account/edit_user.html',{'form':form})

    def post(self, request):
        form=self.form_class(request.POST,instance=request.user.pro)
        if form.is_valid():
            form.save()
            request.user.email=form.cleaned_data['email']
            request.user.save()
            messages.success(request,'your profile edited successfully','success')
        return redirect('account:profile',request.user.id)

