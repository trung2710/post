from .models import *
from django.forms import ModelForm
from django import forms
class ProfileForm(ModelForm):
    
    class Meta:
        model =Profile
        #lay tat ca cac truong thong tin ngoai tru truong nao
        exclude=['user']
        labels={
            'realname':'Name'
        }
        widgets={
            'image': forms.FileInput(),
            'bio': forms.Textarea(attrs={'rows':3, 'placeholder':'Add a bio...', 'class':'front1 text-3xl'}),
        }