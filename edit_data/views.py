from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.models import User
from registration.models import SocialUser
from messenger.models import Messages
import datetime

from .forms import EditDataFormSocialUser, EditDataFormUser
from .services import edit_user, edit_social_user


class EditView(View):
    def get(self, request):
        user = User.objects.get(username=request.user)
        social_user = SocialUser.objects.get(user__username=request.user)
        form_user = EditDataFormUser(instance=user)
        form_social_user = EditDataFormSocialUser(instance=social_user)
        not_readed_messages = Messages.objects.filter(receiver=self.request.user, reeded_flag=False).count()
        curent_date = datetime.datetime.now().strftime('%Y-%m-%d')
        min_date = datetime.datetime.now() - datetime.timedelta(days=(36500+3650))
        min_date = min_date.strftime('%Y-%m-%d')
        context = {'social_user_form':form_social_user, 'user_form':form_user, 'not_readed_messages':not_readed_messages,
                   'curent_date':curent_date, 'min_date': min_date}
        return render(request, 'edit_data/edit.html', context)

    def post(self, request):
        user_form = EditDataFormUser(request.POST)
        social_user_form = EditDataFormSocialUser(request.POST, request.FILES)
        not_readed_messages = Messages.objects.filter(receiver=self.request.user, reeded_flag=False).count()
        if request.method == 'POST' and user_form.is_valid() and social_user_form.is_valid():
            edit_user(user_form, social_user_form, request)
            edit_social_user(user_form, social_user_form, request)
            return redirect('index')
        else:
            context = {'method':request.method, 'user_form':user_form,
                       'social_user_form':social_user_form,  'not_readed_messages':not_readed_messages}
            return render(request, 'edit_data/invalid_form.html', context)