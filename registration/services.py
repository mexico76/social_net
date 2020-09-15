from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate, login

from .models import SocialUser

def create_new_user(reg_form, request):
    try:
        user = User.objects.create_user(username=reg_form.cleaned_data.get('user_login'),
                                        email=reg_form.cleaned_data.get('user_email'),
                                        password=reg_form.cleaned_data.get('user_password'),
                                        first_name=reg_form.cleaned_data.get('user_name'),
                                        last_name=reg_form.cleaned_data.get('user_surname'), )
        return user
    except Exception as inst:
        context = {'error_message': inst, 'registration_form': reg_form}
        return render(request, 'registration/bad_request.html', context)


def create_new_social_user(user, request, reg_form):
    try:
        social_user = SocialUser.objects.create(user=user, main_photo=request.FILES['user_main_photo'], )
        # birth_date='1900-01-01')
        social_user.save()

    except Exception as error_creating_social_user:
        if User.objects.get(username=reg_form.cleaned_data['user_login']).exists():
            user_to_delete = User.objects.get(username=user.username)
            user_to_delete.delete()
            context = {'error_message': error_creating_social_user, 'registration_form': reg_form}
            return render(request, 'registration/bad_request.html', context)

def new_user_auto_loging(reg_form, request):
    new_user = authenticate(username=reg_form.cleaned_data['user_login'],
                            password=reg_form.cleaned_data['user_password'],
                            )
    login(request, new_user)