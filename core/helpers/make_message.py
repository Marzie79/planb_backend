from accounts.models import *

def make_message(receiver, text, project=None):
    message = Message.objects.create(text=text, project=project)
    reciever_objs = []
    for item in receiver:
        reciever_objs.append(Reciever(message=message, user=item.user))
    Reciever.objects.bulk_create(reciever_objs)