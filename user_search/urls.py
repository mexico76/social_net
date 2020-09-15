from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.UserListView.as_view()), name='user_list'),
    path('<slug:user>/', login_required(views.UserDetailView.as_view()), name='user_detail')
]

