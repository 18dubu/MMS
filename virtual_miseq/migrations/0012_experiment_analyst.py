# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_miseq', '0011_auto_20150819_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='analyst',
            field=models.ForeignKey(related_name='analyzing_exp', blank=True, to='virtual_miseq.IDMSUser', null=True),
        ),
    ]
