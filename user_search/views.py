from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
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
        return context

