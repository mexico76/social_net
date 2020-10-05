from django import forms
from django.forms import ClearableFileInput
from .models import Photos

class CreateAlbumForm(forms.Form):
    album_name = forms.CharField(max_length=50,min_length=3)


class LoadPhotosForm(forms.Form):
    photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    # photo = forms.ImageField()
    # class Meta:
    #     model = Photos
    #     fields = ['photo']
    #     widgets = {'photo': ClearableFileInput(attrs={'multiple': True}),}