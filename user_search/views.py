from django.views.generic.list import ListView

from main_page.views import MainListView, MainDetailView
from photo.models import Photos, Album
from registration.models import SocialUser
from django.contrib.auth.models import User
from messenger.models import Messages
from .services import get_last_albums, get_far_user


class UserListView(MainListView):
    paginate_by = 10
    template_name = 'user_search/users_list.html'
    def get_queryset(self):
        return SocialUser.objects.all().exclude(user=self.request.user)

class UserDetailView(MainDetailView):
    model = User
    context_object_name = 'person'
    template_name = 'user_search/user_detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'user'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = Photos.objects.filter(album__owner=context['object'].pk).order_by('-date_time_add')[:4]
        return context

class UserAllPhotoView(MainListView):
    paginate_by = 20
    template_name = 'user_search/all_user_photos.html'
    def get_queryset(self):
        return Photos.objects.filter(album__owner=User.objects.get(username=self.kwargs['user']))
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['albums'] = get_last_albums(self)
        context['person'] = get_far_user(self)
        return context

class UserAlbumListView(MainListView):
    paginate_by = 8
    template_name = 'user_search/all_user_albums.html'
    def get_queryset(self):
        return Album.objects.filter(owner=User.objects.get(username=self.kwargs['user']))
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person'] = get_far_user(self)
        return context

class UserCurentAlbomView(MainListView):
    paginate_by = 20
    template_name = 'user_search/user_curent_album.html'
    def get_queryset(self):
        return Photos.objects.filter(album__owner=User.objects.get(username=self.kwargs['user'])).filter(album__pk=self.kwargs['pk'])
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['person'] = get_far_user(self)
        return context
