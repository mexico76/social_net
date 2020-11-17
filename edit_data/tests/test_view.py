from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from SocialNet.settings import BASE_DIR
import shutil

from registration.models import SocialUser
from edit_data.services import get_user_and_create_user_instance_form, edit_user, edit_social_user


class RegistrationViewTest(TestCase):


    @classmethod
    def setUp(self):
        user = User.objects.create_user(username='Test_user2',
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
                     'user_login': 'Test_user2', 'user_email': 'miha@mail.ru',
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




    def test_get_user_and_create_user_instance_form_and_method_post(self):
        context = {}
        factory = RequestFactory()
        request = factory.get('edit_data')
        request.user = User.objects.get(pk=1)
        get_user_and_instance_form = get_user_and_create_user_instance_form(request, context)
        self.assertEqual(get_user_and_instance_form['user'], User.objects.get(username='Test_user2'))