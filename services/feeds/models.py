from __future__ import unicode_literals

import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from services.vote.managers import VotableManager
from users.models import UserProfile


# Create your models here.
class Feed(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_user = models.ForeignKey(UserProfile, blank=True, null=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=100)
    message = models.TextField()
    parent = models.ForeignKey('self', blank=True, null=True)
    is_media = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content_object  = GenericForeignKey()
    votes = VotableManager()

    @property
    def children(self):
        return Feed.objects.filter(parent=self)

    @property
    def children_count(self):
        return Feed.objects.filter(parent=self).count()
