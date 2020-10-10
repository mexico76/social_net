from django.shortcuts import render, redirect
from messenger.models import Messages

from main_page.views import MainView
from .forms import EditDataFormSocialUser, EditDataFormUser
from .services import edit_user, edit_social_user, get_user_and_create_user_instance_form


class EditView(MainView):
    template_name = 'edit_data/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        get_user_and_create_user_instance_form(self.request, context)
        return context

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

