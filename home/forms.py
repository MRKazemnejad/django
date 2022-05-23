from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post


class PostUpdateView(forms.ModelForm):
    class Meta:
        model=Post
        fields=('body',)

