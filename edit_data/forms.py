from django import forms
# from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from registration.models import SocialUser

class EditDataFormUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    # def clean(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.filter(email=email).exists():
    #         raise ValidationError("Email exists")
    #     return self.cleaned_data

class EditDataFormSocialUser(forms.ModelForm):
    class Meta:
        model = SocialUser
        fields = ['birth_date', 'phone_number', 'hobbies', 'school',
                  'university', 'main_photo']
