# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_miseq', '0006_auto_20150817_1927'),
    ]

    operations = [
        migrations.CreateModel(
            name='Finished_Miseq',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('virtual_id', models.CharField(max_length=200, blank=True)),
                ('miseq_id', models.CharField(max_length=200, blank=True)),
            ],
        ),
    ]
