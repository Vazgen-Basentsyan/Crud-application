from django import forms
from django.forms import inlineformset_factory

from .models import User, Home, HomeImage


class UserForm(forms.ModelForm):
    class Meta:
        fields = "first_name", "last_name", "email", "age"
        model = User

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='image')

    class Meta:
        model = HomeImage
        fields = ['image',]


class HomeForm(forms.ModelForm):

    class Meta:
        fields = "__all__"
        model = Home

imageformset = inlineformset_factory(Home, HomeImage, form=ImageForm, can_delete=True, exclude=[], extra=1)
