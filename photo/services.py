from django.shortcuts import redirect, render

from messenger.models import Messages
from photo.models import Album, Photos
from datetime import datetime


def last_albums(user):
    last_albums = Album.objects.filter(owner=user).order_by('-create_date_time')[:4]
    return last_albums

def add_album(form, request):
    if form.is_valid():
        new_album = Album.objects.create(album_name=form.cleaned_data.get('album_name'),
                                         modified_date_time=datetime.now(), owner=request.user)
        new_album.save()
        return redirect('curent_album', new_album.pk)
    else:
        context = {'album_form': form}
        return render(request, 'photo/create_new_album_error.html', context)

def add_photo(add_photo_form, photos, pk, request):
    if add_photo_form.is_valid():
        for single_photo in photos:
            album = Album.objects.get(pk=pk)
            curent_photo = Photos.objects.create(photo=single_photo, album=album)
            curent_photo.save()
        return redirect('curent_album', pk)
    else:
        context = {'add_photo_form': add_photo_form, 'pk': pk}
        return render(request, 'photo/load_error.html', context)