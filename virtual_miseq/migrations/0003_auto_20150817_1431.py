# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_miseq', '0002_sample_environment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='project_name',
            field=models.CharField(max_length=200),
        ),
    ]
