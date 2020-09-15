from django.test import TestCase
from django.contrib.auth.models import User
from SocialNet.settings import BASE_DIR
from registration.models import SocialUser


class RegistrationModelTest(TestCase):
    new_user = {'username':'miha2', 'email':'miha2@mail.ru',
                 'password':'11111111', 'first_name':'Maha',
                 'last_name':'Petrova','main_photo':f'{BASE_DIR}/_media/pic.png'}
    new_user2 = {'user_login':'miha2', 'user_email':'miha2@mail.ru',
                 'user_password':'11111111', 'confirm_password':'11111111', 'user_name':'Maha',
                 'user_surname':'Petrova','main_photo':f'{BASE_DIR}/_media/pic.png'}
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='Miha',
                                        email='miha@mail.ru',
                                        password='qwerty123',
                                        first_name='Mikhail',
                                        last_name='Makarov',
                                        )
        social_user = SocialUser.objects.create(user=user, main_photo=f'{BASE_DIR}/_media/pic.png',)
        social_user.save()

    def test_get_method(self):
        method_get = self.client.get('/registration')
        self.assertEqual(method_get.status_code, 200)

    def test_post_method(self):
        # Надо разобраться как посылать запрос формы
        method_post = self.client.post('/registration', self.new_user2)
        print(method_post.context['user'])



