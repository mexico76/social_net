from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from photo.models import Photos, Album
from registration.models import SocialUser
from django.contrib.auth.models import User
from messenger.models import Messages


class UserListView(ListView):
    paginate_by = 5
    template_name = 'user_search/users_list.html'

    def get_queryset(self):
        return SocialUser.objects.all().exclude(user=self.request.user)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_readed_messages'] = Messages.objects.filter(receiver=self.request.user, reeded_flag=False).count()
        return context

class UserDetailView(DetailView):
    model = User
    context_object_name = 'person'
    template_name = 'user_search/user_detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'user'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_readed_messages'] = Messages.objects.filter(receiver=self.request.user, reeded_flag=False).count()
        context['photos'] = Photos.objects.filter(album__owner=context['object'].pk).order_by('-date_time_add')[:4]
        return context

class UserAllPhotoView(ListView):
    paginate_by = 20
    template_name = 'user_search/all_user_photos.html'
    def get_queryset(self):
        return Photos.objects.filter(album__owner=User.objects.get(username=self.kwargs['user']))
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_readed_messages'] = Messages.objects.filter(receiver=self.request.user, reeded_flag=False).count()
        last_albums = Album.objects.filter(owner=User.objects.get(username=self.kwargs['user'])).order_by('-create_date_time')[:4]
        context['albums'] = last_albums
        far_user = User.objects.get(username=self.kwargs['user'])
        context['person'] = far_user
        return context

class UserAlbumListView(ListView):
    paginate_by = 8
    template_name = 'user_search/all_user_albums.html'
    def get_queryset(self):
        return Album.objects.filter(owner=User.objects.get(username=self.kwargs['user']))
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_readed_messages'] = Messages.objects.filter(receiver=self.request.user, reeded_flag=False).count()
        far_user = User.objects.get(username=self.kwargs['user'])
        context['person'] = far_user
        return context

class UserCurentAlbomView(ListView):
    paginate_by = 20
    template_name = 'user_search/user_curent_album.html'
    def get_queryset(self):
        return Photos.objects.filter(album__owner=User.objects.get(username=self.kwargs['user'])).filter(album__pk=self.kwargs['pk'])
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_readed_messages'] = Messages.objects.filter(receiver=self.request.user, reeded_flag=False).count()
        context['pk'] = self.kwargs['pk']
        far_user = User.objects.get(username=self.kwargs['user'])
        context['person'] = far_user
        return context
