from django.contrib.auth.models import User

from photo.models import Album


def get_last_albums(self):
    last_albums = Album.objects.filter(owner=User.objects.get(username=self.kwargs['user'])).order_by(
        '-create_date_time')[:4]
    return last_albums

def get_far_user(self):
    far_user = User.objects.get(username=self.kwargs['user'])
    return far_user