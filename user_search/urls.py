from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.UserListView.as_view()), name='user_list'),
    path('<slug:user>/', login_required(views.UserDetailView.as_view()), name='user_detail'),
    path('<slug:user>/photos',login_required(views.UserAllPhotoView.as_view()), name='user_photos'),
    path('<slug:user>/albums', login_required(views.UserAlbumListView.as_view()), name='user_albums'),
    path('<slug:user>/<int:pk>', login_required(views.UserCurentAlbomView.as_view()), name='user_curent_album'),

]

