from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.AllPhotoView.as_view(), name='all_photo'),
    path('albums/', views.AlbumListView.as_view(), name='albums'),
    path('albums/<slug:album_name>', views.CurentAlbomView.as_view(), name='curent_album'),
    path('add_album', views.AddAlbumView.as_view(), name='add_album'),
    path('albums/<slug:album_name>/add_photo/', views.AddPhotoToAlbumView.as_view(), name='add_photo'),
]

