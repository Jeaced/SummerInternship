# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-26 18:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20160614_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
    ]
