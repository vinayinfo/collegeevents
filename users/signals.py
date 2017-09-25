from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from users.models import Users


@receiver(post_save, sender=Users)
def user_signal_update(sender, **kwargs):
    instance = kwargs.get('instance', False)
    if instance:
        pass
