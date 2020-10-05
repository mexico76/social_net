from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.base import View
from datetime import datetime
from django.views.generic.edit import FormView

from .models import Photos, Album
from messenger.models import Messages
from .forms import CreateAlbumForm, LoadPhotosForm

class AllPhotoView(ListView):
    paginate_by = 20
    template_name = 'photo/all_photos.html'
    def get_queryset(self):
        return Photos.objects.filter(album__owner=self.request.user)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_readed_messages'] = Messages.objects.filter(receiver=self.request.user, reeded_flag=False).count()
        last_albums = Album.objects.filter(owner=self.request.user).order_by('-create_date_time')[:4]
        context['albums'] = last_albums
        context['album_form'] = CreateAlbumForm
        return context

class AlbumListView(ListView):
    paginate_by = 20
    template_name = 'photo/all_albums.html'
    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_readed_messages'] = Messages.objects.filter(receiver=self.request.user, reeded_flag=False).count()
        context['album_form'] = CreateAlbumForm
        return context

class CurentAlbomView(ListView):
    paginate_by = 20
    template_name = 'photo/curent_album.html'
    def get_queryset(self):
        return Photos.objects.filter(album__owner=self.request.user).filter(album__pk=self.kwargs['pk'])
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_readed_messages'] = Messages.objects.filter(receiver=self.request.user, reeded_flag=False).count()
        context['pk'] = self.kwargs['pk']
        context['add_photo_form'] = LoadPhotosForm
        context['album_form'] = CreateAlbumForm
        return context

class AddAlbumView(View):
    def post(self, request):
        form = CreateAlbumForm(request.POST)
        if form.is_valid():
            new_album = Album.objects.create(album_name=form.cleaned_data.get('album_name'),
                                             modified_date_time=datetime.now(), owner=self.request.user)
            new_album.save()
            slug = form.cleaned_data.get('album_name')
            return redirect('curent_album', new_album.pk)
        else:
            not_readed_messages = Messages.objects.filter(receiver=self.request.user, reeded_flag=False).count()
            context = {'album_form':form, 'not_readed_messages':not_readed_messages}
            return render(request, 'photo/create_new_album_error.html', context)

class AddPhotoToAlbumView(View):
    def post(self, request, pk):
        add_photo_form = LoadPhotosForm(request.POST, request.FILES)
        photo = request.FILES.getlist('photo')
        if add_photo_form.is_valid():
            for single_photo in photo:
                album = Album.objects.get(pk=pk)
                curent_photo = Photos.objects.create(photo=single_photo, album=album)
                curent_photo.save()
            return redirect('curent_album', pk)
        else:
            not_readed_messages = Messages.objects.filter(receiver=self.request.user, reeded_flag=False).count()
            context = {'add_photo_form': add_photo_form, 'album':pk, 'not_readed_messages':not_readed_messages}
            return render(request, 'photo/load_error.html', context)

