from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth import login, logout, authenticate
from messenger.models import Messages


from .forms import LoginForm


def index(request):
    if request.user.is_authenticated :
        not_readed_messages = Messages.objects.filter(receiver=request.user, reeded_flag=False).count()
    else:
        not_readed_messages = ''
    form = LoginForm()
    user = request.user
    context = {'form': form, 'user':user, 'not_readed_messages':not_readed_messages}
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


