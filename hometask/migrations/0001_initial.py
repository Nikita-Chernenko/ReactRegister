# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-11 12:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('timetable', '0002_auto_20170909_1104'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hometask',
            fields=[
                ('scheduledsubject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='timetable.ScheduledSubject')),
                ('task', models.CharField(max_length=200)),
                ('files', models.FileField(null=True, upload_to='uploads/')),
            ],
            bases=('timetable.scheduledsubject',),
        ),
    ]
