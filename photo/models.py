from django.contrib.auth.models import User
import datetime
import os
from django.db import models

class Album(models.Model):
    album_name = models.CharField(verbose_name='Album name')
    create_date_time = models.DateTimeField(verbose_name='Date of creation album', auto_now_add=True)
    modified_date_time = models.DateTimeField(verbose_name='Date of last change')
    owner = models.ForeignKey(User, verbose_name='Owner of album', on_delete=models.CASCADE)
    delete_flag = models.BooleanField(verbose_name='Was the album deleted')


def user_album_photo_path(instance, filename, album):
    '''make path and name to user's main photo'''
    ext = filename.split('.')[-1]
    filename = f"{instance.user}-{album}-{datetime.datetime.now().strftime('%d.%m.%y %H:%M')}.{ext}"
    return os.path.join(f'registration/main_photos/{instance.user}', filename)

class Photos(models.Model):
    date_time_add = models.DateTimeField(verbose_name='date when photo was add', auto_now_add=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name='Photo', upload_to=user_album_photo_path(album=album), blank=False)
    delite_flag = models.BooleanField(default=False)

