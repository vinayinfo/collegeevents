# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-15 11:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import services.address.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('departments', '0001_initial'),
        ('institutes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutefacility',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='facility_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='institutedepartment',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='departments.Department'),
        ),
        migrations.AddField(
            model_name='institutedepartment',
            name='institute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutes.Institute'),
        ),
        migrations.AddField(
            model_name='institutedepartment',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='institute',
            name='address',
            field=services.address.models.AddressField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.Address'),
        ),
        migrations.AddField(
            model_name='institute',
            name='department',
            field=models.ManyToManyField(through='institutes.InstituteDepartment', to='departments.Department'),
        ),
        migrations.AddField(
            model_name='institute',
            name='facility',
            field=models.ManyToManyField(through='institutes.InstituteFacility', to='departments.Facility'),
        ),
        migrations.AddField(
            model_name='institute',
            name='institute_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutes.InstituteType'),
        ),
        migrations.AddField(
            model_name='institute',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='institute',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutes.Institute'),
        ),
        migrations.AlterUniqueTogether(
            name='institutefacility',
            unique_together=set([('facility', 'institute')]),
        ),
        migrations.AlterUniqueTogether(
            name='institutedepartment',
            unique_together=set([('department', 'institute')]),
        ),
    ]
