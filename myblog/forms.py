from django import forms
from myblog.models import Comment
from captcha.fields import CaptchaField
from myblog.models import Post 

class CommentForm(forms.ModelForm):
     post = forms.ModelChoiceField(queryset=Post.objects.all(), widget=forms.HiddenInput())

     class Meta:
            model = Comment
            fields = ['post','name','email','subject', 'message']