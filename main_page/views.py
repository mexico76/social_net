from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.contrib.auth import login, logout, authenticate


from messenger.models import Messages
from photo.models import Photos

from .forms import LoginForm

class MainView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['not_readed_messages'] = Messages.objects.filter(receiver=self.request.user, reeded_flag=False).count()
        return context

class MainListView(ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['not_readed_messages'] = Messages.objects.filter(receiver=self.request.user, reeded_flag=False).count()
        return context

class MainDetailView(DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['not_readed_messages'] = Messages.objects.filter(receiver=self.request.user, reeded_flag=False).count()
        return context

def index(request):
    if request.user.is_authenticated :
        photos = Photos.objects.filter(album__owner=request.user).order_by('-date_time_add')[:4]
        not_readed_messages = Messages.objects.filter(receiver=request.user, reeded_flag=False).count()
    else:
        photos = ''
        not_readed_messages = ''
    form = LoginForm()
    user = request.user
    context = {'form': form, 'user':user, 'not_readed_messages':not_readed_messages, 'photos':photos}
    return render(request,'main_page/index.html', context)

class Login(View):
    form=LoginForm()
    def get(self, request):
        context = {'form':self.form}
        return render(request, 'main_page/login_form.html', context)
    def post(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # correct username and password login the user
                login(request, user)
                return redirect('index')
            else:
                context = {'form': self.form}
                return render(request, 'main_page/wrong_login.html', context)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('index')


