from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post,Comment


class PostUpdateView(forms.ModelForm):
    class Meta:
        model=Post
        fields=('body',)


class CommentFormView(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('body',)
        widgets={
            'body':forms.Textarea(attrs={'class':'form-control'})
        }

class CommentReplayFormView(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('body',)

class SearchFormView(forms.Form):
    search=forms.CharField(max_length=200)
