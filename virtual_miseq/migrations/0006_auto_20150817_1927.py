# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_miseq', '0005_auto_20150817_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='result_folder',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
