from django.test import TestCase
from django.contrib.auth.models import User
from SocialNet.settings import BASE_DIR
import datetime
from registration.models import SocialUser


class RegistrationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='Miha',
                                        email='miha@mail.ru',
                                        password='qwerty123',
                                        first_name='Mikhail',
                                        last_name='Makarov',
                                        )
        social_user=SocialUser.objects.create(user=user, main_photo=f'{BASE_DIR}/_media/pic.png',)
        social_user.save()

    def test_main_photo_path(self):
        social_user = SocialUser.objects.get(user='1')
        path = social_user._meta.get_field('main_photo').upload_to(social_user, f'{BASE_DIR}/_media/pic.png')
        real_path = f'registration/main_photos/Miha\Miha-{datetime.datetime.now().strftime("%d.%m.%y %H:%M")}.png'
        self.assertEqual(real_path, path, 'The path to store images wrong!'
                                          ' See registration-models func user_main_photo_path')

    def test_birth_date_label(self):
        social_user = SocialUser.objects.get(user='1')
        field_label = social_user._meta.get_field('birth_date').verbose_name
        self.assertEqual(field_label, 'My Birth Date')

    def test_phone_number_label(self):
        social_user = SocialUser.objects.get(user='1')
        field_label = social_user._meta.get_field('phone_number').verbose_name
        self.assertEqual(field_label, 'The number of my phone')

    def test_phone_number_max_lenght(self):
        social_user = SocialUser.objects.get(user='1')
        max_length = social_user._meta.get_field('phone_number').max_length
        self.assertEqual(max_length, 12)

    def test_hobbies_label(self):
        social_user = SocialUser.objects.get(user='1')
        field_label = social_user._meta.get_field('hobbies').verbose_name
        self.assertEqual(field_label, 'My hobbies')

    def test_school_label(self):
        social_user = SocialUser.objects.get(user='1')
        field_label = social_user._meta.get_field('school').verbose_name
        self.assertEqual(field_label, "Schools where I'm studied")

    def test_university_label(self):
        social_user = SocialUser.objects.get(user='1')
        field_label = social_user._meta.get_field('university').verbose_name
        self.assertEqual(field_label, "My Universities")

    def test_main_photo_label(self):
        social_user = SocialUser.objects.get(user='1')
        field_label = social_user._meta.get_field('main_photo').verbose_name
        self.assertEqual(field_label, 'My photo')



