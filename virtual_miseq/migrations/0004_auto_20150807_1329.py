# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_miseq', '0003_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='writer',
            field=models.ManyToManyField(related_name='writer', null=True, to='virtual_miseq.IDMSUser'),
        ),
    ]
