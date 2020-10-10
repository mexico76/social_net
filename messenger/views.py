from django.shortcuts import redirect
from django.views.generic.base import View

from main_page.views import MainView, MainListView
from .models import Messages
from .forms import SendMessageForm
from .services import get_userlist_messaging_with_curent_user, get_last_message_with_each_in_userlist,\
    get_sender_receiver_and_previos_messages, make_messages_reeded_when_open, delete_restore_message, create_message


class MessageListView(MainListView):
    paginate_by = 40
    template_name = 'messenger/message_list.html'
    def get_queryset(self):
        users = get_userlist_messaging_with_curent_user(self.request)
        queryset = get_last_message_with_each_in_userlist(self.request, users)
        object_list = Messages.objects.filter(pk__in=queryset).order_by('-date_time')
        return object_list

class SendMessageView(MainView):
    template_name = 'messenger/send_message.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        make_messages_reeded_when_open(self.request, kwargs['user'])
        context['message_form'] = SendMessageForm()
        context['sender'], context['receiver'], context['previos_messages'] =\
            get_sender_receiver_and_previos_messages(self.request, kwargs['user'])
        return context

    def post(self, request, user):
        message_form = SendMessageForm(request.POST)
        create_message(request, message_form, user)
        return redirect('send_message', user)

class DeleteMessageView(View):
    def post(self, request, pk):
        user = delete_restore_message(pk, True)
        return redirect('send_message', user)

class RestoreMessageView(View):
    def post(self, request, pk):
        user = delete_restore_message(pk, False)
        return redirect('send_message', user)