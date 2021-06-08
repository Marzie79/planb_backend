from accounts.models import NotificationToken, UserProject
from core.helpers.make_message import make_message
from core.helpers.make_notification import make_notification


def make_notification_and_message(text,instance,statuses=None,recievers=None):
    recievers_user = []
    if recievers:
        for item in recievers:
            recievers_user.append(item.user)
    else:
        recievers = UserProject.objects.filter(project=instance).filter(status__in=statuses)
        for item in recievers:
            recievers_user.append(item.user)
    recievers_token = list(NotificationToken.objects.filter(user__in=recievers_user).values_list('token', flat=True))
    make_message(text=text, receiver=recievers, project=instance)
    make_notification(recievers_token, instance.name, text)