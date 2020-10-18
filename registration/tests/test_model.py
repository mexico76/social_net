from django.test import TestCase
from django.contrib.auth.models import User
from SocialNet.settings import BASE_DIR
import datetime
from registration.models import SocialUser


class RegistrationModelTest(TestCase):

    @classmethod
    def setUp(cls):
        user = User.objects.create_user(username='Miha',
                                        email='miha@mail.ru',
                                        password='qwerty123',
                                        first_name='Mikhail',
                                        last_name='Makarov',
                                        )
        social_user=SocialUser.objects.create(user=user, main_photo=f'{BASE_DIR}/_media/pic.png',)
        social_user.save()

    def tearDown(self):
        try:
            user = User.objects.all()
            user.delete()
        except:pass
        try:
            social_user = SocialUser.objects.all()
            social_user.delete()
        except:pass

    def test_main_photo_path(self):
        social_user = SocialUser.objects.get(user='1')
        path = social_user._meta.get_field('main_photo').upload_to(social_user, f'{BASE_DIR}/_media/pic.png')
        real_path = f'registration/main_photos/Miha\Miha-{datetime.datetime.now().strftime("%d.%m.%y %H:%M")}.png'
        self.assertEqual(real_path, path, 'The path to store images wrong!'
                                          ' See registration-models func user_main_photo_path')


    def test_phone_number_max_lenght(self):
        social_user = SocialUser.objects.get(user='1')
        max_length = social_user._meta.get_field('phone_number').max_length
        self.assertEqual(max_length, 15, 'Wrong max lenght of phone number(must be 15)')

