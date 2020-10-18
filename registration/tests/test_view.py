from django.test import TestCase
from django.contrib.auth.models import User
from SocialNet.settings import BASE_DIR
from registration.models import SocialUser
from .test_form import RegistrationFormTest
from registration.services import create_new_user, create_new_social_user
import shutil


class RegistrationViewTest(TestCase):


    @classmethod
    def setUp(self):
        user = User.objects.create_user(username='Miha',
                                        email='miha@mail.ru',
                                        password='qwerty123',
                                        first_name='Mikhail',
                                        last_name='Makarov',
                                        )
        social_user = SocialUser.objects.create(user=user, main_photo=f'{BASE_DIR}/_media/pic2.png')
        social_user.save()
        self.photo = open(f'{BASE_DIR}/_media/pic.png', 'rb')
        self.new_user = {'csrfmiddlewaretoken': '1IEjRrKdLGse3k6F0a792LBdMhEgvKCqfJcMcqbkdO83RwHt2JbTk6NSW9fHWtcl',
                    'user_login': 'Test_user', 'user_email': 'miha2@mail.ru',
                    'user_password': '11111111', 'confirm_password': '11111111', 'user_name': 'Maha',
                    'user_surname': 'Petrova', 'user_main_photo': self.photo}
        self.new_user2 = {'csrfmiddlewaretoken': '1IEjRrKdLGse3k6F0a792LBdMhEgvKCqfJcMcqbkdO83RwHt2JbTk6NSW9fHWtcl',
                     'user_login': 'Test_user2', 'user_email': 'miha3@mail.ru',
                     'user_password': '11111111', 'confirm_password': '11111111', 'user_name': 'Maha',
                     'user_surname': 'Petrova', 'user_main_photo': self.photo}

    def tearDown(self):
        try:
            user = User.objects.all()
            user.delete()
        except:pass
        try:
            social_user = SocialUser.objects.all()
            social_user.delete()
        except:pass
        try:
            shutil.rmtree(f'{BASE_DIR}/_media/registration/main_photos/Test_user')
        except:pass

    def test_get_method(self):
        method_get = self.client.get('/registration')
        self.assertEqual(method_get.status_code, 200, 'registration page is not avaliable')

    def test_post_method(self):
        create_user = self.client.post(path='/registration', data=self.new_user)
        user = User.objects.get(username='Test_user')
        self.assertEqual(user.username, 'Test_user', 'Wrong username in post method. Must be "Test_user"')

    def test_create_new_user(self):
        reg_form, request = RegistrationFormTest.make_reg_form(self, self.new_user)
        if reg_form.is_valid():
            user = create_new_user(reg_form)
            social_user = create_new_social_user(user, request, reg_form)
            self.assertEqual(user.username, 'Test_user', 'Wrong username in "create_new_user"'
                                                         ' function. Must be "Test_user"')
            self.assertEqual(social_user.user.username, 'Test_user', 'Wrong username in "create_new_social_user"'
                                                         ' function. Must be "Test_user"')




