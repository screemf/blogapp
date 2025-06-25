import sys
import os
import django
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
#sys.path.append(os.path.abspath(r'D:/Users/scree/PycharmProjects/project_config'))
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_config.settings')
from blogapp.models import Post, Comment


@receiver(post_save, sender=Post)
def send_post_update_on_save(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'post_updates',
        {
            'type': 'post_message',
            'message': f'Post {instance.id} was updated'
        }
    )


@receiver(post_save, sender=Comment)
def send_comment_update_on_save(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'comment_updates',
        {
            'type': 'comment_message',
            'message': f'Comment {instance.id} was added/updated'
        }
    )

# Create your models here.
