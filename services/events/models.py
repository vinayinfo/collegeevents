from __future__ import unicode_literals

import uuid

from django.contrib.postgres.fields import ArrayField
from django.core.urlresolvers import reverse
from django.db import models

from services.address.models import AddressField
from services.institutes.models import Department, Institute
from services.vote.managers import VotableManager


class Events(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institute = models.ForeignKey(Institute, blank=True, null=True)
    department = models.ForeignKey(Department, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    fee = models.PositiveIntegerField(blank=True,null=True)
    address = AddressField(blank=True, null=True)
    apply_date = models.DateTimeField(blank=True,null=True)
    apply_last_date = models.DateTimeField(blank=True,null=True)
    event_start_date = models.DateTimeField(blank=True,null=True)
    event_last_date = models.DateTimeField(blank=True,null=True)
    availability = models.PositiveIntegerField(blank=True,null=True)
    tags = ArrayField(models.CharField(max_length=200), blank=True)
    avg_rating = models.DecimalField(max_digits=5, decimal_places=3, default=0)
    total_feed = models.IntegerField(default=0)
    is_media = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = VotableManager()
    
    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("institute", "name")
    
    def get_absolute_url(self):
        return reverse('events-detail', args=[str(self.institute.id), str(self.id)])

    def get_absolute_web_url(self):
        return reverse('institute_event_detail', args=[str(self.institute.id), str(self.id)])
