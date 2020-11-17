from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
import datetime
from django.core.exceptions import ValidationError

from edit_data.forms import EditDataFormUser, EditDataFormSocialUser
from registration.models import SocialUser

def get_user_and_create_user_instance_form(request, context):
    context['user'] = User.objects.get(username=request.user)
    context['social_user'] = SocialUser.objects.get(user__username=request.user)
    context['user_form'] = EditDataFormUser(instance=context['user'])
    context['social_user_form'] = EditDataFormSocialUser(instance=context['social_user'])
    context['curent_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
    min_date = datetime.datetime.now() - datetime.timedelta(days=(36500 + 3650))
    context['min_date'] = min_date.strftime('%Y-%m-%d')
    return context

def edit_user(user_form, social_user_form, request):
    try:
        user = User.objects.get(username=request.user)
        user.first_name = user_form.cleaned_data.get('first_name')
        user.last_name = user_form.cleaned_data.get('last_name')
        email_in_form = user_form.cleaned_data.get('email')
        if email_in_form==user.email:
            pass
        elif User.objects.filter(email=email_in_form).exists():
            raise ValidationError("Email exists")
        else:
            user.email = email_in_form
        user.save()
        return user
    except Exception as inst:
        context = {'error_message': inst, 'user_form': user_form, 'social_user_form': social_user_form}
        return render(request, 'edit_data/bad_request.html', context)

def edit_social_user(user_form, social_user_form, request):
    try:
        social_user = SocialUser.objects.get(user=request.user)
        social_user.birth_date = social_user_form.cleaned_data.get('birth_date')
        social_user.phone_number = social_user_form.cleaned_data.get('phone_number')
        social_user.hobbies = social_user_form.cleaned_data.get('hobbies')
        social_user.school = social_user_form.cleaned_data.get('school')
        social_user.university = social_user_form.cleaned_data.get('university')
        if 'main_photo' in request.FILES:
            social_user.main_photo = request.FILES['main_photo']
        else:
            pass
        social_user.save()
        return social_user
    except Exception as inst:
        context = {'error_message': inst, 'user_form': user_form, 'social_user_form': social_user_form}
        return render(request, 'edit_data/bad_request.html', context)