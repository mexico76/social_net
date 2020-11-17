from django.contrib.auth.models import User
import datetime
import os
from django.db import models
import random

import os.path
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from SocialNet.settings import THUMB_SIZE

class Album(models.Model):
    album_name = models.CharField(verbose_name='Album name', max_length=50)
    create_date_time = models.DateTimeField(verbose_name='Date of creation album', auto_now_add=True)
    modified_date_time = models.DateTimeField(verbose_name='Date of last change')
    owner = models.ForeignKey(User, verbose_name='Owner of album', on_delete=models.CASCADE)
    delete_flag = models.BooleanField(verbose_name='Was the album deleted', default=False)


def user_album_photo_path(instance, filename):
    '''make path and name to user's main photo'''
    ext = filename.split('.')[-1]
    # ramdom_number = random.randint(0, 10000)
    filename = f"{instance.album.owner}/{instance.album.album_name}/"
        # f"{datetime.datetime.now().strftime('%d.%m.%y %H:%M')}{ramdom_number}.{ext}"
    return os.path.join(f'photo/', filename)

class Photos(models.Model):
    date_time_add = models.DateTimeField(verbose_name='date when photo was add', auto_now_add=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name='Photo', upload_to=user_album_photo_path, blank=True)
    thumbnail = models.ImageField(upload_to='photo/thmb/', editable=False, default='no-image.svg')
    delite_flag = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # if not self.make_thumbnail():
            # set to a default thumbnail
            # raise Exception('Could not create thumbnail - is the file type valid?')
        self.make_thumbnail()
        super().save(*args, **kwargs)

    def make_thumbnail(self):

        image = Image.open(self.photo)
        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.photo.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        # temp_thumb.close()

        return True


