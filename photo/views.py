from django.shortcuts import render, redirect
from django.views.generic.base import View

from main_page.views import MainListView, MainView
from .models import Photos, Album
from messenger.models import Messages
from .forms import CreateAlbumForm, LoadPhotosForm
from .services import last_albums, add_album, add_photo

class AllPhotoView(MainListView):
    paginate_by = 20
    template_name = 'photo/all_photos.html'
    def get_queryset(self):
        return Photos.objects.filter(album__owner=self.request.user)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['albums'] = last_albums(self.request.user)
        context['album_form'] = CreateAlbumForm
        return context

class AlbumListView(MainListView):
    paginate_by = 20
    template_name = 'photo/all_albums.html'
    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album_form'] = CreateAlbumForm
        return context

class CurentAlbomView(MainListView):
    paginate_by = 20
    template_name = 'photo/curent_album.html'
    def get_queryset(self):
        return Photos.objects.filter(album__owner=self.request.user).filter(album__pk=self.kwargs['pk'])
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['add_photo_form'] = LoadPhotosForm
        return context

class AddAlbumView(MainView):
    def post(self, request):
        form = CreateAlbumForm(request.POST)
        return add_album(form, request)

class AddPhotoToAlbumView(MainView):
    # template_name = 'photo/load_error.html'
    def post(self, request, pk):
        add_photo_form = LoadPhotosForm(request.POST, request.FILES)
        photos = request.FILES.getlist('photo')
        return add_photo(add_photo_form, photos, pk, request)

