from __future__ import absolute_import

from celery import shared_task

from services.events.models import Events
from services.mongo.collections import EventCollection
from services.utils.utils import get_object_or_none


@shared_task
def update_event(event_id, delete=None):
    obj = get_object_or_none(Events, id=event_id)
    if obj:
        ec = EventCollection()
        ec.remove(obj) if delete else ec.save_and_update(obj)
