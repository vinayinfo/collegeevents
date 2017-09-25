from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from services.feeds.models import Feed


@receiver(post_save, sender=Feed)
def feed_signal_update(sender, **kwargs):
    instance = kwargs.get('instance', False)
    if instance:
        pass
