from __future__ import unicode_literals

import uuid

from django.core.urlresolvers import reverse
from django.db import models

from services.vote.managers import VotableManager


class Course(models.Model):
    """
    course is like Bsc, MCA
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=500, unique=True)
    duration = models.IntegerField(default=0)
    start_year = models.IntegerField(default=0)
    end_year = models.IntegerField(default=0)
    avg_rating = models.DecimalField(max_digits=5, decimal_places=3, default=0)
    total_feed = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = VotableManager()
    
    def __str__(self):
        return self.name


class Facility(models.Model):
    """
    facility is like canteen, play ground
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=500, unique=True)
    avg_rating = models.DecimalField(max_digits=5, decimal_places=3, default=0)
    total_feed = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = VotableManager()
    
    def __str__(self):
        return self.name


class Department(models.Model):
    """
    department is like Mathematics, physics
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=500, unique=True)
    is_lab = models.BooleanField(default=False)
    avg_rating = models.DecimalField(max_digits=5, decimal_places=3, default=0)
    total_feed = models.IntegerField(default=0)
    course = models.ManyToManyField(Course, through='DepartmentCourse')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = VotableManager()
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('department-detail', args=[str(self.id)])
    

class DepartmentCourse(models.Model):
    """
    many department have many courses
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.ForeignKey(Department, blank=True, null=True)
    course = models.ForeignKey(Course, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('department', 'course',)
