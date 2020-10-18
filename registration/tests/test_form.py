from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from SocialNet.settings import BASE_DIR
from registration.forms import RegistrationForm
from registration.models import SocialUser


class RegistrationFormTest(TestCase):
    photo = open(f'{BASE_DIR}/_media/pic.png', 'rb')
    photo2 = open(f'{BASE_DIR}/_media/pic.png', 'rb')
    duble_user = {'csrfmiddlewaretoken': '2IEjRrKdLGse3k6F0a792LBdMhEgvKCqfJcMcqbkdO83RwHt2JbTk6NSW9fHWtcl',
                  'user_login': 'Miha', 'user_email': 'mih123@mail.ru',
                  'user_password': '11111111', 'confirm_password': '11111111', 'user_name': 'Maha',
                  'user_surname': 'Petrova', 'user_main_photo': photo2}
    duble_user_by_email = {'csrfmiddlewaretoken': '1IEjRrKdLGse3k6F0a792LBdMhEgvKCqfJcMcqbkdO83RwHt2JbTk6NSW9fHWtcl',
                           'user_login': 'Miha3', 'user_email': 'miha@mail.ru',
                           'user_password': '11111111', 'confirm_password': '11111111', 'user_name': 'Maha',
                           'user_surname': 'Petrova', 'user_main_photo': photo}
    new_user = {'csrfmiddlewaretoken': '1IEjRrKdLGse3k6F0a792LBdMhEgvKCqfJcMcqbkdO83RwHt2JbTk6NSW9fHWtcl',
                'user_login': 'miha2', 'user_email': 'miha2@mail.ru',
                'user_password': '11111111', 'confirm_password': '11111111', 'user_name': 'Maha',
                'user_surname': 'Petrova', 'user_main_photo': ''}

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='Miha',
                                        email='miha@mail.ru',
                                        password='qwerty123',
                                        first_name='Mikhail',
                                        last_name='Makarov',
                                        )
        social_user = SocialUser.objects.create(user=user, main_photo=f'{BASE_DIR}/_media/pic2.png')
        social_user.save()

    def make_reg_form(self, user):
        factory = RequestFactory()
        request = factory.post(path='/registration', data=user)
        reg_form = RegistrationForm(request.POST, request.FILES)
        return reg_form, request

    def test_dubling_user(self):
        reg_form, request = self.make_reg_form(self.duble_user)
        self.assertEqual(reg_form.is_valid(), False)
        self.assertHTMLEqual(str(reg_form.errors), '<ul class="errorlist"><li>__all__<ul class="errorlist nonfield">'
                                                   '<li>Login exists</li></ul></li></ul>')

    def test_dubling_email(self):
        reg_form, request = self.make_reg_form(self.duble_user_by_email)
        self.assertEqual(reg_form.is_valid(), False)
        self.assertHTMLEqual(str(reg_form.errors), '<ul class="errorlist"><li>__all__<ul class="errorlist nonfield">'
                                                   '<li>Email exists</li></ul></li></ul>')

    def test_no_photo(self):
        reg_form, request = self.make_reg_form(self.new_user)
        self.assertEqual(reg_form.is_valid(), False)
        self.assertHTMLEqual(str(reg_form.errors), '<ul class="errorlist"><li>user_main_photo<ul class="errorlist">'
                                                   '<li>Обязательное поле.</li></ul></li></ul>')