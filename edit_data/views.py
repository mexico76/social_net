from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError


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
        if user_form.is_valid() and social_user_form.is_valid():
            edit_user(user_form, social_user_form, request)
            edit_social_user(user_form, social_user_form, request)
            return redirect('index')
        else:
            context = {'user_form':user_form,
                       'social_user_form':social_user_form}
            return render(request, 'edit_data/invalid_form.html', context)

