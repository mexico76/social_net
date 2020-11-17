from django.test import TestCase
from django.contrib.auth.models import User
from SocialNet.settings import BASE_DIR
from registration.models import SocialUser
from .test_form import RegistrationFormTest
from registration.services import create_new_user, create_new_social_user, new_user_auto_loging
import shutil


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

    def test_get_method(self):
        method_get = self.client.get('/registration')
        self.assertEqual(method_get.status_code, 200, 'registration page is not avaliable')

    def test_post_method(self):
        create_user = self.client.post(path='/registration', data=self.new_user)
        user = User.objects.get(username='Test_user')
        self.assertEqual(user.username, 'Test_user', 'Wrong username in post method. Must be "Test_user"')

    def test_post_method_duble_user(self):
        create_user = self.client.post(path='/registration', data=self.new_user2)
        self.assertEqual(create_user.status_code, 200)
        self.assertEqual(create_user.context.get('user').is_authenticated, False,
                         'When you try to registr new user with no data you can not create it')

    def test_post_method_empty_data(self):
        create_user = self.client.post(path='/registration')
        self.assertEqual(create_user.status_code, 200)
        self.assertEqual(create_user.context.get('user').is_authenticated, False,
                         'When you try to registr new user with exists login or email you can not loged in')

    def test_create_new_user_socialuser_and_auto_loging(self):
        reg_form, request = RegistrationFormTest.make_reg_form(self, self.new_user)
        if reg_form.is_valid():
            user = create_new_user(reg_form)
            self.assertEqual(user.username, 'Test_user', 'Wrong username in "create_new_user"'
                                                         ' function. Must be "Test_user"')
            social_user = create_new_social_user(user, request, reg_form)
            self.assertEqual(social_user.user.username, 'Test_user', 'Wrong username in "create_new_social_user"'
                                                         ' function. Must be "Test_user"')
            self.assertEqual(request.user.is_authenticated, False, 'When user is not register he must be logged off')
            auto_log = new_user_auto_loging(reg_form, request)
            self.assertEqual(request.user.is_authenticated, True, 'After registration user must be logged on')

    def test_one_empty_field(self):
        first_empty = self.new_user
        first_empty.pop('user_login')
        second_empty = self.new_user
        second_empty.pop('user_password')
        third_empty = self.new_user
        third_empty.pop('confirm_password')
        fourth_empty = self.new_user
        fourth_empty.pop('user_name')
        fifth_empty = self.new_user
        fifth_empty.pop('user_surname')
        sixth_empty = self.new_user
        sixth_empty.pop('user_email')
        empty_picture = self.new_user
        empty_picture.pop('user_main_photo')
        reg_form1, request1 = RegistrationFormTest.make_reg_form(self, first_empty)
        self.assertEqual(reg_form1.is_valid(), False, 'RegForm must be not valid if login is empty')
        reg_form2, request2 = RegistrationFormTest.make_reg_form(self, second_empty)
        self.assertEqual(reg_form2.is_valid(), False, 'RegForm must be not valid if password is empty')
        reg_form3, request3 = RegistrationFormTest.make_reg_form(self, third_empty)
        self.assertEqual(reg_form3.is_valid(), False, 'RegForm must be not valid if confirm_password is empty')
        reg_form4, request4 = RegistrationFormTest.make_reg_form(self, fourth_empty)
        self.assertEqual(reg_form4.is_valid(), False, 'RegForm must be not valid if user_name is empty')
        reg_form5, request5 = RegistrationFormTest.make_reg_form(self, fifth_empty)
        self.assertEqual(reg_form5.is_valid(), False, 'RegForm must be not valid if user_surname is empty')
        reg_form6, request6 = RegistrationFormTest.make_reg_form(self, sixth_empty)
        self.assertEqual(reg_form6.is_valid(), False, 'RegForm must be not valid if e-mail is empty')
        reg_form7, request7 = RegistrationFormTest.make_reg_form(self, empty_picture)
        self.assertEqual(reg_form7.is_valid(), False, 'RegForm must be not valid if picture is empty')
