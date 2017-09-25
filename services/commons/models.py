from __future__ import unicode_literals

import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from users.models import UserProfile


class UserParticipate(models.Model):
    """
    User Participate  
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_type = models.ForeignKey(ContentType, blank=False, null=False)
    object_id = models.CharField(max_length=100, blank=False, null=False)
    user = models.ForeignKey(UserProfile)
    category = models.CharField(max_length=120, blank=False, null=False)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content_object = GenericForeignKey()
    
    class Meta:
        unique_together = ("content_type", "object_id", "user")
