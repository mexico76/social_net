from django.contrib.auth.models import User
from django.db.models import Q
from .models import Messages

def get_userlist_messaging_with_curent_user(request):
    user_set = set()
    message_user = Messages.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    for addressee in message_user:
        user_set.add(addressee.sender.username)
        user_set.add(addressee.receiver.username)
    user_list = list(user_set)
    users = User.objects.filter(username__in=user_list).exclude(username=request.user)
    return users

def get_last_message_with_each_in_userlist(request, users):
    queryset = []
    for far_user in users:
        messaging_with_user = Messages.objects.filter((Q(sender=request.user) & Q(receiver=far_user)) |
                                                      (Q(sender=far_user) & Q(receiver=request.user)))
        queryset.append(messaging_with_user.last().pk)
    return queryset

def get_sender_receiver_and_previos_messages(request, user):
    sender = User.objects.get(username=request.user)
    receiver = User.objects.get(username=user)
    try:
        previos_messages = Messages.objects.filter(Q(sender=sender) & Q(receiver=receiver) | Q(sender=receiver)
                                                   & Q(receiver=sender)).order_by('-date_time')
    except Exception as no_messages:
        previos_messages = Messages.objects.none()
    return sender, receiver, previos_messages

def make_messages_reeded_when_open(request, user):
    receiver = User.objects.get(username=request.user)
    sender = User.objects.get(username=user)
    messages = Messages.objects.filter(sender=sender, receiver=receiver)
    for message in messages:
        message.reeded_flag = True
        message.save()


