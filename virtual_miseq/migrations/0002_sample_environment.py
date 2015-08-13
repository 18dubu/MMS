# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_miseq', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='environment',
            field=models.CharField(default=b'inVitro', max_length=20, choices=[(b'inVitro', b'inVitro'), (b'inVivo', b'inVivo')]),
        ),
    ]
