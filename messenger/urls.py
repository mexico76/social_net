from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', login_required(views.MessageListView.as_view()), name='my_messages'),
    path('send_to_<slug:user>/', login_required(views.SendMessageView.as_view()), name='send_message'),
    path('delete_<int:pk>/', login_required(views.DeleteMessageView.as_view()), name='delete_message'),
    path('restore_<int:pk>/', login_required(views.RestoreMessageView.as_view()), name='restore_message')
]

