from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.base import View
from .models import Messages
from .forms import SendMessageForm
from .services import get_userlist_messaging_with_curent_user, get_last_message_with_each_in_userlist,\
    get_sender_receiver_and_previos_messages, make_messages_reeded_when_open


class MessageListView(ListView):
    paginate_by = 40
    template_name = 'messenger/message_list.html'
    def get_queryset(self):
        users = get_userlist_messaging_with_curent_user(self.request)
        queryset = get_last_message_with_each_in_userlist(self.request, users)
        object_list = Messages.objects.filter(pk__in=queryset).order_by('-date_time')
        return object_list
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_readed_messages'] = Messages.objects.filter(receiver=self.request.user, reeded_flag=False).count()
        return context

class SendMessageView(View):
    def get(self, request, user):
        not_readed_messages = Messages.objects.filter(receiver=self.request.user, reeded_flag=False).count()
        make_messages_reeded_when_open(self.request, user)
        message_form = SendMessageForm()
        sender, receiver, previos_messages = get_sender_receiver_and_previos_messages(self.request, user)
        context = {'sender':sender, 'receiver':receiver, 'message_form':message_form,
                   'previos_messages':previos_messages, 'not_readed_messages':not_readed_messages}
        return render(request, 'messenger/send_message.html', context)
    def post(self, request, user):
        message_form = SendMessageForm(request.POST)
        if message_form.is_valid() and request.method=='POST':
            create_message = Messages.objects.create(sender=self.request.user, receiver=User.objects.get(username=user),
                                                     message_text=message_form.cleaned_data.get('message_text'))
            create_message.save()
            return redirect('send_message', user)

class DeleteMessageView(View):
    def post(self, request, pk):
        message = Messages.objects.get(pk=pk)
        message.delete_flag = True
        message.save()
        return redirect('send_message', message.receiver.username)


class RestoreMessageView(View):
    def post(self, request, pk):
        message = Messages.objects.get(pk=pk)
        message.delete_flag = False
        message.save()
        return redirect('send_message', message.receiver.username)