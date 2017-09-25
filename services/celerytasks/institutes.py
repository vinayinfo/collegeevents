from __future__ import absolute_import

from celery import shared_task

from services.institutes.models import Institute
from services.mongo.collections import InstituteCollection
from services.utils.utils import get_object_or_none


@shared_task
def update_institue(institute_id, delete=None):
    obj = get_object_or_none(Institute, id=institute_id)
    if obj:
        ic = InstituteCollection()
        ic.remove(obj) if delete else ic.save_and_update(obj)
