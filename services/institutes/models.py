from __future__ import unicode_literals

import uuid

from django.core.urlresolvers import reverse
from django.db import models

from services.address.models import AddressField
from services.departments.models import Department, Facility
from services.vote.managers import VotableManager
from users.models import UserProfile


class InstituteType(models.Model):
    """
    InstituteType is like board, university
    """
    name = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Institute(models.Model):
    """
    parent = None, it is called University, Board
    parent != None, it is called Institute, school
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=500, unique=True)
    owner = models.ForeignKey(UserProfile, blank=True, null=True)
    institute_type = models.ForeignKey(InstituteType, blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    department = models.ManyToManyField(Department, through='InstituteDepartment')
    facility = models.ManyToManyField(Facility, through='InstituteFacility')
    address = AddressField(blank=True, null=True)
    institute_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    established_date = models.DateTimeField(blank=True, null=True)
    avg_rating = models.DecimalField(max_digits=5, decimal_places=3, default=0)
    total_feed = models.IntegerField(default=0)
    is_media = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = VotableManager()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('institute-detail', args=[str(self.id)])
    
    def get_absolute_web_url(self):
        return reverse('institute_detail', args=[str(self.id)])


class InstituteDepartment(models.Model):
    """
    many Institute has many department
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institute = models.ForeignKey(Institute, blank=True, null=True)
    department = models.ForeignKey(Department, blank=True, null=True)
    owner = models.ForeignKey(UserProfile, related_name='owner', blank=True, null=True)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('department', 'institute',)


class InstituteFacility(models.Model):
    """
    many Institute has many facility like canteen
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institute = models.ForeignKey(Institute, blank=True, null=True)
    facility = models.ForeignKey(Facility, blank=True, null=True)
    owner = models.ForeignKey(UserProfile, related_name='facility_owner', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('facility', 'institute')
