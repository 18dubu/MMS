# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_miseq', '0009_auto_20150819_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='idmsuser',
            name='role',
            field=models.CharField(max_length=10, null=True, choices=[(b'analyst', b'analyst'), (b'supervisor', b'supervisor')]),
        ),
    ]
