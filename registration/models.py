import os
from django.contrib.auth.models import User
import datetime
from django.db import models

def user_main_photo_path(instance, filename):
    '''make path and name to user's main photo'''
    ext = filename.split('.')[-1]
    filename = f"{instance.user}-{datetime.datetime.now().strftime('%d.%m.%y %H:%M')}.{ext}"
    return os.path.join(f'registration/main_photos/{instance.user}', filename)

class SocialUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birth_date = models.DateField(verbose_name='My Birth Date', blank=True, null=True)
    phone_number = models.CharField(max_length=15, verbose_name='The number of my phone', blank=True)
    hobbies = models.TextField(verbose_name='My hobbies', blank=True)
    school = models.TextField(verbose_name="Schools where I'm studied", blank=True)
    university = models.TextField(verbose_name="My Universities", blank=True)
    main_photo = models.ImageField(verbose_name='My photo', upload_to=user_main_photo_path, blank=True)

    '''
        Написать функцию добавляющую словарь "страна : [Список городов данной страны]"
        реализовать выбор страны/города для указания школы и института   
    '''
