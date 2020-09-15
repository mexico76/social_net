from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import View

class AllPhotoView(ListView):
    pass

class AlbumListView(ListView):
    pass

class CurentAlbomView(ListView):
    pass

class AddAlbumView(View):
    pass

class AddPhotoToAlbumView(View):
    pass
