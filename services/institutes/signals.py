from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from services.institutes.models import Institute


@receiver(post_save, sender=Institute)
def feed_signal_update(sender, **kwargs):
    instance = kwargs.get('instance', False)
    if instance:
        pass
