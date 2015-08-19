# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_miseq', '0007_finished_miseq'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='comment',
            field=models.TextField(null=True, blank=True),
        ),
    ]
