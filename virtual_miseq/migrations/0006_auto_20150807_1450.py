# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_miseq', '0005_auto_20150807_1329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='related_exp',
        ),
        migrations.AddField(
            model_name='log',
            name='related_exp',
            field=models.ForeignKey(related_name='log_related_exp', blank=True, to='virtual_miseq.Experiment', null=True),
        ),
        migrations.RemoveField(
            model_name='log',
            name='related_sam',
        ),
        migrations.AddField(
            model_name='log',
            name='related_sam',
            field=models.ForeignKey(related_name='log_related_sam', blank=True, to='virtual_miseq.Sample', null=True),
        ),
    ]
