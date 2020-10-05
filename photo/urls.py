from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.AllPhotoView.as_view()), name='all_photo'),
    path('albums/', login_required(views.AlbumListView.as_view()), name='albums'),
    path('albums/<int:pk>', login_required(views.CurentAlbomView.as_view()), name='curent_album'),
    path('add_album', login_required(views.AddAlbumView.as_view()), name='add_album'),
    path('albums/<int:pk>/add_photo/', login_required(views.AddPhotoToAlbumView.as_view()), name='add_photo'),
]

