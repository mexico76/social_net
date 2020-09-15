from django.urls import path

from .views import index, Login, Logout

urlpatterns = [
    path('', index, name='index'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout')
]