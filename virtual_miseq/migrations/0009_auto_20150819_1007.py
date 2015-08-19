# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_miseq', '0008_auto_20150817_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='miseq_folder_name',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
